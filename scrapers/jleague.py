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
    JL_SANKYO_KASHIWA, JL_PEACE_NAGASAKI, JL_MITOSHIN, JL_ICHIGO, JL_SATOYAMA,
    JL_KURASUS, JL_SOYU, JL_HAWAIIANS, JL_PRIFOODS, JL_TOYAMA, JL_FUJIEDA,
    JL_POCARI, JL_CFS, JL_JIT, JL_NACK, JL_ND_YAMAGATA, JL_TOHO, JL_MIRAI,
    JL_KANSEKI, JL_GIKEN, JL_GOGO_KANAZAWA, JL_ALWIN, JL_NINJA, JL_MEGLIO,
    JL_NAGANO_U, JL_HATO, JL_ROHTO, JL_SHODA, JL_OKINAWA, JL_SHIRANAMI,
    JL_HIMA, JL_AXIS, JL_HANAZONO,
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
    "ＪＦＥス": JL_OKAYAMA,     # 🔴カタカナの「ス」（ひらがな「す」だと0件になる・2026-08-09実測）
    "札幌厚別": JL_ATSUBETSU,
    "メルスタ": JL_MERCARI,
    # ── 拡充第2弾（2026-08-09・J公式SFMS01の略称を実測して追加）──
    "三協Ｆ柏": JL_SANKYO_KASHIWA,
    "ピースタ": JL_PEACE_NAGASAKI,
    "水戸信ス": JL_MITOSHIN,
    "いちご": JL_ICHIGO,
    "アシさと": JL_SATOYAMA,
    "クラド": JL_KURASUS,
    "ソユスタ": JL_SOYU,
    "ハワスタ": JL_HAWAIIANS,
    "プラスタ": JL_PRIFOODS,
    "富山": JL_TOYAMA,
    "藤枝サ": JL_FUJIEDA,
    "鳴門大塚": JL_POCARI,
    "ＣＦＳ": JL_CFS,
    "ＪＩＴス": JL_JIT,
    "ＮＡＣＫ": JL_NACK,
    "ＮＤスタ": JL_ND_YAMAGATA,
    "とうスタ": JL_TOHO,
    "みらスタ": JL_MIRAI,
    "カンセキ": JL_KANSEKI,
    "ギケンス": JL_GIKEN,
    "ゴースタ": JL_GOGO_KANAZAWA,
    "サンアル": JL_ALWIN,
    "ニンスタ": JL_NINJA,
    "メグスタ": JL_MEGLIO,
    "長野Ｕ": JL_NAGANO_U,
    "ハトスタ": JL_HATO,
    "ロートＦ": JL_ROHTO,
    "正田スタ": JL_SHODA,
    "沖縄県陸": JL_OKINAWA,
    "白波スタ": JL_SHIRANAMI,
    "ヒマスタ": JL_HIMA,
    "Ａｘｉｓ": JL_AXIS,
    "花園": JL_HANAZONO,
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
