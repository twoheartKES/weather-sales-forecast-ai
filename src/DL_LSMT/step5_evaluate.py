
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# 1. Use the trained xgb_model to make predictions on the X_test dataset
y_pred = xgb_model.predict(X_test)

# 3. Calculate the Mean Absolute Error (MAE)
mae = mean_absolute_error(y_test, y_pred)

# 4. Calculate the Root Mean Squared Error (RMSE)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

# 5. Calculate the R-squared score
r2 = r2_score(y_test, y_pred)

# 6. Print the calculated MAE, RMSE, and R-squared scores
print(f"Model Performance on 2025 Test Data:")
print(f"  Mean Absolute Error (MAE): {mae:.4f}")
print(f"  Root Mean Squared Error (RMSE): {rmse:.4f}")
print(f"  R-squared (R2): {r2:.4f}")