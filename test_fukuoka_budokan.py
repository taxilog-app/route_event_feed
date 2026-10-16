"""福岡武道館（暦のJSON）の読み取り。
  python test_fukuoka_budokan.py   （pytest でも回る）
"""
import datetime as dt
import json
import sys
import types

try:
    from scrapers import fukuoka_budokan as b
except ImportError:  # 手元で全部の部品が入っていない時は、この口だけ読む
    pkg = types.ModuleType("scrapers")
    pkg.__path__ = ["scrapers"]
    sys.modules["scrapers"] = pkg
    import importlib
    b = importlib.import_module("scrapers.fukuoka_budokan")

TODAY = dt.date(2026, 10, 16)
BODY = json.dumps([
    {"title": "九州八段審議　柔道", "allDay": False,
     "start": "2026-10-17T09:00:00", "end": "2026-10-17T17:00:00"},
    {"title": "休館日", "allDay": True, "start": "2026-10-20T00:00:00", "end": "2026-10-21T00:00:00"},
    {"title": "KING OF STRIKERS", "allDay": True,
     "start": "2026-10-18T00:00:00", "end": "2026-10-20T00:00:00"},
], ensure_ascii=False)


def test_closed_day_is_not_an_event():
    got = b._parse(BODY, TODAY)
    assert all("休館" not in e.title for e in got), [e.title for e in got]


def test_timed_and_all_day_events():
    got = b._parse(BODY, TODAY)
    assert (got[0].date, got[0].start_hour, got[0].start_minute) == (dt.date(2026, 10, 17), 9, 0)
    # 終日は end が排他的＝18日・19日の2日
    assert [e.date for e in got if e.title == "KING OF STRIKERS"] == \
        [dt.date(2026, 10, 18), dt.date(2026, 10, 19)]


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"{len(tests)} 件すべて通過")
