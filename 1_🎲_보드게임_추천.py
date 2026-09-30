import streamlit as st
import random
import os
from PIL import Image
from datetime import date

# --- [1] 방문객 수 불러오기 ---
today = str(date.today())

try:
    with open("count.txt", "r", encoding="utf-8") as f:
        saved_date, saved_count = f.read().split(",")
except:
    saved_date = today
    saved_count = "0"

# 날짜가 바뀌면 자동 초기화
if saved_date != today:
    visitor_count = 0
else:
    visitor_count = int(saved_count)

# 현재 정보 저장
with open("count.txt", "w", encoding="utf-8") as f:
    f.write(f"{today},{visitor_count}")

st.markdown("<div id='top'></div>", unsafe_allow_html=True) # 맨 위로 스크롤용 기준점
st.markdown("<br>", unsafe_allow_html=True)

# --- [2] 웹페이지 기본 설정 및 앵커 심기 ---
st.set_page_config(page_title="팝콘에듀 보드게임 추천", page_icon="🎲", layout="centered")

# 🎨 [개선] 상단 타이틀을 화려한 전광판 스타일 배너로 변경
col1, col2 = st.columns([5.2,0.8])

with col1:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg,#FF4B4B,#FF7676);
        padding:18px;
        border-radius:20px;
        color:white;
        height:110px;
        display:flex;
        flex-direction:column;
        justify-content:center;
    ">
        <h1 style="margin:0;">🎲 팝콘에듀 추천 보드게임</h1>
        <p style="margin-top:8px;">
        원하는 인원과 장르를 선택해보세요!
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
        text-align:center;
        margin-top:6px;
    ">
        <div style="
            background:#FEE500;
            color:#3C1E1E;
            padding:3px 6px;
            border-radius:15px;
            font-size:11px;
            font-weight:bold;
            display:inline-block;
            white-space:nowrap;
        ">
            팝콘에듀 카카오톡
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.image("images/popcornqr.png", width=90)


# 📊 [개선] 방문객 카운터를 입구 전광판 느낌의 독립적인 디자인 박스로 분리
col_count1, col_count2 = st.columns([2, 1])
with col_count1:
    st.markdown(f"""
    <div style="background-color: #F8FAFC; padding: 12px; border-radius: 12px; text-align: center; border: 1px solid #E2E8F0; height: 65px; display: flex; flex-direction: column; justify-content: center;">
        <span style="color: #64748B; font-size: 13px; font-weight: bold; display: block; margin-bottom: 2px;">🎪 오늘 함께한 팝업스토어 모험가</span>
        <span style="color: #FF4B4B; font-size: 22px; font-weight: 800; display: block;">{visitor_count} 명째 방문 중!</span>
    </div>
    """, unsafe_allow_html=True)

with col_count2:
    # 박스 높이(65px)에 맞춰 균형을 잡은 방문 인증 버튼
    if st.button("🙋 방문객 등록 버튼", use_container_width=True):
        visitor_count += 1
        with open("count.txt", "w", encoding="utf-8") as f:
            f.write(f"{today},{visitor_count}")
        st.rerun()


