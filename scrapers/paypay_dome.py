"""みずほPayPayドーム福岡（イベントスケジュールのみ）。

コンサート/展示等のイベントは softbankhawks の event_schedule から取得する。
ホークス公式戦（野球）はかつてここで _parse_games が softbankhawks の
game/schedule から取得していたが、同ページの試合リンクが過去試合専用の
/gamelive/result/ 形式で未来の試合を一切含まず、シーズン進行に伴い全試合が
date<today で除外され0件化していた（＝ドームの野球が画面から消える事故）。
そのため野球は未来分も確実に取れる npb.jp（npb_baseball.py、ラベル
「みずほPayPay」）へ移管した。_parse_games と関連定数は回帰テスト
（test_paypay_dome.py）の参照用に残すが fetch では呼ばない。
"""
from __future__ import annotations

import datetime as _dt
import re

from model import Event, guess_genre, GENRE_SPORTS
from venues import PAYPAY_DOME
from .base import http_get, soup_of, extract_ordered_lines

# ── イベントスケジュール ──────────────────────────────────────────────────
_DATE_RE = re.compile(r"^(20\d{2})/(\d{1,2})/(\d{1,2})")
_KAIEN_RE = re.compile(r"開演\s*(\d{1,2}):(\d{2})")
# 開始時刻の書き方は催しごとにばらばら（2026-10-16 実物で確認）：
#   「開演 18:00」「18:30 開演」「イベント開始予定:15:00」「試合開始 14:00」
# どれも読む。「16:30 開場」「入場開始:13:00」は開始ではないので読まない。
_START_PATTERNS = (
    re.compile(r"(?:開演|開始予定|試合開始|(?<!場)開始)\s*[:：]?\s*(\d{1,2})[:：](\d{2})"),
    re.compile(r"(\d{1,2})[:：](\d{2})\s*(?:開演|(?<!場)開始)"),
)


def _start_time(line: str):
    """1行から開始時刻 (時, 分) を取り出す。開場・入場の時刻は取らない。"""
    # 「入場開始」「開場」だけの行は開始時刻ではない
    if re.search(r"開場|入場", line) and not re.search(r"開演|開始予定|試合開始|(?<!場)開始", line):
        return None
    for pat in _START_PATTERNS:
        m = pat.search(line)
        if m:
            hh, mm = int(m.group(1)), int(m.group(2))
            if 0 <= hh <= 23 and 0 <= mm <= 59:
                return hh, mm
    return None
_HEAD_RE = re.compile(r"^(イベント|コンサート|試合|公演|ライブ)$")
_TEL_RE = re.compile(r"TEL[:：]|問い合わせ|お問合せ")

# ── ホークス試合 ──────────────────────────────────────────────────────────
_HREF_RE = re.compile(r"/gamelive/result/(\d{4})(\d{2})(\d{2})\d{2}/?")
# ページ表記は「試合開始 18:00」（"試合開始" が時刻の前）。
_GAME_TIME_RE = re.compile(r"試合開始\s*(\d{1,2}):(\d{2})")
_LOGO_ID_RE = re.compile(r"logo_(\d+)_")
_HAWKS_TEAM_ID = "2005001"
_TEAM_ID_TO_NAME = {
    "2005001": "ホークス",
    # パ・リーグ
    "2005002": "バファローズ",
    "2005003": "イーグルス",
    "2008001": "ライオンズ",
    "1992001": "マリーンズ",
    "2004001": "ファイターズ",
    # セ・リーグ（交流戦の対戦相手）
    "1954001": "ドラゴンズ",
    "2012001": "ベイスターズ",
    "1961001": "タイガース",
    "2006001": "スワローズ",
}


def fetch() -> list[Event]:
    out: list[Event] = []
    year = _dt.date.today().year
    try:
        resp = http_get(
            f"https://www.softbankhawks.co.jp/stadium/event_schedule/{year}/",
            accept="text/html,*/*")
        out.extend(_parse_events(resp.text))
    except Exception:
        pass
    # 注: ホークス公式戦（野球）は npb_baseball.py（npb.jp）へ移管済み。
    # softbankhawks の game/schedule は過去試合専用リンクで未来を取れないため
    # ここでは呼ばない（モジュール冒頭の docstring 参照）。
    return out


def _parse_events(html: str) -> list[Event]:
    doc = soup_of(html)
    lines = extract_ordered_lines(doc.body)
    events: list[Event] = []
    today = _dt.date.today()
    cur_date = None
    cur_title = None
    cur_hh = cur_mm = None

    def flush():
        nonlocal cur_title, cur_hh, cur_mm
        if cur_date and cur_title and cur_date >= today:
            events.append(Event(
                venue=PAYPAY_DOME, date=cur_date, title=cur_title,
                genre=guess_genre(cur_title, is_dome=True),
                start_hour=cur_hh, start_minute=cur_mm,
            ))
        cur_title = None
        cur_hh = cur_mm = None

    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        dm = _DATE_RE.match(line)
        if dm:
            flush()
            try:
                cur_date = _dt.date(int(dm.group(1)), int(dm.group(2)), int(dm.group(3)))
            except ValueError:
                cur_date = None
            continue
        if cur_date is None:
            continue
        st = _start_time(line)
        if st:
            if cur_hh is None:  # 2回公演は先頭の回を採る
                cur_hh, cur_mm = st
            continue
        if len(line) <= 6 and _HEAD_RE.match(line):
            continue
        if _TEL_RE.search(line):
            continue
        if cur_title is None:
            cur_title = line
    flush()
    return events


def _parse_games(html: str) -> list[Event]:
    doc = soup_of(html)
    events: list[Event] = []
    today = _dt.date.today()
    seen = set()
    for a in doc.select("a"):
        href = a.get("href", "")
        m = _HREF_RE.search(href)
        if not m:
            continue
        try:
            date = _dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            continue
        if date < today:
            continue
        # 親方向に c-calendar-list-day を探す
        p = a.parent
        day_card = None
        for _ in range(10):
            if p is None:
                break
            cls = " ".join(p.get("class", [])) if hasattr(p, "get") else ""
            if "c-calendar-list-day" in cls:
                day_card = p
                break
            p = p.parent
        if day_card is None:
            continue
        text = day_card.get_text()
        if "PayPay" not in text:
            continue
        key = date.isoformat()
        if key in seen:
            continue
        seen.add(key)
        hh = mm = None
        tm = _GAME_TIME_RE.search(text)
        if tm:
            hh, mm = int(tm.group(1)), int(tm.group(2))
        opponent = "対戦相手"
        for img in day_card.select(".c-calendar-list-game-vs-teams-team img"):
            src = img.get("data-src") or img.get("src") or ""
            lm = _LOGO_ID_RE.search(src)
            if not lm:
                continue
            tid = lm.group(1)
            if tid == _HAWKS_TEAM_ID:
                continue
            opponent = _TEAM_ID_TO_NAME.get(tid, "対戦相手")
            break
        events.append(Event(
            venue=PAYPAY_DOME, date=date, title=f"ホークス vs {opponent}",
            genre=GENRE_SPORTS, start_hour=hh, start_minute=mm,
        ))
    return events
