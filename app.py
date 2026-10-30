import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="tradewithTushar", page_icon="📈", layout="wide")

# ---------- Language ----------
TEXT = {
    "hi": {
        "subtitle": "भारतीय शेयर बाज़ार रिसर्च डैशबोर्ड",
        "symbol": "स्टॉक सिंबल",
        "period": "डेटा अवधि",
        "interval": "चार्ट टाइमफ्रेम",
        "analyze": "विश्लेषण करें",
        "overview": "स्टॉक ओवरव्यू",
        "chart": "प्राइस चार्ट",
        "plan": "संभावित ट्रेड प्लान",
        "news": "स्टॉक न्यूज़",
        "simulation": "1,000 सिमुलेशन",
        "history": "रणनीति का ऐतिहासिक परीक्षण",
        "price": "आखिरी उपलब्ध कीमत",
        "change": "आज/अवधि बदलाव",
        "rsi": "RSI (14)",
        "trend": "EMA ट्रेंड",
        "volume": "वॉल्यूम",
        "signal": "टेक्निकल स्थिति",
        "entry": "संभावित एंट्री",
        "stop": "स्टॉप-लॉस",
        "target1": "टारगेट 1",
        "target2": "टारगेट 2",
        "rr": "रिस्क : रिवॉर्ड",
        "why": "कारण",
        "simulation": "मोंटे कार्लो सिमुलेशन",
        "capital": "शुरुआती पूंजी (₹)",
        "risk_pct": "प्रति ट्रेड जोखिम (%)",
        "run": "1,000 सिमुलेशन चलाएँ",
        "ending": "अंतिम पूंजी का मध्य अनुमान",
        "p5": "कमज़ोर परिदृश्य (5th percentile)",
        "p95": "बेहतर परिदृश्य (95th percentile)",
        "positive": "अंत में लाभ वाले पथ",
        "backtest": "EMA crossover ऐतिहासिक परीक्षण",
        "winrate": "जीत वाले ट्रेड (%)",
        "return": "रणनीति रिटर्न",
        "drawdown": "अधिकतम ड्रॉडाउन",
        "newsnone": "अभी न्यूज़ परिणाम नहीं मिले।",
        "disclaimer": "महत्वपूर्ण: यह शैक्षिक रिसर्च टूल है, निवेश सलाह नहीं। Yahoo Finance डेटा में देरी/अधूरापन हो सकता है। संकेत नियम-आधारित हैं, AI की गारंटी नहीं। लाइव ऑर्डर नहीं लगाए जाते।",
        "source": "डेटा स्रोत: Yahoo Finance (yfinance) और Google News RSS; उपलब्धता/कवरेज बदल सकती है।",
        "error": "डेटा नहीं मिला। सिंबल जाँचें; भारतीय शेयर के लिए NSE में .NS और BSE में .BO आम तौर पर इस्तेमाल होता है।",
        "reasons": "संकेत के आधार",
        "bull": "संभावित तेजी",
        "bear": "संभावित कमजोरी",
        "wait": "इंतज़ार / स्पष्ट संकेत नहीं",
        "no_news": "न्यूज़ फीड उपलब्ध नहीं है।",
        "ticker_hint": "उदाहरण: RELIANCE.NS, TCS.NS, HDFCBANK.NS, INFY.NS, या AAPL",
        "no_trade": "डेटा के आधार पर साफ ट्रेड सेटअप नहीं है।",
        "news_search": "न्यूज़ खोज",
        "backtest_note": "यह EMA20/EMA50 crossover का सरल ऐतिहासिक परीक्षण है। यह भविष्य के नतीजे नहीं बताता और खर्च/स्लिपेज पूरी तरह शामिल नहीं हैं।",
        "sim_note": "यह ऐतिहासिक दैनिक रिटर्न को bootstrap करके 1,000 संभावित पथ बनाता है। यह भविष्य की भविष्यवाणी नहीं है।",
        "data_time": "अंतिम कैंडल समय",
        "market": "मार्केट",
    },
    "en": {
        "subtitle": "Indian stock market research dashboard",
        "symbol": "Stock symbol",
        "period": "History period",
        "interval": "Chart timeframe",
        "analyze": "Analyze",
        "overview": "Stock overview",
        "chart": "Price chart",
        "plan": "Potential trade plan",
        "news": "Stock news",
        "price": "Last available price",
        "change": "Period change",
        "rsi": "RSI (14)",
        "trend": "EMA trend",
        "volume": "Volume",
        "signal": "Technical stance",
        "entry": "Potential entry",
        "stop": "Stop-loss",
        "target1": "Target 1",
        "target2": "Target 2",
        "rr": "Risk : Reward",
        "why": "Reasoning",
        "simulation": "Monte Carlo simulation",
        "capital": "Starting capital (₹)",
        "risk_pct": "Risk per trade (%)",
        "run": "Run 1,000 simulations",
        "ending": "Median ending equity",
        "p5": "Weak scenario (5th percentile)",
        "p95": "Strong scenario (95th percentile)",
        "positive": "Paths ending profitable",
        "backtest": "EMA crossover historical test",
        "winrate": "Winning trades (%)",
        "return": "Strategy return",
        "drawdown": "Maximum drawdown",
        "newsnone": "No news results found.",
        "disclaimer": "Important: Educational research tool, not investment advice. Yahoo Finance data may be delayed/incomplete. Signals are rule-based, not guaranteed AI predictions. No live orders are placed.",
        "source": "Data sources: Yahoo Finance (yfinance) and Google News RSS; availability and coverage can change.",
        "error": "No data found. Check the symbol; Indian NSE symbols commonly use .NS and BSE symbols .BO.",
        "reasons": "Signal reasoning",
        "bull": "Potentially bullish",
        "bear": "Potential weakness",
        "wait": "Wait / no clear signal",
        "no_news": "News feed unavailable.",
        "ticker_hint": "Examples: RELIANCE.NS, TCS.NS, HDFCBANK.NS, INFY.NS, or AAPL",
        "no_trade": "No clear trade setup from available data.",
        "news_search": "News search",
        "backtest_note": "This is a simple historical EMA20/EMA50 crossover test. It does not predict future outcomes and does not fully model costs/slippage.",
        "sim_note": "Bootstraps historical daily returns to create 1,000 possible paths. This is not a forecast.",
        "data_time": "Last candle time",
        "market": "Market",
    }
}