# --- [3] 보드게임 데이터베이스 데이터 정의 ---
games_data = [
    # (가250, 세300) 개별 편집 적용
    {"name": "바운스 잇!", "genre": ["파티"], "players": ["2명", "3명", "4명", "5명 이상"], "display_players": "2~6명", "time": "15분", "image": "images/bounceit.png", "location": "41,000 > 30% > 28,700"},
    {"name": "슈퍼스시", "genre": ["파티", "순발력", "패밀리"], "players": ["3명", "4명", "5명 이상"], "display_players": "2~6명", "time": "20분", "image": "images/supersushi.jpg", "location": "41,500 > 40% > 24,900"},
    {"name": "포실리스", "genre": ["전략"], "players": ["2명", "3명", "4명", "5명 이상"], "display_players": "2~5명", "time": "45분", "image": "images/fossilis.png", "location": "66,000 > 30% > 46,200"},
    {"name": "더마인드", "genre": ["협력"], "players": ["2명", "3명", "4명"], "display_players": "2~4명", "time": "20분", "image": "images/themind.png", "img_size": (200, 240), "location": "22,000 > 40% > 13,200"},
    {"name": "스위스 사는 스미스씨", "genre": ["패밀리", "파티"], "players": ["2명", "3명", "4명", "5명 이상"], "display_players": "2~6명", "time": "15분", "image": "images/swiss.png", "img_size": (220, 260), "location": "17,000 > 40% > 10,200"},
    {"name": "나홀로 아홀로틀", "genre": ["패밀리", "파티"], "players": ["2명", "3명", "4명", "5명 이상"], "display_players": "2~6명", "time": "15분", "image": "images/Axolotl.png", "img_size": (220, 260), "location": "17,000 > 40% > 10,200"},
    {"name": "바이킹 시소", "genre": ["패밀리", "덱스터리티"], "players": ["2명", "3명", "4명"], "display_players": "2~4명", "time": "10분", "image": "images/vikingseesaw.png", "img_size": (130, 300), "location": "36,000 > 30% > 25,200"},
    {"name": "초밥 마스터", "genre": ["전략"], "players": ["2명", "3명", "4명"], "display_players": "1~4명", "time": "30분", "image": "images/sushimaster.png", "location": "70,000 > 30% > 49,000"},
    {"name": "타코 캣 고트 치즈 피자", "genre": ["파티", '패밀리'], "players": ["2명", "3명", "4명", "5명 이상"], "display_players": "2~8명", "time": "15분", "image": "images/tacocat.png", "img_size": (370, 430), "location": "22,000 > 40% > 13,200"},
    {"name": "블루 샌드 씨사이드", "genre": ["파티", "패밀리"], "players": ["2명", "3명", "4명", "5명 이상"], "display_players": "2~5명", "time": "20분", "image": "images/bluesandsea.png", "img_size": (190, 300), "location": "42,000 > 30% > 29,400"},
    {"name": "촵촵 다이스", "genre": ["전략", "퍼즐"], "players": ["2명", "3명", "4명"], "display_players": "1~4명", "time": "30분", "image": "images/chopchop.png", "img_size": (220, 300), "location": "31,000 > 40% > 18,600"},
    {"name": "차가운 그녀가 눈을 뜨기 전에", "genre": ["머더 미스터리", "추리"], "players": ["3명", "4명", "5명 이상"], "display_players": "3~6명", "time": "10분", "image": "images/sheiscold.png", "location": "24,000 > 30% > 16,800"},
    {"name": "스틱스택", "genre": ["파티", "덱스터리티"], "players": ["2명", "3명", "4명", "5명 이상"], "display_players": "2~10명", "time": "10분", "image": "images/stickstack.png", "img_size": (190, 300), "location": "36,000 > 40% > 21,600"},
    {"name": "크라클 오라클", "genre": ["파티", "추리"], "players": ["2명", "3명", "4명", "5명 이상"], "display_players": "2~8명", "time": "30분", "image": "images/krkork.png", "location": "39,000 > 32% > 26,520"},
    {"name": "펭귄파티", "genre": ["전략", "패밀리"], "players": ["2명", "3명", "4명", "5명 이상"], "display_players": "2~6명", "time": "30분", "image": "images/penguinparty.png", "img_size": (250, 280), "location": "17,000 > 40% > 10,200"},
    {"name": "놉!놉!테이블", "genre": ["파티", "패밀리", "순발력"], "players": ["3명", "4명", "5명 이상"], "display_players": "3~8명", "time": "15분", "image": "images/nono.png", "location": "24,000 > 40% > 14,400"},
    {"name": "궁신", "genre": ["전략", "블러핑"], "players": ["2명", "3명", "4명", "5명 이상"], "display_players": "2~5명", "time": "20분", "image": "images/courtisans.png", "img_size": (160, 300), "location": "40,000 > 40% > 24,000"},
    {"name": "유비보", "genre": ["협력", "패밀리", "덱스터리티"], "players": ["2명", "3명", "4명", "5명 이상"], "display_players": "2~8명", "time": "10분", "image": "images/yubibo.png", "img_size": (170, 300), "location": "34,800 > 30% > 24,360"},
    {"name": "버거와썹", "genre": ["파티", "순발력"], "players": ["2명", "3명", "4명", "5명 이상"], "display_players": "2~5명", "time": "15분", "image": "images/burger.png", "location": "18,000 > 40% > 10,800"},
    {"name": "네코지마 고양이 전봇대", "genre": ["덱스터리티", "패밀리"], "players": ["2명", "3명", "4명", "5명 이상"], "display_players": "1~5명", "time": "15분", "image": "images/nekojima.png", "location": "59,000 > 40% > 35,400"},
    {"name": "셀레스티아 빅박스", "genre": ["파티", "패밀리", "푸시 유어 럭"], "players": ["2명", "3명", "4명", "5명 이상"], "display_players": "2~6명", "time": "30분", "image": "images/celestia.png", "location": "75,000 > 30% > 52,500"},
    {"name": "고양이vs오이", "genre": ["파티", "패밀리", "푸시 유어 럭"], "players": ["2명", "3명", "4명", "5명 이상"], "display_players": "2~6명", "time": "30분", "image": "images/catvs.png", "img_size": (180, 300), "location": "32,000 > 40% > 19,200"},
    {"name": "캘리코", "genre": ["퍼즐", "패밀리", "전략"], "players": ["2명", "3명", "4명"], "display_players": "1~4명", "time": "30~45분", "image": "images/calico.png", "location": "48,000 > 40% > 28,800"},
    {"name": "육식동물짓이야!", "genre": ["추리", "패밀리", "블러핑"], "players": ["2명", "3명", "4명", "5명 이상"], "display_players": "1~5명", "time": "10분", "image": "images/a carnivore did it.png", "img_size": (200, 300), "location": "33,000 > 30% > 23,100"},
    {"name": "쿵쿵쿵 코끼리 해적단", "genre": ["덱스터리티", "패밀리", "파티"], "players": ["2명", "3명", "4명"], "display_players": "2~4명", "time": "15분", "image": "images/stompstompstomp.png", "img_size": (220, 300), "location": "46,000 > 40% > 27,600"},
    {"name": "방방 날아라 돼지!", "genre": ["덱스터리티", "패밀리", "파티"], "players": ["2명", "3명"], "display_players": "2~3명", "time": "10~20분", "image": "images/bangbangpig.png", "location": "36,000 > 40% > 21,600"},
    {"name": "트리올렛", "genre": ["퍼즐", "패밀리", "전략"], "players": ["2명", "3명", "4명"], "display_players": "2~4명", "time": "30분", "image": "images/triolet.png", "img_size": (250, 260), "location": "48,000 > 30% > 33,600"},
    {"name": "3초 트라이", "genre": ["파티", "패밀리", "순발력"], "players": ["2명", "3명", "4명", "5명 이상"], "display_players": "2~7명", "time": "10분", "image": "images/3second try.png", "img_size": (130, 300), "location": "33,000 > 40% > 19,800"},
    {"name": "원더볼링", "genre": ["패밀리", "덱스터리티"], "players": ["2명", "3명", "4명", "5명 이상"], "display_players": "2~6명", "time": "15분", "image": "images/bowling.png", "img_size": (130, 300), "location": "30,000 > 40% > 18,000"},
    {"name": "토마토마토", "genre": ["패밀리", "파티", "순발력"], "players": ["3명", "4명", "5명 이상"], "display_players": "3~6명", "time": "20분", "image": "images/tomatomato.png", "img_size": (190, 280), "location": "27,000 > 25% > 20,250"},
    {"name": "본파이어 파티", "genre": ["파티", "패밀리", "전략"], "players": ["2명", "3명", "4명"], "display_players": "2~4명", "time": "5분", "image": "images/fire.png", "img_size": (130, 300), "location": "30,000 > 30% > 21,000"},
    {"name": "스카우트", "genre": ["패밀리", "전략"], "players": ["2명", "3명", "4명", "5명 이상"], "display_players": "2~5명", "time": "20분", "image": "images/scout.png", "img_size": (190, 280), "location": "33,000 > 25% > 24,750"},
    {"name": "나인타일패닉", "genre": ["퍼즐", "패밀리", "순발력"], "players": ["2명", "3명", "4명", "5명 이상"], "display_players": "2~5명", "time": "20분", "image": "images/ninetilespanic.png", "location": "47,000 > 25% > 35,250"},
    {"name": "해저탐험 DEEP SEA", "genre": ["푸시 유어 럭", "패밀리", "전략"], "players": ["2명", "3명", "4명", "5명 이상"], "display_players": "2~6명", "time": "30분", "image": "images/deepsea.png", "img_size": (190, 280), "location": "27,000 > 25% > 20,250"},
    {"name": "가짜 예술가 뉴욕에 가다", "genre": ["블러핑", "파티", "추리"], "players": ["5명 이상"], "display_players": "5~10명", "time": "20분", "image": "images/newyork.png", "img_size": (190, 280), "location": "27,000 > 25% > 20,250"},
    {"name": "인사이더 레드", "genre": ["블러핑", "파티", "추리"], "players": ["4명", "5명 이상"], "display_players": "4~8명", "time": "15분", "image": "images/insiderred.png", "img_size": (190, 280), "location": "27,000 > 25% > 20,250"},
    {"name": "덤불속", "genre": ["패밀리", "파티", "추리"], "players": ["2명", "3명", "4명", "5명 이상"], "display_players": "2~5명", "time": "20분", "image": "images/inthebush.png", "img_size": (190, 280), "location": "38,400 > 25% > 28,800"},
    {"name": "스탁파일 본판", "genre": ["전략", "블러핑", "추리"], "players": ["2명", "3명", "4명", "5명 이상"], "display_players": "2~5명", "time": "45분", "image": "images/stock.jpg", "location": "77,000 > 30% > 53,900"},
]

