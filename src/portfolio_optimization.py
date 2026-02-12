import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 폰트 설정
import platform
if platform.system() == 'Darwin':
    plt.rc('font', family='AppleGothic')
else:
    plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

def load_data(filepath):
    """데이터 로드 및 Wide Format 변환"""
    if not os.path.exists(filepath):
        print("데이터 파일이 없습니다.")
        return None
    
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Wide Format (날짜 x 종목) 변환
    if 'Ticker' in df.columns:
        df = df.pivot(index='Date', columns='Ticker', values='Close')
    
    # 결측치 제거
    df = df.ffill().dropna()
    return df

def run_monte_carlo_simulation(df, num_simulations=10000):
    """
    몬테카를로 시뮬레이션:
    수만 번의 랜덤 비중 조합을 테스트하여 최적의 포트폴리오를 찾습니다.
    """
    # 일별 수익률
    daily_returns = df.pct_change().dropna()
    
    # 연간 기대 수익률 및 공분산 (252일 = 1년 개장일)
    mean_daily_returns = daily_returns.mean()
    cov_matrix = daily_returns.cov()
    
    # 결과 저장할 리스트
    results = np.zeros((3, num_simulations)) # [수익률, 변동성, 샤프지수]
    weights_record = [] # 비중 저장
    
    tickers = df.columns
    num_assets = len(tickers)
    risk_free_rate = 0.035 # 무위험 이자율 (예: 미국 국채 3.5%)

    print(f"{num_simulations}번의 시뮬레이션을 돌리는 중... (잠시만 기다려주세요)")

    for i in range(num_simulations):
        # 1. 랜덤 비중 생성 (합이 1이 되도록)
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        weights_record.append(weights)
        
        # 2. 포트폴리오 기대 수익률 (연간)
        # 공식: 비중 * 평균수익률 * 252
        portfolio_return = np.sum(weights * mean_daily_returns) * 252
        
        # 3. 포트폴리오 변동성 (Risk)
        # 공식: sqrt(비중.T * 공분산 * 비중) * sqrt(252)
        portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
        
        # 4. 샤프 지수 (Sharpe Ratio)
        # 공식: (수익률 - 무위험이자율) / 변동성
        results[0,i] = portfolio_return
        results[1,i] = portfolio_std_dev
        results[2,i] = (portfolio_return - risk_free_rate) / portfolio_std_dev

    return results, weights_record

def plot_efficient_frontier(results, weights_record, tickers):
    """
    효율적 투자선 시각화
    """
    results_frame = pd.DataFrame(results.T, columns=['Return', 'Volatility', 'Sharpe'])
    
    # 1. 샤프 지수가 가장 높은 포트폴리오 (최고의 선택)
    max_sharpe_idx = results_frame['Sharpe'].idxmax()
    max_sharpe_port = results_frame.iloc[max_sharpe_idx]
    max_sharpe_weights = weights_record[max_sharpe_idx]
    
    # 2. 변동성이 가장 낮은 포트폴리오 (제일 안전한 선택)
    min_vol_idx = results_frame['Volatility'].idxmin()
    min_vol_port = results_frame.iloc[min_vol_idx]
    min_vol_weights = weights_record[min_vol_idx]

    print("\n[최고의 포트폴리오 (Max Sharpe)]")
    print(f"   - 기대 수익률: {max_sharpe_port['Return']*100:.2f}%")
    print(f"   - 리스크(변동성): {max_sharpe_port['Volatility']*100:.2f}%")
    print(f"   - 샤프 지수: {max_sharpe_port['Sharpe']:.2f}")
    print("   - 최적 비중:")
    for ticker, weight in zip(tickers, max_sharpe_weights):
        print(f"     {ticker}: {weight*100:.2f}%")

    print("\n[가장 안전한 포트폴리오 (Min Volatility)]")
    print(f"   - 리스크(변동성): {min_vol_port['Volatility']*100:.2f}%")
    
    # 시각화
    plt.figure(figsize=(12, 8))
    
    # 산점도 (모든 시뮬레이션 결과)
    plt.scatter(results_frame.Volatility, results_frame.Return, c=results_frame.Sharpe, cmap='viridis', alpha=0.5, s=10)
    plt.colorbar(label='Sharpe Ratio')
    
    # Max Sharpe (빨간 별)
    plt.scatter(max_sharpe_port['Volatility'], max_sharpe_port['Return'], marker='*', color='red', s=300, label='Max Sharpe (Best)')
    
    # Min Volatility (파란 별)
    plt.scatter(min_vol_port['Volatility'], min_vol_port['Return'], marker='*', color='blue', s=300, label='Min Volatility (Safe)')

    plt.title('Efficient Frontier (Portfolio Optimization)')
    plt.xlabel('Risk (Volatility)')
    plt.ylabel('Expected Annual Return')
    plt.legend(labelspacing=1.2)
    plt.grid(True, alpha=0.3)
    plt.show()

if __name__ == "__main__":
    file_path = "data/stock_market_data.csv"
    
    # 1. 데이터 로드
    df = load_data(file_path)
    
    if df is not None:
        tickers = df.columns
        print(f"분석 대상 종목: {list(tickers)}")
        
        # 2. 시뮬레이션 실행 (10,000번)
        results, weights = run_monte_carlo_simulation(df, num_simulations=10000)
        
        # 3. 결과 분석 및 시각화
        plot_efficient_frontier(results, weights, tickers)