def t(key):
    return TEXT[st.session_state.get("language", "hi")][key]

st.session_state.setdefault("language", "hi")
with st.sidebar:
    st.title("📈 tradewithTushar")
    st.session_state.language = st.selectbox("Language / भाषा", ["hi", "en"], format_func=lambda x: "हिन्दी" if x == "hi" else "English")
    st.caption(t("subtitle"))
    st.markdown("---")
    symbol_input = st.text_input(t("symbol"), value=st.session_state.get("symbol", "RELIANCE.NS"), help=t("ticker_hint"))
    period = st.selectbox(t("period"), ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
    interval = st.selectbox(t("interval"), ["1d", "1h", "30m", "15m", "5m"], index=0)
    st.caption("Intraday interval availability depends on provider history limits.")
    analyze = st.button(t("analyze"), type="primary", use_container_width=True)
    st.markdown("---")
    st.caption(t("source"))

if analyze or "data" not in st.session_state:
    symbol = symbol_input.strip().upper().replace(" ", "")
    if symbol and "." not in symbol and symbol not in ["^NSEI", "^BSESN"]:
        # Friendly default for Indian symbols, but allow global tickers by entering full symbol.
        symbol = symbol + ".NS"
    st.session_state.symbol = symbol
    with st.spinner("Downloading market data…"):
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval, auto_adjust=True)
            if data is None or data.empty:
                data = pd.DataFrame()
            st.session_state.data = data
            st.session_state.symbol = symbol
            try:
                st.session_state.info = ticker.get_info()
            except Exception:
                st.session_state.info = {}
        except Exception as e:
            st.session_state.data = pd.DataFrame()
            st.session_state.fetch_error = str(e)

