# AlphaSeeker: Financial Data Analysis & Portfolio Optimization

> **"Beating the Market with Data Science"**
> 시장 수익률(Beta)을 초과하는 나만의 알파(Alpha)를 찾기 위한 **금융 데이터 분석 및 포트폴리오 최적화 프로젝트**입니다.
> Python을 활용해 KOSPI/NASDAQ 주요 종목의 기술적 지표를 분석하고, 상관관계 분석 및 Efficient Frontier 시뮬레이션을 통해 최적의 투자 비중을 제안합니다.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python) ![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas) ![Scipy](https://img.shields.io/badge/Scipy-Statistics-8CAAE6?logo=scipy) ![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit)

## 프로젝트 개요 (Overview)
* **목표:** 주식 시장 데이터(OHLCV)를 수집하여 통계적 기법으로 분석하고, 리스크 대비 수익률을 극대화하는 포트폴리오 구성안 도출.
* **기간:** 2026.02.07 ~ (진행 중)
* **역할:** 데이터 수집, 전처리, 통계 분석, 시각화 대시보드 개발 (1인 프로젝트)

## 주요 기능 (Key Features)
1.  **데이터 파이프라인 (Data Pipeline):**
    * `yfinance` API를 활용한 글로벌 주식 데이터(Yahoo Finance) 자동 수집.
    * 수정 종가(Adjusted Close) 기준의 데이터 정제 및 결측치 처리 (Forward Fill).
2.  **기술적 분석 (Technical Analysis):**
    * **Trend:** 이동평균선(MA20, MA60)을 통한 골든크로스/데드크로스 포착.
    * **Momentum:** RSI(14) 지표를 활용한 과매수/과매도 구간 탐지.
    * **Volatility:** 볼린저 밴드(Bollinger Bands)를 활용한 변동성 돌파 전략 분석.
3.  **통계적 분석 (Statistical Analysis):**
    * **상관관계 분석 (Correlation Heatmap):** 자산 간의 움직임 유사도 측정 (분산 투자 효과 검증).
    * **Beta(β) & Alpha(α):** 선형 회귀(Linear Regression)를 통해 시장 민감도(Risk)와 초과 수익률(Return) 산출.
4.  **포트폴리오 최적화 (Optimization):**
    * **Monte Carlo Simulation:** 수만 번의 시뮬레이션을 통해 **효율적 투자선(Efficient Frontier)** 도출. *(Day 5 예정)*
    * **Sharpe Ratio:** 무위험 이자율 대비 초과 수익률이 가장 높은 최적 비중 산출. *(Day 5 예정)*

## 개발 로그 (Development Log)
* **Day 1: 데이터 파이프라인 구축** (`src/data_loader.py`)
    * `yfinance`를 활용한 다중 종목(AAPL, MSFT, ^GSPC 등) 데이터 수집 및 전처리 자동화.
* **Day 2: EDA & 데이터 전처리** (`src/eda.py`)
    * 결측치(NaN) 처리 및 이중축 차트(Dual Axis)를 활용한 국가별 지수 비교.
    * 일별 수익률(Daily Return) 기반의 상관관계 히트맵(Heatmap) 시각화.
* **Day 3: 기술적 지표 분석** (`src/technical_analysis.py`)
    * Pandas `rolling` 함수를 활용한 MA, RSI, Bollinger Bands 수식 구현 및 시각화.
* **Day 4: 통계적 분석 (Beta/Alpha)** (`src/statistical_analysis.py`)
    * `scipy.stats` 선형 회귀(Linear Regression)를 활용하여 개별 종목의 Beta 계수 산출.
    * 산점도(Scatter Plot)와 회귀선을 통한 시장 민감도 시각화.
* **Day 5:** 포트폴리오 최적화 (Efficient Frontier) *(Coming Soon)*
* **Day 6:** 대시보드 구축 (Streamlit) *(Coming Soon)*
* **Day 7:** 최종 리포팅 및 배포 *(Coming Soon)*

## 기술 스택 (Tech Stack)
| Category | Technology | Usage |
| :--- | :--- | :--- |
| **Language** | Python 3.11 | 데이터 분석 및 로직 구현 |
| **Data** | **yfinance** | 주가 데이터(OHLCV) 수집 API |
| **Analysis** | **Pandas, NumPy** | 시계열 데이터 처리 및 수치 연산 |
| **Stats** | **Scikit-learn, Scipy** | 선형 회귀(Beta), 최적화(Optimization) |
| **Visualization** | Matplotlib, Seaborn | 정적 차트 및 히트맵 시각화 |
| **Dashboard** | Streamlit | 인터랙티브 웹 대시보드 구현 |

## 실행 방법 (How to Run)
```bash
# 1. 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\activate

# 2. 필수 라이브러리 설치
pip install -r requirements.txt

# 3. 데이터 수집 (최초 1회)
python src/data_loader.py

# 4. 분석 스크립트 실행
python src/eda.py                 # 탐색적 데이터 분석 (상관관계)
python src/technical_analysis.py  # 기술적 지표 (RSI, 볼린저밴드)
python src/statistical_analysis.py # 통계 분석 (베타, 알파)

```

---

*Created by [Kim Kyunghun]*
