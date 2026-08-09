"""会場マスタ。

福岡9会場はアプリ(event_service.dart)の Venue 定数と key/座標を一致させる。
全国の大箱は需要インパクト大の会場をシード（スクレイパーは順次追加）。
"""
from model import Venue

# ─── 福岡（アプリと同一） ───────────────────────────────────────────────────
MARINE_MESSE_A = Venue(
    key="marine_messe_a", name="マリンメッセ福岡A館",
    lat=33.608276, lng=130.402028, region="福岡", big_box=True,
    official_url="https://www.marinemesse.or.jp/messe/event/",
)
MARINE_MESSE_B = Venue(
    key="marine_messe_b", name="マリンメッセ福岡B館",
    lat=33.606532, lng=130.403585, region="福岡", big_box=True,
    official_url="https://www.marinemesse.or.jp/messe-b/event/",
)
FUKUOKA_CONGRESS = Venue(
    key="fukuoka_congress", name="福岡国際会議場",
    lat=33.604404, lng=130.403444, region="福岡",
    official_url="https://www.marinemesse.or.jp/congress/event/",
)
FUKUOKA_KOKUSAI_CENTER = Venue(
    key="fukuoka_kokusai_center", name="福岡国際センター",
    lat=33.603178, lng=130.401333, region="福岡",
    official_url="https://www.marinemesse.or.jp/kokusai/event/",
)
FUKUOKA_SUNPALACE = Venue(
    key="fukuoka_sunpalace", name="福岡サンパレス",
    lat=33.603445, lng=130.402727, region="福岡",
    official_url="https://www.f-sunpalace.com/hall/",
)
PAYPAY_DOME = Venue(
    key="paypay_dome", name="みずほPayPayドーム福岡",
    lat=33.5957, lng=130.3621, region="福岡", big_box=True,
    official_url="https://www.softbankhawks.co.jp/stadium/",
)
BEST_DENKI_STADIUM = Venue(
    key="best_denki_stadium", name="ベスト電器スタジアム",
    lat=33.593722, lng=130.467500, region="福岡", big_box=True,
    official_url="https://www.avispa.co.jp/",
)
HAKATAZA = Venue(
    key="hakataza", name="博多座",
    lat=33.595734, lng=130.406395, region="福岡",
    official_url="https://www.hakataza.co.jp/lineup/",
)
FUKUOKA_CIVIC_HALL = Venue(
    key="fukuoka_civic_hall", name="福岡市民ホール",
    lat=33.598389, lng=130.398918, region="福岡",
    official_url="https://www.fukuoka-civic-hall.jp/event/",
)
MOMOCHI_BUNKA = Venue(
    key="momochi_bunka", name="SAWARAPIA(ももち文化センター)",
    lat=33.582418, lng=130.347089, region="福岡",
    official_url="https://momochi-bunka.com/event/",
)
FUKUOKA_BUDOKAN = Venue(
    key="fukuoka_budokan", name="福岡武道館",
    lat=33.603306, lng=130.416168, region="福岡",
    official_url="https://fukuokabudokan.jp/",
)