symbol = st.session_state.get("symbol", "RELIANCE.NS")
data = st.session_state.get("data", pd.DataFrame())
info = st.session_state.get("info", {})
st.title("tradewithTushar")
st.caption(t("subtitle"))

if data.empty:
    st.error(t("error"))
    st.info(t("ticker_hint"))
    st.markdown(t("disclaimer"))
    st.stop()

# Normalize and calculate indicators
data = data.copy()
data = data.dropna(subset=["Close"])
data["EMA20"] = data["Close"].ewm(span=20, adjust=False).mean()
data["EMA50"] = data["Close"].ewm(span=50, adjust=False).mean()
delta = data["Close"].diff()
gain = delta.clip(lower=0).rolling(14).mean()
loss = -delta.clip(upper=0).rolling(14).mean()
rs = gain / loss.replace(0, np.nan)
data["RSI"] = 100 - (100 / (1 + rs))
ema12 = data["Close"].ewm(span=12, adjust=False).mean()
ema26 = data["Close"].ewm(span=26, adjust=False).mean()
data["MACD"] = ema12 - ema26
data["MACD_signal"] = data["MACD"].ewm(span=9, adjust=False).mean()
prev_close = data["Close"].shift(1)
tr = pd.concat([(data["High"]-data["Low"]), (data["High"]-prev_close).abs(), (data["Low"]-prev_close).abs()], axis=1).max(axis=1)
data["ATR"] = tr.rolling(14).mean()
last = data.iloc[-1]
price = float(last["Close"])
prev = float(data["Close"].iloc[-2]) if len(data) > 1 else price
change_pct = ((price / prev) - 1) * 100 if prev else 0
rsi = float(last["RSI"]) if pd.notna(last["RSI"]) else 50
ema20 = float(last["EMA20"])
ema50 = float(last["EMA50"])
macd = float(last["MACD"]) if pd.notna(last["MACD"]) else 0
macds = float(last["MACD_signal"]) if pd.notna(last["MACD_signal"]) else 0
atr = float(last["ATR"]) if pd.notna(last["ATR"]) and last["ATR"] > 0 else price * 0.02

bull_points = int(ema20 > ema50) + int(price > ema20) + int(macd > macds) + int(50 <= rsi <= 70)
bear_points = int(ema20 < ema50) + int(price < ema20) + int(macd < macds) + int(rsi < 45 or rsi > 75)
if bull_points >= 3 and bear_points <= 1:
    stance, stance_color = t("bull"), "normal"
elif bear_points >= 3 and bull_points <= 1:
    stance, stance_color = t("bear"), "inverse"
else:
    stance, stance_color = t("wait"), "off"

# Educational ATR-based illustrative levels
entry_low, entry_high = price - 0.15*atr, price + 0.15*atr
if stance == t("bull"):
    stop = price - 1.5*atr
    target1, target2 = price + 1.5*atr, price + 3*atr
elif stance == t("bear"):
    stop = price + 1.5*atr
    target1, target2 = price - 1.5*atr, price - 3*atr
else:
    stop = price - 1.5*atr
    target1, target2 = price + 1.5*atr, price + 3*atr
risk_reward = abs(target2-price)/max(abs(price-stop), 1e-9)
currency = info.get("currency", "INR")
company = info.get("shortName") or info.get("longName") or symbol
latest_time = str(data.index[-1])[:19]

