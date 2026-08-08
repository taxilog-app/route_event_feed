"""J1/J2/J3 全クラブのホーム試合（J公式データサイト1ソース）。

data.j-league.or.jp/SFMS01 の試合検索を competition_frame_ids=1,2,3(J1/J2/J3) で取得。
1テーブルに全試合が並ぶ。会場は略称なので _VENUE_BY_LABEL でマッピングする
（J1全クラブ＋各営業圏の主要スタジアム）。未マップの会場は座標が無いためスキップ。

野球(npb_baseball.py)の設計を踏襲。旧・個別スクレイパー(avispa/cerezo)はこれに統合。
"""
from __future__ import annotations

import datetime as _dt
import re

from model import Event, GENRE_SPORTS
from venues import (
    AJINOMOTO_STADIUM, BEST_DENKI_STADIUM, NISSAN_STADIUM, SAPPORO_DOME,
    JL_KOKURITSU, JL_SAITAMA, JL_TODOROKI, JL_NIPPATSU, JL_LEMON, JL_MACHIDA,
    JL_GIONS, JL_YAMAHA, JL_IAI, JL_TOYOTA, JL_MIZUHO, JL_PANASTA, JL_YODOKO,
    JL_NOEVIR, JL_SANGA, JL_EDION, JL_YURTEC, JL_DENKA, JL_FUKUARI, JL_MIKUNI,
    JL_EKIMAE, JL_EGAO, JL_OKAYAMA, JL_ATSUBETSU, JL_MERCARI,
)
from .base import http_get, soup_of, flatten_ws

_SEARCH = ("https://data.j-league.or.jp/SFMS01/search"
           "?competition_years={y}&competition_frame_ids={f}")

# スタジアム略称（td）→ Venue。J1全クラブ＋各営業圏の主要スタジアム。
_VENUE_BY_LABEL = {
    "味スタ": AJINOMOTO_STADIUM,
    "ベススタ": BEST_DENKI_STADIUM,
    "日産ス": NISSAN_STADIUM,
    "プレド": SAPPORO_DOME,          # 大和ハウス プレミストドーム（札幌ドーム）
    "MUFG国立": JL_KOKURITSU,
    "埼玉": JL_SAITAMA,
    "Ｕ等々力": JL_TODOROKI,
    "ニッパツ": JL_NIPPATSU,
    "レモンＳ": JL_LEMON,
    "Ｇスタ": JL_MACHIDA,
    "ギオンス": JL_GIONS,
    "ヤマハ": JL_YAMAHA,
    "アイスタ": JL_IAI,
    "豊田ス": JL_TOYOTA,
    "パロ瑞穂": JL_MIZUHO,
    "パナスタ": JL_PANASTA,
    "ハナサカ": JL_YODOKO,           # ヨドコウ桜スタジアム
    "ノエスタ": JL_NOEVIR,
    "サンガＳ": JL_SANGA,
    "Ｅピース": JL_EDION,
    "ユアスタ": JL_YURTEC,
    "デンカＳ": JL_DENKA,
    "フクアリ": JL_FUKUARI,
    "ミクスタ": JL_MIKUNI,
    "駅スタ": JL_EKIMAE,
    "えがおＳ": JL_EGAO,
    "ＪＦＥす": JL_OKAYAMA,
    "札幌厚別": JL_ATSUBETSU,
    "メルスタ": JL_MERCARI,
}

_DATE_RE = re.compile(r"(\d{2})/(\d{2})/(\d{2})")   # YY/MM/DD
_TIME_RE = re.compile(r"^(\d{1,2}):(\d{2})$")


def fetch() -> list[Event]:
    today = _dt.date.today()
    # 秋春制でシーズンが年をまたぐため、上期は前年シーズンも見る
    years = {today.year}
    if today.month <= 6:
        years.add(today.year - 1)
    events: list[Event] = []
    seen: set[tuple] = set()
    for y in sorted(years):
        for frame in (1, 2, 3):
            try:
                resp = http_get(_SEARCH.format(y=y, f=frame), accept="text/html,*/*")
            except Exception:
                continue
            for ev in _parse(resp.text, today):
                k = (ev.venue.key, ev.date, ev.title)
                if k in seen:
                    continue
                seen.add(k)
                events.append(ev)
    return events


def _parse(html: str, today: _dt.date) -> list[Event]:
    doc = soup_of(html)
    out: list[Event] = []
    for tr in doc.select("tr"):
        cells = [flatten_ws(c.get_text()) for c in tr.select("td")]
        cells = [c for c in cells if c and c != "\xa0"]
        if "vs" not in cells:
            continue
        i = cells.index("vs")
        if i - 1 < 0 or i + 2 >= len(cells):
            continue
        home, away, label = cells[i - 1], cells[i + 1], cells[i + 2]
        venue = _VENUE_BY_LABEL.get(label)
        if venue is None:
            continue
        dm = next((_DATE_RE.search(c) for c in cells if _DATE_RE.search(c)), None)
        if not dm:
            continue
        date = _dt.date(2000 + int(dm.group(1)), int(dm.group(2)), int(dm.group(3)))
        if date < today:
            continue
        hh = mm = None
        tm = next((_TIME_RE.match(c) for c in cells if _TIME_RE.match(c)), None)
        if tm:
            hh, mm = int(tm.group(1)), int(tm.group(2))
        out.append(Event(
            venue=venue, date=date, title=f"{home} vs {away}",
            genre=GENRE_SPORTS, start_hour=hh, start_minute=mm,
        ))
    return out


if __name__ == "__main__":
    for e in fetch():
        print(e.date, e.start_hour, e.venue.key, e.title)
