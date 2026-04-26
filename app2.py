import streamlit as st
import time
import json
import pandas as pd

# [필수 1] 첫 화면 및 페이지 설정
st.set_page_config(page_title="2024404088 이찬혁 과제", page_icon="🎓", layout="centered")

# 사이드바에 학번/이름 상시 표시 (평가 기준 충족)
st.sidebar.title("👨‍💻 제출자 정보")
st.sidebar.info("학번: 2024404088\n\n이름: 이찬혁")

# [필수 2] 캐싱 기능 (JSON 데이터 로드)
# 예제에서 배운 ttl과 show_spinner 매개변수를 활용하여 완성도를 높였습니다.
@st.cache_data(ttl=600, show_spinner="퀴즈 데이터를 불러오는 중...")
def load_quiz_data():
    time.sleep(1.5)  # 캐싱 효과 시연을 위한 의도적 지연
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # 파일이 없을 경우를 대비한 기본 데이터
        return [
            {"question": "Streamlit은 파이썬만으로 웹 서비스를 만들 수 있다.", "answer": "O"},
            {"question": "st.cache_data는 모델 연결과 같은 리소스 저장에 적합하다.", "answer": "X"}
        ]

# --- 세션 상태 관리 (지우지 마세요!) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'quiz_step' not in st.session_state:
    st.session_state.quiz_step = 0
if 'score' not in st.session_state:
    st.session_state.score = 0

# [필수 3] 로그인 기능
if not st.session_state.logged_in:
    st.title("🔐 서비스 로그인")
    st.write("본 서비스를 이용하시려면 로그인이 필요합니다.")
    
    with st.container(border=True):
        user_id = st.text_input("아이디", placeholder="user 입력")
        user_pw = st.text_input("비밀번호", type="password", placeholder="1234 입력")
        
        if st.button("로그인하기", use_container_width=True):
            if user_id == "user" and user_pw == "1234":
                st.session_state.logged_in = True
                st.success("로그인에 성공했습니다!")
                st.rerun()
            else:
                st.error("아이디 또는 비밀번호가 올바르지 않습니다.")

# [필수 4] 퀴즈 기능
else:
    st.title("🧠 상식 퀴즈 챌린지")
    
    # 캐싱된 데이터 호출
    quiz_data = load_quiz_data()
    
    # 상단 진행바 (예제에서 배운 시각적 요소 추가)
    progress = (st.session_state.quiz_step) / len(quiz_data)
    st.progress(progress)

    if st.session_state.quiz_step < len(quiz_data):
        item = quiz_data[st.session_state.quiz_step]
        
        st.subheader(f"문제 {st.session_state.quiz_step + 1}")
        
        # 퀴즈 카드 형태 구성
        with st.container(border=True):
            st.markdown(f"### {item['question']}")
            ans = st.radio("정답을 선택해주세요:", ["O", "X"], 
                           key=f"q_{st.session_state.quiz_step}", horizontal=True)
            
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("제출 및 다음"):
                    if ans == item["answer"]:
                        st.session_state.score += 1
                    st.session_state.quiz_step += 1
                    st.rerun()
    
    else:
        # 최종 결과 화면
        st.balloons()
        st.header("🎊 퀴즈 결과")
        
        final_score = st.session_state.score
        total_q = len(quiz_data)
        
        col1, col2 = st.columns(2)
        col1.metric("맞힌 개수", f"{final_score}개")
        col2.metric("최종 점수", f"{(final_score/total_q)*100:.0f}점")
        
        if st.button("다시 도전하기", type="primary"):
            st.session_state.quiz_step = 0
            st.session_state.score = 0
            st.rerun()

    # 사이드바 하단 로그아웃 버튼
    if st.sidebar.button("로그아웃"):
        st.session_state.logged_in = False
        st.session_state.quiz_step = 0
        st.session_state.score = 0
        st.rerun()
