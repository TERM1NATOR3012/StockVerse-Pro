from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app)

STOCKS = [
    "RELIANCE.NS","TCS.NS","HDFCBANK.NS","ICICIBANK.NS","INFY.NS",
    "ITC.NS","SBIN.NS","BHARTIARTL.NS","KOTAKBANK.NS","LT.NS"
]

@app.route("/api/stocks")
def stocks():
    result = []

    for sym in STOCKS:
        s = yf.Ticker(sym)
        info = s.history(period="1d", interval="1m")

        if not info.empty:
            last = info.iloc[-1]

            result.append({
                "symbol": sym.replace(".NS",""),
                "price": float(last["Close"]),
                "open": float(info["Open"][0]),
                "high": float(info["High"].max()),
                "low": float(info["Low"].min()),
                "close": float(last["Close"])
            })

    return jsonify(result)

@app.route("/api/history/<symbol>")
def history(symbol):
    s = yf.Ticker(symbol + ".NS")
    hist = s.history(period="1d", interval="5m")

    data = []
    for index, row in hist.iterrows():
        data.append({
            "time": int(index.timestamp()),
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"])
        })

    return jsonify(data)

if __name__ == "__main__":
    app.run(port=5000)