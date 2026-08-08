"""営業圏キーの回帰テスト。build.py を回さずに検査部だけ確かめる。

2026-08-09 の失敗（areaKey を出力に足したが validate_schema の
「項目が完全一致か」の定義を直し忘れ、配信が丸ごと止まった）の再発防止。
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build  # noqa: E402
from venue_areas import VENUE_AREAS  # noqa: E402
from venues import ALL_VENUES  # noqa: E402


def _sample_feed():
    """出力と同じ形の小さなフィードを組む（ネットに出ない）。"""
    vs = [v.to_json() for v in ALL_VENUES[:3]]
    return {
        "schemaVersion": 1,
        "generatedAt": "2026-08-09T00:00:00+00:00",
        "venues": vs,
        "events": [{"venueKey": vs[0]["key"], "date": "2026-08-09",
                    "title": "テスト", "genre": "other",
                    "startHour": 10, "startMinute": 0}],
    }


def test_全会場に営業圏キーの割り当てがある():
    missing = [v.key for v in ALL_VENUES if v.key not in VENUE_AREAS]
    assert not missing, f"venue_areas.py に行が無い会場: {missing}"


def test_営業圏キーは83地区の名簿の中にある():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "area_keys.json")
    with open(path, encoding="utf-8") as f:
        allowed = {a["key"] for a in json.load(f)["areas"]}
    bad = {k: a for k, a in VENUE_AREAS.items() if a not in allowed}
    assert not bad, f"名簿に無い営業圏キー: {bad}"


def test_営業圏キーを付けた後も形の検査を通る():
    """🔴 これが 2026-08-09 に落ちた検査。出力へ項目を足したら
    _required_venue_keys() も直す必要がある、を固定する。"""
    feed = _sample_feed()
    assert not build.apply_area_keys(feed)
    assert all("areaKey" in v for v in feed["venues"]), "areaKey が付いていない"
    assert not build.validate_schema(feed), "形の検査で弾かれた"


def test_割り当てを壊すとビルドが止まる():
    feed = _sample_feed()
    orig = dict(build.VENUE_AREAS)
    try:
        build.VENUE_AREAS = {**orig, feed["venues"][0]["key"]: "not_exist"}
        assert build.apply_area_keys(feed), "存在しないキーが素通りした"
    finally:
        build.VENUE_AREAS = orig


if __name__ == "__main__":
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"✅ {name}")
            except AssertionError as e:
                fails += 1
                print(f"❌ {name}: {e}")
    print("\n全部通りました" if not fails else f"\n{fails}件 失敗")
    sys.exit(1 if fails else 0)
