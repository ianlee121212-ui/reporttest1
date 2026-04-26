import streamlit as st
import time
import json

# [필수 1] 첫 화면 설정 - 학번 및 이름
st.title('중간고사 대체 과제')
st.info('학번: 2024404088 / 이름: 이찬혁')

# [필수 2] 캐싱 기능 적용 (데이터 로딩)
@st.cache_data
def load():
    # 예제에서 배운 것처럼 지연 시간 추가
    time.sleep(2) 
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return [{"question": "데이터 파일 오류", "dap": "X"}]

# 세션 상태 초기화 (배운 내용 활용)
if 'login' not in st.sessiontest:
    st.sessiontest.login = False
if 'step' not in st.sessiontest:
    st.sessiontest.step = 0
if 'score' not in st.sessiontest:
    st.sessiontest.score = 0

# [필수 3] 로그인 기능 (입력 위젯 활용)
if not st.sessiontest.login:
    st.header('로그인 인증')
    
    col1, col2 = st.columns(2)
    with col1:
        id = st.text_input('아이디', value='user')
    with col2:
        pw = st.text_input('비밀번호', type='password', value='1234')

    if st.button('로그인 하기'):
        if id == 'user' and pw == '1234':
            st.sessiontest.login = True
            st.success('환영합니다!')
            st.rerun()
        else:
            st.error('아이디나 비밀번호가 틀렸습니다.')

# [필수 4] 퀴즈 기능
else:
    # 사이드바 로그아웃 (예제 활용)
    st.sidebar.header('메뉴')
    if st.sidebar.button('로그아웃'):
        st.sessiontest.login = False
        st.sessiontest.step = 0
        st.sessiontest.score = 0
        st.rerun()

    # 캐싱된 데이터 가져오기
    data = load()
    
    if st.sessiontest.step < len(data):
        currentquiz = data[st.sessiontest.step]
        
        st.subheader(f'문제 {st.sessiontest.step + 1}')
        st.write(f"질문: {currentquiz['question']}")
        
        # 선택 위젯
        userdap = st.radio('정답을 고르세요', ['O', 'X'], key=f'dap_{st.sessiontest.step}')
        
        if st.button('다음으로 넘어가기'):
            if userdap == currentquiz['dap']:
                st.sessiontest.score += 1
            
            st.sessiontest.step += 1
            st.rerun()
            
    else:
        # 결과 표시 (축하 효과 활용)
        st.header('퀴즈가 모두 끝났습니다!')
        st.balloons()
        
        final = st.sessiontest.score
        st.metric(label="최종 점수", value=f"{final}점", delta=f"{len(data)}문제 중")
        
        if st.button('처음부터 다시 풀기'):
            st.sessiontest.step = 0
            st.sessiontest.score = 0
            st.rerun()
