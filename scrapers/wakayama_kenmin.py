"""和歌山県民文化会館（大ホール・小ホール）。

和歌山地区は営業圏の中で会場が1つも無かった（2026-08-09 時点）。
Jリーグ・Bリーグのどちらも和歌山に本拠地が無いため、ここが唯一の入口になる。

ページの作り（2026-08-09 実測）:
  http://www.wacaf.or.jp/event/event_view.html?fyy=2026&fmm=08&hall=1
  - 🔴 https は WRONG_VERSION_NUMBER で繋がらない＝ http のみ
  - 🔴 文字コードは Shift_JIS（cp932）。requests の推定に任せると文字化けする
  - 中身は素の HTML テーブル。1行 = 日 / 曜 / 催物名 / 開演 / 入場料 / 主催
  - hall=1 大ホール / hall=2 小ホール（展示室 hall=345 は小さい展示のみで
    タクシー需要に結び付かないため取らない）
  - 月送りは fyy/fmm のパラメータ直指定。2027年3月分まで実データあり

開演の欄は「9:30」のほか「①11:30 ②15:00」（2回公演）や「未定」もある。
最初の時刻を採用し、取れなければ None（アプリがジャンル別の既定時刻を使う）。
"""
from __future__ import annotations

import datetime as _dt
import re

import requests

from model import Event, guess_genre
from venues import WAKAYAMA_KENMIN
from .base import UA, soup_of, flatten_ws

_URL = "http://www.wacaf.or.jp/event/event_view.html?fyy={y}&fmm={m:02d}&hall={h}"
_HALLS = (1, 2)          # 1=大ホール 2=小ホール
_MONTHS_AHEAD = 4

_WEEKDAY = "月火水木金土日"
_TIME_RE = re.compile(r"(\d{1,2}):(\d{2})")


def fetch() -> list[Event]:
    today = _dt.date.today()
    events: list[Event] = []
    seen: set[tuple] = set()
    for offset in range(_MONTHS_AHEAD):
        y, m = _add_months(today.year, today.month, offset)
        for hall in _HALLS:
            try:
                html = _get(_URL.format(y=y, m=m, h=hall))
            except Exception:
                continue
            for ev in _parse(html, y, m, today):
                k = ev.dedup_key()
                if k in seen:
                    continue
                seen.add(k)
                events.append(ev)
    return events


def _get(url: str) -> str:
    resp = requests.get(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"},
                        timeout=20)
    resp.raise_for_status()
    resp.encoding = "cp932"     # 🔴 明示しないと文字化けする
    return resp.text


def _parse(html: str, year: int, month: int, today: _dt.date) -> list[Event]:
    doc = soup_of(html)
    out: list[Event] = []
    for tr in doc.select("tr"):
        cells = [flatten_ws(td.get_text()) for td in tr.find_all("td", recursive=False)]
        if len(cells) != 6:
            continue
        day, week, title, start = cells[0], cells[1], cells[2], cells[3]
        if not day.isdigit() or week not in _WEEKDAY or not title:
            continue
        try:
            date = _dt.date(year, month, int(day))
        except ValueError:
            continue
        if date < today:
            continue
        hh = mm = None
        tm = _TIME_RE.search(start)      # 「①11:30 ②15:00」は先頭の回を採る
        if tm:
            h, mi = int(tm.group(1)), int(tm.group(2))
            if 0 <= h <= 23 and 0 <= mi <= 59:
                hh, mm = h, mi
        out.append(Event(
            venue=WAKAYAMA_KENMIN, date=date, title=title,
            genre=guess_genre(title), start_hour=hh, start_minute=mm,
        ))
    return out


def _add_months(year: int, month: int, delta: int) -> tuple[int, int]:
    idx = (year * 12 + (month - 1)) + delta
    return idx // 12, idx % 12 + 1


if __name__ == "__main__":
    for e in fetch():
        print(e.date, e.start_hour, e.genre, e.title)
