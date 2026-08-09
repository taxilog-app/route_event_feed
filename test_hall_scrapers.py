"""ホール系スクレイパーの解析部の回帰テスト（ネットに出ない）。

和歌山・函館は「その営業圏で唯一の会場」なので、解析が壊れると
その圏のイベントが丸ごと0件になる（＝運転手には「何も無い」に見える）。
サイトの作りが変わったときに気づけるよう、実物から取った見本で解析部だけを検査する。

実行:  python3 test_hall_scrapers.py
"""
import datetime as _dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scrapers import wakayama_kenmin as wk          # noqa: E402
from scrapers import hakodate_kaikan as hk          # noqa: E402

TODAY = _dt.date(2026, 8, 1)

# ── 和歌山県民文化会館：実物のテーブル1行ぶん（2026-08 大ホール より） ──
WAKAYAMA_HTML = """
<table><tr><td>1</td><td>土</td><td></td><td></td><td></td><td></td></tr>
<tr><td>4</td><td>火</td><td>第2回日本和歌山国際音楽祭大祭</td><td>9:30</td>
    <td>無料</td><td>日本和歌山国際音楽祭 新希望楽団</td></tr>
<tr><td>9</td><td>日</td><td>爆笑!!お笑いフェスin和歌山</td>
    <td>&#9312;11:30 &#9313;15:00</td><td>前売4,500円</td><td>主催者</td></tr>
<tr><td>29</td><td>土</td><td>ゴスペラーズ坂ツアー2026</td><td>17:00</td>
    <td>9,000</td><td>サウンドクリエーター</td></tr>
<tr><td>30</td><td>日</td><td>時刻未定の催し</td><td>未定</td><td></td><td></td></tr>
</table>
"""

# ── 函館市民会館：pypdf が実際に返したテキスト（2026-08 大ホール より） ──
HAKODATE_TEXT = """大ホール
日 曜
日 催  物  開 始 終 了 入 場 料 チケット取扱・他詳細 主 催 者・問 合 せ
1 土 遺愛女子高等学校吹奏楽局
第36回定期演奏会 16:00 18:30 前売・当日
1,000円 ― 遺愛女子高等学校吹奏楽局
9 日
令和8年度市民舞台芸術奨励事業
北海道教育大学函館校吹奏楽団
創立50周年記念演奏会
14:00 16:00 前売・当日　1,000円
16 日 三浦一馬五重奏団（キンテート） 14:00 16:00 全席指定・税込
"""


def _run(name, fn):
    try:
        fn()
        print("✅", name)
        return 0
    except AssertionError as e:
        print("❌", name, e)
        return 1


def test_和歌山_日付と催物名と開演時刻が取れる():
    evs = wk._parse(WAKAYAMA_HTML, 2026, 8, TODAY)
    got = {(e.date.day, e.title, e.start_hour, e.start_minute) for e in evs}
    assert (4, "第2回日本和歌山国際音楽祭大祭", 9, 30) in got, got
    assert (29, "ゴスペラーズ坂ツアー2026", 17, 0) in got, got
    # 催物名が空の行は拾わない（空セルだけの日）
    assert not any(e.date.day == 1 for e in evs), got


def test_和歌山_2回公演は先頭の回を採る():
    evs = wk._parse(WAKAYAMA_HTML, 2026, 8, TODAY)
    e = next(e for e in evs if e.date.day == 9)
    assert (e.start_hour, e.start_minute) == (11, 30), (e.start_hour, e.start_minute)


def test_和歌山_時刻が未定なら時刻なしで残す():
    evs = wk._parse(WAKAYAMA_HTML, 2026, 8, TODAY)
    e = next(e for e in evs if e.date.day == 30)
    assert e.start_hour is None and e.start_minute is None
    assert e.title == "時刻未定の催し"


def test_和歌山_過去の日は落とす():
    evs = wk._parse(WAKAYAMA_HTML, 2026, 8, _dt.date(2026, 8, 20))
    assert {e.date.day for e in evs} == {29, 30}, {e.date.day for e in evs}


def test_函館_折り返した催物名を1件にまとめる():
    evs = hk._parse(HAKODATE_TEXT, 2026, 8, TODAY)
    by_day = {e.date.day: e for e in evs}
    assert by_day[1].title == "遺愛女子高等学校吹奏楽局 第36回定期演奏会", by_day[1].title
    assert (by_day[1].start_hour, by_day[1].start_minute) == (16, 0)
    # 3行に折り返した催物名
    assert by_day[9].title.startswith("令和8年度市民舞台芸術奨励事業"), by_day[9].title
    assert by_day[9].title.endswith("創立50周年記念演奏会"), by_day[9].title
    assert (by_day[9].start_hour, by_day[9].start_minute) == (14, 0)


def test_函館_見出し行を催物として拾わない():
    evs = hk._parse(HAKODATE_TEXT, 2026, 8, TODAY)
    titles = [e.title for e in evs]
    assert not any("催  物" in t or t.startswith("曜") for t in titles), titles
    assert len(evs) == 3, titles


if __name__ == "__main__":
    fails = 0
    for _name, _fn in sorted(globals().items()):
        if _name.startswith("test_") and callable(_fn):
            fails += _run(_name, _fn)
    sys.exit(1 if fails else 0)
