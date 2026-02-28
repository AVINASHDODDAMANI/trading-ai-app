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
model = joblib.load("model.pkl")

# ✅ Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= AI ANALYSIS FUNCTION =================
def analyze_stock(symbol: str):
    symbol = symbol.upper()
    # Auto add NSE SUFFIX IF MISSING
    if not symbol.endswith(".NS"):
        symbol += ".NS"
    df = yf.download(symbol, period="3mo", interval="1d")

    df["Return"] = df["Close"].pct_change()
    df["MA5"] = df["Close"].rolling(5).mean()
    df["MA10"] = df["Close"].rolling(10).mean()
    df = df.dropna()

    latest = df.iloc[-1]
    current_price = float(latest["Close"])
    
    #Simple buy price logic
    suggested_buy = round(current_price * 0.995, 2)  # 0.5% below current price
    suggested_sell = round(current_price * 1.01, 2)  # 1% above current price

    X_live = np.array([[latest["Return"], latest["MA5"], latest["MA10"]]])

    prediction = model.predict(X_live)[0]

    signal = "BUY" if prediction == 1 else "SELL"

    return {
        "stock": symbol.upper(),
        "signal": signal,
        "current_price": round(current_price, 2),
        "buy_price": suggested_buy,
        "target_price": suggested_sell,
        "risk": "AI Based",
        "date_time_ist": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }

# ================= API ENDPOINT =================
@app.get("/analyze")
def analyze(symbol: str):
    return analyze_stock(symbol)