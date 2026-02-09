import pandas as pd
import matplotlib.pyplot as plt
import os

# 폰트 설정
import platform
if platform.system() == 'Darwin':
    plt.rc('font', family='AppleGothic')
else:
    plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)

def load_ticker_data(filepath, ticker):
    """
    CSV 파일에서 특정 종목(ticker)의 데이터만 뽑아옵니다.
    """
    if not os.path.exists(filepath):
        print(f"파일 없음: {filepath}")
        return None
    
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 특정 종목 필터링
    target_df = df[df['Ticker'] == ticker].copy()
    target_df.set_index('Date', inplace=True)
    target_df.sort_index(inplace=True)
    
    print(f"{ticker} 데이터 로드 완료 ({len(target_df)} rows)")
    return target_df

def add_technical_indicators(df):
    """
    데이터프레임에 기술적 지표 컬럼을 추가합니다.
    """
    # 1. 이동평균선 (Moving Average)
    # 20일선(단기 추세), 60일선(중기 추세)
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA60'] = df['Close'].rolling(window=60).mean()

    # 2. 볼린저 밴드 (Bollinger Bands)
    # 중간선: 20일 이동평균
    # 상단선: 중간선 + (2 * 표준편차)
    # 하단선: 중간선 - (2 * 표준편차)
    std_dev = df['Close'].rolling(window=20).std()
    df['Bollinger_Upper'] = df['MA20'] + (std_dev * 2)
    df['Bollinger_Lower'] = df['MA20'] - (std_dev * 2)

    # 3. RSI (Relative Strength Index) - 14일 기준
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()

    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    return df

def plot_technical_analysis(df, ticker):
    """
    가격, 볼린저 밴드, RSI를 시각화합니다.
    """
    # 최근 1년치 데이터만 보기 (너무 길면 안 보임)
    recent_df = df.tail(250)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [3, 1]})
    
    # [위쪽 차트] 가격 + 이평선 + 볼린저 밴드
    ax1.plot(recent_df.index, recent_df['Close'], label='Close Price', color='black', alpha=0.6)
    ax1.plot(recent_df.index, recent_df['MA20'], label='MA20', color='green', linestyle='--')
    ax1.plot(recent_df.index, recent_df['MA60'], label='MA60', color='orange', linestyle='--')
    
    # 볼린저 밴드 영역 채우기
    ax1.fill_between(recent_df.index, 
                     recent_df['Bollinger_Upper'], 
                     recent_df['Bollinger_Lower'], 
                     color='gray', alpha=0.2, label='Bollinger Band')
    
    ax1.set_title(f'{ticker} Technical Analysis (Price & Bands)')
    ax1.set_ylabel('Price')
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)

    # [아래쪽 차트] RSI
    ax2.plot(recent_df.index, recent_df['RSI'], label='RSI(14)', color='purple')
    
    # RSI 과매수(70) / 과매도(30) 기준선
    ax2.axhline(70, color='red', linestyle='--', alpha=0.5)
    ax2.axhline(30, color='blue', linestyle='--', alpha=0.5)
    ax2.fill_between(recent_df.index, 70, 30, color='purple', alpha=0.1)
    
    ax2.set_title('RSI (Momentum)')
    ax2.set_ylabel('RSI Score')
    ax2.set_ylim(0, 100) # RSI는 0~100 사이
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    file_path = "data/stock_market_data.csv"
    
    # 분석할 종목 선택 (삼성전자: 005930.KS, 애플: AAPL 등)
    target_ticker = "005930.KS"  
    
    # 1. 데이터 로드
    df = load_ticker_data(file_path, target_ticker)
    
    if df is not None:
        # 2. 지표 계산
        df = add_technical_indicators(df)
        
        # 3. 결측치 제거 (이평선 계산 초반엔 NaN 생김)
        df.dropna(inplace=True)
        
        # 4. 시각화
        print(f"\n{target_ticker} 기술적 분석 차트를 그립니다...")
        plot_technical_analysis(df, target_ticker)