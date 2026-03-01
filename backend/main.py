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

# ================= LOAD MODEL SAFELY =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
model = joblib.load(MODEL_PATH)

# ================= CORS =================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= SYMBOL FIX =================
def fix_symbol(symbol: str) -> str:
    symbol = symbol.upper().strip()
    if not symbol.endswith(".NS"):
        symbol += ".NS"
    return symbol


# ================= AI ANALYSIS FUNCTION =================
def analyze_stock(symbol: str):
    symbol = fix_symbol(symbol)

    # --- IST time ---
    ist = pytz.timezone("Asia/Kolkata")
    current_time = datetime.now(ist).strftime("%d-%m-%Y %H:%M:%S")

    try:
        # --- download data ---
        df = yf.download(symbol, period="3mo", interval="1d")

        # --- fix multi-index ---
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # --- check empty ---
        if df.empty:
            return {
                "stock": symbol,
                "signal": "NO DATA",
                "current_price": None,
                "buy_price": None,
                "target_price": None,
                "risk": "Unknown",
                "date_time_ist": current_time,
            }

        # --- indicators ---
        df["Return"] = df["Close"].pct_change()
        df["MA5"] = df["Close"].rolling(5).mean()
        df["MA10"] = df["Close"].rolling(10).mean()
        df = df.dropna()

        # --- check again ---
        if df.empty or len(df) < 1:
            return {
                "stock": symbol,
                "signal": "INSUFFICIENT DATA",
                "current_price": None,
                "buy_price": None,
                "target_price": None,
                "risk": "Unknown",
                "date_time_ist": current_time,
            }

        latest = df.iloc[-1]

        # --- safe price ---
        try:
            current_price = float(latest["Close"])
        except Exception:
            current_price = None

        # --- buy/sell levels ---
        suggested_buy = (
            round(current_price * 0.995, 2) if current_price else None
        )
        suggested_sell = (
            round(current_price * 1.01, 2) if current_price else None
        )

        # --- AI prediction ---
        X_live = np.array(
            [[latest["Return"], latest["MA5"], latest["MA10"]]]
        )

        prediction = model.predict(X_live)[0]
        signal = "BUY" if prediction == 1 else "SELL"

        return {
            "stock": symbol,
            "signal": signal,
            "current_price": current_price,
            "buy_price": suggested_buy,
            "target_price": suggested_sell,
            "risk": "AI Based",
            "date_time_ist": current_time,
        }

    except Exception as e:
        # --- catch ALL crashes (prevents 500) ---
        return {
            "stock": symbol,
            "signal": "ERROR",
            "current_price": None,
            "buy_price": None,
            "target_price": None,
            "risk": f"Error: {str(e)}",
            "date_time_ist": current_time,
        }


# ================= API =================
@app.get("/analyze")
def analyze(symbol: str):
    return analyze_stock(symbol)