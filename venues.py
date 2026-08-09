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

# ─── ホール（Jリーグ・Bリーグが届かない営業圏の入口） ─────────────────────
# 座標はOSM実測・営業圏は境界ポリゴンで確認（2026-08-09）。
WAKAYAMA_KENMIN = Venue(
    key="wakayama_kenmin", name="和歌山県民文化会館",
    lat=34.224865, lng=135.167887, region="和歌山",
    official_url="http://www.wacaf.or.jp/event/event_view.html?hall=1",
)
# ネーミングライツで「函館サーモン・まるなまホール」に改称済み。
# 運転手が呼び慣れた旧称を主にし、現名称を括弧で添える。
HAKODATE_KAIKAN = Venue(
    key="hakodate_kaikan", name="函館市民会館(まるなまホール)",
    lat=41.782914, lng=140.784128, region="北海道",
    official_url="https://www.zaidan-hakodate.com/kaikan/",
)


# ─── Bリーグ（PREMIER/ONE/NEXT）のアリーナ ───────────────────────────────
# 2026-08-09 追加。Jリーグ・プロ野球では会場が作れない営業圏（京都市域・福井・三重・
# 福岡県B地区・島根・岩手・徳島市部 ほか）を埋める要。
# 座標は住所検索(Nominatim)と名前検索(Overpass)の2系統で取り、市区町村まで一致した
# ものだけ採用している（総称名『体育館』に釣られて別の建物を掴む事故が実際に起きた）。
_BL_URL = "https://www.bleague.jp/schedule/"
BL_TOYOTA_ARENA_TOKYO = Venue(key="bl_toyota_arena_tokyo", name="TOYOTA ARENA TOKYO", lat=35.626591, lng=139.782654, region="東京", big_box=True, official_url=_BL_URL)
BL_YOKOHAMA_BUNTAI = Venue(key="bl_yokohama_buntai", name="横浜BUNTAI", lat=35.440972, lng=139.636517, region="神奈川", big_box=True, official_url=_BL_URL)
BL_SAGA_ARENA = Venue(key="bl_saga_arena", name="SAGAアリーナ", lat=33.274746, lng=130.292846, region="佐賀", big_box=True, official_url=_BL_URL)
BL_HOKKAI_KITAERU = Venue(key="bl_hokkai_kitaeru", name="北海きたえーる", lat=43.043985, lng=141.376249, region="北海道", big_box=True, official_url=_BL_URL)
BL_TODOROKI_ARENA = Venue(key="bl_todoroki_arena", name="東急ドレッセとどろきアリーナ", lat=35.586639, lng=139.646581, region="神奈川", big_box=True, official_url=_BL_URL)
BL_LALA_ARENA = Venue(key="bl_lala_arena", name="LaLa arena TOKYO-BAY", lat=35.683809, lng=139.989729, region="千葉", big_box=True, official_url=_BL_URL)
BL_MORIOKA_TAKAYA = Venue(key="bl_morioka_takaya", name="盛岡タカヤアリーナ", lat=39.690895, lng=141.120444, region="岩手", big_box=True, official_url=_BL_URL)
BL_TACHIKAWA_TACHIHI = Venue(key="bl_tachikawa_tachihi", name="アリーナ立川立飛", lat=35.714418, lng=139.417141, region="東京", big_box=True, official_url=_BL_URL)
BL_HAPPINESS_ARENA = Venue(key="bl_happiness_arena", name="ハピネスアリーナ(長崎)", lat=32.759331, lng=129.864632, region="長崎", big_box=True, official_url=_BL_URL)
BL_OPENHOUSE_OTA = Venue(key="bl_openhouse_ota", name="オープンハウスアリーナ太田", lat=36.2765, lng=139.395909, region="群馬", big_box=True, official_url=_BL_URL)
BL_NISSHIN_KYOTO = Venue(key="bl_nisshin_kyoto", name="にっしんでんきアリーナ京都(京都市体育館)", lat=34.995511, lng=135.71502, region="京", big_box=True, official_url=_BL_URL)
BL_WHITE_RING = Venue(key="bl_white_ring", name="ホワイトリング(長野)", lat=36.6047, lng=138.20627, region="長野", big_box=True, official_url=_BL_URL)
BL_GLION_KOBE = Venue(key="bl_glion_kobe", name="GLION ARENA KOBE", lat=34.681661, lng=135.196072, region="兵庫", big_box=True, official_url=_BL_URL)
BL_MATSUE_TAIIKUKAN = Venue(key="bl_matsue_taiikukan", name="松江市総合体育館", lat=35.471291, lng=133.066009, region="島根", big_box=True, official_url=_BL_URL)
BL_CHIBA_PORT_ARENA = Venue(key="bl_chiba_port_arena", name="千葉ポートアリーナ", lat=35.603845, lng=140.110992, region="千葉", big_box=True, official_url=_BL_URL)
BL_YKKAP_ARENA = Venue(key="bl_ykkap_arena", name="YKK APアリーナ(富山)", lat=36.644418, lng=137.19052, region="富山", big_box=True, official_url=_BL_URL)
BL_OKINAWA_SUNTORY = Venue(key="bl_okinawa_suntory", name="沖縄サントリーアリーナ", lat=26.33278, lng=127.783571, region="沖縄", big_box=True, official_url=_BL_URL)
BL_KOSHIGAYA = Venue(key="bl_koshigaya", name="越谷市立総合体育館", lat=35.902755, lng=139.813467, region="埼玉", big_box=True, official_url=_BL_URL)
BL_ADASTRIA_MITO = Venue(key="bl_adastria_mito", name="アダストリアみとアリーナ", lat=36.380431, lng=140.448767, region="茨城", big_box=True, official_url=_BL_URL)
BL_XEBIO_SENDAI = Venue(key="bl_xebio_sendai", name="ゼビオアリーナ仙台", lat=38.230297, lng=140.887247, region="宮城", big_box=True, official_url=_BL_URL)
BL_CNA_AKITA = Venue(key="bl_cna_akita", name="CNAアリーナ☆あきた", lat=39.725785, lng=140.087708, region="秋田", big_box=True, official_url=_BL_URL)
BL_KUMAMOTO_KENSO = Venue(key="bl_kumamoto_kenso", name="熊本県立総合体育館", lat=32.814457, lng=130.701509, region="熊本", big_box=True, official_url=_BL_URL)
BL_OTA_SOGO = Venue(key="bl_ota_sogo", name="EBARA WAVE アリーナおおた(大田区総合体育館)", lat=35.564601, lng=139.727862, region="東京", big_box=True, official_url=_BL_URL)
BL_ROHTO_ARENA_NARA = Venue(key="bl_rohto_arena_nara", name="ロートアリーナ奈良", lat=34.695175, lng=135.828037, region="奈良", big_box=True, official_url=_BL_URL)
BL_SHIGA_DAIHATSU = Venue(key="bl_shiga_daihatsu", name="滋賀ダイハツアリーナ", lat=34.970826, lng=135.951016, region="滋賀", big_box=True, official_url=_BL_URL)
BL_OOKINI_MAISHIMA = Venue(key="bl_ookini_maishima", name="おおきにアリーナ舞洲", lat=34.665471, lng=135.397633, region="大阪", big_box=True, official_url=_BL_URL)
BL_AORE_NAGAOKA = Venue(key="bl_aore_nagaoka", name="シティホールプラザ アオーレ長岡", lat=37.446216, lng=138.851374, region="新潟", big_box=True, official_url=_BL_URL)
BL_ESFORTA_HACHIOJI = Venue(key="bl_esforta_hachioji", name="エスフォルタアリーナ八王子", lat=35.639903, lng=139.292541, region="東京", big_box=True, official_url=_BL_URL)
BL_URAWA_KOMABA = Venue(key="bl_urawa_komaba", name="浦和駒場体育館", lat=35.872395, lng=139.662174, region="埼玉", big_box=True, official_url=_BL_URL)
BL_ANABUKI_KAGAWA = Venue(key="bl_anabuki_kagawa", name="あなぶきアリーナ香川", lat=34.353791, lng=134.046089, region="香川", big_box=True, official_url=_BL_URL)
BL_TERIHA_SEKISUI = Venue(key="bl_teriha_sekisui", name="照葉積水ハウスアリーナ", lat=33.667667, lng=130.417605, region="福岡", big_box=True, official_url=_BL_URL)
BL_YOKOHAMA_BUDOKAN = Venue(key="bl_yokohama_budokan", name="横浜武道館", lat=35.439739, lng=139.63634, region="神奈川", big_box=True, official_url=_BL_URL)
BL_BREX_UTSUNOMIYA = Venue(key="bl_brex_utsunomiya", name="ブレックスアリーナ宇都宮", lat=36.561143, lng=139.910806, region="栃木", big_box=True, official_url=_BL_URL)
BL_MATSUYAMA_COMI = Venue(key="bl_matsuyama_comi", name="松山市総合コミュニティセンター", lat=33.83585, lng=132.755154, region="愛媛", big_box=True, official_url=_BL_URL)
BL_HIROSHIMA_GREEN = Venue(key="bl_hiroshima_green", name="広島グリーンアリーナ", lat=34.399457, lng=132.455075, region="広島", big_box=True, official_url=_BL_URL)
BL_WING_KARIYA = Venue(key="bl_wing_kariya", name="ウィングアリーナ刈谷", lat=35.019371, lng=137.010336, region="愛知", big_box=True, official_url=_BL_URL)
BL_TOMONY_TOKUSHIMA = Venue(key="bl_tomony_tokushima", name="とくぎんトモニアリーナ(徳島市立体育館)", lat=34.076443, lng=134.549957, region="徳島", big_box=True, official_url=_BL_URL)
BL_SHIGETO_OKAYAMA = Venue(key="bl_shigeto_okayama", name="シゲトーアリーナ岡山", lat=34.677455, lng=133.919924, region="岡山", big_box=True, official_url=_BL_URL)
BL_OKB_GIFU = Venue(key="bl_okb_gifu", name="OKBぎふ清流アリーナ", lat=35.391322, lng=136.725615, region="岐阜", big_box=True, official_url=_BL_URL)
BL_YAMAGATA_KENSO = Venue(key="bl_yamagata_kenso", name="山形県総合運動公園", lat=38.335961, lng=140.377547, region="山形", big_box=True, official_url=_BL_URL)
BL_BIWAJIMA = Venue(key="bl_biwajima", name="名古屋市枇杷島スポーツセンター", lat=35.187863, lng=136.875091, region="愛知", big_box=True, official_url=_BL_URL)
BL_ISHIKAWA_SPORTS = Venue(key="bl_ishikawa_sports", name="いしかわ総合スポーツセンター", lat=36.579561, lng=136.598213, region="石川", big_box=True, official_url=_BL_URL)
BL_TAWARADA = Venue(key="bl_tawarada", name="俵田翁記念体育館(宇部)", lat=33.946834, lng=131.272205, region="山口", big_box=True, official_url=_BL_URL)
BL_KAGOSHIMA_KENSO = Venue(key="bl_kagoshima_kenso", name="鹿児島県総合体育センター体育館", lat=31.566708, lng=130.555024, region="鹿児島", big_box=False, official_url=_BL_URL)
BL_AGF_SUZUKA = Venue(key="bl_agf_suzuka", name="AGF鈴鹿体育館", lat=34.842809, lng=136.590933, region="三重", big_box=False, official_url=_BL_URL)
BL_KAKUHIRO_AOMORI = Venue(key="bl_kakuhiro_aomori", name="カクヒログループスーパーアリーナ(青森市総合体育館)", lat=40.838998, lng=140.841383, region="青森", big_box=False, official_url=_BL_URL)
BL_KARIYA_SHITAI = Venue(key="bl_kariya_shitai", name="刈谷市体育館", lat=34.990779, lng=136.984945, region="愛知", big_box=False, official_url=_BL_URL)
BL_KANAZAWA_SHISO = Venue(key="bl_kanazawa_shiso", name="金沢市総合体育館", lat=36.539941, lng=136.650211, region="石川", big_box=False, official_url=_BL_URL)
BL_SHIZUOKA_CHUO = Venue(key="bl_shizuoka_chuo", name="静岡市中央体育館", lat=34.981635, lng=138.385021, region="静岡", big_box=False, official_url=_BL_URL)
BL_TSUYAMA = Venue(key="bl_tsuyama", name="津山総合体育館", lat=35.068961, lng=134.008342, region="岡山", big_box=False, official_url=_BL_URL)
BL_AKIBADAI = Venue(key="bl_akibadai", name="秋葉台文化体育館(藤沢)", lat=35.390322, lng=139.445109, region="神奈川", big_box=False, official_url=_BL_URL)
BL_DEAI_DOME = Venue(key="bl_deai_dome", name="岐阜メモリアルセンター で愛ドーム", lat=35.44119, lng=136.76412, region="岐阜", big_box=False, official_url=_BL_URL)
BL_NIKKAN_TOCHIGI = Venue(key="bl_nikkan_tochigi", name="日環アリーナ栃木", lat=36.512303, lng=139.866243, region="栃木", big_box=False, official_url=_BL_URL)
BL_BUTTERFLY_TOKOROZAWA = Venue(key="bl_butterfly_tokorozawa", name="バタフライアリーナ所沢(所沢市民体育館)", lat=35.810025, lng=139.463156, region="埼玉", big_box=False, official_url=_BL_URL)
BL_JTEKT_NARA = Venue(key="bl_jtekt_nara", name="ジェイテクトアリーナ奈良", lat=34.49072, lng=135.791422, region="奈良", big_box=False, official_url=_BL_URL)
BL_HAMAMATSU_ARENA = Venue(key="bl_hamamatsu_arena", name="浜松アリーナ", lat=34.71777, lng=137.766861, region="静岡", big_box=False, official_url=_BL_URL)
BL_SUNARENA_SENDAI = Venue(key="bl_sunarena_sendai", name="サンアリーナせんだい(薩摩川内)", lat=31.851534, lng=130.302662, region="鹿児島", big_box=False, official_url=_BL_URL)
BL_YOYOGI_2 = Venue(key="bl_yoyogi_2", name="国立代々木競技場 第二体育館", lat=35.666258, lng=139.700084, region="東京", big_box=False, official_url=_BL_URL)
BL_SAMUKAWA = Venue(key="bl_samukawa", name="シンコースポーツ寒川アリーナ", lat=35.375142, lng=139.385575, region="神奈川", big_box=False, official_url=_BL_URL)
BL_FPCO_FUKUYAMA = Venue(key="bl_fpco_fukuyama", name="エフピコアリーナふくやま", lat=34.466808, lng=133.367616, region="広島", big_box=False, official_url=_BL_URL)
BL_TOGOSHI = Venue(key="bl_togoshi", name="品川区立戸越体育館", lat=35.610819, lng=139.720609, region="東京", big_box=False, official_url=_BL_URL)
BL_ASUE_OSAKA = Venue(key="bl_asue_osaka", name="Asueアリーナ大阪(大阪市中央体育館)", lat=34.65963, lng=135.44485, region="大阪", big_box=False, official_url=_BL_URL)
BL_HITACHI_IKENOKAWA = Venue(key="bl_hitachi_ikenokawa", name="日立市池の川さくらアリーナ", lat=36.576541, lng=140.647487, region="茨城", big_box=False, official_url=_BL_URL)
BL_SHIMADZU_KYOTO = Venue(key="bl_shimadzu_kyoto", name="島津アリーナ京都", lat=35.023411, lng=135.728412, region="京", big_box=False, official_url=_BL_URL)
BL_EHIME_BUDOKAN = Venue(key="bl_ehime_budokan", name="愛媛県武道館", lat=33.810824, lng=132.745601, region="愛媛", big_box=False, official_url=_BL_URL)
BL_MACHIDA_SHITAI = Venue(key="bl_machida_shitai", name="町田市立総合体育館", lat=35.536228, lng=139.479338, region="東京", big_box=False, official_url=_BL_URL)
BL_FLAT_HACHINOHE = Venue(key="bl_flat_hachinohe", name="FLAT HACHINOHE(八戸)", lat=40.511448, lng=141.427858, region="青森", big_box=False, official_url=_BL_URL)
BL_TSURUSHIN_KOMAGI = Venue(key="bl_tsurushin_komagi", name="つるしんアリーナ小真木原(鶴岡)", lat=38.713739, lng=139.81337, region="山形", big_box=False, official_url=_BL_URL)
BL_EDOGAWA = Venue(key="bl_edogawa", name="江戸川区スポーツセンター", lat=35.667908, lng=139.862524, region="東京", big_box=False, official_url=_BL_URL)
BL_TAKAYAMA_BIG = Venue(key="bl_takayama_big", name="飛騨高山ビッグアリーナ", lat=36.150291, lng=137.232704, region="岐阜", big_box=False, official_url=_BL_URL)
BL_MUTSU_MAEDA = Venue(key="bl_mutsu_maeda", name="むつマエダアリーナ", lat=41.28144, lng=141.172925, region="青森", big_box=False, official_url=_BL_URL)
BL_ICHINOSEKI_UDOME = Venue(key="bl_ichinoseki_udome", name="一関ヒロセユードーム", lat=38.940751, lng=141.155497, region="岩手", big_box=False, official_url=_BL_URL)
BL_TOMONY_NAKA = Venue(key="bl_tomony_naka", name="とくぎんトモニアリーナ那賀", lat=33.856602, lng=134.496569, region="徳島", big_box=False, official_url=_BL_URL)
BL_AIRA = Venue(key="bl_aira", name="ビーラインスポーツパーク姶良体育館", lat=31.742458, lng=130.665765, region="鹿児島", big_box=False, official_url=_BL_URL)
BL_NAKAMURA_SPORTS = Venue(key="bl_nakamura_sports", name="名古屋市中村スポーツセンター", lat=35.173269, lng=136.857827, region="愛知", big_box=False, official_url=_BL_URL)
BL_MAEDA_ARENA = Venue(key="bl_maeda_arena", name="マエダアリーナ(新青森県総合運動公園)", lat=40.841406, lng=140.843532, region="青森", big_box=False, official_url=_BL_URL)
BL_MARUGAME_SHIMIN = Venue(key="bl_marugame_shimin", name="丸亀市民体育館", lat=34.263044, lng=133.78878, region="香川", big_box=False, official_url=_BL_URL)
BL_NIIGATA_HIGASHI = Venue(key="bl_niigata_higashi", name="新潟市東総合スポーツセンター", lat=37.915179, lng=139.105058, region="新潟", big_box=False, official_url=_BL_URL)
BL_ENTRIO_TOYODA = Venue(key="bl_entrio_toyoda", name="豊田合成記念体育館エントリオ", lat=35.254536, lng=136.821667, region="愛知", big_box=False, official_url=_BL_URL)
BL_YAMAGATA_SPORTS = Venue(key="bl_yamagata_sports", name="山形市総合スポーツセンター", lat=38.28042, lng=140.347582, region="山形", big_box=False, official_url=_BL_URL)
BL_AOMORI_BUDOKAN = Venue(key="bl_aomori_budokan", name="青森県武道館", lat=40.810668, lng=140.79925, region="青森", big_box=False, official_url=_BL_URL)
BL_TSURUGA_SOGO = Venue(key="bl_tsuruga_sogo", name="敦賀市総合運動公園体育館", lat=35.642471, lng=136.032711, region="福井", big_box=False, official_url=_BL_URL)
BL_ZENTSUJI = Venue(key="bl_zentsuji", name="善通寺市民体育館", lat=34.239109, lng=133.792369, region="香川", big_box=False, official_url=_BL_URL)
BL_AISIN_ECHIZEN = Venue(key="bl_aisin_echizen", name="越前市アイシンスポーツアリーナ", lat=35.910226, lng=136.176757, region="福井", big_box=False, official_url=_BL_URL)
BL_KURUME_ARENA = Venue(key="bl_kurume_arena", name="久留米アリーナ", lat=33.32116, lng=130.530522, region="福岡", big_box=False, official_url=_BL_URL)
BL_KIKUYO = Venue(key="bl_kikuyo", name="菊陽町総合体育館", lat=32.868324, lng=130.803368, region="熊本", big_box=False, official_url=_BL_URL)
BL_HISAI = Venue(key="bl_hisai", name="津市久居体育館", lat=34.680138, lng=136.48433, region="三重", big_box=False, official_url=_BL_URL)
BL_SOKO_YOKKAICHI = Venue(key="bl_soko_yokkaichi", name="相好アリーナ四日市", lat=34.952246, lng=136.614855, region="三重", big_box=False, official_url=_BL_URL)
BL_ARAKAWA = Venue(key="bl_arakawa", name="荒川総合スポーツセンター", lat=35.735848, lng=139.791278, region="東京", big_box=False, official_url=_BL_URL)
BL_OGINO = Venue(key="bl_ogino", name="荻野運動公園体育館(厚木)", lat=35.482068, lng=139.320859, region="神奈川", big_box=False, official_url=_BL_URL)
BL_JCOM_SHIMONOSEKI = Venue(key="bl_jcom_shimonoseki", name="J:comアリーナ下関", lat=33.987888, lng=130.933555, region="山口", big_box=False, official_url=_BL_URL)
BL_CHICHIBUNOMIYA = Venue(key="bl_chichibunomiya", name="秩父宮記念体育館(藤沢)", lat=35.332375, lng=139.489009, region="神奈川", big_box=False, official_url=_BL_URL)
BL_HIROSHIMA_SUNPLAZA = Venue(key="bl_hiroshima_sunplaza", name="広島サンプラザホール", lat=34.37068, lng=132.394542, region="広島", big_box=False, official_url=_BL_URL)
BL_FUNABASHI_ARENA = Venue(key="bl_funabashi_arena", name="船橋アリーナ", lat=35.729655, lng=140.052551, region="千葉", big_box=False, official_url=_BL_URL)
BL_KITAKYUSHU_SOGO = Venue(key="bl_kitakyushu_sogo", name="北九州市立総合体育館", lat=33.87317, lng=130.841751, region="福岡", big_box=False, official_url=_BL_URL)
BL_TAKAMATSU_SOGO = Venue(key="bl_takamatsu_sogo", name="高松市総合体育館", lat=34.342031, lng=134.074029, region="香川", big_box=False, official_url=_BL_URL)

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
    WAKAYAMA_KENMIN, HAKODATE_KAIKAN,
    BL_TOYOTA_ARENA_TOKYO, BL_YOKOHAMA_BUNTAI, BL_SAGA_ARENA,
    BL_HOKKAI_KITAERU, BL_TODOROKI_ARENA, BL_LALA_ARENA,
    BL_MORIOKA_TAKAYA, BL_TACHIKAWA_TACHIHI, BL_HAPPINESS_ARENA,
    BL_OPENHOUSE_OTA, BL_NISSHIN_KYOTO, BL_WHITE_RING,
    BL_GLION_KOBE, BL_MATSUE_TAIIKUKAN, BL_CHIBA_PORT_ARENA,
    BL_YKKAP_ARENA, BL_OKINAWA_SUNTORY, BL_KOSHIGAYA,
    BL_ADASTRIA_MITO, BL_XEBIO_SENDAI, BL_CNA_AKITA,
    BL_KUMAMOTO_KENSO, BL_OTA_SOGO, BL_ROHTO_ARENA_NARA,
    BL_SHIGA_DAIHATSU, BL_OOKINI_MAISHIMA, BL_AORE_NAGAOKA,
    BL_ESFORTA_HACHIOJI, BL_URAWA_KOMABA, BL_ANABUKI_KAGAWA,
    BL_TERIHA_SEKISUI, BL_YOKOHAMA_BUDOKAN, BL_BREX_UTSUNOMIYA,
    BL_MATSUYAMA_COMI, BL_HIROSHIMA_GREEN, BL_WING_KARIYA,
    BL_TOMONY_TOKUSHIMA, BL_SHIGETO_OKAYAMA, BL_OKB_GIFU,
    BL_YAMAGATA_KENSO, BL_BIWAJIMA, BL_ISHIKAWA_SPORTS,
    BL_TAWARADA, BL_KAGOSHIMA_KENSO, BL_AGF_SUZUKA,
    BL_KAKUHIRO_AOMORI, BL_KARIYA_SHITAI, BL_KANAZAWA_SHISO,
    BL_SHIZUOKA_CHUO, BL_TSUYAMA, BL_AKIBADAI,
    BL_DEAI_DOME, BL_NIKKAN_TOCHIGI, BL_BUTTERFLY_TOKOROZAWA,
    BL_JTEKT_NARA, BL_HAMAMATSU_ARENA, BL_SUNARENA_SENDAI,
    BL_YOYOGI_2, BL_SAMUKAWA, BL_FPCO_FUKUYAMA,
    BL_TOGOSHI, BL_ASUE_OSAKA, BL_HITACHI_IKENOKAWA,
    BL_SHIMADZU_KYOTO, BL_EHIME_BUDOKAN, BL_MACHIDA_SHITAI,
    BL_FLAT_HACHINOHE, BL_TSURUSHIN_KOMAGI, BL_EDOGAWA,
    BL_TAKAYAMA_BIG, BL_MUTSU_MAEDA, BL_ICHINOSEKI_UDOME,
    BL_TOMONY_NAKA, BL_AIRA, BL_NAKAMURA_SPORTS,
    BL_MAEDA_ARENA, BL_MARUGAME_SHIMIN, BL_NIIGATA_HIGASHI,
    BL_ENTRIO_TOYODA, BL_YAMAGATA_SPORTS, BL_AOMORI_BUDOKAN,
    BL_TSURUGA_SOGO, BL_ZENTSUJI, BL_AISIN_ECHIZEN,
    BL_KURUME_ARENA, BL_KIKUYO, BL_HISAI,
    BL_SOKO_YOKKAICHI, BL_ARAKAWA, BL_OGINO,
    BL_JCOM_SHIMONOSEKI, BL_CHICHIBUNOMIYA, BL_HIROSHIMA_SUNPLAZA,
    BL_FUNABASHI_ARENA, BL_KITAKYUSHU_SOGO, BL_TAKAMATSU_SOGO,
]

# マリンメッセ系: CMS会場ID → Venue
MARINE_MESSE_VENUE_ID_MAP = {
    "rhPkRp7kYFiu7CuFjFaW": MARINE_MESSE_A,
    "1uLqpDJwQBdRWOuFnLUm": MARINE_MESSE_B,
    "M1a4HXq8jUU5bnAKafsY": FUKUOKA_CONGRESS,
    "ZxskZD69QFYho9rXNUZl": FUKUOKA_KOKUSAI_CENTER,
}
