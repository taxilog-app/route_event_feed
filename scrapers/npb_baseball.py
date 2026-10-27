"""プロ野球 球場（npb.jp の月別カレンダー schedule_MM.html）。

明治神宮野球場(ヤクルト)/横浜スタジアム(DeNA)/ZOZOマリン(ロッテ)/阪神甲子園(阪神)
/みずほPayPayドーム(ソフトバンク) の本拠地開催を npb.jp の公式日程から一括取得する。
（PayPayドームのホークス戦は元々 softbankhawks 専用スクレイパーが担当していたが、
そちらは過去試合の /gamelive/result/ リンク依存で未来の試合を取得できないため、
未来分も月ナビ付きで確実に取れる npb.jp 経由へ移管した。
バンテリンD/京セラD/ベルーナD/東京Dは引き続き各専用スクレイパーが担当。）

カレンダーの1日セルは `td > div.date`（日番号）＋`a.link_block`（1試合）。
各 link_block は:
  `td.team1 img[alt]`=ホーム、`td.team2 img[alt]`=ビジター、
  1つ目 `td.state`=開始時刻("18:00")、2つ目 `td.state`=開催球場名("神宮"/"横浜"/
  "ZOZOマリン"/"甲子園"、地方開催時は"盛岡"等)。
2つ目 state の球場名が対象4球場と完全一致した試合だけ採用（地方開催・予備日は除外）。
npb.jp は UTF-8 だが requests が latin-1 と誤判定するため content を明示デコードする。
"""
from __future__ import annotations

import datetime as _dt
import re

from model import Event, GENRE_SPORTS
from venues import (
    MEIJI_JINGU, YOKOHAMA_STADIUM, ZOZO_MARINE, KOSHIEN, PAYPAY_DOME,
    ESCON_FIELD, RAKUTEN_PARK, MAZDA_STADIUM,
)
from .base import http_get, soup_of, flatten_ws

# 2つ目 td.state の球場名（空白除去後）→ Venue
_VENUE_BY_LABEL = {
    "神宮": MEIJI_JINGU,
    "横浜": YOKOHAMA_STADIUM,
    "ZOZOマリン": ZOZO_MARINE,
    "甲子園": KOSHIEN,
    "みずほPayPay": PAYPAY_DOME,  # ソフトバンク本拠地（過去は専用スクレイパー担当）
    "エスコンＦ": ESCON_FIELD,      # 日本ハム（npb.jp表記は全角Ｆ）
    "楽天モバイル": RAKUTEN_PARK,    # 楽天
    "マツダスタジアム": MAZDA_STADIUM,  # 広島
}
# チーム正式名(img alt)→短縮名
_SHORT = {
    "読売ジャイアンツ": "巨人",
    "東京ヤクルトスワローズ": "ヤクルト",
    "阪神タイガース": "阪神",
    "中日ドラゴンズ": "中日",
    "横浜DeNAベイスターズ": "DeNA",
    "広島東洋カープ": "広島",
    "北海道日本ハムファイターズ": "日本ハム",
    "オリックス・バファローズ": "オリックス",
    "東北楽天ゴールデンイーグルス": "楽天",
    "千葉ロッテマリーンズ": "ロッテ",
    "福岡ソフトバンクホークス": "ソフトバンク",
    "埼玉西武ライオンズ": "西武",
}
_TIME_RE = re.compile(r"(\d{1,2}):(\d{2})")


def fetch() -> list[Event]:
    today = _dt.date.today()
    events: list[Event] = []
    seen: set[tuple] = set()
    # 🔴 読めたページの数。1つも読めなければ失敗として上げる（2026-10-28：GitHubの機械から
    #    npb.jp が読めず「正常・0件」に見えて、日本シリーズの漏れに気づけなかった）。
    ok_pages = 0
    errors: list[str] = []
    # 🔴 日本シリーズは月別カレンダーに載らない（別ページ /nippons/YYYY/）。
    #    2026-10-27 の第3戦（みずほPayPayドーム）が配信から漏れ、アプリのイベント・
    #    AIの日報に出なかった（社長指摘 2026-10-28）。日本シリーズのページも読む。
    try:
        resp = http_get(f"https://npb.jp/nippons/{today.year}/",
                        accept="text/html,*/*")
        ok_pages += 1
        html = resp.content.decode("utf-8", "replace")
        for ev in _parse_nippon_series(html, today.year, today):
            key = (ev.venue.key, ev.date, ev.title)
            if key not in seen:
                seen.add(key)
                events.append(ev)
    except Exception as ex:
        # シリーズ前・ページ無し（404）は普通にある。月別も全部読めない時だけ失敗にする
        errors.append(f"nippons: {type(ex).__name__}: {ex}")
    for month_offset in range(4):
        y, m = _add_months(today.year, today.month, month_offset)
        url = f"https://npb.jp/games/{y}/schedule_{m:02d}.html"
        try:
            resp = http_get(url, accept="text/html,*/*")
        except Exception as ex:
            errors.append(f"{url}: {type(ex).__name__}: {ex}")
            continue
        ok_pages += 1
        html = resp.content.decode("utf-8", "replace")
        for ev in _parse(html, y, m, today):
            key = (ev.venue.key, ev.date, ev.title)
            if key in seen:
                continue
            seen.add(key)
            events.append(ev)
    if ok_pages == 0 and errors:
        raise RuntimeError("npb.jp を1ページも読めなかった: " + " / ".join(errors[:2]))
    return events


