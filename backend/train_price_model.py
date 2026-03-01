import yfinance as yf
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor

print("Downloading data...")

# Download large history for better AI
df = yf.download("RELIANCE.NS", period="5y", interval="1d")

# ================= FEATURES =================
df["Return"] = df["Close"].pct_change()
df["MA5"] = df["Close"].rolling(5).mean()
df["MA10"] = df["Close"].rolling(10).mean()
df["Volatility"] = df["Close"].rolling(10).std()

# 🎯 TARGET = Next day close price
df["Target"] = df["Close"].shift(-1)

df = df.dropna()

# ================= TRAIN DATA =================
X = df[["Return", "MA5", "MA10", "Volatility"]]
y = df["Target"]

print("Training AI price model...")

model = RandomForestRegressor(
    n_estimators=120,
    max_depth=8,
    random_state=42
)

model.fit(X, y)

joblib.dump(model, "price_model.pkl")

print("✅ Price model trained and saved!")