# ─── 全国の大箱（座標シード・スクレイパーは順次追加） ───────────────────────
# まずは「終演後にタクシー需要が大きく出る」大規模アリーナ/ドーム/スタジアムから。
TOKYO_DOME = Venue(
    key="tokyo_dome", name="東京ドーム",
    lat=35.705622, lng=139.751853, region="東京", big_box=True,
    official_url="https://www.tokyo-dome.co.jp/dome/",
)
SAITAMA_SUPER_ARENA = Venue(
    key="saitama_super_arena", name="さいたまスーパーアリーナ",
    lat=35.894940, lng=139.630700, region="埼玉", big_box=True,
    official_url="https://www.saitama-arena.co.jp/",
)
YOKOHAMA_ARENA = Venue(
    key="yokohama_arena", name="横浜アリーナ",
    lat=35.512200, lng=139.617000, region="神奈川", big_box=True,
    official_url="https://www.yokohama-arena.co.jp/",
)
K_ARENA = Venue(
    key="k_arena", name="Kアリーナ横浜",
    lat=35.466400, lng=139.630300, region="神奈川", big_box=True,
    official_url="https://k-arena.com/schedule/",
)
ARIAKE_ARENA = Venue(
    key="ariake_arena", name="有明アリーナ",
    lat=35.642000, lng=139.793700, region="東京", big_box=True,
    official_url="https://ariake-arena.tokyo/event/",
)
NISSAN_STADIUM = Venue(
    key="nissan_stadium", name="日産スタジアム",
    lat=35.509900, lng=139.606200, region="神奈川", big_box=True,
    official_url="https://www.nissan-stadium.jp/calendar/",
)
AJINOMOTO_STADIUM = Venue(
    key="ajinomoto_stadium", name="味の素スタジアム",
    lat=35.664500, lng=139.527500, region="東京", big_box=True,
    official_url="https://www.ajinomotostadium.com/schedule/",
)
BELLUNA_DOME = Venue(
    key="belluna_dome", name="ベルーナドーム",
    lat=35.768900, lng=139.420800, region="埼玉", big_box=True,
    official_url="https://bellunadome.seibulions.co.jp/",
)
TOKYO_INTL_FORUM = Venue(
    key="tokyo_intl_forum", name="東京国際フォーラム",
    lat=35.677200, lng=139.763700, region="東京", big_box=True,
    official_url="https://www.t-i-forum.co.jp/visitors/event/",
)
OSAKA_JO_HALL = Venue(
    key="osaka_jo_hall", name="大阪城ホール",
    lat=34.687300, lng=135.532000, region="大阪", big_box=True,
    official_url="https://www.osaka-johall.com/event/",
)
FESTIVAL_HALL = Venue(
    key="festival_hall", name="フェスティバルホール",
    lat=34.693800, lng=135.494400, region="大阪", big_box=True,
    official_url="https://www.festivalhall.jp/events/",
)
IG_ARENA = Venue(
    key="ig_arena", name="IGアリーナ",
    lat=35.184600, lng=136.899000, region="愛知", big_box=True,
    official_url="https://www.ig-arena.jp/events/",
)
KYOCERA_DOME = Venue(
    key="kyocera_dome", name="京セラドーム大阪",
    lat=34.669358, lng=135.476056, region="大阪", big_box=True,
    official_url="https://www.kyoceradome-osaka.jp/",
)
NAGOYA_DOME = Venue(
    key="vantelin_dome", name="バンテリンドーム ナゴヤ",
    lat=35.186500, lng=136.947500, region="愛知", big_box=True,
    official_url="https://www.nagoya-dome.co.jp/",
)
SAPPORO_DOME = Venue(
    key="sapporo_dome", name="札幌ドーム",
    lat=43.015100, lng=141.409800, region="北海道", big_box=True,
    official_url="https://www.sapporo-dome.co.jp/",
)
PIA_ARENA_MM = Venue(
    key="pia_arena_mm", name="ぴあアリーナMM",
    lat=35.461300, lng=139.629600, region="神奈川", big_box=True,
    official_url="https://pia-arena-mm.jp/event/",
)
# ヤンマースタジアム長居 と ヨドコウ桜スタジアムは長居公園内で隣接（約150m）。
# セレッソ大阪のホーム戦をまとめて1会場として扱う（タクシー需要上は同一エリア）。
NAGAI_STADIUM = Venue(
    key="nagai_stadium", name="ヤンマースタジアム長居（長居公園）",
    lat=34.614900, lng=135.517800, region="大阪", big_box=True,
    official_url="https://www.cerezo.jp/matches/",
)
# ─── プロ野球（npb.jp の月別カレンダーから取得） ───────────────────────────
MEIJI_JINGU = Venue(
    key="meiji_jingu", name="明治神宮野球場",
    lat=35.674700, lng=139.717200, region="東京", big_box=True,
    official_url="https://npb.jp/games/2026/",
)
YOKOHAMA_STADIUM = Venue(
    key="yokohama_stadium", name="横浜スタジアム",
    lat=35.443300, lng=139.640000, region="神奈川", big_box=True,
    official_url="https://npb.jp/games/2026/",
)
ZOZO_MARINE = Venue(
    key="zozo_marine", name="ZOZOマリンスタジアム",
    lat=35.645200, lng=140.031200, region="千葉", big_box=True,
    official_url="https://npb.jp/games/2026/",
)
KOSHIEN = Venue(
    key="koshien", name="阪神甲子園球場",
    lat=34.721100, lng=135.361700, region="兵庫", big_box=True,
    official_url="https://npb.jp/games/2026/",
)
# NPB本拠地の穴埋め（2026-07 追加）。日本ハムは北広島へ移転
# （北広島市は札幌交通圏ではなく千歳・空知・後志地区＝境界データで実測 2026-08-09）。
ESCON_FIELD = Venue(
    key="escon_field", name="エスコンフィールド北海道",
    lat=42.940300, lng=141.610000, region="北海道", big_box=True,
    official_url="https://npb.jp/games/2026/",
)
RAKUTEN_PARK = Venue(
    key="rakuten_park", name="楽天モバイルパーク宮城",
    lat=38.256400, lng=140.902700, region="宮城", big_box=True,
    official_url="https://npb.jp/games/2026/",
)
MAZDA_STADIUM = Venue(
    key="mazda_stadium", name="MAZDA Zoom-Zoomスタジアム広島",
    lat=34.391900, lng=132.484700, region="広島", big_box=True,
    official_url="https://npb.jp/games/2026/",
)