# --- [4] 안정적인 오리지널 게임 카드 출력 함수 ---
def display_game_card(game, is_lucky=False):
    with st.container():
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if os.path.exists(game["image"]):
                img_path = game["image"]
            else:
                img_path = "images/popcorngames.png"
                st.caption(f"⚠️ '{game['name']}' 이미지 준비중")
            
            try:
                img = Image.open(img_path)
                target_size = game.get("img_size", (250, 300))
                img_resized = img.resize(target_size)
    
# 💡 [1] 가운데 정렬을 시작하는 상자 열기
                st.markdown("<div style='display: flex; justify-content: center; align-items: center;'>", unsafe_allow_html=True)
    
# 💡 [2] 이미지 출력 (use_container_width=False 필수!)
                st.image(img_resized, use_container_width=False)
    
# 💡 [3] 상자 닫기
                st.markdown("</div>", unsafe_allow_html=True)

            except Exception:
                st.error("이미지를 불러올 수 없습니다.")
            
        with col2:
            title_emoji = "🏆" if is_lucky else "🎲"
            st.subheader(f"{title_emoji} {game['name']}")
            
            # 요구하셨던 깔끔한 세로 정렬 줄바꿈 출력
            st.write(f"🏷️ **장르** : {', '.join(game['genre'])}")
            st.write(f"⏱️ **시간** : {game['time']}")
            st.write(f"👥 **인원** : {game['display_players']}")

            # 📍 위치 정보 출력 (가시성을 위해 붉은색 강조 추가)
            location_info = game.get("location", "매장 문의")
            st.write(f"📍 **가격** : :red[{location_info}]")

        st.markdown("")