st.subheader(f"{company} · {symbol}")
st.caption(f"{t('data_time')}: {latest_time} | {t('market')}: {currency}")
c1,c2,c3,c4 = st.columns(4)
c1.metric(t("price"), f"{currency} {price:,.2f}", f"{change_pct:+.2f}%")
c2.metric(t("rsi"), f"{rsi:.1f}", "Overbought > 70 / Oversold < 30")
c3.metric(t("trend"), "Bullish" if ema20 > ema50 else "Bearish", f"EMA20 {ema20:.2f} / EMA50 {ema50:.2f}")
vol = last.get("Volume", np.nan)
c4.metric(t("volume"), f"{vol:,.0f}" if pd.notna(vol) else "N/A")
st.markdown(f"### {t('signal')}: **{stance}**")
with st.expander(t("reasons"), expanded=True):
    reasons = [
        f"EMA20 {'>' if ema20 > ema50 else '<='} EMA50",
        f"Price {'above' if price > ema20 else 'below'} EMA20",
        f"MACD {'above' if macd > macds else 'below/equal to'} signal",
        f"RSI = {rsi:.1f}"
    ]
    st.write(" · ".join(reasons))
    st.caption(t("disclaimer"))

left, right = st.columns([1.7, 1])
with left:
    st.subheader(t("chart"))
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.04, row_heights=[0.72,0.28])
    fig.add_trace(go.Candlestick(x=data.index, open=data["Open"], high=data["High"], low=data["Low"], close=data["Close"], name="OHLC"), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data["EMA20"], name="EMA20", line=dict(width=1.5)), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data["EMA50"], name="EMA50", line=dict(width=1.5)), row=1, col=1)
    fig.add_trace(go.Bar(x=data.index, y=data["Volume"], name="Volume", opacity=0.5), row=2, col=1)
    fig.update_layout(height=550, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=5,r=5,t=25,b=5), legend=dict(orientation="h"))
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader(t("plan"))
    st.caption(t("no_trade") if stance == t("wait") else t("disclaimer"))
    st.metric(t("entry"), f"{entry_low:,.2f} – {entry_high:,.2f}")
    st.metric(t("stop"), f"{stop:,.2f}")
    st.metric(t("target1"), f"{target1:,.2f}")
    st.metric(t("target2"), f"{target2:,.2f}")
    st.metric(t("rr"), f"1 : {risk_reward:.2f}")
    st.caption("ATR-based illustrative levels only. These are not orders or personalized recommendations.")

st.divider()
st.subheader(t("news"))
news_col1, news_col2 = st.columns([1, 2])
with news_col1:
    news_query = st.text_input(t("news_search"), value=(company if company else symbol))
    news_btn = st.button("Fetch news", use_container_width=True)
with news_col2:
    st.caption("Google News RSS results may be incomplete or delayed. Headlines should be independently verified.")
if news_btn or "news_items" not in st.session_state:
    try:
        q = requests.utils.quote(f'{news_query} stock India')
        rss_url = f"https://news.google.com/rss/search?q={q}&hl=en-IN&gl=IN&ceid=IN:en"
        resp = requests.get(rss_url, timeout=12, headers={"User-Agent":"Mozilla/5.0"})
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
        items = []
        for item in root.findall(".//item")[:12]:
            title = item.findtext("title", default="Untitled")
            link = item.findtext("link", default="")
            pub = item.findtext("pubDate", default="")
            source = item.findtext("source", default="Google News")
            items.append({"title": title, "link": link, "pub": pub, "source": source})
        st.session_state.news_items = items
    except Exception:
        st.session_state.news_items = []
items = st.session_state.get("news_items", [])
if items:
    for item in items:
        st.markdown(f"- **[{item['title']}]({item['link']})**  \n  <small>{item['source']} · {item['pub']}</small>", unsafe_allow_html=True)
else:
    st.info(t("newsnone"))

st.divider()
st.subheader(t("simulation"))
st.write(t("sim_note"))
sc1, sc2 = st.columns(2)
with sc1:
    capital = st.number_input(t("capital"), min_value=1000, max_value=1000000000, value=100000, step=10000)
