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
    # ── 拡充第2弾（2026-08-09）。境界の形がある圏はポリゴン点検✅・
    #    形なし圏は運賃ブロックCSV(taxi_fare_blocks.csv)の市町村定義で判定 ──
    "jl_sankyo_kashiwa": "chiba",          # 柏市（ポリゴン✅）
    "jl_peace_nagasaki": "nagasaki",       # 長崎市（ポリゴン✅）
    "jl_mitoshin_kasamatsu": "ibaraki",    # 那珂市・笠松運動公園（水戸市ではない・ポリゴン✅）
    "jl_ichigo_shintomi": "miyazaki",      # 児湯郡新富町（ポリゴン✅）
    "jl_satoyama_imabari": "ehime",        # 今治市（愛媛=全県1地区）
    "jl_kurasus_oita": "oita",             # 大分市（ポリゴン✅）
    "jl_soyu_akita": "akita",              # 秋田市（秋田=全県1地区）
    "jl_hawaiians_iwaki": "fukushima",     # いわき市（福島=全県1地区）
    "jl_prifoods_hachinohe": "aomori",     # 八戸市（青森=全県1地区）
    "jl_toyama": "toyama",                 # 富山市（富山=全県1地区）
    "jl_fujieda": "shizuoka",              # 藤枝市（ポリゴン✅）
    "jl_pocari_naruto": "tokushima_city",  # 鳴門市（徳島県市部地区）
    "jl_cfs_tochigi_city": "tochigi",      # 栃木市（ポリゴン✅）
    "jl_jit_kofu": "yamanashi_a",          # 甲府市＝甲府交通圏（ポリゴン✅・Bに入らないことも✅）
    "jl_nack_omiya": "saitama_s",          # さいたま市大宮区（ポリゴン✅）
    "jl_nd_yamagata": "yamagata",          # 天童市（山形=全県1地区）
    "jl_toho_fukushima": "fukushima",      # 福島市（福島=全県1地区）
    "jl_mirai_yamaguchi": "yamaguchi",     # 山口市（山口=全県1地区）
    "jl_kanseki_utsunomiya": "tochigi",    # 宇都宮市（ポリゴン✅）
    "jl_giken_kochi": "kochi_city",        # 高知市春野町（高知市域地区=高知市＋旧伊野町）
    "jl_gogo_kanazawa": "ishikawa",        # 金沢市（石川=全県1地区）
    "jl_alwin_matsumoto": "nagano_b",      # 松本市（長野A=旧長野市・千曲市・埴科郡のみ→Aではない）
    "jl_ninja_matsuyama": "ehime",         # 松山市（愛媛=全県1地区）
    "jl_meglio_marugame": "kagawa",        # 丸亀市（香川地区=小豆郡・直島以外の全域）
    "jl_nagano_u": "nagano_a",             # 長野市篠ノ井（1966年合併=H17以前の旧長野市域→A地区）
    "jl_hato_hikone": "shiga",             # 彦根市（ポリゴン✅）
    "jl_rohto_nara": "nara",               # 奈良市鴻ノ池（ポリゴン✅）
    "jl_shoda_gunma": "gunma_a",           # 前橋市＝中・西毛交通圏（ポリゴン✅・Bに入らないことも✅）
    "jl_okinawa_athletic": "okinawa_main", # 沖縄市（ポリゴン✅）
    "jl_shiranami_kagoshima": "kagoshima", # 鹿児島市鴨池（ポリゴン✅）
    "jl_himastadium_gifu": "gifu",         # 岐阜市長良（ポリゴン✅）
    "jl_axis_tottori": "tottori",          # 鳥取市（鳥取=全県1地区）
    "jl_hanazono": "osaka",                # 東大阪市（大阪市域交通圏に含む・ポリゴン✅）
    # ── ホール（球技場もアリーナも無い営業圏の入口・2026-08-09）──
    "wakayama_kenmin": "wakayama",         # 和歌山市小松原通（ポリゴン✅）
    "hakodate_kaikan": "hakodate_a",       # 函館市湯川町＝函館交通圏（A地区は函館市・北斗市・七飯町）
    # ── 本土なのに会場0だった営業圏の入口（2026-08-10）──
    # 🔴 宮城は境界の形が無いので運賃ブロックの定義で判定した。宮城地区＝「仙台地区を
    #    除く宮城県の全域」。利府町は仙台市ではなく、仙台の形の外にあることも確認済み。
    "sekisui_heim_super_arena": "miyagi",  # 宮城郡利府町菅谷（形なし→運賃ブロックの定義で判定）
    "sakuramate": "saitama_n",             # 熊谷市拾六間＝県北交通圏（ポリゴン✅）
    "odawara_sannomaru_hall": "odawara",   # 小田原市本町＝小田原交通圏（ポリゴン✅）
    "kirara_yamanakako": "yamanashi_b",    # 南都留郡山中湖村平野＝東部・富士北麓交通圏（ポリゴン✅）
    # ── Bリーグのアリーナ（2026-08-09）。判定の根拠を各行に残す ──
    #    形＝境界の形で1つに決まった／人＝運賃ブロックCSVの市町村定義で判断
    #    1県1地区＝県まるごと1地区の県
    "bl_toyota_arena_tokyo": "tokyo23",         # 形
    "bl_yokohama_buntai": "keihin",             # 形
    "bl_saga_arena": "saga",                    # 形
    "bl_hokkai_kitaeru": "sapporo",             # 形
    "bl_todoroki_arena": "keihin",              # 形
    "bl_lala_arena": "chiba",                   # 形
    "bl_morioka_takaya": "iwate_a",             # 人:盛岡市本宮＝旧玉山村ではないのでA地区
    "bl_tachikawa_tachihi": "tama",             # 形
    "bl_happiness_arena": "nagasaki",           # 人:長崎市＝本土地区（離島の形が重なる既知のクセ）
    "bl_openhouse_ota": "gunma_a",              # 形
    "bl_nisshin_kyoto": "kyoto_city",           # 人:京都市右京区西京極＝京都市域地区。北部地区ではない
    "bl_white_ring": "nagano_a",                # 人:長野市真島町＝1966年に更北村として編入＝H17.1.1以前の長野市域
    "bl_glion_kobe": "kobe",                    # 形
    "bl_matsue_taiikukan": "shimane_mainland",  # 人:松江市＝隠岐郡以外
    "bl_chiba_port_arena": "chiba",             # 形
    "bl_ykkap_arena": "toyama",                 # 1県1地区
    "bl_okinawa_suntory": "okinawa_main",       # 形
    "bl_koshigaya": "saitama_s",                # 形
    "bl_adastria_mito": "ibaraki",              # 形
    "bl_xebio_sendai": "sendai",                # 形
    "bl_cna_akita": "akita",                    # 1県1地区
    "bl_kumamoto_kenso": "kumamoto",            # 形
    "bl_ota_sogo": "tokyo23",                   # 形
    "bl_rohto_arena_nara": "nara",              # 形
    "bl_shiga_daihatsu": "shiga",               # 形
    "bl_ookini_maishima": "osaka",              # 形
    "bl_aore_nagaoka": "niigata_b",             # 人:長岡市＝A地区(旧新潟市・旧豊栄市・旧亀田町・聖籠町)以外
    "bl_esforta_hachioji": "tama",              # 形
    "bl_urawa_komaba": "saitama_s",             # 形
    "bl_anabuki_kagawa": "kagawa",              # 人:高松市＝小豆郡・直島町以外
    "bl_teriha_sekisui": "fukuoka",             # 形
    "bl_yokohama_budokan": "keihin",            # 形
    "bl_brex_utsunomiya": "tochigi",            # 形
    "bl_matsuyama_comi": "ehime",               # 1県1地区
    "bl_hiroshima_green": "hiroshima_city",     # 形
    "bl_wing_kariya": "owari_mikawa",           # 形
    "bl_tomony_tokushima": "tokushima_city",    # 人:徳島市＝市部地区
    "bl_shigeto_okayama": "okayama",            # 形
    "bl_okb_gifu": "gifu",                      # 形
    "bl_yamagata_kenso": "yamagata",            # 1県1地区
    "bl_biwajima": "nagoya",                    # 形
    "bl_ishikawa_sports": "ishikawa",           # 1県1地区
    "bl_tawarada": "yamaguchi",                 # 1県1地区
    "bl_kagoshima_kenso": "kagoshima",          # 形
    "bl_agf_suzuka": "mie",                     # 形
    "bl_kakuhiro_aomori": "aomori",             # 1県1地区
    "bl_kariya_shitai": "owari_mikawa",         # 形
    "bl_kanazawa_shiso": "ishikawa",            # 1県1地区
    "bl_shizuoka_chuo": "shizuoka",             # 形
    "bl_tsuyama": "okayama",                    # 形
    "bl_akibadai": "sagami",                    # 形
    "bl_deai_dome": "gifu",                     # 形
    "bl_nikkan_tochigi": "tochigi",             # 形
    "bl_butterfly_tokorozawa": "saitama_s",     # 形
    "bl_jtekt_nara": "nara",                    # 形
    "bl_hamamatsu_arena": "shizuoka",           # 形
    "bl_sunarena_sendai": "kagoshima",          # 形
    "bl_yoyogi_2": "tokyo23",                   # 形
    "bl_samukawa": "sagami",                    # 形
    "bl_fpco_fukuyama": "hiroshima",            # 人:福山市＝広島市域地区以外
    "bl_togoshi": "tokyo23",                    # 形
    "bl_asue_osaka": "osaka",                   # 形
    "bl_hitachi_ikenokawa": "ibaraki",          # 形
    "bl_shimadzu_kyoto": "kyoto_city",          # 人:京都市北区＝京都市域地区
    "bl_ehime_budokan": "ehime",                # 1県1地区
    "bl_machida_shitai": "tama",                # 形
    "bl_flat_hachinohe": "aomori",              # 人:八戸市（青森＝全県1地区）
    "bl_tsurushin_komagi": "yamagata",          # 人:鶴岡市（山形＝全県1地区）
    "bl_edogawa": "tokyo23",                    # 形
    "bl_takayama_big": "hida",                  # 人:高山市＝旧飛騨地区
    "bl_mutsu_maeda": "aomori",                 # 1県1地区
    "bl_ichinoseki_udome": "iwate_b",           # 人:一関市＝A地区(盛岡市・滝沢市・矢巾町)以外
    "bl_tomony_naka": "tokushima_city",         # 人:那賀町＝那賀郡は市部地区に含まれる（CSVの定義）
    "bl_aira": "kagoshima",                     # 形
    "bl_nakamura_sports": "nagoya",             # 形
    "bl_maeda_arena": "aomori",                 # 1県1地区
    "bl_marugame_shimin": "kagawa",             # 人:丸亀市
    "bl_niigata_higashi": "niigata_a",          # 形
    "bl_entrio_toyoda": "owari_mikawa",         # 形
    "bl_yamagata_sports": "yamagata",           # 1県1地区
    "bl_aomori_budokan": "aomori",              # 1県1地区
    "bl_tsuruga_sogo": "fukui",                 # 形
    "bl_zentsuji": "kagawa",                    # 人:善通寺市
    "bl_aisin_echizen": "fukui",                # 形
    "bl_kurume_arena": "fukuoka_b",             # 形
    "bl_kikuyo": "kumamoto",                    # 形
    "bl_hisai": "mie",                          # 形
    "bl_soko_yokkaichi": "mie",                 # 形
    "bl_arakawa": "tokyo23",                    # 形
    "bl_ogino": "sagami",                       # 形
    "bl_jcom_shimonoseki": "yamaguchi",         # 1県1地区
    "bl_chichibunomiya": "sagami",              # 形
    "bl_hiroshima_sunplaza": "hiroshima_city",  # 形
    "bl_funabashi_arena": "chiba",              # 形
    "bl_kitakyushu_sogo": "kitakyushu",         # 形
    "bl_takamatsu_sogo": "kagawa",              # 人:高松市
}
