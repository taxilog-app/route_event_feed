"""ホール系スクレイパーの解析部の回帰テスト（ネットに出ない）。

和歌山・函館・宮城・埼玉北部・小田原・山梨Bは「その営業圏で唯一の会場」なので、
解析が壊れるとその圏のイベントが丸ごと0件になる（＝運転手には「何も無い」に見える）。
サイトの作りが変わったときに気づけるよう、実物から取った見本で解析部だけを検査する。

実行:  python3 test_hall_scrapers.py
"""
import datetime as _dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scrapers import wakayama_kenmin as wk          # noqa: E402
from scrapers import hakodate_kaikan as hk          # noqa: E402
from scrapers import grande21 as g21                # noqa: E402
from scrapers import sakuramate as sm               # noqa: E402
from scrapers import odawara_hall as oh             # noqa: E402
from scrapers import kirara as kr                   # noqa: E402

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


# ══════════════════════════════════════════════════════════════════════════
# 本土なのに会場0だった4圏（2026-08-10 追加）
# ══════════════════════════════════════════════════════════════════════════

# ── グランディ・21：実物の「開催期間補足」4種（2026-08-10 実測） ──
# 🔴 一番の勘所＝「期間」だけを読むと公演の無い日まで出てしまう点。
def test_宮城_設営日を公演日として出さない():
    """期間 9/9〜9/12 のうち、実際の公演は 9/9・9/11・9/12（9/10 は設営日）。"""
    days = g21._resolve_days(
        "2026.09/09(水) ～ 2026.09/12(土)",
        "9/9（水）11（金）開場17：30 開演18：30 / 9/12（土）開場15：30 開演16：30",
        TODAY)
    assert [(d.day, h, m) for d, h, m in days] == [(9, 18, 30), (11, 18, 30), (12, 16, 30)], days


def test_宮城_区切りが中黒でも読める():
    days = g21._resolve_days("2026.09/05(土) ～ 2026.09/06(日)",
                             "9/5（土）開演17：00 ・ 9/6（日）開演16：00", TODAY)
    assert [(d.day, h, m) for d, h, m in days] == [(5, 17, 0), (6, 16, 0)], days


def test_宮城_2回公演は先頭の回を採る():
    days = g21._resolve_days("2026.08/29(土) ～ 2026.08/30(日)",
                             "8/29(土)開演17:00 / 8/30(日)開演①13：00　②17：30", TODAY)
    assert [(d.day, h, m) for d, h, m in days] == [(29, 17, 0), (30, 13, 0)], days


def test_宮城_開場の時刻を開演として拾わない():
    days = g21._resolve_days("2026.08/25(火) ～ 2026.08/26(水)",
                             "8/25（火）開場17：30 開演18：30 ・ 8/26（水）開場17：00 開演18：00",
                             TODAY)
    assert [(h, m) for _d, h, m in days] == [(18, 30), (18, 0)], days


def test_宮城_補足が読めなければ期間をそのまま使う():
    """保険の道。壊れても圏が0件にならないことを守る。"""
    days = g21._resolve_days("2026.09/05(土) ～ 2026.09/06(日)", "", TODAY)
    assert [(d.day, h, m) for d, h, m in days] == [(5, None, None), (6, None, None)], days


def test_宮城_期間の外の日付は捨てる():
    """補足に紛れた発売日などを公演日にしない。"""
    days = g21._resolve_days("2026.09/05(土) ～ 2026.09/06(日)",
                             "6/1（月）発売 ・ 9/5（土）開演17：00", TODAY)
    assert [(d.day, h, m) for d, h, m in days] == [(5, 17, 0)], days


# ── さくらめいと：実物の1件ぶん（2026-08-10 実測） ──
SAKURAMATE_HTML = """
<li class="events-archive__item"><div class="events-archive__item-body">
<ul class="events-category"><li><span class="post-category">さくらめいと</span></li>
<li><span class="post-category">主催</span></li></ul>
<p class="events-archive__item-title">劇団四季ミュージカル『コーラスライン』</p>
<dl><div><dt class="events-archive__item-list-title"></dt>
<dd class="events-archive__item-list-text">11月21日（土）開場13:15 開演14:00</dd></div>
<div><dt class="events-archive__item-list-title">【会場】</dt>
<dd class="events-archive__item-list-text">熊谷文化創造館さくらめいと「太陽のホール」</dd></div>
</dl></div></li>
<li class="events-archive__item"><div class="events-archive__item-body">
<ul class="events-category"><li><span class="post-category">あすねっと</span></li></ul>
<p class="events-archive__item-title">KidSwing レッツゴー・ジャズ・らんど♪</p>
<dl><div><dt class="events-archive__item-list-title"></dt>
<dd class="events-archive__item-list-text">12月19日（土）開場10:30 開演11:00</dd></div>
<div><dt class="events-archive__item-list-title">【会場】</dt>
<dd class="events-archive__item-list-text">大里生涯学習センターあすねっと</dd></div>
</dl></div></li>
"""


def test_埼玉北部_開演時刻と催物名が取れる():
    evs = sm._parse(SAKURAMATE_HTML, TODAY)
    assert len(evs) == 1, [e.title for e in evs]
    e = evs[0]
    assert e.title == "劇団四季ミュージカル『コーラスライン』"
    assert (e.date, e.start_hour, e.start_minute) == (_dt.date(2026, 11, 21), 14, 0)


