import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 한글 폰트 및 마이너스 기호 깨짐 방지 설정
import platform
if platform.system() == 'Darwin':
    plt.rc('font', family='AppleGothic')
else:
    plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

# 웹 페이지 전체 설정 (제목, 화면 넓게 쓰기)
st.set_page_config(page_title="알파 시커 대시보드", page_icon="📈", layout="wide")

st.title("알파 시커 (AlphaSeeker) 분석 대시보드")
st.markdown("금융 데이터 분석 및 시각화 결과를 한눈에 확인하세요.")

# 1. 데이터 불러오기 함수 (캐시를 사용해 매번 새로 읽지 않도록 속도 향상)
@st.cache_data
def load_data():
    filepath = "data/stock_market_data.csv"
    if not os.path.exists(filepath):
        return None
    
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 데이터를 분석하기 좋게 변환 (날짜를 행으로, 종목을 열로)
    if 'Ticker' in df.columns:
        df = df.pivot(index='Date', columns='Ticker', values='Close')
        
    # 빈 값(결측치) 처리
    return df.ffill().dropna()

df = load_data()

# 데이터가 잘 불러와졌을 경우에만 화면에 표시
if df is not None:
    # 2. 왼쪽 사이드바 (설정 메뉴)
    st.sidebar.header("분석 설정")
    tickers = df.columns.tolist()
    
    # 사용자가 직접 보고 싶은 종목을 선택할 수 있게 만듦
    selected_tickers = st.sidebar.multiselect(
        "비교할 종목을 선택하세요:", 
        tickers, 
        default=tickers[:3] # 기본으로 처음 3개 선택
    )

    if selected_tickers:
        # 3. 주가 흐름 차트 (스트림릿 기본 제공 차트 사용)
        st.subheader("주가 흐름 비교")
        st.line_chart(df[selected_tickers])

        # 화면을 반으로 나누기
        col1, col2 = st.columns(2)

        with col1:
            # 4. 상관관계 히트맵
            st.subheader("종목 간 상관관계")
            # 일별 수익률 계산
            daily_returns = df[selected_tickers].pct_change().dropna()
            
            fig, ax = plt.subplots(figsize=(6, 5))
            sns.heatmap(daily_returns.corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
            # 스트림릿에 만든 그림표를 넘겨줌
            st.pyplot(fig)
            
        with col2:
            # 5. 실제 데이터 표
            st.subheader("최근 데이터 확인")
            # 가장 최근 10일 치 데이터만 표 형태로 보여줌
            st.dataframe(df[selected_tickers].tail(10), use_container_width=True)

else:
    # 데이터가 없을 경우 에러 메시지 띄우기
    st.error("데이터 파일이 없습니다. 먼저 데이터 수집 파이썬 파일을 실행해주세요.")