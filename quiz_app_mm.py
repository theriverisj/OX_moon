import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="물권법 중간고사",
    page_icon="❓",
    layout="centered"
)

# 비밀번호 설정
PASSWORD = "ajou18"

# 인증 상태 초기화
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# 로그인 화면
if not st.session_state.authenticated:

    st.title("🔐 퀴즈 접속")

    password = st.text_input("비밀번호를 입력하세요", type="password")

    if st.button("입장"):
        if password == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("비밀번호가 틀렸습니다.")

    st.stop()

st.title("📱 문물권 OX")

# 엑셀 불러오기
df = pd.read_excel("mid_term.xlsx", header=None)
df = df.iloc[1:].reset_index(drop=True)

num_col = 0
question_col = 1
answer_col = 2
explain_col = 3


# 퀴즈 초기화 함수
def reset_quiz():
    st.session_state.questions = df.sample(frac=1).reset_index(drop=True)
    st.session_state.index = 0
    st.session_state.answered = False
    st.session_state.correct = None
    st.session_state.quiz_end = False


# 최초 실행 시 초기화
if "questions" not in st.session_state:
    reset_quiz()

questions = st.session_state.questions
index = st.session_state.index
total = len(questions)


# 종료 화면
if st.session_state.quiz_end:

    st.warning("퀴즈를 종료했습니다.")

    if st.button("다시 시작", use_container_width=True):
        reset_quiz()
        st.rerun()


# 문제 다 풀었을 때
elif index >= total:

    st.success("퀴즈 끝!")
    st.write("모든 문제를 풀었습니다.")

    if st.button("다시 시작", use_container_width=True):
        reset_quiz()
        st.rerun()


# 문제 진행
else:

    # 진행률
    progress = index / total
    st.progress(progress)

    st.write(f"문제 {index+1} / {total}")

    # 종료 버튼
    if st.button("🛑 퀴즈 종료", use_container_width=True):
        st.session_state.quiz_end = True
        st.rerun()

    row = questions.iloc[index]

    question = row[question_col]
    answer = str(row[answer_col]).strip().upper()
    explanation = str(row[explain_col])

    st.markdown(
        f"<p style='font-size:20px; font-weight:600; text-align:left;'>{question}</p>",
        unsafe_allow_html=True
    )

    # 아직 답 안 했을 때
    if not st.session_state.answered:

        col1, col2 = st.columns(2)

        if col1.button("⭕", use_container_width=True):
            user = "O"
        elif col2.button("❌", use_container_width=True):
            user = "X"
        else:
            user = None

        if user:

            st.session_state.answered = True

            if user == answer:
                st.session_state.correct = True
            else:
                st.session_state.correct = False

            st.rerun()

    # 답한 후 결과 표시
    else:

        if st.session_state.correct:
            st.success("정답입니다!")
        else:
            st.error(f"오답입니다! 정답: {answer}")

        st.info(f"💡 해설: {explanation}")

        if st.button("다음 문제", use_container_width=True):

            st.session_state.index += 1
            st.session_state.answered = False
            st.session_state.correct = None

            st.rerun()