# ── J-League スタジアム（2026-07 統一スクレイパー jleague.py 用）──
_JL_URL = "https://data.j-league.or.jp/SFMS01/"
JL_KOKURITSU = Venue(key="jl_kokuritsu", name="国立競技場", lat=35.677800, lng=139.714700, region="東京", big_box=True, official_url=_JL_URL)
JL_SAITAMA = Venue(key="jl_saitama_stadium", name="埼玉スタジアム2002", lat=35.903600, lng=139.717500, region="埼玉", big_box=True, official_url=_JL_URL)
JL_TODOROKI = Venue(key="jl_todoroki", name="等々力陸上競技場", lat=35.564700, lng=139.660300, region="神奈川", big_box=True, official_url=_JL_URL)
JL_NIPPATSU = Venue(key="jl_nippatsu", name="ニッパツ三ツ沢球技場", lat=35.475000, lng=139.597800, region="神奈川", big_box=True, official_url=_JL_URL)
JL_LEMON = Venue(key="jl_lemon_hiratsuka", name="レモンガススタジアム平塚", lat=35.341900, lng=139.338900, region="神奈川", big_box=True, official_url=_JL_URL)
JL_MACHIDA = Venue(key="jl_machida", name="町田GIONスタジアム", lat=35.588900, lng=139.454700, region="東京", big_box=True, official_url=_JL_URL)
JL_GIONS = Venue(key="jl_gion_sagamihara", name="ギオンスタジアム(相模原)", lat=35.552000, lng=139.360000, region="神奈川", big_box=True, official_url=_JL_URL)
JL_YAMAHA = Venue(key="jl_yamaha", name="ヤマハスタジアム", lat=34.718600, lng=137.883600, region="静岡", big_box=True, official_url=_JL_URL)
JL_IAI = Venue(key="jl_iai_nihondaira", name="IAIスタジアム日本平", lat=34.957800, lng=138.449700, region="静岡", big_box=True, official_url=_JL_URL)
JL_TOYOTA = Venue(key="jl_toyota", name="豊田スタジアム", lat=35.083900, lng=137.171900, region="愛知", big_box=True, official_url=_JL_URL)
JL_MIZUHO = Venue(key="jl_mizuho", name="パロマ瑞穂スタジアム", lat=35.128900, lng=136.950800, region="愛知", big_box=True, official_url=_JL_URL)
JL_PANASTA = Venue(key="jl_panasonic_suita", name="パナソニックスタジアム吹田", lat=34.803600, lng=135.538900, region="大阪", big_box=True, official_url=_JL_URL)
JL_YODOKO = Venue(key="jl_yodoko", name="ヨドコウ桜スタジアム", lat=34.614400, lng=135.518300, region="大阪", big_box=True, official_url=_JL_URL)
JL_NOEVIR = Venue(key="jl_noevir_kobe", name="ノエビアスタジアム神戸", lat=34.656700, lng=135.169400, region="兵庫", big_box=True, official_url=_JL_URL)
JL_SANGA = Venue(key="jl_sanga_kameoka", name="サンガスタジアム by KYOCERA", lat=35.011900, lng=135.574700, region="京都", big_box=True, official_url=_JL_URL)
JL_EDION = Venue(key="jl_edion_peace", name="エディオンピースウイング広島", lat=34.396900, lng=132.451900, region="広島", big_box=True, official_url=_JL_URL)
JL_YURTEC = Venue(key="jl_yurtec_sendai", name="ユアテックスタジアム仙台", lat=38.271600, lng=140.880300, region="宮城", big_box=True, official_url=_JL_URL)
JL_DENKA = Venue(key="jl_denka_swan", name="デンカビッグスワンスタジアム", lat=37.886900, lng=139.065300, region="新潟", big_box=True, official_url=_JL_URL)
JL_FUKUARI = Venue(key="jl_fukuari", name="フクダ電子アリーナ", lat=35.561900, lng=140.106400, region="千葉", big_box=True, official_url=_JL_URL)
JL_MIKUNI = Venue(key="jl_mikuni_kitakyushu", name="ミクニワールドスタジアム北九州", lat=33.896300, lng=130.924700, region="福岡", big_box=True, official_url=_JL_URL)
JL_EKIMAE = Venue(key="jl_ekimae_tosu", name="駅前不動産スタジアム", lat=33.373600, lng=130.521900, region="佐賀", big_box=True, official_url=_JL_URL)
JL_EGAO = Venue(key="jl_egao_kumamoto", name="えがお健康スタジアム", lat=32.784700, lng=130.794700, region="熊本", big_box=True, official_url=_JL_URL)
JL_OKAYAMA = Venue(key="jl_okayama", name="JFE晴れの国スタジアム(岡山)", lat=34.663600, lng=133.946300, region="岡山", big_box=True, official_url=_JL_URL)
JL_ATSUBETSU = Venue(key="jl_atsubetsu", name="厚別公園競技場", lat=43.035600, lng=141.447200, region="北海道", big_box=True, official_url=_JL_URL)
JL_MERCARI = Venue(key="jl_mercari_kashima", name="メルカリスタジアム", lat=35.992200, lng=140.640800, region="茨城", big_box=True, official_url=_JL_URL)

