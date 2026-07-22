import streamlit as st
import random

# 페이지 기본 설정
st.set_page_config(page_title="스틱번호 추첨기", page_icon="🎲", layout="centered")

st.header("🎲 스틱번호 추첨")
st.write("벌칙자나 순서를 정할 때 번호를 뽑아보세요!")

start_num = st.number_input(
    "시작 번호",
    min_value=1,
    value=1,
    step=1,
    key="start"
)

end_num = st.number_input(
    "마지막 번호",
    min_value=start_num,
    value=100,
    step=1,
    key="end"
)

if st.button("😢 스틱번호 추첨하기", use_container_width=True):

    messages = [
        "😢 오늘은 당신입니다.",
        "😂 당첨(?) 축하드립니다.",
        "🥲 피할 수 없었습니다.",
        "😭 운명이 선택했습니다.",
        "💀 행운은 아니네요...",
        "🙈 모두가 지켜보고 있습니다."
    ]

    message = random.choice(messages)
    number = random.randint(start_num, end_num)

    st.markdown(f"""
<div style="
    text-align:center;
    padding:30px;
    border-radius:20px;
    border:3px solid #666666;
    background:#F3F4F6;
">
    <h3>{message}</h3>
    <h1 style="font-size: 110px; font-weight: 800; margin: 10px 0;">{number}</h1>
</div>
""", unsafe_allow_html=True)