import pandas as pd
import sys
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.config import DAILY_CASES_DIR, CLIMATE_DIR, CLIMATE_CLEAN_DIR
import os

# ===============================
# 1. 경로 설정
# ===============================
disease_dir = DAILY_CASES_DIR
weather_dir = CLIMATE_DIR 
## 병합
output_dir  = CLIMATE_CLEAN_DIR
print("_________________________기상", weather_dir)
os.makedirs(output_dir, exist_ok=True)

# ===============================
# 2. 날짜 범위 정의
# ===============================
date_ranges = {
    2023: {'start_date': '2023-01-01', 'end_date': '2023-12-30'},
    2024: {'start_date': '2023-12-31', 'end_date': '2024-12-28'},
    2025: {'start_date': '2024-12-29', 'end_date': '2025-12-06'},
}

# ===============================
# 3. 지역 → 기상 관측 지점 매핑
# ===============================
mapping_regions = {
    '동두천': [
        '경기_구리시_082','경기_부천시_오정구_088','경기_과천시_079','경기_부천시_130',
        '경기_광명시_080','경기_부천시_소사구_087','경기_고양시_덕양구_076',
        '경기_의정부시_112','경기_고양시_일산동구_077','경기_고양시_일산서구_078',
        '경기_하남시_117','경기_남양주시_085','경기_김포시_084','경기_양주시_103',
        '경기_파주시_114','경기_동두천시_086',
    ],
    '수원': [
        '경기_수원시_팔달구_096','경기_수원시_장안구_095','경기_수원시_권선구_093',
        '경기_화성시_118','경기_수원시_영통구_094','경기_군포시_083',
        '경기_용인시_기흥구_108','경기_의왕시_111','경기_성남시_수정구_091',
        '경기_안산시_단원구_098','경기_성남시_중원구_092','경기_오산시_107',
        '경기_안산시_상록구_099','경기_안양시_동안구_101','경기_용인시_수지구_109',
        '경기_시흥시_097','경기_안양시_만안구_102','경기_성남시_분당구_090',
        '경기_용인시_처인구_110','경기_평택시_115',
    ],
    '양평': ['경기_양평군_104','경기_광주시_081','경기_가평군_075'],
    '이천': ['경기_이천시_113','경기_여주시_105','경기_안성시_100'],
    '파주': ['경기_포천시_116','경기_연천군_106'],
    '서울': ['서울_010'],
}

region_to_station = {
    region: station
    for station, regions in mapping_regions.items()
    for region in regions
}

# ===============================
# 4. 연도별 처리
# ===============================
for year in [2023, 2024, 2025]:

    print(f"\n===== {year}년 처리 시작 =====")

    # ---------------------------
    # 4-1. 기상 데이터 로드
    # ---------------------------
    from pathlib import Path

    weather_path = CLIMATE_DIR / f"OBS_ASOS_DD_{year}.csv"


    df_weather = pd.read_csv(weather_path, encoding='cp949')
    df_weather['일시'] = pd.to_datetime(df_weather['일시'])

    # ---------------------------
    # 4-2. 질병 데이터 로드 (일별)
    # ---------------------------
    disease_path = disease_dir / f"{year}년_일별_지역별_확진자.csv"
    ##disease_path = f"{disease_dir}{year}년_일별_지역별_확진자.csv"

    df_disease = pd.read_csv(disease_path, encoding='utf-8-sig')
    df_disease['date'] = pd.to_datetime(df_disease['date'])

    print("질병컬럼",df_disease.columns)
    print("기상컬럼",df_weather.columns)

    assert df_disease['confirmed_cases'].isna().sum() == 0


    df_disease['date'] = pd.to_datetime(df_disease['date'])

    # ---------------------------
    # 4-3. 날짜 범위 필터링
    # ---------------------------
    dr = date_ranges[year]
    df_disease = df_disease[
        (df_disease['date'] >= dr['start_date']) &
        (df_disease['date'] <= dr['end_date'])
    ]

    # ---------------------------
    # 4-4. 지역 → 관측지점 매핑
    # ---------------------------
    df_disease['지점명'] = df_disease['region'].map(region_to_station)
    df_disease = df_disease.dropna(subset=['지점명'])

    # =====================================================
    # 4-5. ★ 핵심 로직 ★
    #      일별 질병 × 일별 기상 데이터 병합
    # =====================================================
    df_merged = pd.merge(
        df_disease,
        df_weather,
        left_on=['date', '지점명'],
        right_on=['일시', '지점명'],
        how='inner'
    )

    # ---------------------------
    # 4-6. 정렬
    # ---------------------------
    df_merged = df_merged.sort_values(
        by=['date', 'region', 'disease_subtitle']
    )

    # ---------------------------
    # 4-7. 저장
    # ---------------------------
    output_path = os.path.join(
        output_dir,
        f"{year}년_일별_지역별_확진자_기상매핑.csv"
    )

    df_merged.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"[완료] 저장 완료: {output_path}")
