import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 폰트 설정
import platform
if platform.system() == 'Darwin':
    plt.rc('font', family='AppleGothic')
else:
    plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

st.set_page_config(page_title="AlphaSeeker Dashboard", page_icon="📈", layout="wide")

st.title("AlphaSeeker (알파 시커) 분석 대시보드")
st.markdown("금융 데이터 분석 및 포트폴리오 최적화 시뮬레이터")

@st.cache_data
def load_data():
    filepath = "data/stock_market_data.csv"
    if not os.path.exists(filepath):
        return None
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    if 'Ticker' in df.columns:
        df = df.pivot(index='Date', columns='Ticker', values='Close')
    return df.ffill().dropna()

df = load_data()

if df is not None:
    st.sidebar.header("분석 설정")
    tickers = df.columns.tolist()
    
    selected_tickers = st.sidebar.multiselect(
        "비교할 종목을 선택하세요 (최소 2개):", 
        tickers, 
        default=["AAPL", "005930.KS", "^GSPC"] if len(tickers) >= 3 else tickers
    )

    if len(selected_tickers) >= 2:
        # 🌟 핵심: 화면을 2개의 탭으로 나눕니다!
        tab1, tab2 = st.tabs(["탐색적 분석 (EDA)", "포트폴리오 최적화"])

        # ---------------------------------------------------------
        # 탭 1: 탐색적 데이터 분석 (어제 만든 내용)
        # ---------------------------------------------------------
        with tab1:
            st.subheader("주가 흐름 비교")
            st.line_chart(df[selected_tickers])

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("종목 간 상관관계")
                daily_returns = df[selected_tickers].pct_change().dropna()
                fig, ax = plt.subplots(figsize=(6, 5))
                sns.heatmap(daily_returns.corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
                st.pyplot(fig)
                
            with col2:
                st.subheader("최근 10일 데이터")
                st.dataframe(df[selected_tickers].tail(10), use_container_width=True)

        # ---------------------------------------------------------
        # 탭 2: 포트폴리오 최적화 (Day 5 내용 이식)
        # ---------------------------------------------------------
        with tab2:
            st.subheader("몬테카를로 시뮬레이션 기반 자산 배분")
            st.write("선택한 종목들로 최적의 투자 비중(Efficient Frontier)을 계산합니다.")
            
            # 사용자가 시뮬레이션 횟수를 직접 고를 수 있게 바(Slider) 추가
            num_simulations = st.slider("시뮬레이션 횟수 (많을수록 정교함)", min_value=1000, max_value=20000, value=5000, step=1000)
            
            # 실행 버튼 추가
            if st.button("최적화 실행하기"):
                # 로딩 스피너 표시
                with st.spinner('수만 번의 포트폴리오를 계산 중입니다... 잠시만 기다려주세요!'):
                    daily_returns = df[selected_tickers].pct_change().dropna()
                    mean_returns = daily_returns.mean()
                    cov_matrix = daily_returns.cov()
                    num_assets = len(selected_tickers)
                    risk_free_rate = 0.035
                    
                    results = np.zeros((3, num_simulations))
                    weights_record = []
                    
                    for i in range(num_simulations):
                        weights = np.random.random(num_assets)
                        weights /= np.sum(weights)
                        weights_record.append(weights)
                        
                        portfolio_return = np.sum(weights * mean_returns) * 252
                        portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
                        
                        results[0,i] = portfolio_return
                        results[1,i] = portfolio_std_dev
                        results[2,i] = (portfolio_return - risk_free_rate) / portfolio_std_dev
                    
                    results_df = pd.DataFrame(results.T, columns=['Return', 'Volatility', 'Sharpe'])
                    max_sharpe_idx = results_df['Sharpe'].idxmax()
                    max_sharpe_weights = weights_record[max_sharpe_idx]
                    
                    # 결과 시각화
                    fig2, ax2 = plt.subplots(figsize=(10, 6))
                    scatter = ax2.scatter(results_df['Volatility'], results_df['Return'], c=results_df['Sharpe'], cmap='viridis', alpha=0.5, s=10)
                    plt.colorbar(scatter, label='Sharpe Ratio')
                    
                    # 빨간 별 (최고의 포트폴리오)
                    ax2.scatter(results_df.iloc[max_sharpe_idx]['Volatility'], results_df.iloc[max_sharpe_idx]['Return'], marker='*', color='red', s=300, label='Max Sharpe')
                    
                    ax2.set_title('Efficient Frontier (효율적 투자선)')
                    ax2.set_xlabel('Risk (Volatility)')
                    ax2.set_ylabel('Expected Return')
                    ax2.legend()
                    st.pyplot(fig2)
                    
                    # 🌟 최종 최적 비중 출력 (시각적으로 예쁘게)
                    st.success("최적화가 완료되었습니다! (빨간 별 위치의 비중입니다)")
                    st.subheader("최적의 투자 비중 (Max Sharpe Ratio)")
                    
                    # 스트림릿의 컬럼 기능을 활용해 결과를 예쁘게 나열
                    cols = st.columns(num_assets)
                    for idx, col in enumerate(cols):
                        ticker_name = selected_tickers[idx]
                        weight_percent = max_sharpe_weights[idx] * 100
                        col.metric(label=ticker_name, value=f"{weight_percent:.1f} %")

    else:
        st.warning("포트폴리오 최적화를 위해 사이드바에서 **최소 2개 이상의 종목**을 선택해주세요.")
else:
    st.error("데이터 파일이 없습니다. `src/data_loader.py`를 먼저 실행해주세요.")