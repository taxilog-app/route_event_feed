"""熊谷文化創造館さくらめいと（埼玉県熊谷市拾六間）。

埼玉県北部地区＝県北交通圏（熊谷市・行田市・本庄市・深谷市ほか）＋秩父交通圏。
さいたま市や所沢のホールは全部「南部地区」なので、北部には会場が1つも無かった。

ページの作り（2026-08-10 実測）:
  https://www.sakuramate.jp/events/          （2ページ目以降 /events/page/N/）
  - li.events-archive__item が1公演
    .events-archive__item-title      … 催し名
    .events-archive__item-list-text  … 1つ目＝日時、【会場】の行＝会場名
    .post-category                   … 主催／共催／貸館 と 館の名前
  - 並びは「主催・共催 → 貸館」の順で、各グループの中は日付の**降順**

🔴 **年が書いていない**（「12月19日（土）」だけ）。ここが一番危ない所で、
   単純に「今の月より前なら翌年」とすると、ページの奥にある**終わった公演が
   来年の予定として生き返る**（貸館は過去ぶんも載ったままのため）。
   そこで曜日を検算に使う＝「12月19日（土）」が土曜になる年を選ぶ。
   曜日は年ごとにずれるので、今年か翌年かはこれで一意に決まる。
   曜日が書いていない行だけ、従来どおり月の大小で推測する。

3つの館（さくらめいと・あすねっと・ピピア）の予定が混ざっているが、
**さくらめいと（太陽のホール／月のホール）の分だけ**を取る。
あすねっと・ピピアは OSM に無く座標が取れなかった（2026-08-10）。
別の建物の座標で出すと運転手が違う場所へ向かうので、出さない方を選ぶ。
"""
from __future__ import annotations

import datetime as _dt
import re

from model import Event, guess_genre
from venues import SAKURAMATE
from .base import flatten_ws, http_get, soup_of

_URL = "https://www.sakuramate.jp/events/"
_PAGE_URL = "https://www.sakuramate.jp/events/page/{n}/"
_MAX_PAGES = 5          # 奥は終わった公演ばかり。5ページで先の予定は出そろう

# この館だけ取る（座標があるのはここだけ）
_OURS = ("さくらめいと", "太陽のホール", "月のホール")
_NOT_OURS = ("あすねっと", "ピピア")

_WEEKDAYS = "月火水木金土日"
_DATE_RE = re.compile(r"(\d{1,2})\s*月\s*(\d{1,2})\s*日\s*[（(]?\s*([月火水木金土日])?\s*[）)]?")
_KAIEN_RE = re.compile(r"開演\s*(\d{1,2}):(\d{2})")


def fetch() -> list[Event]:
    today = _dt.date.today()
    events: list[Event] = []
    seen: set[tuple] = set()
    for n in range(1, _MAX_PAGES + 1):
        url = _URL if n == 1 else _PAGE_URL.format(n=n)
        try:
            html = http_get(url, accept="text/html,*/*", timeout=20).text
        except Exception:
            break
        items = _parse(html, today)
        for ev in items:
            k = ev.dedup_key()
            if k in seen:
                continue
            seen.add(k)
            events.append(ev)
    return events


def _parse(html: str, today: _dt.date) -> list[Event]:
    doc = soup_of(html)
    out: list[Event] = []
    for li in doc.select("li.events-archive__item"):
        title_el = li.select_one(".events-archive__item-title")
        title = flatten_ws(title_el.get_text(" ")) if title_el else ""
        if not title:
            continue
        texts = [flatten_ws(t.get_text(" "))
                 for t in li.select(".events-archive__item-list-text")]
        if not texts:
            continue
        when = texts[0]
        hall = " ".join(texts[1:])
        cats = " ".join(flatten_ws(c.get_text(" ")) for c in li.select(".post-category"))
        place = f"{hall} {cats}"
        if any(x in place for x in _NOT_OURS) and not any(x in hall for x in ("太陽のホール", "月のホール")):
            continue
        if not any(x in place for x in _OURS):
            continue
        date = _date_of(when, today)
        if date is None or date < today:
            continue
        hh, mm = _start_time(when)
        out.append(Event(venue=SAKURAMATE, date=date, title=title,
                         genre=guess_genre(f"{title} {hall}"),
                         start_hour=hh, start_minute=mm))
    return out


def _date_of(when: str, today: _dt.date) -> _dt.date | None:
    """「12月19日（土）」→ 曜日が合う年を選ぶ。曜日が無ければ月の大小で推測。"""
    m = _DATE_RE.search(when)
    if not m:
        return None
    month, day = int(m.group(1)), int(m.group(2))
    weekday = m.group(3)
    candidates: list[_dt.date] = []
    for year in (today.year, today.year + 1):
        try:
            candidates.append(_dt.date(year, month, day))
        except ValueError:
            continue
    if not candidates:
        return None
    if weekday:
        for c in candidates:
            if _WEEKDAYS[c.weekday()] == weekday:
                return c
        return None            # どの年も曜日が合わない＝読み違い。出さない
    # 曜日なし＝従来どおりの推測（今より前の月なら翌年）
    for c in candidates:
        if c >= today:
            return c
    return candidates[0]


def _start_time(when: str) -> tuple[int | None, int | None]:
    m = _KAIEN_RE.search(when)
    if not m:
        return None, None
    hh, mm = int(m.group(1)), int(m.group(2))
    if 0 <= hh <= 23 and 0 <= mm <= 59:
        return hh, mm
    return None, None