# ── J-League 拡充第2弾（2026-08-09・会場0の営業圏を埋める）──
# 座標はOSM実測・営業圏は境界ポリゴン点検＋運賃ブロックCSV（taxi_fare_blocks.csv）で確認。
JL_SANKYO_KASHIWA = Venue(key="jl_sankyo_kashiwa", name="三協フロンテア柏スタジアム", lat=35.848479, lng=139.975052, region="千葉", big_box=True, official_url=_JL_URL)
JL_PEACE_NAGASAKI = Venue(key="jl_peace_nagasaki", name="ピーススタジアム(長崎)", lat=32.759052, lng=129.864960, region="長崎", big_box=True, official_url=_JL_URL)
JL_MITOSHIN = Venue(key="jl_mitoshin_kasamatsu", name="水戸信用金庫スタジアム(笠松)", lat=36.457294, lng=140.538191, region="茨城", big_box=True, official_url=_JL_URL)
JL_ICHIGO = Venue(key="jl_ichigo_shintomi", name="いちご宮崎新富サッカー場", lat=32.073711, lng=131.491396, region="宮崎", big_box=True, official_url=_JL_URL)
JL_SATOYAMA = Venue(key="jl_satoyama_imabari", name="アシックス里山スタジアム(今治)", lat=34.040663, lng=132.958807, region="愛媛", big_box=True, official_url=_JL_URL)
JL_KURASUS = Venue(key="jl_kurasus_oita", name="クラサスドーム大分", lat=33.200768, lng=131.657485, region="大分", big_box=True, official_url=_JL_URL)
JL_SOYU = Venue(key="jl_soyu_akita", name="ソユースタジアム(秋田)", lat=39.721521, lng=140.095762, region="秋田", big_box=True, official_url=_JL_URL)
JL_HAWAIIANS = Venue(key="jl_hawaiians_iwaki", name="ハワイアンズスタジアムいわき", lat=37.017238, lng=140.864412, region="福島", big_box=True, official_url=_JL_URL)
JL_PRIFOODS = Venue(key="jl_prifoods_hachinohe", name="プライフーズスタジアム(八戸)", lat=40.590392, lng=141.457085, region="青森", big_box=True, official_url=_JL_URL)
JL_TOYAMA = Venue(key="jl_toyama", name="富山県総合運動公園陸上競技場", lat=36.625020, lng=137.195574, region="富山", big_box=True, official_url=_JL_URL)
JL_FUJIEDA = Venue(key="jl_fujieda", name="藤枝総合運動公園サッカー場", lat=34.881507, lng=138.232894, region="静岡", big_box=True, official_url=_JL_URL)
JL_POCARI = Venue(key="jl_pocari_naruto", name="ポカリスエットスタジアム(鳴門)", lat=34.168307, lng=134.617860, region="徳島", big_box=True, official_url=_JL_URL)
JL_CFS = Venue(key="jl_cfs_tochigi_city", name="CITY FOOTBALL STATION(栃木市)", lat=36.337568, lng=139.645288, region="栃木", big_box=True, official_url=_JL_URL)
JL_JIT = Venue(key="jl_jit_kofu", name="JITリサイクルインクスタジアム(甲府)", lat=35.622343, lng=138.589833, region="山梨", big_box=True, official_url=_JL_URL)
JL_NACK = Venue(key="jl_nack_omiya", name="NACK5スタジアム大宮", lat=35.916197, lng=139.633475, region="埼玉", big_box=True, official_url=_JL_URL)
JL_ND_YAMAGATA = Venue(key="jl_nd_yamagata", name="NDソフトスタジアム山形", lat=38.335599, lng=140.378390, region="山形", big_box=True, official_url=_JL_URL)
JL_TOHO = Venue(key="jl_toho_fukushima", name="とうほう・みんなのスタジアム(福島)", lat=37.723265, lng=140.361302, region="福島", big_box=True, official_url=_JL_URL)
JL_MIRAI = Venue(key="jl_mirai_yamaguchi", name="維新みらいふスタジアム(山口)", lat=34.154402, lng=131.437475, region="山口", big_box=True, official_url=_JL_URL)
JL_KANSEKI = Venue(key="jl_kanseki_utsunomiya", name="カンセキスタジアムとちぎ(宇都宮)", lat=36.515020, lng=139.857453, region="栃木", big_box=True, official_url=_JL_URL)
JL_GIKEN = Venue(key="jl_giken_kochi", name="GIKENスタジアム(高知・春野)", lat=33.511272, lng=133.502781, region="高知", big_box=True, official_url=_JL_URL)
JL_GOGO_KANAZAWA = Venue(key="jl_gogo_kanazawa", name="金沢ゴーゴーカレースタジアム", lat=36.595926, lng=136.657685, region="石川", big_box=True, official_url=_JL_URL)
JL_ALWIN = Venue(key="jl_alwin_matsumoto", name="サンプロアルウィン(松本)", lat=36.179716, lng=137.917138, region="長野", big_box=True, official_url=_JL_URL)
JL_NINJA = Venue(key="jl_ninja_matsuyama", name="ニンジニアスタジアム(松山)", lat=33.768231, lng=132.797610, region="愛媛", big_box=True, official_url=_JL_URL)
JL_MEGLIO = Venue(key="jl_meglio_marugame", name="四国化成MEGLIOスタジアム(丸亀)", lat=34.261783, lng=133.785766, region="香川", big_box=True, official_url=_JL_URL)
JL_NAGANO_U = Venue(key="jl_nagano_u", name="長野Uスタジアム", lat=36.580017, lng=138.169421, region="長野", big_box=True, official_url=_JL_URL)
JL_HATO = Venue(key="jl_hato_hikone", name="平和堂HATOスタジアム(彦根)", lat=35.281691, lng=136.255226, region="滋賀", big_box=True, official_url=_JL_URL)
JL_ROHTO = Venue(key="jl_rohto_nara", name="ロートフィールド奈良", lat=34.697587, lng=135.829169, region="奈良", big_box=True, official_url=_JL_URL)
JL_SHODA = Venue(key="jl_shoda_gunma", name="正田醤油スタジアム群馬(前橋)", lat=36.411607, lng=139.053189, region="群馬", big_box=True, official_url=_JL_URL)
JL_OKINAWA = Venue(key="jl_okinawa_athletic", name="沖縄県総合運動公園陸上競技場", lat=26.308613, lng=127.821115, region="沖縄", big_box=True, official_url=_JL_URL)
JL_SHIRANAMI = Venue(key="jl_shiranami_kagoshima", name="白波スタジアム(鹿児島)", lat=31.564895, lng=130.560167, region="鹿児島", big_box=True, official_url=_JL_URL)
JL_HIMA = Venue(key="jl_himastadium_gifu", name="ヒマラヤスタジアム岐阜(長良川)", lat=35.441335, lng=136.766064, region="岐阜", big_box=True, official_url=_JL_URL)
JL_AXIS = Venue(key="jl_axis_tottori", name="Axisバードスタジアム(鳥取)", lat=35.458227, lng=134.221760, region="鳥取", big_box=True, official_url=_JL_URL)
JL_HANAZONO = Venue(key="jl_hanazono", name="東大阪市花園ラグビー場", lat=34.669327, lng=135.626569, region="大阪", big_box=True, official_url=_JL_URL)

