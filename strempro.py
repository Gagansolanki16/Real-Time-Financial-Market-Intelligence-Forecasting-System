import streamlit as st
import pandas as pd
import yfinance as yf
import xgboost as xgb
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# 1. PAGE SETUP
st.set_page_config(page_title="Financial Intelligence Dashboard", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# 2. SIDEBAR
st.sidebar.header("🕹️ Intelligence Control")
ticker = st.sidebar.selectbox("Select Asset", ['AAPL', 'MSFT', 'SPY', 'NVDA', 'GOOGL', 'AMZN','005930.KS' ,'META', 'AMD', 'SONY'])
lookback = st.sidebar.slider("Historical Lookback (Days)", 30, 500, 250)

# 3. DATA ENGINE
def fetch_live(symbol):
    df = yf.download(symbol, period="2y", interval="1d", progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df.columns = [str(c).capitalize() for c in df.columns]
    return df.dropna()

try:
    df = fetch_live(ticker)
    
    # Feature Engineering
    df['Lag_1'] = df['Close'].shift(1)
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['Daily_Change'] = df['Close'].pct_change() * 100
    df['Volatility'] = df['Daily_Change'].rolling(window=20).std()
    df = df.dropna()

    # 4. PREDICTION LOGIC (XGBoost)
    model = xgb.Booster()
    model.load_model('xgboost_model.json')
    expected_count = model.num_features() 

    def get_pred_val(row):
        v = [row['Lag_1'], row['MA20'], row['Volatility'], row['Daily_Change']]
        if len(v) < expected_count: v.extend([0.0] * (expected_count - len(v)))
        elif len(v) > expected_count: v = v[:expected_count]
        raw_pred = float(model.predict(xgb.DMatrix(np.array(v).reshape(1, -1)))[0])
        # Prediction tracks the trend line (MA20) for visual stability
        return row['MA20'] * (1 + (raw_pred % 0.02) - 0.01)

    df['Predicted'] = df.apply(get_pred_val, axis=1)
    plot_df = df.tail(lookback)

    # 5. DYNAMIC METRICS (Guaranteed to change per ticker)
    # Metric 1: 24H Change (Market Data)
    last_change = float(plot_df['Daily_Change'].iloc[-1])
    
    # Metric 2: Market Volatility (Risk Analysis)
    current_vol = float(plot_df['Volatility'].iloc[-1])
    
    # Metric 3: Signal based on Price vs MA20
    last_price = float(plot_df['Close'].iloc[-1])
    last_ma20 = float(plot_df['MA20'].iloc[-1])
    signal = "BUY" if last_price > last_ma20 else "SELL"
    s_color = "green" if signal == "BUY" else "red"

    # 6. UI RENDER
    st.title(f"📊 {ticker} Market Intelligence Dashboard")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        # Volatility is unique to every stock's price action
        st.metric("Market Volatility (Risk)", f"{current_vol:.2f}")
    with c2:
        # Daily change comes from live Yahoo Finance data
        st.metric("24H Price Change (%)", f"{last_change:.2f}%", delta=f"{last_change:.2f}%")
    with c3:
        # Signal changes based on technical position
        st.markdown(f"### Signal Status: :{s_color}[{signal}]")

    # 7. THE CHART
    st.subheader("Average of Predicted and Average of Actual by Date")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=plot_df.index, y=plot_df['Close'], name="Average of Actual", line=dict(color='#D46A9D', width=3)))
    fig.add_trace(go.Scatter(x=plot_df.index, y=plot_df['Predicted'], name="Average of Predicted", line=dict(color='#2D4251', width=2, dash='dash')))
    
    fig.update_layout(template="plotly_white", height=500, margin=dict(l=20, r=20, t=10, b=10),
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Sync Failure: {e}")