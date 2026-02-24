import pandas as pd

def calculate_signal(df):
    try:
        # Ensure columns are lowercase
        df.columns = [str(c).lower() for c in df.columns]

        # Safety check
        if 'close' not in df.columns:
            return "HOLD", "High Risk"

        # Moving averages
        df['ma20'] = df['close'].rolling(window=20).mean()
        df['ma50'] = df['close'].rolling(window=50).mean()

        # Remove NaN rows
        df = df.dropna()

        if df.empty:
            return "HOLD", "High Risk"

        latest = df.iloc[-1]

        # Signal logic
        if latest['ma20'] > latest['ma50']:
            return "BUY", "Low Risk"
        elif latest['ma20'] < latest['ma50']:
            return "SELL", "Medium Risk"
        else:
            return "HOLD", "High Risk"

    except Exception as e:
        return "HOLD", f"Error: {str(e)}"