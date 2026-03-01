import matplotlib
matplotlib.use("Agg")

import os
import joblib
import numpy as np
import yfinance as yf
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from datetime import datetime
import pytz

app = FastAPI()

# ✅ Load trained model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
model = joblib.load(MODEL_PATH)

# ✅ Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= SYMBOL FIXER =================
def fix_symbol(symbol: str):
    symbol = symbol.upper().strip()

    # If already has suffix, keep it
    if "." in symbol:
        return symbol

    # Default to NSE
    return symbol + ".NS"


# ================= AI ANALYSIS FUNCTION =================
def analyze_stock(symbol: str):
    symbol = fix_symbol(symbol)

    # Download data
    df = yf.download(symbol, period="3mo", interval="1d")

    # ✅ Handle no data safely
    if df.empty:
        ist = pytz.timezone("Asia/Kolkata")
        current_time = datetime.now(ist).strftime("%d-%m-%Y %H:%M:%S")

        return {
            "stock": symbol,
            "signal": "NO DATA",
            "current_price": None,
            "buy_price": None,
            "target": None,
            "risk": "Unknown",
            "date_time_ist": current_time
        }

    # Indicators
    df["Return"] = df["Close"].pct_change()
    df["MA5"] = df["Close"].rolling(5).mean()
    df["MA10"] = df["Close"].rolling(10).mean()
    df = df.dropna()

    latest = df.iloc[-1]
    current_price = float(latest["Close"])

    # Simple buy/sell logic
    suggested_buy = round(current_price * 0.995, 2)
    suggested_sell = round(current_price * 1.01, 2)

    X_live = np.array([[latest["Return"], latest["MA5"], latest["MA10"]]])
    prediction = model.predict(X_live)[0]

    signal = "BUY" if prediction == 1 else "SELL"

    # ✅ IST time
    ist = pytz.timezone("Asia/Kolkata")
    current_time = datetime.now(ist).strftime("%d-%m-%Y %H:%M:%S")

    return {
        "stock": symbol,
        "signal": signal,
        "current_price": round(current_price, 2),
        "buy_price": suggested_buy,
        "target": suggested_sell,  # ⚠️ IMPORTANT NAME
        "risk": "AI Based",
        "date_time_ist": current_time
    }


# ================= API ENDPOINT =================
@app.get("/analyze")
def analyze(symbol: str):
    return analyze_stock(symbol)