"""会場 → 営業圏キーの割り当て表。

営業圏キーは area_keys.json（83地区の正式名簿）の中から選ぶ。
build.py が出力時に各会場へ areaKey として付け、アプリはこれと
「選択中の営業圏（料金プリセット）」を突き合わせて絞り込む。

🔴 会場を venues.py に足したら、必ずここにも1行足すこと。
   忘れると build.py が止まる（黙って全国表示になる事故を防ぐため）。

⚠️ 「県名」ではなく「営業圏」で選ぶこと。同じ県でも交通圏が違えば別
   （例: ミクニワールドスタジアムは福岡県だが北九州市域＝ fukuoka ではない）。
   境界データがある53地区は tools の点検（境界の形に会場座標が入るか）で
   検証済み（2026-08-09）。形が無い地区は市区町村の所属で判断した。
"""

VENUE_AREAS = {
    # ── 福岡交通圏（福岡市・春日・大野城ほか） ──
    "marine_messe_a": "fukuoka",
    "marine_messe_b": "fukuoka",
    "fukuoka_congress": "fukuoka",
    "fukuoka_kokusai_center": "fukuoka",
    "fukuoka_sunpalace": "fukuoka",
    "paypay_dome": "fukuoka",
    "best_denki_stadium": "fukuoka",     # 博多区東平尾公園
    "hakataza": "fukuoka",
    "fukuoka_civic_hall": "fukuoka",
    "momochi_bunka": "fukuoka",
    "fukuoka_budokan": "fukuoka",
    # ── 九州（福岡交通圏の外） ──
    "jl_mikuni_kitakyushu": "kitakyushu",  # 北九州市小倉北区（福岡県だが別交通圏）
    "jl_ekimae_tosu": "saga",              # 鳥栖市
    "jl_egao_kumamoto": "kumamoto",        # 熊本市東区
    # ── 東京23区・武三交通圏 ──
    "tokyo_dome": "tokyo23",               # 文京区
    "tokyo_intl_forum": "tokyo23",         # 千代田区
    "ariake_arena": "tokyo23",             # 江東区
    "meiji_jingu": "tokyo23",              # 新宿区
    "jl_kokuritsu": "tokyo23",             # 新宿区
    # ── 多摩地区 ──
    "ajinomoto_stadium": "tama",           # 調布市
    "jl_machida": "tama",                  # 町田市
    # ── 京浜地区（横浜・川崎） ──
    "yokohama_arena": "keihin",            # 横浜市港北区
    "k_arena": "keihin",                   # 横浜市西区
    "nissan_stadium": "keihin",            # 横浜市港北区
    "yokohama_stadium": "keihin",          # 横浜市中区
    "pia_arena_mm": "keihin",              # 横浜市西区
    "jl_todoroki": "keihin",               # 川崎市中原区
    "jl_nippatsu": "keihin",               # 横浜市神奈川区
    # ── 相模・鎌倉地区 ──
    "jl_lemon_hiratsuka": "sagami",        # 平塚市
    "jl_gion_sagamihara": "sagami",        # 相模原市南区
    # ── 埼玉南部地区 ──
    "saitama_super_arena": "saitama_s",    # さいたま市中央区
    "belluna_dome": "saitama_s",           # 所沢市
    "jl_saitama_stadium": "saitama_s",     # さいたま市緑区
    # ── 千葉地区 ──
    "zozo_marine": "chiba",                # 千葉市美浜区
    "jl_fukuari": "chiba",                 # 千葉市中央区
    # ── 大阪市域交通圏 ──
    "kyocera_dome": "osaka",               # 大阪市西区
    "osaka_jo_hall": "osaka",              # 大阪市中央区
    "festival_hall": "osaka",              # 大阪市北区
    "nagai_stadium": "osaka",              # 大阪市東住吉区
    "jl_yodoko": "osaka",                  # 大阪市住吉区
    "jl_panasonic_suita": "osaka",         # 吹田市（大阪市域交通圏に含む）
    # ── 兵庫 ──
    "koshien": "kobe",                     # 西宮市（神戸市域交通圏＝阪神間を含む）
    "jl_noevir_kobe": "kobe",              # 神戸市兵庫区
    # ── 京都市域地区 ──
    "jl_sanga_kameoka": "kyoto_n",         # 亀岡市（境界実測＝京都北部地区。京都市域ではない）
    # ── 名古屋交通圏 ──
    "vantelin_dome": "nagoya",             # 名古屋市東区
    "ig_arena": "nagoya",                  # 名古屋市北区
    "jl_mizuho": "nagoya",                 # 名古屋市瑞穂区
    # ── 尾張・三河地区 ──
    "jl_toyota": "owari_mikawa",           # 豊田市
    # ── 静岡地区 ──
    "jl_yamaha": "shizuoka",               # 磐田市
    "jl_iai_nihondaira": "shizuoka",       # 静岡市清水区
    # ── 札幌・小樽地区 ──
    "sapporo_dome": "sapporo",             # 札幌市豊平区
    "escon_field": "chitose",             # 北広島市（境界実測＝千歳・空知・後志地区。札幌ではない）
    "jl_atsubetsu": "sapporo",             # 札幌市厚別区
    # ── 形なし地区（市区町村の所属で判断） ──
    "rakuten_park": "sendai",              # 仙台市宮城野区
    "jl_yurtec_sendai": "sendai",          # 仙台市泉区
    "mazda_stadium": "hiroshima_city",     # 広島市南区
    "jl_edion_peace": "hiroshima_city",    # 広島市中区
    "jl_denka_swan": "niigata_a",          # 新潟市中央区（A地区=新潟市側）
    "jl_okayama": "okayama",               # 岡山市北区
    "jl_mercari_kashima": "ibaraki",       # 鹿嶋市
}
