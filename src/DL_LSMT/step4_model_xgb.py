from xgboost import XGBRegressor

# 1. Initialize XGBoost Regressor model with specified parameters
xgb_model = XGBRegressor(
    n_estimators=300, ##트리(tree)를 몇 개 만들 것인가
    max_depth=5, ##각 결정트리의 깊이
    learning_rate=0.05, ##의미: 각 트리가 기존 모델을 얼마나 강하게 수정할지 작을수록 천천히, 안정적으로 학습
    subsample=0.8, ## 각 트리를 만들 때 전체 데이터 중 80%만 사용
    colsample_bytree=0.8,
    random_state=42,
    objective='reg:squarederror',
    n_jobs=-1  # Use all available CPU cores
)

print("XGBoost Regressor model initialized.")

# 2. Train the XGBoost model using X_train and y_train
print("Training XGBoost model...")
xgb_model.fit(X_train, y_train)

print("XGBoost model training completed.")