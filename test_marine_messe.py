"""マリンメッセ（4会場まとめて取る口）の日程の読み取り。

2026-10-16：1件だけ年付きの「2028.1.29(土)17:00～」を「28月1日」と読んで例外になり、
4会場（A館・B館・国際会議場・国際センター）が丸ごと0件で配信されていた。その再発防止。
CI（.github/workflows/build.yml）で配信の前に回す。落ちたら配信しない。
  python test_marine_messe.py   （pytest でも回る）
"""
import datetime as dt
import sys
import types

try:
    from scrapers import marine_messe as m
except ImportError:  # 手元で全部の部品が入っていない時は、この口だけ読む
    pkg = types.ModuleType("scrapers")
    pkg.__path__ = ["scrapers"]
    sys.modules["scrapers"] = pkg
    import importlib
    m = importlib.import_module("scrapers.marine_messe")

TODAY = dt.date(2026, 10, 16)


def test_year_prefixed_dates():
    got = m._expand_schedule("2028.1.29(土)17:00～<br>2028.1.30(日)17:00～", TODAY)
    assert got == [(dt.date(2028, 1, 29), 17, 0), (dt.date(2028, 1, 30), 17, 0)], got


def test_plain_single_date():
    assert m._expand_schedule("10.24(土)18:00～", TODAY) == [(dt.date(2026, 10, 24), 18, 0)]


def test_plain_range_with_time_on_next_line():
    got = m._expand_schedule("11.20(水)～11.22(金)<br>10:00～17:00", TODAY)
    assert [d for d, _, _ in got] == [dt.date(2026, 11, d) for d in (20, 21, 22)]
    assert all((h, mm) == (10, 0) for _, h, mm in got)


def test_year_prefixed_range():
    got = m._expand_schedule("2027.1.5(火)～2027.1.6(水)", TODAY)
    assert [d for d, _, _ in got] == [dt.date(2027, 1, 5), dt.date(2027, 1, 6)], got


def _rec(title, date_string, venue_id="rhPkRp7kYFiu7CuFjFaW"):
    return {"document": {"fields": {"default": {"mapValue": {"fields": {
        "title": {"stringValue": title},
        "RIeOyB9L": {"stringValue": date_string},
        "zu0OnEpi": {"document": {"name": venue_id}},
    }}}}}}


def test_one_unreadable_record_does_not_drop_the_rest():
    # 読めない日付（13月）が混ざっても、他の公演は残る
    recs = [_rec("壊れた日程", "2099.13.40(土)"), _rec("ふつうの公演", "2099.1.5(月)18:00～")]
    got = m._parse_records(recs)
    assert [e.title for e in got] == ["ふつうの公演"], got


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"{len(tests)} 件すべて通過")
