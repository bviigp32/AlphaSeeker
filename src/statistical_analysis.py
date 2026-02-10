import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

# 폰트 설정
import platform
if platform.system() == 'Darwin':
    plt.rc('font', family='AppleGothic')
else:
    plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

def load_and_prep_data(filepath):
    """데이터 로드 및 수익률 변환"""
    if not os.path.exists(filepath):
        print("데이터 파일이 없습니다.")
        return None
    
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Wide Format으로 변환 (날짜 x 종목)
    if 'Ticker' in df.columns:
        df = df.pivot(index='Date', columns='Ticker', values='Close')
    
    # 결측치 제거
    df = df.ffill().dropna()
    
    # ⭐️ 핵심: 가격(Price) -> 일별 수익률(Daily Returns)로 변환
    # 로그 수익률을 쓰기도 하지만, 여기선 이해하기 쉬운 퍼센트 수익률 사용
    returns = df.pct_change().dropna()
    
    return returns

def calculate_beta(returns_df, market_ticker, stock_ticker):
    """
    선형 회귀를 통해 Beta와 Alpha를 계산
    """
    # 두 종목의 데이터만 추출
    if market_ticker not in returns_df.columns or stock_ticker not in returns_df.columns:
        print(f"데이터 부족: {stock_ticker} 또는 {market_ticker}")
        return None

    x = returns_df[market_ticker] # 시장 (독립변수)
    y = returns_df[stock_ticker]  # 개별 종목 (종속변수)

    # 선형 회귀 분석 (Linear Regression)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    
    beta = slope       # 기울기 = 베타
    alpha = intercept  # 절편 = 알파
    
    return beta, alpha, r_value**2

def plot_beta_scatter(returns_df, market_ticker, stock_ticker, beta, alpha):
    """
    산점도와 회귀선 시각화
    """
    x = returns_df[market_ticker]
    y = returns_df[stock_ticker]

    plt.figure(figsize=(10, 6))
    
    # 1. 산점도 (Scatter Plot)
    sns.scatterplot(x=x, y=y, alpha=0.5, label='Daily Returns')
    
    # 2. 회귀선 (Regression Line)
    # y = beta * x + alpha
    regression_line = beta * x + alpha
    plt.plot(x, regression_line, color='red', linewidth=2, label=f'Regression Line (β={beta:.2f})')

    plt.title(f'Beta Analysis: {stock_ticker} vs {market_ticker}')
    plt.xlabel(f'{market_ticker} Daily Return')
    plt.ylabel(f'{stock_ticker} Daily Return')
    plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
    plt.axvline(0, color='black', linestyle='--', linewidth=0.8)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

if __name__ == "__main__":
    file_path = "data/stock_market_data.csv"
    
    # 벤치마크 지수 (시장 기준)
    market_ticker = "^GSPC" # S&P 500
    
    # 분석할 종목들
    target_tickers = ["AAPL", "005930.KS", "MSFT"]
    
    # 1. 데이터 로드
    returns_df = load_and_prep_data(file_path)
    
    if returns_df is not None:
        print(f"벤치마크 지수: {market_ticker}\n")
        
        for ticker in target_tickers:
            if ticker == market_ticker: continue # 자기 자신은 제외
            
            # 2. 베타 계산
            result = calculate_beta(returns_df, market_ticker, ticker)
            
            if result:
                beta, alpha, r_squared = result
                print(f"[{ticker}] 분석 결과")
                print(f"   - Beta (민감도)  : {beta:.4f}")
                print(f"   - Alpha (초과수익): {alpha:.6f}")
                print(f"   - R-squared (설명력): {r_squared:.4f}")
                
                # 해석 출력
                if beta > 1.2: print("공격형 자산 (High Risk, High Return)")
                elif beta < 0.8: print("방어형 자산 (Low Risk)")
                else: print("시장 추종형 자산")
                print("-" * 30)

                # 3. 시각화 (하나씩 팝업 뜸)
                plot_beta_scatter(returns_df, market_ticker, ticker, beta, alpha)