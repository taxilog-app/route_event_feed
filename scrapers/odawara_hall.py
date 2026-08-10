"""小田原三の丸ホール（正式名称：小田原市民ホール）。

小田原地区＝小田原交通圏（小田原市・南足柄市・大井町・開成町・山北町・松田町・
箱根町・湯河原町・真鶴町）。Jクラブもバスケも無く、会場が1つも無かった営業圏。

ページの作り（2026-08-10 実測）:
  https://ooo-hall.jp/event/?ey=2026&em=09   ← 月は ey/em の直指定で送れる
  - ul.extEventDetailListUL > li が1公演
    .bCatListLabel .bcatlabellist … 会場（大ホール／小ホール／展示室／スタジオ…）
    strong > a                    … 催し名
    table の「日時」行             … 2026年8月2日（日） 14:00～16:00（13:30 開場）
  - 日時に**西暦が入っている**ので年を推測しなくてよい（さくらめいと等と違う点）

取る会場を大ホール・小ホールに絞る:
  展示室・ギャラリー回廊・スタジオ・練習室・会議室は数人〜数十人規模で、
  タクシー需要に結び付かない。和歌山県民文化会館で展示室を外したのと同じ判断。
  ここを入れると「イベントあり」が毎日点いて、本当の公演の価値が薄まる。

開演時刻は「14:00～16:00（13:30 開場）」の**最初の時刻**を採る（＝開演）。
「（13:30 開場）」の方を拾わないよう、括弧の外側の時刻を先に見る。
"""
from __future__ import annotations

import datetime as _dt
import re

from model import Event, guess_genre
from venues import ODAWARA_SANNOMARU_HALL
from .base import flatten_ws, http_get, soup_of

_URL = "https://ooo-hall.jp/event/?ey={y}&em={m:02d}"
_MONTHS_AHEAD = 4

# タクシー需要になる箱だけ（上の注記）
_WANTED_HALLS = ("大ホール", "小ホール")

_DATE_RE = re.compile(r"(\d{4})年\s*(\d{1,2})月\s*(\d{1,2})日")
# 「～8月9日」「～2027年1月5日」＝終わり側は年・月が省かれることがある
_END_RE = re.compile(r"[～〜~]\s*(?:(\d{4})年\s*)?(?:(\d{1,2})月\s*)?(\d{1,2})日")
_TIME_RE = re.compile(r"(\d{1,2}):(\d{2})")

_MAX_SPAN_DAYS = 40      # これを超える長期展示は開始日だけ（base.expand_jp_date_range と同じ考え）


def fetch() -> list[Event]:
    today = _dt.date.today()
    events: list[Event] = []
    seen: set[tuple] = set()
    for offset in range(_MONTHS_AHEAD):
        y, m = _add_months(today.year, today.month, offset)
        try:
            html = http_get(_URL.format(y=y, m=m), accept="text/html,*/*", timeout=20).text
        except Exception:
            continue
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
    for li in doc.select("ul.extEventDetailListUL > li"):
        label = li.select_one(".bCatListLabel .bcatlabellist")
        hall = flatten_ws(label.get_text(" ")) if label else ""
        if not any(w in hall for w in _WANTED_HALLS):
            continue
        title_el = li.select_one("strong a") or li.select_one("strong")
        title = flatten_ws(title_el.get_text(" ")) if title_el else ""
        if not title:
            continue
        when = _row_value(li, "日時")
        if not when:
            continue
        dates = _dates_of(when, today)
        if not dates:
            continue
        hh, mm = _start_time(when)
        genre = guess_genre(f"{title} {hall}")
        for d in dates:
            out.append(Event(venue=ODAWARA_SANNOMARU_HALL, date=d, title=title,
                             genre=genre, start_hour=hh, start_minute=mm))
    return out


def _row_value(li, header: str) -> str:
    """table の「日時」など見出し行の中身を取る。"""
    for tr in li.select("table tr"):
        th = tr.find("th")
        td = tr.find("td")
        if th is None or td is None:
            continue
        if header in flatten_ws(th.get_text(" ")):
            return flatten_ws(td.get_text(" "))
    return ""


def _dates_of(when: str, today: _dt.date) -> list[_dt.date]:
    sm = _DATE_RE.search(when)
    if not sm:
        return []
    try:
        start = _dt.date(int(sm.group(1)), int(sm.group(2)), int(sm.group(3)))
    except ValueError:
        return []
    end = start
    em = _END_RE.search(when[sm.end():])
    if em:
        year = int(em.group(1)) if em.group(1) else start.year
        month = int(em.group(2)) if em.group(2) else start.month
        if em.group(1) is None and month < start.month:
            year = start.year + 1          # 12月～1月 のまたぎ
        try:
            cand = _dt.date(year, month, int(em.group(3)))
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


def _start_time(when: str) -> tuple[int | None, int | None]:
    """開演時刻＝括弧の外の最初の時刻。「（13:30 開場）」を拾わないため。"""
    outside = re.sub(r"[（(][^）)]*[）)]", " ", when)
    m = _TIME_RE.search(outside) or _TIME_RE.search(when)
    if not m:
        return None, None
    hh, mm = int(m.group(1)), int(m.group(2))
    if 0 <= hh <= 23 and 0 <= mm <= 59:
        return hh, mm
    return None, None


def _add_months(year: int, month: int, offset: int) -> tuple[int, int]:
    total = (year * 12 + month - 1) + offset
    return total // 12, total % 12 + 1
