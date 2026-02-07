import yfinance as yf
import pandas as pd
import os
from datetime import datetime

# 데이터 저장할 폴더 생성
if not os.path.exists("data"):
    os.makedirs("data")

def download_stock_data(tickers, start_date, end_date):
    """
    yfinance를 이용해 주가 데이터를 다운로드하고 저장하는 함수
    """
    print(f"데이터 수집 시작: {tickers}")
    print(f"기간: {start_date} ~ {end_date}")

    # yfinance로 데이터 다운로드
    # auto_adjust=True: 수정 종가(Adj Close)를 자동으로 반영해줌 
    data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True)
    
    # 데이터가 잘 받아졌는지 확인 (Multi-index 처리)
    if len(tickers) > 1:
        # 여러 종목일 경우 종목 코드가 컬럼 레벨에 생기므로 정리
        data = data.stack(level=1).rename_axis(['Date', 'Ticker']).reset_index(level=1)

    return data

if __name__ == "__main__":
    # 1. 분석할 종목 리스트 (포트폴리오 구성용)
    # AAPL(애플), MSFT(마이크로소프트), ^GSPC(S&P500 지수 - 시장 기준), 005930.KS(삼성전자)
    my_tickers = ["AAPL", "MSFT", "GOOGL", "^GSPC", "005930.KS"]
    
    # 2. 기간 설정 (최근 5년)
    start = "2019-01-01"
    end = datetime.today().strftime('%Y-%m-%d')

    # 3. 데이터 다운로드
    df = download_stock_data(my_tickers, start, end)

    # 4. 데이터 확인 (EDA 기초)
    print("\n데이터 미리보기:")
    print(df.head())
    
    print("\n데이터 정보:")
    print(df.info())

    # 5. 파일로 저장 (CSV)
    file_path = "data/stock_market_data.csv"
    df.to_csv(file_path)
    print(f"\n데이터 저장 완료: {file_path}")