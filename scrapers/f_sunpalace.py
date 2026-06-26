"""福岡サンパレス（f-sunpalace.com/hall/）。

event_service.dart の _fetchSunpalace / _parseSunpalaceHtml を移植。
現在月＋翌月を取得して結合。
"""
from __future__ import annotations

import datetime as _dt
import re

from model import Event, guess_genre
from venues import FUKUOKA_SUNPALACE
from .base import http_get, soup_of, flatten_ws

_DAY_RE = re.compile(r"(\d{1,2})")
_TIME_RE = re.compile(r"(\d{1,2}):(\d{2})")


def fetch() -> list[Event]:
    now = _dt.date.today()
    nxt = _dt.date(now.year + (now.month // 12), (now.month % 12) + 1, 1)
    out: list[Event] = []
    for year, month in ((now.year, now.month), (nxt.year, nxt.month)):
        try:
            resp = http_get(
                f"https://www.f-sunpalace.com/hall/?ym={year}-{month:02d}",
                accept="text/html,*/*")
            out.extend(_parse(resp.text, year, month))
        except Exception:
            continue
    return out


def _parse(html: str, year: int, month: int) -> list[Event]:
    # 年月は取得対象の ym をそのまま使う（ページからは推測しない）。
    # 公式ページの見出しには月表記が無く、本文先頭のカレンダーが常に当月を
    # 指すため、以前は7月ページの公演を6月と誤判定し、浜崎あゆみ等が
    # 1ヶ月手前にズレて配信されていた。
    doc = soup_of(html)
    events: list[Event] = []
    today = _dt.date.today()
    section = doc.select_one("section.schedule")
    if section is None:
        return events

    for li in section.select("li"):
        date_el = li.select_one(".date")
        if date_el is None:
            continue
        en_el = date_el.select_one(".en")
        day_str = (en_el.get_text() if en_el else date_el.get_text()).strip()
        dm = _DAY_RE.search(day_str)
        if not dm:
            continue
        day = int(dm.group(1))
        try:
            date = _dt.date(year, month, day)
        except ValueError:
            continue
        if date < today:
            continue
        name_el = li.select_one(".name")
        title = flatten_ws(name_el.get_text() if name_el else "")
        if not title:
            continue
        hh = mm = None
        start_el = li.select_one(".starting")
        if start_el:
            tm = _TIME_RE.search(start_el.get_text())
            if tm:
                hh, mm = int(tm.group(1)), int(tm.group(2))
        events.append(Event(
            venue=FUKUOKA_SUNPALACE, date=date, title=title,
            genre=guess_genre(title), start_hour=hh, start_minute=mm,
        ))
    return events
