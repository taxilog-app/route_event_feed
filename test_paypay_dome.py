"""PayPayドーム（ホークス戦）スクレイパーの回帰テスト。

2026-06-12 の事故の再発防止:
  ① ホークス公式の試合カードは「試合開始 18:00」（"試合開始" が時刻の前）表記
     だが、正規表現が逆順 "(HH):(MM)試合開始" を期待していたため全試合で
     開始時刻が None になり、アプリ側デフォルト時刻で誤表示していた。
  ② 交流戦のセ・リーグ対戦相手IDが未登録で「対戦相手」と表示されていた。

ネットワーク非依存（実HTML断片に対する純パーステスト）。CIで build 前に実行する。
失敗時は exit(1)。
"""
from __future__ import annotations

import sys

try:
    from scrapers.paypay_dome import _GAME_TIME_RE, _TEAM_ID_TO_NAME, _LOGO_ID_RE, _start_time, _parse_events
except ImportError:  # 手元で全部の部品が入っていない時は、この口だけ読む
    import importlib
    import types
    _pkg = types.ModuleType("scrapers")
    _pkg.__path__ = ["scrapers"]
    sys.modules["scrapers"] = _pkg
    _m = importlib.import_module("scrapers.paypay_dome")
    _GAME_TIME_RE, _TEAM_ID_TO_NAME, _LOGO_ID_RE = _m._GAME_TIME_RE, _m._TEAM_ID_TO_NAME, _m._LOGO_ID_RE
    _start_time, _parse_events = _m._start_time, _m._parse_events

# ホークス公式 game/schedule の試合カード get_text() の実サンプル（2026-06）。
_CARD_DAY_GAME = " 試合開始 14:00 みずほPayPay 勝敗(分) 先発 本塁打 チケット購入 "
_CARD_NIGHT_GAME = " 試合開始 18:00 みずほPayPay 勝敗(分) 0-0 先発 前田純 本塁打 "


def _check(name: str, cond: bool) -> bool:
    print(("[ok] " if cond else "[NG] ") + name)
    return cond


def main() -> int:
    ok = True

    # ① 開始時刻が「試合開始 HH:MM」順で抽出できる（逆順regexだと None になる）
    m = _GAME_TIME_RE.search(_CARD_DAY_GAME)
    ok &= _check("デーゲーム 14:00 を抽出",
                 bool(m) and (int(m.group(1)), int(m.group(2))) == (14, 0))
    m = _GAME_TIME_RE.search(_CARD_NIGHT_GAME)
    ok &= _check("ナイター 18:00 を抽出",
                 bool(m) and (int(m.group(1)), int(m.group(2))) == (18, 0))

    # ② 交流戦のセ・リーグ6球団＋パ・リーグ5球団が対戦相手として解決できる
    pacific = {"2005002", "2005003", "2008001", "1992001", "2004001"}
    central = {"1954001", "2012001", "1961001", "2006001"}  # 中日/DeNA/阪神/ヤクルト
    for tid in pacific | central:
        ok &= _check(f"対戦相手ID {tid} が登録済み", tid in _TEAM_ID_TO_NAME)

    # ③ ロゴURLから球団IDを取り出せる（opponent抽出の前提）
    lm = _LOGO_ID_RE.search("/media/sites/7/common/teamlogo/2026/logo_2006001_s.png")
    ok &= _check("ロゴURLからID抽出", bool(lm) and lm.group(1) == "2006001")

    # ④ イベント予定の開始時刻（2026-10-16：書き方がばらばらで、コンサートの開始時刻が
    #    抜け、ドームの規制の知らせが出なくなるところだった）
    for line, want in [("開演 18:00", (18, 0)), ("18:30 開演", (18, 30)),
                       ("イベント開始予定:15:00", (15, 0)), ("試合開始 14:00", (14, 0)),
                       ("16:30 開場", None), ("入場開始:13:00", None), ("開場 16:00", None),
                       ("開演時間", None), ("TEL：092-712-4221", None)]:
        ok &= _check(f"開始時刻 {line!r} → {want}", _start_time(line) == want)

    # ドーム公式 stadium/event_schedule の実物の形（2026-10-16 取得・年だけ2099に変更）
    html = """<html><body><dl class="temp_calendarList">
<dt>2099/10/24（<span class="cmn_tBlue">土</span>）</dt><dd><table>
<tr><th>イベント</th><td><a href="#"><span>Stray Kids World Tour &#0060;RUN IT JAPAN&#0062;</span></a></td></tr>
<tr><th>開演時間</th><td>16:30 開場<br>18:30 開演</td></tr>
<tr><th>お問い合わせ</th><td>BEA<br>TEL：092-712-4221<br>（月～金 12:00～16:00）</td></tr>
</table></dd>
<dt>2099/11/07（<span class="cmn_tBlue">土</span>）</dt><dd><table>
<tr><th>イベント</th><td><span>MLBx: Fukuoka</span></td></tr>
<tr><th>開演時間</th><td>入場開始:13:00<br>イベント開始予定:15:00</td></tr>
</table></dd></dl></body></html>"""
    got = [(str(e.date), e.title, e.start_hour, e.start_minute) for e in _parse_events(html)]
    ok &= _check(f"実物の形の予定表から開始時刻を取る {got}",
                 got == [("2099-10-24", "Stray Kids World Tour <RUN IT JAPAN>", 18, 30),
                         ("2099-11-07", "MLBx: Fukuoka", 15, 0)])

    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
