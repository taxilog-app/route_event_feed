"""配信の見張り（2026-10-16 マリンメッセ4会場が黙って0件になった件の再発防止）。

起きたこと:
  マリンメッセの取り込み口が、1件だけ年付きの日程「2028.1.29」を読めずに例外で落ち、
  同じ口で集めている4会場（A館・B館・国際会議場・国際センター）が丸ごと0件になった。
  失敗は CI のログに1行出るだけで配信は続き（全体の件数は少し減っただけ）、
  急減の見張りは「全体の件数」しか見ておらず、しかも比べる相手が git に残った
  8月の古いファイルだったので、誰も気づかなかった。

ここでやること:
  1. 比べる相手は**今公開している配信**（取れなければ手元の out/）。
  2. **会場ごと**に「これからの予定」の件数を比べ、前回3件以上→今回0件を「消えた」とする。
  3. 消えた会場は、前回の配信にあった**これからの予定を引き継ぐ**（最長14日）。
     運転手の画面から会場が消えないようにする。14日を過ぎたら引き継ぎをやめる。
  4. 取り込み口の失敗・消えた会場・引き継ぎ中を health.json に書き、
     1つでもあれば CI を赤にする（GitHub が持ち主へメールで知らせる＝0円の通知）。
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import urllib.request

LIVE_BASE = "https://taxilog-app.github.io/route_event_feed"
DROP_MIN_PREV = 3        # 前回これ以上あった会場が0件になったら「消えた」
CARRY_MAX_DAYS = 14      # 引き継ぎの上限日数

# ── 最重要の会場（2026-10-16 社長「ドームの情報は命・絶対に外さない」）──
# アプリはドームの催しの開始時刻から「規制が始まる」を読み上げる。予定が消えても、
# 開始時刻が抜けても、知らせは黙って出なくなる。なのでここだけは厳しく見る：
#   ① これから45日の予定が0件 → 赤（ドームは毎月なにかある）
#   ② これから14日の予定に開始時刻が無い → 赤（manual_events.json で補うまで鳴り続ける）
CRITICAL_VENUES = {
    "paypay_dome": "みずほPayPayドーム（規制の知らせの元）",
}
CRITICAL_HORIZON_DAYS = 45
CRITICAL_START_TIME_DAYS = 14

# 事情が分かっていて手を打ってある取り込み口の失敗。health.json には書くが CI を赤にしない
# （毎回赤だと通知が鳴りっぱなしになり、本物の故障を見逃す）。直ったら行ごと消すこと。
KNOWN_FAILURES = {
    "fukuoka_budokan": "武道館のサイトがGitHubからの問い合わせを403で断る。"
                       "アプリが端末から直接取っている（2026-10-16〜・正式な了解を依頼中）",
}


def _load_json_url(url: str, timeout: int = 20):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:  # noqa: S310 - 自分の配信
            return json.loads(r.read().decode("utf-8"))
    except Exception:  # noqa: BLE001 - 取れなければ None（手元へ落とす）
        return None


def _load_json_file(path: str):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:  # noqa: BLE001
        return None


def load_previous(out_dir: str, name: str):
    """前回の配信。公開中のものを優先し、取れなければ手元の out/ を使う。"""
    if os.environ.get("FEED_WATCH_OFFLINE") != "1":
        live = _load_json_url(f"{LIVE_BASE}/{name}")
        if live is not None:
            return live
    return _load_json_file(os.path.join(out_dir, name))


def future_counts(feed: dict | None, today: _dt.date) -> dict[str, int]:
    """会場ごとの「今日以降の予定」の件数。"""
    out: dict[str, int] = {}
    if not feed:
        return out
    t = today.isoformat()
    for e in feed.get("events", []):
        if (e.get("date") or "") >= t:
            k = e.get("venueKey")
            out[k] = out.get(k, 0) + 1
    return out


def apply_manual(feed: dict, manual: list, all_venues_json: dict[str, dict],
                 today: _dt.date) -> list[str]:
    """人の手で補う予定（manual_events.json）を当てる。適用した内容の説明を返す。

    1件の書き方：{"venueKey","date","startHour","startMinute"} ＋任意で
    "title"（その日の同じ会場で、題名にこれを含む予定だけに当てる）・"genre"・"note"。
    - その日・その会場に予定があれば、開始時刻だけ書き換える（取れていない時の補い）
    - 無ければ1件足す（"title" と "genre" が要る）
    過ぎた日の行は使わない（消し忘れても害が無い）。
    """
    applied: list[str] = []
    t = today.isoformat()
    venue_keys = {v["key"] for v in feed.get("venues", [])}
    for m in manual or []:
        d = m.get("date") or ""
        k = m.get("venueKey")
        if d < t or not k:
            continue
        hits = [e for e in feed["events"]
                if e.get("venueKey") == k and e.get("date") == d
                and (not m.get("title") or m["title"] in (e.get("title") or ""))]
        if hits:
            for e in hits:
                e["startHour"], e["startMinute"] = m["startHour"], m["startMinute"]
            applied.append(f"{d} {k} 開始時刻を補った {m['startHour']}:{m['startMinute']:02d}")
        elif m.get("title") and m.get("genre"):
            feed["events"].append({
                "venueKey": k, "date": d, "title": m["title"], "genre": m["genre"],
                "startHour": m["startHour"], "startMinute": m["startMinute"],
            })
            if k not in venue_keys and k in all_venues_json:
                feed["venues"].append(dict(all_venues_json[k]))
                venue_keys.add(k)
            applied.append(f"{d} {k} 予定を足した {m['title']}")
    feed["events"].sort(key=lambda e: (e.get("date") or "", e.get("startHour") or 0,
                                       e.get("startMinute") or 0))
    return applied


def critical_problems(feed: dict, today: _dt.date) -> list[str]:
    """最重要の会場（ドーム）の見張り。"""
    out: list[str] = []
    t = today.isoformat()
    horizon = (today + _dt.timedelta(days=CRITICAL_HORIZON_DAYS)).isoformat()
    near = (today + _dt.timedelta(days=CRITICAL_START_TIME_DAYS)).isoformat()
    for key, name in CRITICAL_VENUES.items():
        evs = [e for e in feed.get("events", [])
               if e.get("venueKey") == key and t <= (e.get("date") or "") <= horizon]
        if not evs:
            out.append(f"🔴最重要 {name}: これから{CRITICAL_HORIZON_DAYS}日の予定が0件")
        for e in evs:
            if e.get("date") <= near and e.get("startHour") is None:
                out.append(f"🔴最重要 {name}: {e['date']}「{e.get('title')}」に開始時刻が無い"
                           "（規制の知らせが出ない）→ 公式で確かめて manual_events.json に足す")
    return out


def watch_and_carry(feed: dict, prev_feed: dict | None, prev_health: dict | None,
                    all_venues_json: dict[str, dict], scraper_status: dict,
                    today: _dt.date) -> dict:
    """消えた会場を見つけて前回の予定を引き継ぎ、health を返す（feed を書き換える）。"""
    prev_counts = future_counts(prev_feed, today)
    now_counts = future_counts(feed, today)
    prev_carried = (prev_health or {}).get("carried", {}) or {}

    dropped: list[str] = []
    carried: dict[str, str] = {}
    lost: list[str] = []
    t = today.isoformat()
    venue_keys = {v["key"] for v in feed.get("venues", [])}

    for key, n_prev in sorted(prev_counts.items()):
        if now_counts.get(key, 0) > 0:
            continue
        # 前回が引き継ぎ中なら、その時の始まりの日を受け継ぐ（引き継ぎの連鎖で永遠に残さない）
        since = prev_carried.get(key)
        if n_prev < DROP_MIN_PREV and since is None:
            continue
        dropped.append(key)
        since = since or t
        if (today - _dt.date.fromisoformat(since)).days > CARRY_MAX_DAYS:
            lost.append(key)
            continue
        carry = [e for e in prev_feed.get("events", [])
                 if e.get("venueKey") == key and (e.get("date") or "") >= t]
        if not carry:
            continue
        feed["events"].extend(carry)
        carried[key] = since
        if key not in venue_keys and key in all_venues_json:
            feed["venues"].append(dict(all_venues_json[key]))
            venue_keys.add(key)

    if carried:
        feed["events"].sort(key=lambda e: (e.get("date") or "",
                                           e.get("startHour") or 0,
                                           e.get("startMinute") or 0))

    problems: list[str] = []
    known: list[str] = []
    for name, st in sorted(scraper_status.items()):
        if not st.get("ok"):
            if name in KNOWN_FAILURES:
                known.append(f"{name}: {KNOWN_FAILURES[name]}")
            else:
                problems.append(f"取り込み口が失敗: {name}: {st.get('error')}")
    for key in dropped:
        if key in lost:
            problems.append(f"会場が消えた（引き継ぎ{CARRY_MAX_DAYS}日を過ぎ・配信から外れた）: {key}")
        elif key in carried:
            problems.append(f"会場が消えた（前回の予定を引き継ぎ中・{carried[key]}から）: {key}")
        else:
            problems.append(f"会場が消えた（引き継げる予定なし）: {key}")

    problems.extend(critical_problems(feed, today))
    counts = future_counts(feed, today)
    return {
        "generatedAt": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "scrapers": scraper_status,
        "venueFutureCounts": counts,
        # 登録してあるのに「これからの予定」が0件の会場（赤にはしない＝本当に無いこともある）。
        # 前回比の見張りは「前から0件」の会場に鳴らないので、ここで一覧にして見えるようにする
        # （2026-10-16 時点で福岡武道館ほか3会場が8月から0件のままだった）。
        "zeroVenues": sorted(k for k in all_venues_json if counts.get(k, 0) == 0),
        "dropped": dropped,
        "carried": carried,
        "problems": problems,
        "knownFailures": known,
    }
