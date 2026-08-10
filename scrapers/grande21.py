"""グランディ・21（宮城県総合運動公園／セキスイハイムスーパーアリーナ）。

宮城地区＝「仙台地区を除く宮城県の全域」。仙台市内の会場（楽天モバイルパーク・
ユアテックスタジアム）はどれも仙台地区なので、宮城地区にはこれまで会場が1つも
無かった（2026-08-10 時点）。利府町のこのアリーナがその入口になる。

ページの作り（2026-08-10 実測）:
  一覧 https://www.mspf.jp/grande21/index.php?action=event_show_list
    - table.tbl-event-index / 1行 = イベント名・カテゴリ・内容・開催期間
    - イベント名のリンクが詳細ページ（event_id）
  詳細 index.php?action=event_show_detail&event_id=NNNN
    - 「開催期間」    2026.09/09(水) ～ 2026.09/12(土)
    - 「開催期間補足」9/9（水）11（金）開場17：30 開演18：30 / 9/12（土）開場15：30 開演16：30

🔴 **開催期間だけを読むと嘘になる。** 上の桑田佳祐の例では期間が4日ぶんあるが、
   実際に公演があるのは 9/9・9/11・9/12 の3日で 9/10 は無い（設営日）。
   無い日に「イベントあり」と出すと、運転手を客のいない場所へ向かわせてしまう。
   そこで詳細ページの「開催期間補足」を読んで公演日を1日ずつ取り出す。
   補足が読めなかったときだけ、期間をそのまま日ごとに展開する（安全側の保険）。

補足の書き方は揺れる（実測8件すべての形）:
   9/5（土）開演17：00 ・ 9/6（日）開演16：00      … 区切りが「・」
   8/29(土)開演17:00 / 8/30(日)開演①13：00 ②17：30  … 半角括弧・半角コロン・2回公演
   9/9（水）11（金）開場17：30 開演18：30            … 月を省いた日が続く／1つの時刻を共有
2回公演（①②）は最初の時刻を採る（他のホール系スクレイパーと揃える）。

🔴 文字コードの罠（2026-08-10 実測）:
   サイトは「charset=EUC-JP」と名乗るが、丸数字①②は素のEUC-JPに無い文字（NEC特殊文字）。
   requests の推定に任せると①②だけ壊れ、「開演①13:00」が読めず時刻が丸ごと落ちる。
   euc_jis_2004 で復号すると通る。和歌山（cp932）と同じ型の罠。
"""
from __future__ import annotations

import datetime as _dt
import re

import requests

from model import Event, guess_genre
from venues import SEKISUI_HEIM_SUPER_ARENA
from .base import UA, flatten_ws, soup_of

_BASE = "https://www.mspf.jp/grande21/"
_LIST_URL = _BASE + "index.php?action=event_show_list"
_DETAIL_URL = _BASE + "index.php?action=event_show_detail&event_id={id}&target="

# 「2026.09/09(水)」
_PERIOD_RE = re.compile(r"(\d{4})\.(\d{1,2})/(\d{1,2})")
# 「9/9(水)」「11(金)」＝月は省略されることがある
_DAY_RE = re.compile(r"(?:(\d{1,2})/)?(\d{1,2})\s*[（(]\s*[月火水木金土日]\s*[）)]")
# 「開演18:30」。①②が挟まることがある。開場は取らない
_KAIEN_RE = re.compile(r"開演\s*[①-⑨]?\s*(\d{1,2}):(\d{2})")
_TOKEN_RE = re.compile(f"({_DAY_RE.pattern})|({_KAIEN_RE.pattern})")

_MAX_EVENTS = 40          # 一覧が壊れて全ページを踏みに行くのを防ぐ
_MAX_SPAN_DAYS = 14       # これより長い「期間」は興行でなく展示・工事とみなし開始日だけ


def _get(url: str) -> str:
    """🔴 euc_jis_2004 で読む。EUC-JPと名乗るが丸数字①②が入るため（上の注記）。"""
    resp = requests.get(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"},
                        timeout=20)
    resp.raise_for_status()
    return resp.content.decode("euc_jis_2004", errors="replace")


def fetch() -> list[Event]:
    today = _dt.date.today()
    html = _get(_LIST_URL)
    out: list[Event] = []
    seen: set[tuple] = set()
    for title, category, event_id, period in _parse_list(html):
        detail = ""
        if event_id:
            try:
                detail = _get(_DETAIL_URL.format(id=event_id))
            except Exception:
                detail = ""
        for date, hh, mm in _resolve_days(period, _extract_supplement(detail), today):
            if date < today:
                continue
            ev = Event(
                venue=SEKISUI_HEIM_SUPER_ARENA, date=date,
                title=title,
                genre=guess_genre(f"{title} {category}", is_dome=True),
                start_hour=hh, start_minute=mm,
            )
            k = ev.dedup_key()
            if k in seen:
                continue
            seen.add(k)
            out.append(ev)
    return out


