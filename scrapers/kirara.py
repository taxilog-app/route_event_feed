"""山中湖交流プラザ きらら（山梨県南都留郡山中湖村）。

山梨県B地区＝東部・富士北麓交通圏（富士吉田市・大月市・都留市・山中湖村ほか）。
甲府のホールは全部A地区なので、B地区には会場が1つも無かった。
ここは SWEET LOVE SHOWER・Mt.FUJIMAKI といった屋外の大型フェス会場で、
動員が数万人規模＝この営業圏では突出して大きいタクシー需要になる。

ページの作り（2026-08-10 実測）:
  http://www.kirarayamanakako.jp/event.php   ← 🔴 https は繋がらない（http のみ）
  - 「年」ごとにテーブルが1つ（2026年ぶん／2027年ぶん）
  - 見出し行 = 日程 / イベント名 / 会場 / イベント情報
  - 「8月」だけの1セル行が月の区切り。以降の行はその月の日として読む
  - 日程は「8日(土)～9日(日)」「5日(土)」＝**月も年も書いていない**
  - 会場は「全施設」「シアターひびき」「原っぱ 臨時駐車場」など

年は「テーブルの前に出てくる 20XX 年」から取る。月は直前の月区切り行から取る。
開演時刻は載っていないので None（アプリがジャンル別の既定時刻を使う）。
"""
from __future__ import annotations

import datetime as _dt
import re

from model import Event, guess_genre
from venues import KIRARA_YAMANAKAKO
from .base import flatten_ws, http_get, soup_of

# 🔴 https は証明書が繋がらない（2026-08-10 実測）。http で取る。
_URL = "http://www.kirarayamanakako.jp/event.php"

_YEAR_RE = re.compile(r"(20\d{2})\s*年")
_MONTH_RE = re.compile(r"^(\d{1,2})\s*月$")
_DAY_RE = re.compile(r"(\d{1,2})\s*日")
_MAX_SPAN_DAYS = 10       # フェスは長くて数日。これを超える行は形が壊れたとみなし開始日だけ


def fetch() -> list[Event]:
    today = _dt.date.today()
    html = http_get(_URL, accept="text/html,*/*", timeout=20).text
    events: list[Event] = []
    seen: set[tuple] = set()
    for ev in _parse(html, today):
        k = ev.dedup_key()
        if k in seen:
            continue
        seen.add(k)
        events.append(ev)
    return events


def _parse(html: str, today: _dt.date) -> list[Event]:
    doc = soup_of(html)
    out: list[Event] = []
    for table in doc.find_all("table"):
        year = _year_before(table, today)
        month: int | None = None
        for tr in table.find_all("tr"):
            cells = [flatten_ws(c.get_text(" ")) for c in tr.find_all(["th", "td"])]
            cells = [c for c in cells if c != ""]
            if len(cells) == 1:
                m = _MONTH_RE.match(cells[0])
                if m:
                    month = int(m.group(1))
                continue
            if len(cells) < 2 or month is None:
                continue
            when, title = cells[0], cells[1]
            hall = cells[2] if len(cells) > 2 else ""
            if title in ("イベント名",) or "日程" in when:
                continue                      # 見出し行
            for d in _dates_of(when, year, month, today):
                out.append(Event(venue=KIRARA_YAMANAKAKO, date=d, title=title,
                                 genre=guess_genre(f"{title} {hall}", is_dome=True),
                                 start_hour=None, start_minute=None))
    return out


def _year_before(table, today: _dt.date) -> int:
    """テーブルの直前に出てくる「20XX 年」を年とする。無ければ今年。"""
    node = table
    for _ in range(6):
        node = node.find_previous(string=_YEAR_RE)
        if node is None:
            break
        m = _YEAR_RE.search(str(node))
        if m:
            return int(m.group(1))
    return today.year


def _dates_of(when: str, year: int, month: int, today: _dt.date) -> list[_dt.date]:
    """「8日(土)～9日(日)」「5日(土)」を日付に開く。

    月をまたぐ「31日～1日」も扱う（終わりが始まりより小さければ翌月）。
    """
    days = [int(x) for x in _DAY_RE.findall(when)]
    if not days:
        return []
    try:
        start = _dt.date(year, month, days[0])
    except ValueError:
        return []
    end = start
    if len(days) > 1:
        y2, m2 = (year, month) if days[-1] >= days[0] else _next_month(year, month)
        try:
            cand = _dt.date(y2, m2, days[-1])
            if cand >= start:
                end = cand
        except ValueError:
            pass
    if (end - start).days > _MAX_SPAN_DAYS:
        end = start
    out = []
    d = start
    while d <= end:
        if d >= today:
            out.append(d)
        d += _dt.timedelta(days=1)
    return out


def _next_month(year: int, month: int) -> tuple[int, int]:
    return (year + 1, 1) if month == 12 else (year, month + 1)
