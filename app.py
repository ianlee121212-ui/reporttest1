
import streamlit as st
import time

# [필수 1] 첫 화면: 학번 및 이름 표시
st.set_page_config(page_title="중간고사 대체 과제", layout="centered")
st.title("🎓 Streamlit 퀴즈 애플리케이션")
st.info("학번: 202412345 / 이름: 홍길동")

# [필수 2] 캐싱 기능 구현
# 퀴즈 데이터를 불러오거나 무거운 계산을 할 때 사용합니다.
@st.cache_data
def load_quiz_data():
    # 실제로는 외부 JSON/CSV를 읽어오는 로직을 넣으면 좋습니다.
    time.sleep(2)  # 캐싱 효과를 확인하기 위한 의도적 지연
    return [
        {"q": "Python의 Streamlit은 웹 개발 프레임워크이다.", "a": "O"},
        {"q": "Streamlit에서 캐싱을 위해 사용하는 데코레이터는 @st.cache_data 이다.", "a": "O"},
        {"q": "Streamlit 앱은 반드시 서버에 배포해야만 작동한다.", "a": "X"}
    ]

# 세션 상태 초기화 (로그인 및 퀴즈 상태 관리)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'quiz_step' not in st.session_state:
    st.session_state.quiz_step = 0
if 'score' not in st.session_state:
    st.session_state.score = 0

# [필수 3] 로그인 기능
if not st.session_state.logged_in:
    st.header("🔐 로그인")
    user_id = st.text_input("아이디 (힌트: user)")
    user_pw = st.text_input("비밀번호 (힌트: 1234)", type="password")
    
    if st.button("로그인"):
        if user_id == "user" and user_pw == "1234":
            st.session_state.logged_in = True
            st.success("로그인 성공!")
            st.rerun()
        else:
            st.error("아이디 또는 비밀번호가 틀렸습니다.")

# [필수 4] 퀴즈 기능 (로그인 후 접근 가능)
else:
    st.sidebar.button("로그아웃", on_click=lambda: st.session_state.update({"logged_in": False}))
    
    st.header("📝 퀴즈 타임!")
    quiz_data = load_quiz_data() # 캐싱된 함수 호출
    
    if st.session_state.quiz_step < len(quiz_data):
        item = quiz_data[st.session_state.quiz_step]
        st.subheader(f"문제 {st.session_state.quiz_step + 1}")
        st.write(item["q"])
        
        answer = st.radio("정답을 선택하세요", ["O", "X"], key=f"q_{st.session_state.quiz_step}")
        
        if st.button("다음 문제"):
            if answer == item["a"]:
                st.session_state.score += 1
            st.session_state.quiz_step += 1
            st.rerun()
            
    else:
        # 결과 화면
        st.balloons()
        st.success(f"퀴즈 완료! 당신의 점수는 {st.session_state.score} / {len(quiz_data)} 입니다.")
        if st.button("다시 풀기"):
            st.session_state.quiz_step = 0
            st.session_state.score = 0
            st.rerun()
