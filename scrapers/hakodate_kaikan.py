"""函館市民会館（函館サーモン・まるなまホール）。

函館Ａ地区は会場が1つも無かった（2026-08-09 時点）。Jリーグ・Bリーグとも
函館に本拠地が無いため、ここが唯一の入口になる。

ページの作り（2026-08-09 実測）:
  https://www.zaidan-hakodate.com/kaikan/ に月次の催物案内PDFへのリンクがある。
  ファイル名は moyoosi{令和年2桁}{月2桁}01.pdf（例 moyoosi080801.pdf = 令和8年8月）。
  規則で決め打ちできるが、掲載が無い月は404になるのでHTMLからリンクを拾う。

  🔴 掲載は当月分のみ（前月25日ごろ更新）＝**先読みは約1か月しかない**。
     他の会場のように3〜4か月先までは出ない。それでも「今日・今週ここで催しがあるか」
     は分かるので入れている。

PDFの中身（pypdf の抽出テキスト）は
    1 土 遺愛女子高等学校吹奏楽局
    第36回定期演奏会 16:00 18:30 前売・当日
のように「日 曜」で始まり、催物名が複数行に折り返し、そのあとに開始・終了時刻が続く。
そこで「日 曜」で始まる行を1件の区切りとし、最初の HH:MM を開始時刻、
それより前の文字を催物名として取る。大ホール・小ホールは同じ建物なので1会場に束ねる。

※ 姫路のアクリエひめじは公式カレンダーが calendar.google.com にあり、
   そちらの robots.txt が全面 Disallow のため保留（社長判断待ち）。
"""
from __future__ import annotations

import datetime as _dt
import io
import re

import pypdf

from model import Event, guess_genre
from venues import HAKODATE_KAIKAN
from .base import http_get, soup_of

_INDEX = "https://www.zaidan-hakodate.com/kaikan/"
_PDF_RE = re.compile(r"moyoosi(\d{2})(\d{2})\d{2}\.pdf")
# 「1 土 …」「12 水 …」で1件が始まる
_ROW_RE = re.compile(r"^\s*(\d{1,2})\s+([日月火水木金土])\s*(.*)$")
_TIME_RE = re.compile(r"(\d{1,2}):(\d{2})")


def fetch() -> list[Event]:
    today = _dt.date.today()
    events: list[Event] = []
    seen: set[tuple] = set()
    for url, year, month in _pdf_links():
        try:
            resp = http_get(url, accept="application/pdf,*/*", timeout=60)
            reader = pypdf.PdfReader(io.BytesIO(resp.content))
            text = "\n".join((p.extract_text() or "") for p in reader.pages)
        except Exception:
            continue
        for ev in _parse(text, year, month, today):
            k = ev.dedup_key()
            if k in seen:
                continue
            seen.add(k)
            events.append(ev)
    return events


def _pdf_links() -> list[tuple[str, int, int]]:
    """一覧ページから催物案内PDFのURLと、その年月を拾う。"""
    try:
        doc = soup_of(http_get(_INDEX, accept="text/html,*/*").text)
    except Exception:
        return []
    out = []
    for a in doc.select("a[href]"):
        href = a.get("href") or ""
        m = _PDF_RE.search(href)
        if not m:
            continue
        url = href if href.startswith("http") else _INDEX + href.lstrip("./")
        url = url.replace("http://", "https://")
        reiwa, month = int(m.group(1)), int(m.group(2))
        if not 1 <= month <= 12:
            continue
        out.append((url, 2018 + reiwa, month))   # 令和1年=2019
    return list(dict.fromkeys(out))


def _parse(text: str, year: int, month: int, today: _dt.date) -> list[Event]:
    lines = [ln.rstrip() for ln in text.splitlines()]
    records: list[tuple[int, list[str]]] = []
    for ln in lines:
        m = _ROW_RE.match(ln)
        if m and 1 <= int(m.group(1)) <= 31:
            records.append((int(m.group(1)), [m.group(3)]))
        elif records:
            records[-1][1].append(ln)

    out: list[Event] = []
    for day, body in records:
        blob = " ".join(x for x in body if x).strip()
        tm = _TIME_RE.search(blob)
        title = (blob[: tm.start()] if tm else blob).strip()
        title = re.sub(r"\s+", " ", title).strip(" 　-―─")
        if len(title) < 3:
            continue                 # 見出し行・空セルの取りこぼしを捨てる
        try:
            date = _dt.date(year, month, day)
        except ValueError:
            continue
        if date < today:
            continue
        hh = mm = None
        if tm:
            h, mi = int(tm.group(1)), int(tm.group(2))
            if 0 <= h <= 23 and 0 <= mi <= 59:
                hh, mm = h, mi
        out.append(Event(
            venue=HAKODATE_KAIKAN, date=date, title=title[:80],
            genre=guess_genre(title), start_hour=hh, start_minute=mm,
        ))
    return out


if __name__ == "__main__":
    for e in fetch():
        print(e.date, e.start_hour, e.genre, e.title)