def _parse_list(html: str) -> list[tuple[str, str, str, str]]:
    """一覧から (イベント名, カテゴリ, event_id, 開催期間) を取り出す。"""
    doc = soup_of(html)
    rows: list[tuple[str, str, str, str]] = []
    table = doc.select_one("table.tbl-event-index") or doc.find("table")
    if table is None:
        return rows
    for tr in table.find_all("tr"):
        cells = tr.find_all("td")
        if len(cells) < 4:
            continue                      # 見出し行（th）はここで落ちる
        title = flatten_ws(cells[0].get_text(" "))
        category = flatten_ws(cells[1].get_text(" "))
        period = flatten_ws(cells[3].get_text(" "))
        if not title or not _PERIOD_RE.search(period):
            continue
        a = cells[0].find("a", href=True)
        m = re.search(r"event_id=(\d+)", a["href"]) if a else None
        rows.append((title, category, m.group(1) if m else "", period))
        if len(rows) >= _MAX_EVENTS:
            break
    return rows


def _extract_supplement(html: str) -> str:
    """詳細ページから「開催期間補足」の中身だけを取り出す。"""
    if not html:
        return ""
    text = flatten_ws(soup_of(html).get_text(" "))
    m = re.search(r"開催期間補足\s*(.*?)\s*開催場所", text)
    return m.group(1) if m else ""


def _resolve_days(period: str, supplement: str,
                  today: _dt.date) -> list[tuple[_dt.date, int | None, int | None]]:
    """公演日と開演時刻を決める。補足が読めればそちら、駄目なら期間を展開。"""
    span = _period_range(period)
    if not span:
        return []
    start, end = span
    days = _parse_supplement(supplement, start, end) if supplement else []
    if days:
        return days
    # 保険＝期間をそのまま日ごとに展開（時刻は不明＝アプリのジャンル別既定時刻に任せる）
    if (end - start).days > _MAX_SPAN_DAYS:
        end = start
    out = []
    d = start
    while d <= end:
        out.append((d, None, None))
        d += _dt.timedelta(days=1)
    return out


def _period_range(period: str) -> tuple[_dt.date, _dt.date] | None:
    found = _PERIOD_RE.findall(period)
    if not found:
        return None
    def to_date(t):
        return _dt.date(int(t[0]), int(t[1]), int(t[2]))
    start = to_date(found[0])
    end = to_date(found[-1]) if len(found) > 1 else start
    if end < start:
        end = start
    return start, end


def _parse_supplement(text: str, start: _dt.date,
                      end: _dt.date) -> list[tuple[_dt.date, int | None, int | None]]:
    """補足の文を頭から舐めて、日付と開演時刻を並び順どおりに結びつける。

    日付が続いたあとに1つ時刻が来たら、溜まっている日付ぜんぶにその時刻を配る
    （「9/9（水）11（金）… 開演18：30」＝2日とも18:30）。
    """
    text = text.replace("：", ":").replace("　", " ")
    pending: list[_dt.date] = []
    month = start.month
    out: list[tuple[_dt.date, int | None, int | None]] = []
    for m in _TOKEN_RE.finditer(text):
        day_m = _DAY_RE.fullmatch(m.group(1)) if m.group(1) else None
        if day_m:
            if day_m.group(1):
                month = int(day_m.group(1))
            date = _to_date(month, int(day_m.group(2)), start, end)
            if date is not None:
                pending.append(date)
            continue
        kaien_m = _KAIEN_RE.fullmatch(m.group(4)) if m.group(4) else None
        if kaien_m and pending:
            hh, mm = int(kaien_m.group(1)), int(kaien_m.group(2))
            if 0 <= hh <= 23 and 0 <= mm <= 59:
                out.extend((d, hh, mm) for d in pending)
            else:
                out.extend((d, None, None) for d in pending)
            pending = []
    out.extend((d, None, None) for d in pending)   # 時刻が付かなかった日
    return out


def _to_date(month: int, day: int, start: _dt.date, end: _dt.date) -> _dt.date | None:
    """月日に年を当てる。年をまたぐ期間（12月→1月）でも正しく収まる方を選ぶ。

    🔴 期間の外に落ちるものは捨てる＝補足に紛れ込んだ関係ない日付（発売日など）を
       公演日として出さないため。
    """
    for year in {start.year, end.year}:
        try:
            cand = _dt.date(year, month, day)
        except ValueError:
            continue
        if start <= cand <= end:
            return cand
    return None