def _parse(html: str, year: int, month: int, today: _dt.date) -> list[Event]:
    doc = soup_of(html)
    events: list[Event] = []
    for a in doc.select("a.link_block"):
        states = a.select("td.state")
        if len(states) < 2:
            continue
        label = re.sub(r"\s", "", states[1].get_text())
        venue = _VENUE_BY_LABEL.get(label)
        if venue is None:
            continue  # 対象4球場以外（地方開催・他球場・予備日）
        cell = a.find_parent("td")
        date_el = cell.select_one("div.date") if cell else None
        if date_el is None:
            continue
        dm = re.search(r"(\d{1,2})", date_el.get_text())
        if not dm:
            continue
        try:
            d = _dt.date(year, month, int(dm.group(1)))
        except ValueError:
            continue
        if d < today:
            continue
        t1 = a.select_one("td.team1 img")
        t2 = a.select_one("td.team2 img")
        home = _SHORT.get((t1.get("alt") if t1 else "") or "", flatten_ws(t1.get("alt")) if t1 else "")
        away = _SHORT.get((t2.get("alt") if t2 else "") or "", flatten_ws(t2.get("alt")) if t2 else "")
        if not home or not away:
            continue
        hh = mm = None
        tm = _TIME_RE.search(states[0].get_text())
        if tm:
            hh, mm = int(tm.group(1)), int(tm.group(2))
        events.append(Event(
            venue=venue, date=d, title=f"{home} vs {away}",
            genre=GENRE_SPORTS, start_hour=hh, start_minute=mm,
        ))
    return events


# 日本シリーズのページの球団表記（地域名つき）→短縮名
_SERIES_SHORT = {
    "福岡ソフトバンク": "ソフトバンク", "横浜DeNA": "DeNA", "読売": "巨人", "巨人": "巨人",
    "東京ヤクルト": "ヤクルト", "阪神": "阪神", "中日": "中日", "広島東洋": "広島",
    "広島": "広島", "北海道日本ハム": "日本ハム", "オリックス": "オリックス",
    "東北楽天": "楽天", "千葉ロッテ": "ロッテ", "埼玉西武": "西武",
}
# 結果のリンク（/scores/YYYY/MMDD/h-db-03/）の先頭＝ホーム球団の記号→本拠地
#（終わった試合は球場名が消えるため。対象はこの取り込み口が持つ球場だけ）
_HOME_BY_CODE = {
    "h": PAYPAY_DOME, "db": YOKOHAMA_STADIUM, "s": MEIJI_JINGU, "t": KOSHIEN,
    "m": ZOZO_MARINE, "f": ESCON_FIELD, "e": RAKUTEN_PARK, "c": MAZDA_STADIUM,
}


def _parse_nippon_series(html: str, year: int, today: _dt.date) -> list[Event]:
    """日本シリーズ（npb.jp/nippons/YYYY/ の「試合日程・結果」）→ 予定。

    1試合＝`table.sp_table`：`th`=第N戦／`td.r1`=「10月28日（水）」／
    `td.r2 .t1`=ホーム（先に書かれる方）・`.score`=開始時刻（終わると点数）・`.t2`=ビジター／
    `td.r3`=球場名（終わった試合には無い→結果リンクのホーム記号から本拠地）。
    """
    doc = soup_of(html)
    events: list[Event] = []
    for tbl in doc.select("#series_result table.sp_table"):
        th = tbl.select_one("th")
        r1 = tbl.select_one("td.r1")
        if th is None or r1 is None:
            continue
        dm = re.search(r"(\d{1,2})月\s*(\d{1,2})日", r1.get_text())
        if not dm:
            continue
        try:
            d = _dt.date(year, int(dm.group(1)), int(dm.group(2)))
        except ValueError:
            continue
        if d < today:
            continue
        r3 = tbl.select_one("td.r3")
        venue = None
        if r3 is not None:
            venue = _VENUE_BY_LABEL.get(re.sub(r"\s", "", r3.get_text()))
        if venue is None:
            a = tbl.find_parent("a")
            m = re.search(r"/scores/\d{4}/\d{4}/([a-z]+)-", (a.get("href") if a else "") or "")
            if m:
                venue = _HOME_BY_CODE.get(m.group(1))
        if venue is None:
            continue  # この取り込み口が持たない球場（東京D・京セラD 等）
        def team(sel: str) -> str:
            el = tbl.select_one(sel)
            raw = re.sub(r"[○●△\s]", "", el.get_text() if el else "")
            return _SERIES_SHORT.get(raw, raw)
        home, away = team("td.r2 .t1"), team("td.r2 .t2")
        if not home or not away:
            continue
        hh = mm = None
        sc = tbl.select_one("td.r2 .score")
        tm = _TIME_RE.fullmatch(re.sub(r"\s", "", sc.get_text())) if sc else None
        if tm:
            hh, mm = int(tm.group(1)), int(tm.group(2))
        game_no = re.sub(r"\s", "", th.get_text())
        events.append(Event(
            venue=venue, date=d, title=f"日本シリーズ {game_no} {home} vs {away}",
            genre=GENRE_SPORTS, start_hour=hh, start_minute=mm,
        ))
    return events


def _add_months(year: int, month: int, delta: int) -> tuple[int, int]:
    idx = (year * 12 + (month - 1)) + delta
    return idx // 12, idx % 12 + 1


if __name__ == "__main__":
    for e in fetch():
        print(e.date, e.start_hour, e.venue.key, e.title)