# --- [5] 게임 검색 기능 ---
st.markdown("### 🔍 게임 검색")
search = st.text_input("검색하고 싶은 게임 이름을 입력하세요.", placeholder="예: 슈퍼스시, 바운스 잇!")

if search:
    found_any = False
    st.markdown(f"**'{search}'** 검색 결과입니다.")
    for game in games_data:
        if search.lower() in game["name"].lower():
            found_any = True
            display_game_card(game)
    if not found_any:
        st.warning(f"😢 '{search}'와(과) 일치하는 게임을 찾지 못했습니다. 다른 이름으로 검색해 보세요!")
else:
    st.info("💡 위의 검색창에 게임 이름을 입력하시면 상세 정보를 바로 확인할 수 있습니다!")

st.markdown("---")

# --- [6] 사용자 조건 선택 및 세션 초기화 ---
if "recommend_mode" not in st.session_state:
    st.session_state.recommend_mode = None
if "recommended_list" not in st.session_state:
    st.session_state.recommended_list = []

def clear_recommendation():
    st.session_state.recommend_mode = None
    st.session_state.recommended_list = []

players = st.selectbox("몇 명이 플레이하나요?", ["전체", "2명", "3명", "4명", "5명 이상"], on_change=clear_recommendation)
genre = st.selectbox("좋아하는 장르는?", ["전체", "파티", "전략", "협력", "패밀리", "추리", "퍼즐", "블러핑", "머더 미스터리", "덱스터리티", "순발력", "푸시 유어 럭"], on_change=clear_recommendation)

