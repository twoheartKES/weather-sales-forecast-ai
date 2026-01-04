import pandas as pd
import sys
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.config import DISEASE_WEEKLY_DIR, DAILY_CASES_DIR

# ===============================
# 0. 기본 설정
# ===============================
years = [2023, 2024, 2025]

regions = [
    '경기_가평군_075','경기_고양시_덕양구_076','경기_고양시_일산동구_077',
    '경기_고양시_일산서구_078','경기_과천시_079','경기_광명시_080',
    '경기_광주시_081','경기_구리시_082','경기_군포시_083','경기_김포시_084',
    '경기_남양주시_085','경기_동두천시_086','경기_부천시_130',
    '경기_부천시_소사구_087','경기_부천시_오정구_088',
    '경기_성남시_분당구_090','경기_성남시_수정구_091','경기_성남시_중원구_092',
    '경기_수원시_권선구_093','경기_수원시_영통구_094',
    '경기_수원시_장안구_095','경기_수원시_팔달구_096',
    '경기_시흥시_097','경기_안산시_단원구_098','경기_안산시_상록구_099',
    '경기_안성시_100','경기_안양시_동안구_101','경기_안양시_만안구_102',
    '경기_양주시_103','경기_양평군_104','경기_여주시_105',
    '경기_연천군_106','경기_오산시_107',
    '경기_용인시_기흥구_108','경기_용인시_수지구_109','경기_용인시_처인구_110',
    '경기_의왕시_111','경기_의정부시_112','경기_이천시_113',
    '경기_파주시_114','경기_평택시_115','경기_포천시_116',
    '경기_하남시_117','경기_화성시_118','서울_010'
]

date_ranges = {
    2023: {'start_date': '2023-01-01', 'end_date': '2023-12-30'},
    2024: {'start_date': '2023-12-31', 'end_date': '2024-12-28'},
    2025: {'start_date': '2024-12-29', 'end_date': '2025-12-06'}
}

# ===============================
# 1. 연도별 처리
# ===============================
for year in years:
    print(f"\n===== {year}년 처리 시작 =====")
    yearly_records = []

    for region in regions:
        input_path = (
            DISEASE_WEEKLY_DIR
            / str(year)
            / f"kdca_{year}_week_{region}.csv"
        )

        if not input_path.exists():
            print(f"[경고] 파일 없음: {input_path}")
            continue

        df = pd.read_csv(input_path, encoding='utf-8-sig')

        year_start = pd.to_datetime(f"{year}-01-01")
        first_sunday = year_start + pd.Timedelta(days=(6 - year_start.weekday()) % 7)

        week_columns = [
            col for col in df.columns
            if col.startswith('COLUMN') and col != 'COLUMN1'
        ]

        for _, row in df.iterrows():
            disease = row['SUBTITLE']

            for week_idx, week_col in enumerate(week_columns):
                weekly_cases = row[week_col]
                if pd.isna(weekly_cases):
                    weekly_cases = 0

                daily_cases = weekly_cases / 7
                week_start = first_sunday + pd.Timedelta(days=week_idx * 7)

                for d in range(7):
                    yearly_records.append({
                        'date': week_start + pd.Timedelta(days=d),
                        'region': region,
                        'disease_subtitle': disease,
                        'confirmed_cases': daily_cases
                    })

    df_year = pd.DataFrame(yearly_records)

    dr = date_ranges[year]
    df_year = df_year[
        (df_year['date'] >= dr['start_date']) &
        (df_year['date'] <= dr['end_date'])
    ]

    df_year = df_year.sort_values(
        ['date', 'region', 'disease_subtitle']
    ).reset_index(drop=True)

    output_path = DAILY_CASES_DIR / f"{year}년_일별_지역별_확진자.csv"

    df_year.to_csv(
        output_path,
        index=False,
        encoding='utf-8-sig'
    )

    print(f"[완료] 저장 완료: {output_path}")
