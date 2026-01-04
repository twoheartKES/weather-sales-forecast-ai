질병–기상 기반 일별 확진자 예측 AI 모델
(Disease–Climate Daily Prediction Model)

1. 프로젝트 개요

본 프로젝트는 질병 발생 데이터와 기상 데이터를 결합하여,
지역별·질병별 일별 확진자 수를 예측하는 AI 모델을 구축하는 것을 목표로 합니다.

예측 단위: 일별

예측 대상: 지역 × 질병별 확진자 수

모델 목적: 평균 오차(MAE) ±1~2명 수준의 정량적 예측

사용 모델: XGBoost Regressor

본 프로젝트는 단순한 모델 학습이 아니라,
데이터 전처리 → 특징 생성 → 모델 학습 → 평가 → 후처리까지
전 과정을 재현 가능하게 구성한 데이터 파이프라인 기반 AI 프로젝트입니다.

2. 전체 파이프라인 개요

<그림 1> 전체 데이터 처리 및 모델링 흐름

```
주간 질병 데이터
        ↓
[Step 1] 일별 확진자 변환
        ↓
기상 원시 데이터
        ↓
[Step 2] 기상 데이터 정제
        ↓
[Step 3] 질병–기상 Feature 생성
        ↓
 모델 학습 / 예측 / 평가

```

3. 디렉터리 구조 설명
```
kdbs_dis/
│
├── data/
│ ├── raw/                # 원본 데이터 (수정 금지)
│ │ ├── disease_weekly/   # 주간 질병 발생 데이터
│ │ └── climate/          # 기상 원시 데이터
│ │
│ ├── processed/          # 전처리 결과 데이터
│ │ ├── daily_cases/      # 주간 → 일별 변환 결과
│ │ ├── climate_clean/    # 정제된 기상 데이터
│ │ ├── climate_mapped/   # daily_cases폴더안안의 일별 변환 결과와 기상 climate 폴더 원시 데이터
│ │ └── feature_dataset/ # 모델 입력용 최종 데이터셋
│ │
│ └── README.md           # 데이터 설명 문서
│
├── src/
│ ├── config.py           # 전역 설정 (경로, 공통 변수)
│ │
│ ├── step1_weekly_to_daily.py     # Step 1: 주간 → 일별 변환
│ ├── step2_climate_cleaning.py    # Step 2: 기상 데이터 정제
│ ├── step3_feature_engineering.py # Step 3: Feature 생성
│ │
│ └── kes/                # ★ 예측 모델 전용 패키지
│     ├── __init__.py
│     ├── dataset.py            # 데이터 로딩 및 분할
│     ├── target_transform.py   # 타겟 변환 (log1p 등)
│     ├── model_xgb.py          # XGBoost 모델 정의
│     ├── train.py              # 모델 학습
│     ├── evaluate.py           # 성능 평가 (MAE 중심)
│     └── postprocess.py        # 예측값 후처리
│
├── requirements.txt      # Python 의존성 목록
└── run_all.py            # 전체 파이프라인 실행 스크립트

```
   