# 조건에 맞는 게임 미리 필터링
filtered_games = []
for game in games_data:
    match_players = (players == "전체") or (players in game["players"])
    match_genre = (genre == "전체") or (genre in game["genre"])
    if match_players and match_genre:
        filtered_games.append(game)

# --- [7] 버튼 클릭 이벤트 처리 ---
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button("🔥 조건에 맞는 게임 추천받기", use_container_width=True):
        if filtered_games:
            st.session_state.recommend_mode = "normal"
            st.session_state.recommended_list = filtered_games
        else:
            st.session_state.recommend_mode = "empty"
            st.session_state.recommended_list = []

with col_btn2:
    if st.button("🎲 결정이 힘들다면? 랜덤 추천!", use_container_width=True):
        if filtered_games:
            st.balloons() 
            st.session_state.recommend_mode = "lucky"
            st.session_state.recommended_list = [random.choice(filtered_games)]
        else:
            st.session_state.recommend_mode = "empty"
            st.session_state.recommended_list = []

# 💡 [새로 추가된 기능] 추천 결과만 깔끔하게 지워주는 초기화 버튼
if st.button("🔄 추천 결과 초기화 (비우기)", use_container_width=True):
    clear_recommendation()
    st.rerun()

# --- [8] 진짜 화면 고정 출력부 ---
if st.session_state.recommend_mode == "normal":
    st.info(f"🎯 [{players} / {genre}] 조건에 맞는 추천 게임입니다!")
    for game in st.session_state.recommended_list:
        display_game_card(game)

elif st.session_state.recommend_mode == "lucky":
    st.markdown("### 🔮 오늘의 운명적인 추천 게임은 바로!")
    for game in st.session_state.recommended_list:
        display_game_card(game, is_lucky=True)

elif st.session_state.recommend_mode == "empty":
    st.warning("😢 아쉽게도 해당 조건에 맞는 게임이 없습니다. 다른 조건을 선택해 주세요!")

# --- [9] 🔝 화면 최상단으로 이동하는 링크 버튼 ---
st.markdown("---")
st.markdown(
    """
    <a href="#top" target="_self" style="text-decoration: none;">
        <button style="
            width: 100%;
            background-color: #FF4B4B;
            color: white;
            border: none;
            padding: 12px 0px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
        ">
            🔝 맨 위로 올라가기
        </button>
    </a>
    """,
    unsafe_allow_html=True
)