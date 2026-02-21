# AlphaSeeker: Financial Data Analysis & Portfolio Optimization

> **"Beating the Market with Data Science"**
> 시장 수익률(Beta)을 초과하는 나만의 알파(Alpha)를 찾기 위한 **금융 데이터 분석 및 포트폴리오 최적화 프로젝트**입니다.
> Python을 활용해 KOSPI/NASDAQ 주요 종목의 기술적 지표를 분석하고, 상관관계 분석 및 Efficient Frontier 시뮬레이션을 통해 최적의 투자 비중을 제안하는 인터랙티브 웹 대시보드를 구축했습니다.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python) ![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas) ![NumPy](https://img.shields.io/badge/NumPy-Computation-013243?logo=numpy) ![Scipy](https://img.shields.io/badge/Scipy-Statistics-8CAAE6?logo=scipy) ![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit)

## 프로젝트 개요 (Overview)
* **목표:** 주식 시장 데이터(OHLCV)를 수집하여 통계적 기법으로 분석하고, 리스크 대비 수익률을 극대화하는 포트폴리오 구성안을 웹 서비스 형태로 도출.
* **기간:** 2026.02.07 ~ 2026.02.21 (프로젝트 완료)
* **역할:** 데이터 수집 파이프라인 구축, EDA, 통계 분석, UI/UX 대시보드 개발 (1인 프로젝트)

## 주요 기능 (Key Features)
1.  **데이터 파이프라인 (Data Pipeline):**
    * `yfinance` API를 활용한 글로벌 주식 데이터 자동 수집 및 수정 종가(Adjusted Close) 기준 정제.
2.  **탐색적 & 기술적 분석 (EDA & Technical Analysis):**
    * 이중축 차트(Dual Axis)를 활용한 지수 비교 및 일별 수익률 기반 상관관계 히트맵(Correlation Heatmap) 시각화.
    * 이동평균선(MA), RSI(14), 볼린저 밴드(Bollinger Bands) 등 모멘텀/변동성 지표 산출.
3.  **통계적 분석 (Statistical Analysis):**
    * `scipy.stats` 선형 회귀(Linear Regression)를 통해 벤치마크 대비 시장 민감도(Beta)와 초과 수익률(Alpha) 산출.
4.  **인터랙티브 대시보드 & 포트폴리오 최적화 (Web Dashboard & Optimization):**
    * **Streamlit 기반 UI:** 사용자가 직접 비교 종목과 시뮬레이션 횟수를 설정할 수 있는 웹 환경 제공.
    * **Monte Carlo Simulation:** 수만 번의 동적 시뮬레이션을 통해 효율적 투자선(Efficient Frontier) 도출.
    * **Max Sharpe Ratio:** 무위험 이자율 대비 리스크를 최소화하고 수익을 극대화하는 최적의 자산 배분 비중(%) 자동 계산 및 시각화.

## 개발 로그 (Development Log)
* **Day 1: 데이터 파이프라인 구축** (`src/data_loader.py`) - `yfinance` 연동 및 데이터 수집
* **Day 2: EDA & 데이터 전처리** (`src/eda.py`) - 결측치 처리 및 상관관계 시각화
* **Day 3: 기술적 지표 분석** (`src/technical_analysis.py`) - MA, RSI, 볼린저 밴드 구현
* **Day 4: 통계적 분석** (`src/statistical_analysis.py`) - Beta/Alpha 산출
* **Day 5: 포트폴리오 최적화** (`src/portfolio_optimization.py`) - 몬테카를로 시뮬레이션
* **Day 6: 대시보드 프로토타입** (`app.py`) - Streamlit 기본 레이아웃 및 차트 연동
* **Day 7: 통합 웹 서비스 완성** (`app.py`) - 탭(Tab) 기반 UI 구성 및 동적 포트폴리오 최적화 시뮬레이터 연동 완료 🎉

## 기술 스택 (Tech Stack)
| Category | Technology | Usage |
| :--- | :--- | :--- |
| **Language** | Python 3.11 | 데이터 분석 및 로직 구현 |
| **Data** | yfinance | 주가 데이터(OHLCV) 수집 API |
| **Analysis** | Pandas, NumPy | 시계열 데이터 처리, 행렬 연산, 시뮬레이션 |
| **Stats** | Scikit-learn, Scipy | 선형 회귀(Beta), 최적화(Optimization) |
| **Visualization** | Matplotlib, Seaborn | 정적 차트 및 히트맵, 효율적 투자선 시각화 |
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

# 4. 알파 시커 대시보드 실행 🚀
streamlit run app.py

```

---

*Created by [Kim Kyunghun]*
