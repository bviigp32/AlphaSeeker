import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 폰트 설정 (Mac/Windows 호환)
import platform
if platform.system() == 'Darwin':
    plt.rc('font', family='AppleGothic')
else:
    plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

def load_data(filepath):
    """
    CSV 파일을 로드하고 'Wide Format'으로 변환합니다.
    """
    if not os.path.exists(filepath):
        print(f"데이터 파일이 없습니다: {filepath}")
        return None
    
    # 1. 일단 평범하게 읽어옵니다.
    df = pd.read_csv(filepath)
    
    # 2. 날짜 컬럼을 datetime 형식으로 변환
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
    
    # 3. 데이터 구조 확인 및 변환 (Pivot)
    # 만약 'Ticker' 컬럼이 존재한다면 -> Long Format이므로 Wide Format으로 변환해야 함
    if 'Ticker' in df.columns and 'Close' in df.columns:
        print("데이터를 분석용 형태(Wide Format)로 변환 중...")
        # 행: 날짜, 열: 종목명, 값: 종가(Close)
        df = df.pivot(columns='Ticker', values='Close')
    
    print("데이터 로드 및 변환 완료")
    print(f"포함된 종목: {list(df.columns)}")
    return df

def preprocess_data(df):
    """
    결측치(NaN) 처리
    """
    print("\n결측치(NaN) 확인 (전처리 전):")
    print(df.isnull().sum())
    
    # 주식 데이터의 결측치는 '직전 거래일 데이터'로 채움 (Forward Fill)
    df = df.ffill()
    
    # 맨 앞부분 결측치는 제거
    df = df.dropna()
    
    return df

def plot_price_trend(df, ticker1, ticker2):
    """
    두 종목의 가격 비교 (이중축)
    """
    # 컬럼이 있는지 확인
    if ticker1 not in df.columns or ticker2 not in df.columns:
        print(f"경고: {ticker1} 또는 {ticker2} 가 데이터에 없습니다.")
        return

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # 왼쪽 축
    color = 'tab:blue'
    ax1.set_xlabel('Date')
    ax1.set_ylabel(f'{ticker1} Price', color=color)
    ax1.plot(df.index, df[ticker1], color=color, label=ticker1)
    ax1.tick_params(axis='y', labelcolor=color)

    # 오른쪽 축
    ax2 = ax1.twinx()  
    color = 'tab:red'
    ax2.set_ylabel(f'{ticker2} Price', color=color)
    ax2.plot(df.index, df[ticker2], color=color, label=ticker2)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title(f'Price Comparison: {ticker1} vs {ticker2}')
    fig.tight_layout()
    plt.show()

def plot_correlation(df):
    """
    상관관계 히트맵
    """
    # 일별 수익률로 변환
    daily_returns = df.pct_change().dropna()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(daily_returns.corr(), annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    plt.title('Stock Correlation Matrix (Daily Returns)')
    plt.show()

if __name__ == "__main__":
    file_path = "data/stock_market_data.csv"
    
    # 1. 데이터 로드
    raw_df = load_data(file_path)
    
    if raw_df is not None:
        # 2. 전처리
        clean_df = preprocess_data(raw_df)
        
        # 3. 시각화
        print("\n가격 비교 차트 생성...")
        plot_price_trend(clean_df, '005930.KS', '^GSPC')
        
        print("\n상관관계 히트맵 생성...")
        plot_correlation(clean_df)