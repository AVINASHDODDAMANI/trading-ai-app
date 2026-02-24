from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas as pd
from datetime import datetime
import pytz

app = FastAPI()

# ✅ Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Simple analysis function
def analyze_stock(symbol: str):
    data = yf.download(symbol, period="3mo")

    if data.empty:
        return {"error": "Invalid stock symbol"}

    # Moving averages
    data["MA20"] = data["Close"].rolling(20).mean()
    data["MA50"] = data["Close"].rolling(50).mean()

    last_ma20 = data["MA20"].iloc[-1]
    last_ma50 = data["MA50"].iloc[-1]

    if last_ma20 > last_ma50:
        signal = "BUY"
        risk = "Medium Risk"
    else:
        signal = "SELL"
        risk = "High Risk"

    # ✅ Indian time
    ist = pytz.timezone("Asia/Kolkata")
    indian_time = datetime.now(ist).strftime("%d-%m-%Y %H:%M:%S")

    return {
        "stock": symbol,
        "signal": signal,
        "risk": risk,
        "date_time_ist": indian_time,
    }

# ✅ API endpoint
@app.get("/analyze")
def analyze(symbol: str):
    return analyze_stock(symbol)