with sc2:
    risk_pct = st.slider(t("risk_pct"), min_value=0.1, max_value=5.0, value=1.0, step=0.1)
if st.button(t("run"), type="primary"):
    daily_returns = data["Close"].pct_change().dropna().replace([np.inf,-np.inf], np.nan).dropna().values
    if len(daily_returns) < 30:
        st.warning("At least 30 historical returns are needed for a useful simulation.")
    else:
        rng = np.random.default_rng(42)
        n_sims, horizon = 1000, min(252, max(60, len(daily_returns)))
        paths = np.empty((n_sims, horizon + 1))
        paths[:,0] = float(capital)
        # Bootstrap historical daily returns; capped to avoid a single extreme data point dominating.
        returns = np.clip(daily_returns, np.quantile(daily_returns, .01), np.quantile(daily_returns, .99))
        sampled = rng.choice(returns, size=(n_sims,horizon), replace=True)
        for i in range(horizon):
            paths[:,i+1] = paths[:,i] * (1 + sampled[:,i])
        ending = paths[:,-1]
        p5, median, p95 = np.percentile(ending, [5,50,95])
        positive = float(np.mean(ending > capital)*100)
        a,b,c,d = st.columns(4)
        a.metric(t("ending"), f"₹{median:,.0f}")
        b.metric(t("p5"), f"₹{p5:,.0f}")
        c.metric(t("p95"), f"₹{p95:,.0f}")
        d.metric(t("positive"), f"{positive:.1f}%")
        simfig = go.Figure()
        for j in range(0,n_sims,25):
            simfig.add_trace(go.Scatter(y=paths[j], mode="lines", line=dict(width=1), opacity=.25, showlegend=False))
        simfig.update_layout(template="plotly_dark", height=350, title="Sample paths (25 of 1,000)", xaxis_title="Trading days", yaxis_title="Portfolio value (₹)")
        st.plotly_chart(simfig, use_container_width=True)
        st.caption("This bootstrap simulation applies the stock's historical returns to the portfolio. The risk-per-trade slider is collected for later strategy sizing; this simple price-path simulation does not yet use it to size trades.")

st.divider()
st.subheader(t("backtest"))
st.write(t("backtest_note"))
bt = data[["Close","EMA20","EMA50"]].dropna().copy()
if len(bt) > 5:
    bt["position"] = (bt["EMA20"] > bt["EMA50"]).astype(int)
    bt["daily_return"] = bt["Close"].pct_change().fillna(0)
    bt["strategy_return"] = bt["position"].shift(1).fillna(0) * bt["daily_return"]
    equity = (1 + bt["strategy_return"]).cumprod()
    bh = (1 + bt["daily_return"]).cumprod()
    trade_returns = bt.loc[bt["position"].diff().fillna(0) != 0, "strategy_return"]
    winrate = float((trade_returns > 0).mean()*100) if len(trade_returns) else 0.0
    total_return = (float(equity.iloc[-1])-1)*100
    peak = equity.cummax()
    maxdd = float(((equity/peak)-1).min()*100)
    a,b,c = st.columns(3)
    a.metric(t("winrate"), f"{winrate:.1f}%")
    b.metric(t("return"), f"{total_return:+.2f}%")
    c.metric(t("drawdown"), f"{maxdd:.2f}%")
    bfig = go.Figure()
    bfig.add_trace(go.Scatter(x=bt.index, y=equity, name="EMA20/EMA50 strategy"))
    bfig.add_trace(go.Scatter(x=bt.index, y=bh, name="Buy & hold"))
    bfig.update_layout(template="plotly_dark", height=350, yaxis_title="Growth of ₹1 (before costs)")
    st.plotly_chart(bfig, use_container_width=True)
else:
    st.info("Not enough historical data for a backtest.")

st.markdown("---")
st.warning(t("disclaimer"))
st.caption(t("source"))