def test_埼玉北部_座標の無い別の館は出さない():
    """あすねっと・ピピアは OSM に無い＝別の建物の座標で出すくらいなら出さない。"""
    evs = sm._parse(SAKURAMATE_HTML, TODAY)
    assert not any("あすねっと" in e.title or "KidSwing" in e.title for e in evs)


def test_埼玉北部_曜日で年を決める():
    """🔴 年が書いていないページ。曜日が合う年を選ぶ＝終わった公演を来年に生き返らせない。"""
    # 2026-12-27 は日曜／2027-12-27 は月曜。よって「12月27日(日)」は 2026 年。
    assert sm._date_of("12月27日(日)", TODAY) == _dt.date(2026, 12, 27)
    # 2026-02-14 は土曜／2027-02-14 は日曜。今日(8/1)より前の 2026 は落ち、2027 が残る。
    assert sm._date_of("2月14日（日）", TODAY) == _dt.date(2027, 2, 14)


def test_埼玉北部_どの年も曜日が合わなければ出さない():
    """読み違いを黙って通さない（間違った日に「イベントあり」と出さない）。

    12月27日は 2026=日曜 / 2027=月曜。水曜はどちらの年にも無いので捨てる。
    """
    assert sm._date_of("12月27日(水)", TODAY) is None
    # 対になる確認＝翌年側が合うならちゃんと拾う（捨てすぎていないこと）
    assert sm._date_of("12月27日(月)", TODAY) == _dt.date(2027, 12, 27)


# ── 小田原三の丸ホール：実物の1件ぶん（2026-08-10 実測） ──
ODAWARA_HTML = """
<ul class="extEventDetailListUL">
<li><div class="extEventDetailListInner">
<div class="bCatListLabel"><span class="bcatlabellist">大ホール</span></div>
<strong><a href="#">混声合唱団シグナス2026定期演奏会</a></strong>
<table><tr><th>日時</th><td>2026年8月2日（日）<br>14:00～16:00（13:30 開場）</td></tr>
<tr><th>会場</th><td>大ホール</td></tr></table>
</div></li>
<li><div class="extEventDetailListInner">
<div class="bCatListLabel"><span class="bcatlabellist">展示室</span></div>
<strong><a href="#">第22回 小田原書道連盟会員展</a></strong>
<table><tr><th>日時</th><td>2026年8月7日（金）～8月9日（日）<br>10:00～17:00</td></tr></table>
</div></li>
</ul>
"""


def test_小田原_開場でなく開演の時刻を採る():
    evs = oh._parse(ODAWARA_HTML, TODAY)
    e = next(e for e in evs if "シグナス" in e.title)
    assert (e.start_hour, e.start_minute) == (14, 0), (e.start_hour, e.start_minute)


def test_小田原_展示室は取らない():
    """数十人規模の展示で「イベントあり」を点けると、本当の公演の価値が薄まる。"""
    evs = oh._parse(ODAWARA_HTML, TODAY)
    assert not any("書道連盟" in e.title for e in evs), [e.title for e in evs]


def test_小田原_複数日の催しは日ごとに開く():
    html = ODAWARA_HTML.replace("展示室", "小ホール")
    evs = oh._parse(html, TODAY)
    days = sorted(e.date.day for e in evs if "書道連盟" in e.title)
    assert days == [7, 8, 9], days


# ── 山中湖きらら：実物の表（2026-08-10 実測） ──
KIRARA_HTML = """
<p>2026 年</p>
<table class="border"><tr><th>日程</th><th>イベント名</th><th>会場</th><th>イベント情報</th></tr>
<tr><td>8月</td></tr>
<tr><td>28日(金)～30日(日)</td><td>SWEET LOVE SHOWER 2026</td><td>全施設</td><td>公式サイト</td></tr>
<tr><td>10月</td></tr>
<tr><td>3日(土)</td><td>Mt.FUJIMAKI 2026</td><td>全施設</td><td>公式サイト</td></tr>
</table>
"""


def test_山梨B_月の区切り行を跨いで日付を組み立てる():
    evs = kr._parse(KIRARA_HTML, TODAY)
    got = sorted((e.date.isoformat(), e.title) for e in evs)
    assert ("2026-08-28", "SWEET LOVE SHOWER 2026") in got, got
    assert ("2026-08-30", "SWEET LOVE SHOWER 2026") in got, got
    assert ("2026-10-03", "Mt.FUJIMAKI 2026") in got, got


def test_山梨B_複数日フェスを日ごとに開く():
    evs = kr._parse(KIRARA_HTML, TODAY)
    days = sorted(e.date.day for e in evs if "SHOWER" in e.title)
    assert days == [28, 29, 30], days


def test_山梨B_見出し行を催物として拾わない():
    evs = kr._parse(KIRARA_HTML, TODAY)
    assert not any(e.title == "イベント名" for e in evs), [e.title for e in evs]


if __name__ == "__main__":
    fails = 0
    for _name, _fn in sorted(globals().items()):
        if _name.startswith("test_") and callable(_fn):
            fails += _run(_name, _fn)
    sys.exit(1 if fails else 0)
