"""配信の見張り（feed_watch.py）：会場が黙って0件になったら気づき、前回の予定を引き継ぐ。
  python test_feed_watch.py   （pytest でも回る）
"""
import datetime as dt

from feed_watch import watch_and_carry

TODAY = dt.date(2026, 10, 16)
V = {"a": {"key": "a", "name": "A"}, "b": {"key": "b", "name": "B"}}


def _ev(k, d):
    return {"venueKey": k, "date": d, "title": f"{k}{d}", "genre": "concert",
            "startHour": 18, "startMinute": 0}


def _prev():
    return {"venues": [V["a"], V["b"]],
            "events": [_ev("a", "2026-10-20"), _ev("a", "2026-10-24"), _ev("a", "2026-10-25"),
                       _ev("a", "2026-10-01"), _ev("b", "2026-10-21")]}


def test_dropped_venue_is_carried_and_reported():
    feed = {"venues": [V["b"]], "events": [_ev("b", "2026-10-21")]}
    h = watch_and_carry(feed, _prev(), None, V, {"marine": {"ok": False, "error": "x"}}, TODAY)
    assert h["dropped"] == ["a"]
    assert h["carried"] == {"a": "2026-10-16"}
    # 過去の分（10/01）は引き継がない
    assert sorted(e["date"] for e in feed["events"] if e["venueKey"] == "a") == \
        ["2026-10-20", "2026-10-24", "2026-10-25"]
    assert any(v["key"] == "a" for v in feed["venues"])
    assert len(h["problems"]) == 2  # 取り込み口の失敗＋会場が消えた


def test_healthy_run_has_no_problems():
    feed = _prev()
    h = watch_and_carry(feed, _prev(), None, V, {"x": {"ok": True, "count": 5}}, TODAY)
    assert h["problems"] == [] and h["dropped"] == []


def test_small_venue_dropping_is_not_alarm():
    # 前回1件（b）だけの会場が0件になっても騒がない（終わっただけのことが多い）
    feed = {"venues": [V["a"]], "events": [e for e in _prev()["events"] if e["venueKey"] == "a"]}
    h = watch_and_carry(feed, _prev(), None, V, {}, TODAY)
    assert h["problems"] == []


def test_carry_stops_after_14_days():
    feed = {"venues": [V["b"]], "events": [_ev("b", "2026-10-21")]}
    prev_health = {"carried": {"a": "2026-10-01"}}
    h = watch_and_carry(feed, _prev(), prev_health, V, {}, TODAY)
    assert "a" not in h["carried"]
    assert not any(e["venueKey"] == "a" for e in feed["events"])
    assert "引き継ぎ14日を過ぎ" in h["problems"][0]


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"{len(tests)} 件すべて通過")
