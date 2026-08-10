"""会場別スクレイパー。各モジュールは fetch() -> list[Event] を公開する。"""
from . import (
    marine_messe,
    f_sunpalace,
    paypay_dome,
    hakataza,
    fukuoka_civic_hall,
    momochi,
    fukuoka_budokan,
    tokyo_dome,
    saitama_super_arena,
    yokohama_arena,
    k_arena,
    kyocera_dome,
    nagoya_dome,
    ig_arena,
    ariake_arena,
    nissan_stadium,
    ajinomoto_stadium,
    belluna_dome,
    tokyo_intl_forum,
    osaka_jo_hall,
    festival_hall,
    pia_arena_mm,
    npb_baseball,
    jleague,   # J1/J2/J3統一（旧 avispa/cerezo を統合）
    bleague,           # B1/B2/B3統一（京都市域・福井・三重・福岡県B地区ほかの要）
    wakayama_kenmin,   # 和歌山地区の唯一の入口
    hakodate_kaikan,   # 函館Ａ地区の唯一の入口（PDF・先読み1か月）
    # ── 本土なのに会場0だった営業圏の唯一の入口（2026-08-10）──
    grande21,          # 宮城地区（仙台市の外＝利府町）
    sakuramate,        # 埼玉県北部地区（熊谷市）
    odawara_hall,      # 小田原地区
    kirara,            # 山梨県B地区（屋外の大型フェス）
)

# build.py はこのリストを順に実行する。失敗しても他に影響しないよう個別try。
ALL_SCRAPERS = [
    marine_messe,
    f_sunpalace,
    paypay_dome,
    hakataza,
    fukuoka_civic_hall,
    momochi,
    fukuoka_budokan,
    tokyo_dome,
    saitama_super_arena,
    yokohama_arena,
    k_arena,
    kyocera_dome,
    nagoya_dome,
    ig_arena,
    ariake_arena,
    nissan_stadium,
    ajinomoto_stadium,
    belluna_dome,
    tokyo_intl_forum,
    osaka_jo_hall,
    festival_hall,
    pia_arena_mm,
    npb_baseball,
    jleague,
    bleague,
    wakayama_kenmin,
    hakodate_kaikan,
    grande21,
    sakuramate,
    odawara_hall,
    kirara,
]
