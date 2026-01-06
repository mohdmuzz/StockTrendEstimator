import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Stock Trend Estimation System",
    page_icon="📈",
    layout="wide"
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("📌 Project Details")
st.sidebar.markdown("""
**Language:** Python  
**UI Framework:** Streamlit  

✅ Frontend Completed  
⏳ ML Forecasting (Next Phase)
""")

ticker = st.sidebar.text_input("Stock Symbol", "TCS.NS")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

load_btn = st.sidebar.button("📊 Load Stock Data")

st.sidebar.markdown("""
⚠️ **Disclaimer**  
Educational use only.  
No trading or investment advice.
""")

# ---------------- MAIN TITLE ----------------
st.markdown(
    "<h1 style='color:#2ECC71;'>📈 Stock Trend Estimation System</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='color:gray;'>Academic Project | Market Data Visualization</p>",
    unsafe_allow_html=True
)
st.divider()

# ---------------- MAIN LOGIC ----------------
if load_btn:
    ticker = ticker.strip().upper()

    with st.spinner("Fetching stock data..."):
        data = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            progress=False
        )

    # -------- VALIDATION --------
    if data is None or data.empty:
        st.error("No data found. Check stock symbol or date range.")
        st.stop()

    st.success("Stock data loaded successfully")

    # -------- SAFE CLOSE PRICE EXTRACTION --------
    # THIS IS THE KEY FIX
    # SAFE, FLATTENED DATA FOR PLOTTING
    close_values = data["Close"].values.astype(float).ravel()
    close_index = data.index

    plot_df = pd.DataFrame({
        "Date": close_index,
        "Close Price": close_values
})


    # -------- METRICS --------
    last_price = float(close_values[-1].item())
    prev_price = float(close_values[-2].item())


    change = last_price - prev_price
    percent = (change / prev_price) * 100

    c1, c2, c3 = st.columns(3)
    c1.metric("Last Close Price", f"₹{last_price:.2f}")
    c2.metric("Daily Change", f"₹{change:.2f}", f"{percent:.2f}%")
    c3.metric("Total Records", len(close_values))

    st.divider()

    # -------- GRAPH (BULLETPROOF) --------
    st.subheader("📊 Historical Closing Price")
    st.subheader("📊 Historical Closing Price (Interactive)")

    plot_df = pd.DataFrame({
    "Date": close_index,
    "Close Price": close_values
})

    fig = go.Figure()

    fig.add_trace(
    go.Scatter(
        x=plot_df["Date"],
        y=plot_df["Close Price"],
        mode="lines",
        name="Close Price",
        line=dict(color="#2ECC71", width=2),
        hovertemplate=
        "<b>Date:</b> %{x}<br>" +
        "<b>Price:</b> ₹%{y:.2f}<extra></extra>"
    )
)

    fig.update_layout(
    template="plotly_dark",
    height=500,
    margin=dict(l=40, r=40, t=40, b=40),
    xaxis_title="Date",
    yaxis_title="Price (₹)",
    hovermode="x unified",
    dragmode="zoom"
)

    st.plotly_chart(fig, use_container_width=True)


    # -------- FUTURE TREND (UI ONLY) --------
    st.subheader("🔮 Future Trend Estimation (Educational Demo)")

    horizon = st.radio(
        "Select estimation horizon (days)",
        [7, 14, 30],
        horizontal=True
    )

    if st.button("Generate Trend Estimation (Demo)"):
        st.warning(
            "⚠️ Educational demonstration only.\n"
            "Not trading or investment advice."
        )

        future_dates = pd.date_range(
            start=close_index[-1],
            periods=horizon + 1,
            freq="B"
        )[1:]

        future_values = np.linspace(
            last_price,
            last_price * 1.05,
            horizon
        )

        future_df = pd.DataFrame(
            future_values,
            index=future_dates,
            columns=["Estimated Price (Demo)"]
        )

        st.line_chart(future_df)

# ---------------- FOOTER ----------------
st.divider()
st.caption(
    "This project is strictly for academic and educational purposes only."
)
