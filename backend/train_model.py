import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

# ================= FETCH DATA =================
df = yf.download("BEL.NS", period="2y", interval="1d")

# ================= FEATURES =================
df["Return"] = df["Close"].pct_change()
df["SMA10"] = df["Close"].rolling(10).mean()
df["SMA20"] = df["Close"].rolling(20).mean()

# ================= TARGET =================
df["Target"] = np.where(df["Close"].shift(-1) > df["Close"], 1, 0)

df = df.dropna()

features = ["Return", "SMA10", "SMA20"]
X = df[features]
y = df["Target"]

# ================= MODEL =================
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# ================= SAVE MODEL =================
joblib.dump(model, "model.pkl")

print("✅ Model trained and saved")