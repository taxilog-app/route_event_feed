"""日本シリーズのページの読み取り検査（2026-10-28：第3戦がドームの配信から漏れた件の再発防止）。

公式ページの写し（test_npb_nippons_fixture.html・2026-10-28 取得）で、
これから行う PayPayドームの2試合が取れることを確かめる。落ちたら配信しない。
"""
import datetime as dt

from scrapers.npb_baseball import _parse_nippon_series

html = open("test_npb_nippons_fixture.html", encoding="utf-8").read()

# 10/27 の時点：第3戦（試合後＝球場名なし→結果リンクから本拠地）も今日なので残る
evs = _parse_nippon_series(html, 2026, dt.date(2026, 10, 27))
dome = [e for e in evs if e.venue.key == "paypay_dome"]
got = {(e.date.isoformat(), e.title, e.start_hour) for e in dome}
assert ("2026-10-27", "日本シリーズ 第3戦 ソフトバンク vs DeNA", None) in got, got
assert ("2026-10-28", "日本シリーズ 第4戦 ソフトバンク vs DeNA", 18) in got, got
assert ("2026-10-29", "日本シリーズ 第5戦 ソフトバンク vs DeNA", 18) in got, got
# 横浜開催（第6・7戦）は横浜スタジアムに入る
yk = [e for e in evs if e.venue.key == "yokohama_stadium"]
assert any(e.date == dt.date(2026, 10, 31) and e.start_hour == 18 and e.start_minute == 30 for e in yk), yk
# 過ぎた日は出さない
evs2 = _parse_nippon_series(html, 2026, dt.date(2026, 10, 28))
assert all(e.date >= dt.date(2026, 10, 28) for e in evs2)
print("ok: 日本シリーズ", len(evs), "試合")
