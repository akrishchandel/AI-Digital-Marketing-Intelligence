import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score


# --------------------------------------------------
# 1. Load dataset
# --------------------------------------------------

df = pd.read_csv("data/analyzed_campaigns.csv")


# --------------------------------------------------
# 2. Select features and target
# --------------------------------------------------

features = [
    "impressions",
    "clicks",
    "spend"
]

target = "conversions"

X = df[features]
y = df[target]


# --------------------------------------------------
# 3. Split dataset
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# --------------------------------------------------
# 4. Create model
# --------------------------------------------------

model = LinearRegression()


# --------------------------------------------------
# 5. Train model
# --------------------------------------------------

model.fit(X_train, y_train)


# --------------------------------------------------
# 6. Make predictions
# --------------------------------------------------

predictions = model.predict(X_test)


# --------------------------------------------------
# 7. Evaluate model
# --------------------------------------------------

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("\n" + "=" * 50)
print("MACHINE LEARNING MODEL")
print("=" * 50)

print("\nModel: Linear Regression")

print("\nMean Absolute Error:")
print(round(mae, 2))

print("\nR² Score:")
print(round(r2, 2))


# --------------------------------------------------
# 8. Example prediction
# --------------------------------------------------

example = pd.DataFrame({
    "impressions": [80000],
    "clicks": [4000],
    "spend": [12000]
})

predicted_conversions = model.predict(example)[0]

print("\nExample Prediction")
print("-" * 40)

print("Impressions: 80,000")
print("Clicks: 4,000")
print("Spend: ₹12,000")

print(
    "Predicted Conversions:",
    round(predicted_conversions)
)


# --------------------------------------------------
# 9. Save model
# --------------------------------------------------

joblib.dump(model, "model/conversion_model.pkl")

print("\nModel saved successfully!")
print("File: model/conversion_model.pkl")