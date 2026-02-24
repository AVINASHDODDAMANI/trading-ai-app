import yfinance as yf

print("Downloading...")
df = yf.download("TCS.NS", period="5d", interval="5m", progress=False)

print("Data shape:", None if df is None else df.shape)
print(df.tail())