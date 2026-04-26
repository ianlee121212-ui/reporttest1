import streamlit as st
import time
import json

# [필수 1] 첫 화면: 학번 및 이름 표시
st.set_page_config(page_title="중간고사 대체 과제", layout="centered")
st.title("이찬혁의 퀴즈 앱")
st.info("학번: 2024404088 / 이름: 이찬혁")

# [필수 2] 캐싱 기능 (1개 집중 적용: JSON 파일 읽기)
@st.cache_data
def load_quiz_data():
    # 파일 읽기 지연을 시뮬레이션하기 위해 2초 대기
    time.sleep(2) 
    try:
        with open('quiz_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return [{"question": "JSON 파일이 없습니다.", "answer": "X"}]

# 세션 상태 관리
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'quiz_step' not in st.session_state:
    st.session_state.quiz_step = 0
if 'score' not in st.session_state:
    st.session_state.score = 0

# [필수 3] 로그인 기능
if not st.session_state.logged_in:
    st.header("🔐 로그인")
    user_id = st.text_input("아이디", value="user")
    user_pw = st.text_input("비밀번호", type="password", value="1234")
    
    if st.button("로그인", use_container_width=True):
        if user_id == "user" and user_pw == "1234":
            st.session_state.logged_in = True
            st.success("로그인 성공!")
            st.rerun()
        else:
            st.error("정보가 일치하지 않습니다.")

# [필수 4] 퀴즈 기능
else:
    # 캐싱된 함수 호출
    quiz_data = load_quiz_data()
    
    if st.session_state.quiz_step < len(quiz_data):
        item = quiz_data[st.session_state.quiz_step]
        
        st.subheader(f"문제 {st.session_state.quiz_step + 1}")
        st.markdown(f"### {item['question']}")
        
        ans = st.radio("정답 선택:", ["O", "X"], key=f"q_{st.session_state.quiz_step}", horizontal=True)
        
        if st.button("다음 문제"):
            if ans == item["answer"]:
                st.session_state.score += 1
            st.session_state.quiz_step += 1
            st.rerun()
            
    else:
        st.balloons()
        st.success(f"퀴즈 완료! 점수: {st.session_state.score} / {len(quiz_data)}")
        
        if st.button("다시 풀기"):
            st.session_state.quiz_step = 0
            st.session_state.score = 0
            st.rerun()

    if st.sidebar.button("로그아웃"):
        st.session_state.logged_in = False
        st.rerun()
