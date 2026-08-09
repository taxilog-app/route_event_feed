"""B.LEAGUE（PREMIER / ONE / NEXT）全クラブのホーム試合。

Jリーグ・プロ野球では会場が1つも作れない営業圏（京都市域・福井・三重・福岡県B地区
・島根・岩手・徳島市部 ほか）を埋める要。2026-08-09 の実測で全国113アリーナ・908試合。

ページの作り（2026-08-09 実測）:
  https://www.bleague.jp/schedule/?tab={1|2|3}&year=YYYY&mon=MM[&day=DD]
  - tab は 1=PREMIER / 2=ONE / 3=NEXT
  - 🔴 月を指定しただけでは**その月の最初の開催日1日分しか出ない**。
    同じページに `a.js_click_data[data-day]` として開催日の一覧が入っているので、
    そこから日を拾って `&day=DD` で1日ずつ取る（だから1回の実行で百数十リクエストになる）。
  - 1試合 = `li.list-item`。`.info-arena` が「県名 | アリーナ略称 開始時刻」、
    `.team-name` が ホーム・アウェイの順で2つ。

会場はJリーグ同様に**略称**でしか出ないので _VENUE_BY_LABEL で対応させる。
未対応の略称は座標が無いのでスキップする（黙って落ちるが、会場を足せば拾える）。
略称は (都道府県, 略称) の組で引く＝同じ略称が別の県にあっても取り違えない。
"""
from __future__ import annotations

import datetime as _dt
import re
import time

from model import Event, GENRE_SPORTS
from .base import http_get, soup_of, flatten_ws

_URL = "https://www.bleague.jp/schedule/?tab={tab}&year={y}&mon={m:02d}"
_TABS = (1, 2, 3)
_MONTHS_AHEAD = 3        # 当月＋2か月。増やすとリクエスト数が比例して増える
_SLEEP = 0.3             # 相手のサーバーに優しくする間隔

_TIME_RE = re.compile(r"(\d{1,2}):(\d{2})")

# (都道府県, アリーナ略称) → Venue。venues.py の定義と1対1。
_VENUE_BY_LABEL: dict[tuple[str, str], object] = {}


def fetch() -> list[Event]:
    today = _dt.date.today()
    events: list[Event] = []
    seen: set[tuple] = set()
    for tab in _TABS:
        for offset in range(_MONTHS_AHEAD):
            y, m = _add_months(today.year, today.month, offset)
            base = _URL.format(tab=tab, y=y, m=m)
            try:
                html = http_get(base, accept="text/html,*/*").text
            except Exception:
                continue
            days = _days_in(html)
            for day in days:
                try:
                    page = http_get(f"{base}&day={day}", accept="text/html,*/*").text
                except Exception:
                    continue
                for ev in _parse(page, y, m, day, today):
                    k = ev.dedup_key()
                    if k in seen:
                        continue
                    seen.add(k)
                    events.append(ev)
                time.sleep(_SLEEP)
            time.sleep(_SLEEP)
    return events


def _days_in(html: str) -> list[str]:
    doc = soup_of(html)
    days = {a.get("data-day") for a in doc.select("a.js_click_data[data-day]")}
    return sorted(d for d in days if d and d.isdigit())


def _parse(html: str, year: int, month: int, day: str,
           today: _dt.date) -> list[Event]:
    doc = soup_of(html)
    try:
        date = _dt.date(year, month, int(day))
    except ValueError:
        return []
    if date < today:
        return []
    out: list[Event] = []
    for li in doc.select("li.list-item"):
        arena_el = li.select_one(".info-arena")
        if arena_el is None:
            continue
        pref, _, rest = flatten_ws(arena_el.get_text()).partition("|")
        bits = rest.strip().split(" ")
        if not bits:
            continue
        venue = _VENUE_BY_LABEL.get((pref.strip(), bits[0]))
        if venue is None:
            continue                    # 未対応のアリーナ（座標が無い）
        names = [flatten_ws(x.get_text()) for x in li.select(".team-name")]
        if len(names) < 2 or not names[0] or not names[1]:
            continue
        hh = mm = None
        tm = _TIME_RE.search(rest)
        if tm:
            h, mi = int(tm.group(1)), int(tm.group(2))
            if 0 <= h <= 23 and 0 <= mi <= 59:
                hh, mm = h, mi
        out.append(Event(
            venue=venue, date=date, title=f"{names[0]} vs {names[1]}",
            genre=GENRE_SPORTS, start_hour=hh, start_minute=mm,
        ))
    return out


def _add_months(year: int, month: int, delta: int) -> tuple[int, int]:
    idx = (year * 12 + (month - 1)) + delta
    return idx // 12, idx % 12 + 1


if __name__ == "__main__":
    for e in fetch():
        print(e.date, e.start_hour, e.venue.key, e.title)
