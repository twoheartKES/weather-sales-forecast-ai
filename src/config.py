from pathlib import Path

# 프로젝트 루트
BASE_DIR = Path(__file__).resolve().parent.parent


# 데이터 디렉토리
DATA_DIR = BASE_DIR / "data"

RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

DISEASE_WEEKLY_DIR = RAW_DIR / "disease_weekly"
CLIMATE_DIR = RAW_DIR / "climate"

DAILY_CASES_DIR = PROCESSED_DIR / "daily_cases" ## 질병데이터 일별로 전처리
CLIMATE_MAPPED_DIR = CLIMATE_DIR / "climate_mapped" ## 기상데이터와 질병 일별 전처리 병합
CLIMATE_CLEAN_DIR = PROCESSED_DIR / "climate_clean"
FEATURE_DATASET_DIR = PROCESSED_DIR / "feature_dataset"

# 자동 생성
for d in [
    DAILY_CASES_DIR,
    CLIMATE_CLEAN_DIR,
    FEATURE_DATASET_DIR
]:
    d.mkdir(parents=True, exist_ok=True)
