import pandas as pd
import sys
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.config import PROCESSED_DIR

# ===============================
# 0. 경로 설정
# ===============================
INPUT_DIR = PROCESSED_DIR / "climate_clean"
OUTPUT_DIR = PROCESSED_DIR / "feature_dataset"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

years = [2023, 2024, 2025]

# ===============================
# 1. Feature 정의
# ===============================
lag_cols = [
    '평균기온(°C)',
    '평균 상대습도(%)',
    '일강수량(mm)'
]

rolling_cols = [
    '평균기온(°C)',
    '일강수량(mm)',
    '평균 상대습도(%)',
    '합계 일조시간(hr)',
    '합계 일사량(MJ/m2)',
    'confirmed_cases'
]

# ===============================
# 2. 연도별 처리
# ===============================
for year in years:
    print(f"\n===== {year}년 Feature Engineering 시작 =====")

    input_path = INPUT_DIR / f"{year}년_일별_지역별_확진자_기상매핑.csv"

    if not input_path.exists():
        print(f"[경고] 파일 없음: {input_path}")
        continue

    df = pd.read_csv(input_path, encoding="utf-8-sig")
    df['date'] = pd.to_datetime(df['date'])

    df = df.sort_values(
        by=['region', 'disease_subtitle', 'date']
    ).reset_index(drop=True)

    # ===============================
    # (A) Lag Feature
    # ===============================
    for col in lag_cols:
        df[f'{col}_lag1'] = df.groupby(['region', 'disease_subtitle'])[col].shift(1)
        df[f'{col}_lag7'] = df.groupby(['region', 'disease_subtitle'])[col].shift(7)

    # ===============================
    # (B) Rolling Feature
    # ===============================
    for col in rolling_cols:
        df[f'{col}_rollmean7'] = (
            df.groupby(['region', 'disease_subtitle'])[col]
            .transform(lambda x: x.rolling(7, min_periods=1).mean())
        )

        df[f'{col}_rollstd7'] = (
            df.groupby(['region', 'disease_subtitle'])[col]
            .transform(lambda x: x.rolling(7, min_periods=1).std())
        )

        df[f'{col}_rollmean30'] = (
            df.groupby(['region', 'disease_subtitle'])[col]
            .transform(lambda x: x.rolling(30, min_periods=1).mean())
        )

    # ===============================
    # (C) Seasonality
    # ===============================
    df['month'] = df['date'].dt.month
    df['day_of_week'] = df['date'].dt.dayofweek
    df['day_of_year'] = df['date'].dt.dayofyear
    df['week_of_year'] = df['date'].dt.isocalendar().week.astype(int)

    # ===============================
    # 결측치 처리
    # ===============================
    df = df.fillna(0)

    # ===============================
    # 저장
    # ===============================
    output_path = OUTPUT_DIR / f"{year}년도_feature_engineered.csv"
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"[완료] 저장 완료: {output_path}")
    print("전체 결측치 수:", df.isnull().sum().sum())
