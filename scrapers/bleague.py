"""B.LEAGUE（PREMIER / ONE / NEXT）全クラブのホーム試合。

Jリーグ・プロ野球では会場が1つも作れない営業圏（京都市域・福井・三重・福岡県B地区
・島根・岩手・徳島市部 ほか）を埋める要。2026-08-09 の実測で全国113アリーナ・908試合。

ページの作り（2026-08-09 実測）:
  https://www.bleague.jp/schedule/?tab={1|2|3}&year=YYYY&mon=MM[&day=DD]
  - tab は 1=PREMIER / 2=ONE / 3=NEXT
  - 🔴 月を指定しただけでは**その月の最初の開催日1日分しか出ない**。
    同じページに `a.js_click_data[data-day]` として開催日の一覧が入っているので、
    そこから日を拾って `&day=DD` で1日ずつ取る。クラブ指定(`club=`)や月指定なしでも
    1日分しか返らないことを実測で確認済み＝**日ごとに取るしか手が無い**。
    このため1回の実行で **約300リクエスト**（3カテゴリ×5か月×約20開催日）になる。
    0.4秒ずつ間を空けて約2分。増やすときはこの数が比例して増えることを意識する。
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
from venues import (
    ARIAKE_ARENA, BL_ADASTRIA_MITO, BL_AGF_SUZUKA,
    BL_AIRA, BL_AISIN_ECHIZEN, BL_AKIBADAI,
    BL_ANABUKI_KAGAWA, BL_AOMORI_BUDOKAN, BL_AORE_NAGAOKA,
    BL_ARAKAWA, BL_ASUE_OSAKA, BL_BIWAJIMA,
    BL_BREX_UTSUNOMIYA, BL_BUTTERFLY_TOKOROZAWA, BL_CHIBA_PORT_ARENA,
    BL_CHICHIBUNOMIYA, BL_CNA_AKITA, BL_DEAI_DOME,
    BL_EDOGAWA, BL_EHIME_BUDOKAN, BL_ENTRIO_TOYODA,
    BL_ESFORTA_HACHIOJI, BL_FLAT_HACHINOHE, BL_FPCO_FUKUYAMA,
    BL_FUNABASHI_ARENA, BL_GLION_KOBE, BL_HAMAMATSU_ARENA,
    BL_HAPPINESS_ARENA, BL_HIROSHIMA_GREEN, BL_HIROSHIMA_SUNPLAZA,
    BL_HISAI, BL_HITACHI_IKENOKAWA, BL_HOKKAI_KITAERU,
    BL_ICHINOSEKI_UDOME, BL_ISHIKAWA_SPORTS, BL_JCOM_SHIMONOSEKI,
    BL_JTEKT_NARA, BL_KAGOSHIMA_KENSO, BL_KAKUHIRO_AOMORI,
    BL_KANAZAWA_SHISO, BL_KARIYA_SHITAI, BL_KIKUYO,
    BL_KITAKYUSHU_SOGO, BL_KOSHIGAYA, BL_KUMAMOTO_KENSO,
    BL_KURUME_ARENA, BL_LALA_ARENA, BL_MACHIDA_SHITAI,
    BL_MAEDA_ARENA, BL_MARUGAME_SHIMIN, BL_MATSUE_TAIIKUKAN,
    BL_MATSUYAMA_COMI, BL_MORIOKA_TAKAYA, BL_MUTSU_MAEDA,
    BL_NAKAMURA_SPORTS, BL_NIIGATA_HIGASHI, BL_NIKKAN_TOCHIGI,
    BL_NISSHIN_KYOTO, BL_OGINO, BL_OKB_GIFU,
    BL_OKINAWA_SUNTORY, BL_OOKINI_MAISHIMA, BL_OPENHOUSE_OTA,
    BL_OTA_SOGO, BL_ROHTO_ARENA_NARA, BL_SAGA_ARENA,
    BL_SAMUKAWA, BL_SHIGA_DAIHATSU, BL_SHIGETO_OKAYAMA,
    BL_SHIMADZU_KYOTO, BL_SHIZUOKA_CHUO, BL_SOKO_YOKKAICHI,
    BL_SUNARENA_SENDAI, BL_TACHIKAWA_TACHIHI, BL_TAKAMATSU_SOGO,
    BL_TAKAYAMA_BIG, BL_TAWARADA, BL_TERIHA_SEKISUI,
    BL_TODOROKI_ARENA, BL_TOGOSHI, BL_TOMONY_NAKA,
    BL_TOMONY_TOKUSHIMA, BL_TOYOTA_ARENA_TOKYO, BL_TSURUGA_SOGO,
    BL_TSURUSHIN_KOMAGI, BL_TSUYAMA, BL_URAWA_KOMABA,
    BL_WHITE_RING, BL_WING_KARIYA, BL_XEBIO_SENDAI,
    BL_YAMAGATA_KENSO, BL_YAMAGATA_SPORTS, BL_YKKAP_ARENA,
    BL_YOKOHAMA_BUDOKAN, BL_YOKOHAMA_BUNTAI, BL_YOYOGI_2,
    BL_ZENTSUJI, IG_ARENA,
)
from .base import http_get, soup_of, flatten_ws

_URL = "https://www.bleague.jp/schedule/?tab={tab}&year={y}&mon={m:02d}"
_TABS = (1, 2, 3)
# 🔴 当月＋4か月。3か月では季節を捉えられない（2026-27シーズンの試合の山は10〜1月で、
#    久留米アリーナ＝12月のみ・敦賀＝11月のみ。窓が狭いと福岡県B地区と福井が空になる）。
_MONTHS_AHEAD = 5
_SLEEP = 0.4             # 相手のサーバーに優しくする間隔

_TIME_RE = re.compile(r"(\d{1,2}):(\d{2})")

# (都道府県, アリーナ略称) → Venue。venues.py の定義と1対1。
_VENUE_BY_LABEL = {
    ("東京都", "トヨタA"): BL_TOYOTA_ARENA_TOKYO,
    ("神奈川県", "横浜BT"): BL_YOKOHAMA_BUNTAI,
    ("佐賀県", "Sアリ"): BL_SAGA_ARENA,
    ("北海道", "北海きた"): BL_HOKKAI_KITAERU,
    ("神奈川県", "とどろき"): BL_TODOROKI_ARENA,
    ("千葉県", "ららアリ"): BL_LALA_ARENA,
    ("岩手県", "盛岡"): BL_MORIOKA_TAKAYA,
    ("東京都", "立川立飛"): BL_TACHIKAWA_TACHIHI,
    ("長崎県", "ハピアリ"): BL_HAPPINESS_ARENA,
    ("群馬県", "オプアリ"): BL_OPENHOUSE_OTA,
    ("京都府", "日新電機"): BL_NISSHIN_KYOTO,
    ("長野県", "ホワイト"): BL_WHITE_RING,
    ("兵庫県", "Gアリ"): BL_GLION_KOBE,
    ("島根県", "松江総体"): BL_MATSUE_TAIIKUKAN,
    ("千葉県", "千葉PA"): BL_CHIBA_PORT_ARENA,
    ("富山県", "APアリ"): BL_YKKAP_ARENA,
    ("沖縄県", "沖アリ"): BL_OKINAWA_SUNTORY,
    ("埼玉県", "越谷"): BL_KOSHIGAYA,
    ("茨城県", "ADみと"): BL_ADASTRIA_MITO,
    ("宮城県", "ゼビオ"): BL_XEBIO_SENDAI,
    ("秋田県", "CNA"): BL_CNA_AKITA,
    ("熊本県", "熊本県総"): BL_KUMAMOTO_KENSO,
    ("東京都", "大田総合"): BL_OTA_SOGO,
    ("奈良県", "ロート"): BL_ROHTO_ARENA_NARA,
    ("滋賀県", "滋賀DH"): BL_SHIGA_DAIHATSU,
    ("大阪府", "おおきに"): BL_OOKINI_MAISHIMA,
    ("新潟県", "アオーレ"): BL_AORE_NAGAOKA,
    ("東京都", "エスアリ"): BL_ESFORTA_HACHIOJI,
    ("埼玉県", "浦和駒場"): BL_URAWA_KOMABA,
    ("香川県", "あなアリ"): BL_ANABUKI_KAGAWA,
    ("福岡県", "照葉積水"): BL_TERIHA_SEKISUI,
    ("神奈川県", "横浜武道"): BL_YOKOHAMA_BUDOKAN,
    ("栃木県", "ブレアリ"): BL_BREX_UTSUNOMIYA,
    ("愛媛県", "コミセン"): BL_MATSUYAMA_COMI,
    ("広島県", "グリアリ"): BL_HIROSHIMA_GREEN,
    ("愛知県", "WA刈谷"): BL_WING_KARIYA,
    ("徳島県", "トモニ"): BL_TOMONY_TOKUSHIMA,
    ("岡山県", "シゲトー"): BL_SHIGETO_OKAYAMA,
    ("岐阜県", "OKB"): BL_OKB_GIFU,
    ("山形県", "山形県総"): BL_YAMAGATA_KENSO,
    ("愛知県", "枇杷島"): BL_BIWAJIMA,
    ("石川県", "いしかわ"): BL_ISHIKAWA_SPORTS,
    ("山口県", "俵田"): BL_TAWARADA,
    ("鹿児島県", "鹿児体"): BL_KAGOSHIMA_KENSO,
    ("三重県", "AGF"): BL_AGF_SUZUKA,
    ("青森県", "カクヒロ"): BL_KAKUHIRO_AOMORI,
    ("愛知県", "刈谷市体"): BL_KARIYA_SHITAI,
    ("石川県", "金沢市総"): BL_KANAZAWA_SHISO,
    ("静岡県", "静岡中央"): BL_SHIZUOKA_CHUO,
    ("岡山県", "津山"): BL_TSUYAMA,
    ("神奈川県", "秋葉台"): BL_AKIBADAI,
    ("岐阜県", "で愛"): BL_DEAI_DOME,
    ("栃木県", "日環栃木"): BL_NIKKAN_TOCHIGI,
    ("埼玉県", "所沢市民"): BL_BUTTERFLY_TOKOROZAWA,
    ("奈良県", "Jアリ"): BL_JTEKT_NARA,
    ("静岡県", "浜松"): BL_HAMAMATSU_ARENA,
    ("鹿児島県", "せんだい"): BL_SUNARENA_SENDAI,
    ("東京都", "代々木２"): BL_YOYOGI_2,
    ("神奈川県", "寒川"): BL_SAMUKAWA,
    ("広島県", "エフピコ"): BL_FPCO_FUKUYAMA,
    ("東京都", "戸越"): BL_TOGOSHI,
    ("大阪府", "大阪中央"): BL_ASUE_OSAKA,
    ("茨城県", "日立アリ"): BL_HITACHI_IKENOKAWA,
    ("京都府", "島津"): BL_SHIMADZU_KYOTO,
    ("愛媛県", "愛媛武道"): BL_EHIME_BUDOKAN,
    ("東京都", "町田市体"): BL_MACHIDA_SHITAI,
    ("青森県", "FLAT"): BL_FLAT_HACHINOHE,
    ("山形県", "つるしん"): BL_TSURUSHIN_KOMAGI,
    ("東京都", "江戸川区"): BL_EDOGAWA,
    ("岐阜県", "高山"): BL_TAKAYAMA_BIG,
    ("青森県", "むつ"): BL_MUTSU_MAEDA,
    ("岩手県", "一関"): BL_ICHINOSEKI_UDOME,
    ("徳島県", "トモニ那"): BL_TOMONY_NAKA,
    ("鹿児島県", "姶良"): BL_AIRA,
    ("愛知県", "中村"): BL_NAKAMURA_SPORTS,
    ("青森県", "マエダ"): BL_MAEDA_ARENA,
    ("香川県", "丸亀"): BL_MARUGAME_SHIMIN,
    ("新潟県", "東総合"): BL_NIIGATA_HIGASHI,
    ("愛知県", "エントリ"): BL_ENTRIO_TOYODA,
    ("山形県", "山形スポ"): BL_YAMAGATA_SPORTS,
    ("青森県", "青森武道"): BL_AOMORI_BUDOKAN,
    ("福井県", "敦賀総合"): BL_TSURUGA_SOGO,
    ("香川県", "善通寺"): BL_ZENTSUJI,
    ("福井県", "アイシン"): BL_AISIN_ECHIZEN,
    ("福岡県", "久留米"): BL_KURUME_ARENA,
    ("熊本県", "菊陽総合"): BL_KIKUYO,
    ("三重県", "久居"): BL_HISAI,
    ("三重県", "相好アリ"): BL_SOKO_YOKKAICHI,
    ("東京都", "荒川総合"): BL_ARAKAWA,
    ("神奈川県", "荻野"): BL_OGINO,
    ("山口県", "下関"): BL_JCOM_SHIMONOSEKI,
    ("神奈川県", "秩父宮"): BL_CHICHIBUNOMIYA,
    ("広島県", "サンプラ"): BL_HIROSHIMA_SUNPLAZA,
    ("千葉県", "船アリ"): BL_FUNABASHI_ARENA,
    ("福岡県", "北九州"): BL_KITAKYUSHU_SOGO,
    ("香川県", "高松総合"): BL_TAKAMATSU_SOGO,
    ("愛知県", "IGアリ"): IG_ARENA,
    ("東京都", "有明M"): ARIAKE_ARENA,
    ("東京都", "有明S"): ARIAKE_ARENA,
}


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
