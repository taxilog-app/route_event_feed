"""ボートレース福岡（福岡市中央区那の津）の開催日。社長指示 2026-10-06。

開催日は那の津・天神周辺で帰りのお客様が増える（最終レースの後）。

【🔴 許諾の状況＝問い合わせ中・事実だけ出す】
  BOAT RACE オフィシャル（boatrace.jp）の規定は「著作権者の許諾なく、私的使用など
  法律によって認められる範囲を超えて、無断で使用することはできません」。
  社長判断 2026-10-06＝**(A) ボートレース福岡へ問い合わせる**と**同時に**、
  **(B) 開催日・競走名・レース時刻という事実だけ**を出す。
  文面＝~/Developer/taxi関連/書類/問い合わせ_ボートレース福岡_開催日程の利用_2026-10-06.md
  先方から止めるよう連絡が来たら **ENABLED = False** にして配り直せば、この会場だけ消える。

【ページの作り（2026-10-06 実測）】
  月間スケジュール https://www.boatrace.jp/owpc/pc/race/monthlyschedule?ym=YYYYMM
  - 表は**前月末〜翌月頭**まで約39日の横長（見出し行に「27日」「28月」…と日付）
  - 1行＝1つのボートレース場。福岡は場コード22（行の中に jcd=22）
  - 開催は colspan＝日数 のセル。空き日は &nbsp; のセル。
    ⚠️ セルの中のリンクの hd= は開催の初日とは限らない（開催中は「今日」になる）。
       **日付は必ず見出しの列の位置から取る**（hd= を信じない）。
  レース時刻 https://www.boatrace.jp/owpc/pc/race/raceindex?jcd=22&hd=YYYYMMDD
  - 締切予定時刻が12個並ぶ（例 11:00 … 16:41）。**当日・直前しか出ない**（先の日は空）。

【時刻の扱い】
  取れた日は「第1レースの時刻」を開始にし、題名に「最終レース16:41頃」を付ける。
  取れない日（先の日）は、実測（2026-10-06：11:00〜16:41＝昼開催）に合わせて 11:00 開始。
  アプリは会場ごとの所要時間で終わりを見積もる（boatrace_fukuoka＝約5時間45分）。
"""
from __future__ import annotations

import datetime as _dt
import re

from model import Event, GENRE_SPORTS
from venues import BOATRACE_FUKUOKA
from .base import http_get

# 🔴 先方から止めるよう連絡が来たら False にする（この会場だけ消える）
ENABLED = True

_JCD = "22"
_MONTHLY = "https://www.boatrace.jp/owpc/pc/race/monthlyschedule?ym={ym}"
_RACEINDEX = "https://www.boatrace.jp/owpc/pc/race/raceindex?jcd=22&hd={hd}"
_DEFAULT_START = (11, 0)  # 実測 2026-10-06（昼開催）

_ROW_RE = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S)
_CELL_RE = re.compile(r"<(t[hd])([^>]*)>(.*?)</t[hd]>", re.S)
_COLSPAN_RE = re.compile(r'colspan\s*=\s*"?(\d+)')
_TAG_RE = re.compile(r"<[^>]+>")
_HEAD_DAY_RE = re.compile(r"^(\d{1,2})")
_TIME_RE = re.compile(r"\b(\d{1,2}):(\d{2})\b")


def fetch() -> list[Event]:
    if not ENABLED:
        return []
    if BOATRACE_FUKUOKA.lat is None:
        # 🔴 場所（タクシーが着ける所）が未確認。当てずっぽうの座標は配らない。
        print("  ⚠️ ボートレース福岡：場所が未設定のため配りません（venues.py）")
        return []
    today = _dt.date.today()
    days: dict[_dt.date, str] = {}
    first = today.replace(day=1)
    nxt = (first + _dt.timedelta(days=32)).replace(day=1)
    for m in (first, nxt):
        html = http_get(_MONTHLY.format(ym=m.strftime("%Y%m")),
                        accept="text/html,*/*").text
        # 2か月ぶんの表は日付が重なる。名前が空の側で、名前のある日を上書きしない
        for d, name in parse_monthly(html, m).items():
            if name or d not in days:
                days[d] = name
    events = []
    for d in sorted(days):
        if d < today:
            continue
        title = days[d] or "開催"
        sh, sm = _DEFAULT_START
        times = _race_times(d) if (d - today).days <= 1 else []
        suffix = "（昼開催）"
        if len(times) >= 2:
            sh, sm = times[0]
            lh, lm = times[-1]
            suffix = f"（最終レース {lh}:{lm:02d}頃）"
        events.append(Event(
            venue=BOATRACE_FUKUOKA, date=d,
            title=f"ボートレース福岡 {title}{suffix}",
            genre=GENRE_SPORTS, start_hour=sh, start_minute=sm,
        ))
    return events


def _race_times(d: _dt.date) -> list[tuple[int, int]]:
    try:
        html = http_get(_RACEINDEX.format(hd=d.strftime("%Y%m%d")),
                        accept="text/html,*/*").text
    except Exception:
        return []
    ts = sorted({(int(h), int(m)) for h, m in _TIME_RE.findall(html)
                 if 8 <= int(h) <= 22})
    return ts if len(ts) >= 6 else []  # 12レース分が並んでいない時は使わない


def _text(s: str) -> str:
    return re.sub(r"\s+", " ", _TAG_RE.sub("", s)).replace("&nbsp;", "").strip()


def parse_monthly(html: str, month: _dt.date) -> dict[_dt.date, str]:
    """月間スケジュールから、福岡の開催日 → 競走名。見出しの列の位置で日付を決める。"""
    rows = _ROW_RE.findall(html)
    head = None
    for r in rows:
        cells = _CELL_RE.findall(r)
        texts = [_text(c[2]) for c in cells]
        if sum(1 for t in texts if re.match(r"^\d{1,2}[月火水木金土日]$", t)) >= 20:
            head = texts[1:]
            break
    if head is None:
        raise ValueError("月間スケジュールの見出し（日付の列）が見つからない＝ページの作りが変わった")

    # 見出しの日付を本当の日付に直す。1日に戻ったら次の月。
    start_month = month if int(_HEAD_DAY_RE.match(head[0]).group(1)) <= 7 \
        else (month - _dt.timedelta(days=1)).replace(day=1)
    dates: list[_dt.date] = []
    y, m = start_month.year, start_month.month
    prev = 0
    for t in head:
        dd = int(_HEAD_DAY_RE.match(t).group(1))
        if dd < prev:
            m += 1
            if m == 13:
                y, m = y + 1, 1
        dates.append(_dt.date(y, m, dd))
        prev = dd

    row = next((r for r in rows if f"jcd={_JCD}" in r), None)
    if row is None:
        raise ValueError("福岡（jcd=22）の行が見つからない")
    out: dict[_dt.date, str] = {}
    col = 0
    for tag, attrs, inner in _CELL_RE.findall(row):
        if tag == "th":
            continue
        span = int(_COLSPAN_RE.search(attrs).group(1)) if _COLSPAN_RE.search(attrs) else 1
        is_meet = "gradeColor" in attrs
        if is_meet:
            name = _text(inner)
            for i in range(col, min(col + span, len(dates))):
                out[dates[i]] = name
        col += span
    if col != len(dates):
        raise ValueError(f"列の数が合わない（見出し{len(dates)}列・福岡の行{col}列）")
    return out