# 全会場リスト（build.py から参照）
ALL_VENUES = [
    MARINE_MESSE_A, MARINE_MESSE_B, FUKUOKA_CONGRESS, FUKUOKA_KOKUSAI_CENTER,
    FUKUOKA_SUNPALACE, PAYPAY_DOME, BEST_DENKI_STADIUM, HAKATAZA,
    FUKUOKA_CIVIC_HALL, MOMOCHI_BUNKA, FUKUOKA_BUDOKAN,
    TOKYO_DOME, SAITAMA_SUPER_ARENA, YOKOHAMA_ARENA, KYOCERA_DOME,
    NAGOYA_DOME, SAPPORO_DOME,
    K_ARENA, ARIAKE_ARENA, NISSAN_STADIUM, AJINOMOTO_STADIUM,
    BELLUNA_DOME, TOKYO_INTL_FORUM, OSAKA_JO_HALL, FESTIVAL_HALL, IG_ARENA,
    PIA_ARENA_MM, NAGAI_STADIUM,
    MEIJI_JINGU, YOKOHAMA_STADIUM, ZOZO_MARINE, KOSHIEN,
    ESCON_FIELD, RAKUTEN_PARK, MAZDA_STADIUM,
    JL_KOKURITSU, JL_SAITAMA, JL_TODOROKI, JL_NIPPATSU, JL_LEMON, JL_MACHIDA,
    JL_GIONS, JL_YAMAHA, JL_IAI, JL_TOYOTA, JL_MIZUHO, JL_PANASTA, JL_YODOKO,
    JL_NOEVIR, JL_SANGA, JL_EDION, JL_YURTEC, JL_DENKA, JL_FUKUARI, JL_MIKUNI,
    JL_EKIMAE, JL_EGAO, JL_OKAYAMA, JL_ATSUBETSU, JL_MERCARI,
    JL_SANKYO_KASHIWA, JL_PEACE_NAGASAKI, JL_MITOSHIN, JL_ICHIGO, JL_SATOYAMA,
    JL_KURASUS, JL_SOYU, JL_HAWAIIANS, JL_PRIFOODS, JL_TOYAMA, JL_FUJIEDA,
    JL_POCARI, JL_CFS, JL_JIT, JL_NACK, JL_ND_YAMAGATA, JL_TOHO, JL_MIRAI,
    JL_KANSEKI, JL_GIKEN, JL_GOGO_KANAZAWA, JL_ALWIN, JL_NINJA, JL_MEGLIO,
    JL_NAGANO_U, JL_HATO, JL_ROHTO, JL_SHODA, JL_OKINAWA, JL_SHIRANAMI,
    JL_HIMA, JL_AXIS, JL_HANAZONO,
]

# マリンメッセ系: CMS会場ID → Venue
MARINE_MESSE_VENUE_ID_MAP = {
    "rhPkRp7kYFiu7CuFjFaW": MARINE_MESSE_A,
    "1uLqpDJwQBdRWOuFnLUm": MARINE_MESSE_B,
    "M1a4HXq8jUU5bnAKafsY": FUKUOKA_CONGRESS,
    "ZxskZD69QFYho9rXNUZl": FUKUOKA_KOKUSAI_CENTER,
}
