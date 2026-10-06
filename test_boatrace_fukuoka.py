"""ボートレース福岡：月間スケジュールの読み取り（2026-10-06 の実物を切り出した表で検査）。"""
import datetime as dt
import os

from scrapers import boatrace_fukuoka as b

HERE = os.path.dirname(os.path.abspath(__file__))


def _parse():
    with open(os.path.join(HERE, "test_boatrace_fukuoka_fixture.html"), encoding="utf-8") as f:
        return b.parse_monthly(f.read(), dt.date(2026, 10, 1))


def test_dates_come_from_column_position_not_link():
    d = _parse()
    # 開催中のセルのリンクは hd=20261006（今日）だが、開催は 10/1〜10/6
    assert d[dt.date(2026, 10, 1)] == "マンスリーＢＯＡＴＲＡＣＥ杯"
    assert d[dt.date(2026, 10, 6)] == "マンスリーＢＯＡＴＲＡＣＥ杯"
    assert dt.date(2026, 10, 7) not in d


def test_three_october_meets():
    d = _parse()
    oct_days = sorted(x for x in d if x.month == 10)
    assert len(oct_days) == 18
    assert d[dt.date(2026, 10, 10)] == "日本トーター杯"
    assert d[dt.date(2026, 10, 28)].startswith("ボートレース福岡天神")


def test_month_rolls_over():
    d = _parse()
    assert dt.date(2026, 9, 27) in d      # 見出しは前月27日から始まる
    assert dt.date(2026, 11, 4) in d      # 翌月4日まで


if __name__ == "__main__":
    test_dates_come_from_column_position_not_link()
    test_three_october_meets()
    test_month_rolls_over()
    print("ok")
