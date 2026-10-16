#!/usr/bin/env python3
"""ドームの見張り役（カナリア）。公開中の配信を外から確かめる（2026-10-16 社長「ドームは命」）。

build.yml（1日3回）とは別に、3時間ごとに走る。見るのは「運転手の端末に届いている物」：
  ① 配信が古くなっていないか（12時間を超えたら、作り直しが止まっている）
  ② ドームのこれからの予定があるか・近い予定に開始時刻があるか（feed_watch と同じ判定）
1つでも引っかかれば exit 1 ＝ GitHub が持ち主へメールで知らせる（0円）。
"""
import datetime as dt
import json
import sys
import urllib.request

from feed_watch import LIVE_BASE, critical_problems

MAX_AGE_H = 12


def main() -> int:
    with urllib.request.urlopen(f"{LIVE_BASE}/events_jp.json", timeout=30) as r:  # noqa: S310
        feed = json.loads(r.read().decode("utf-8"))
    problems = []
    gen = dt.datetime.fromisoformat(feed["generatedAt"])
    age_h = (dt.datetime.now(dt.timezone.utc) - gen).total_seconds() / 3600
    if age_h > MAX_AGE_H:
        problems.append(f"配信が {age_h:.1f} 時間 作り直されていない（{MAX_AGE_H}時間を超えた）")
    jst_today = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=9)).date()
    problems += critical_problems(feed, jst_today)
    dome = [e for e in feed.get("events", []) if e.get("venueKey") == "paypay_dome"
            and e.get("date", "") >= jst_today.isoformat()]
    print(f"配信 {feed['generatedAt']}（{age_h:.1f}時間前）・ドームのこれからの予定 {len(dome)} 件")
    for e in dome[:3]:
        print(f"  {e['date']} {e.get('startHour')}:{e.get('startMinute')} {e.get('title')}")
    if problems:
        for p in problems:
            print(f"::error::{p}")
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
