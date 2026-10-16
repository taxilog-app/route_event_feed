"""配信の見張り（feed_watch.py）：会場が黙って0件になったら気づき、前回の予定を引き継ぐ。
  python test_feed_watch.py   （pytest でも回る）
"""
import datetime as dt

from feed_watch import apply_manual, critical_problems, watch_and_carry

TODAY = dt.date(2026, 10, 16)
V = {"a": {"key": "a", "name": "A"}, "b": {"key": "b", "name": "B"}}


def _probs(h):
    """ドームの見張り（最重要）を除いた問題。見本にドームを入れていないテスト用。"""
    return [p for p in h["problems"] if "最重要" not in p]


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
    assert len(_probs(h)) == 2  # 取り込み口の失敗＋会場が消えた


def test_healthy_run_has_no_problems():
    feed = _prev()
    h = watch_and_carry(feed, _prev(), None, V, {"x": {"ok": True, "count": 5}}, TODAY)
    assert _probs(h) == [] and h["dropped"] == []


def test_small_venue_dropping_is_not_alarm():
    # 前回1件（b）だけの会場が0件になっても騒がない（終わっただけのことが多い）
    feed = {"venues": [V["a"]], "events": [e for e in _prev()["events"] if e["venueKey"] == "a"]}
    h = watch_and_carry(feed, _prev(), None, V, {}, TODAY)
    assert _probs(h) == []


def test_carry_stops_after_14_days():
    feed = {"venues": [V["b"]], "events": [_ev("b", "2026-10-21")]}
    prev_health = {"carried": {"a": "2026-10-01"}}
    h = watch_and_carry(feed, _prev(), prev_health, V, {}, TODAY)
    assert "a" not in h["carried"]
    assert not any(e["venueKey"] == "a" for e in feed["events"])
    assert "引き継ぎ14日を過ぎ" in _probs(h)[0]


def test_known_failure_is_listed_but_not_alarm():
    feed = _prev()
    h = watch_and_carry(feed, _prev(), None, V,
                        {"fukuoka_budokan": {"ok": False, "error": "403"}}, TODAY)
    assert _probs(h) == []
    assert h["knownFailures"] and h["knownFailures"][0].startswith("fukuoka_budokan")


def _dome(d, h=18):
    return {"venueKey": "paypay_dome", "date": d, "title": f"催し{d}", "genre": "concert",
            "startHour": h, "startMinute": 0 if h is not None else None}


def test_dome_with_no_events_is_alarm():
    assert any("0件" in p for p in critical_problems({"events": []}, TODAY))


def test_dome_missing_start_time_soon_is_alarm_but_far_is_not():
    feed = {"events": [_dome("2026-10-24", None), _dome("2026-11-23", None), _dome("2026-10-25")]}
    probs = critical_problems(feed, TODAY)
    assert any("2026-10-24" in p and "開始時刻が無い" in p for p in probs)
    assert not any("2026-11-23" in p for p in probs)  # 14日より先はまだ鳴らさない


def test_healthy_dome_has_no_alarm():
    assert critical_problems({"events": [_dome("2026-10-20"), _dome("2026-11-01")]}, TODAY) == []


def test_manual_fills_missing_start_time_and_adds_missing_event():
    feed = {"venues": [], "events": [_dome("2026-10-24", None)]}
    applied = apply_manual(feed, [
        {"venueKey": "paypay_dome", "date": "2026-10-24", "startHour": 18, "startMinute": 30},
        {"venueKey": "paypay_dome", "date": "2026-10-30", "title": "追加の催し", "genre": "concert",
         "startHour": 17, "startMinute": 0},
        {"venueKey": "paypay_dome", "date": "2026-10-01", "startHour": 9, "startMinute": 0},  # 過ぎた日は使わない
    ], {"paypay_dome": {"key": "paypay_dome", "name": "ドーム"}}, TODAY)
    assert len(applied) == 2
    assert (feed["events"][0]["startHour"], feed["events"][0]["startMinute"]) == (18, 30)
    assert any(e["title"] == "追加の催し" for e in feed["events"])
    assert feed["venues"] and feed["venues"][0]["key"] == "paypay_dome"
    assert critical_problems(feed, TODAY) == []


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"{len(tests)} 件すべて通過")
