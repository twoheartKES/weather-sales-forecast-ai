import subprocess

steps = [
    "src/step1_weekly_to_daily.py",
    "src/step2_climate_cleaning.py",
    "src/step3_feature_engineering.py"
]

for step in steps:
    print(f"\n🚀 실행 중: {step}")
    subprocess.run(["python", step], check=True)
