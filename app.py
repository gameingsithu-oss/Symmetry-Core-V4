import streamlit as st
import pandas as pd
import time
import requests
import feedparser # සජීවීව News ඇදලා ගන්න
from textblob import TextBlob
from database_handler import init_db, save_decision, get_history

init_db()

st.set_page_config(page_title="SYMMETRY | Autonomous Intelligence", layout="wide")

# Professional Styling
st.markdown("""
    <style>
    .stApp { background: #050510; color: #f1c40f; }
    .stMetric { background: rgba(255,255,255,0.05); border: 1px solid #f1c40f; border-radius: 12px; }
    .news-card { background: rgba(241, 196, 15, 0.1); padding: 15px; border-radius: 10px; border: 1px solid #f1c40f; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 1. සජීවීව ප්‍රවෘත්ති ඇදගන්නා Function එක
def fetch_live_news():
    # Google News Financial RSS feed
    feed_url = "https://news.google.com/rss/search?q=bitcoin+crypto+economy&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(feed_url)
    news_items = []
    for entry in feed.entries[:5]: # අලුත්ම ප්‍රවෘත්ති 5ක් ගන්න
        news_items.append(entry.title)
    return " ".join(news_items)

def get_crypto_prices():
    try:
        url = "https://api.binance.com/api/v3/ticker/price"
        symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']
        response = requests.get(url)
        data = response.json()
        return {item['symbol']: float(item['price']) for item in data if item['symbol'] in symbols}
    except: return {'BTCUSDT': 77000.0, 'ETHUSDT': 2300.0, 'BNBUSDT': 630.0}

# --- UI CONTENT ---
st.title("🤖 SYMMETRY: AUTONOMOUS CORE")
prices = get_crypto_prices()

# Live Market Row
m1, m2, m3 = st.columns(3)
m1.metric("BTC Price", f"${prices['BTCUSDT']:,.2f}")
m2.metric("ETH Price", f"${prices['ETHUSDT']:,.2f}")
m3.metric("BNB Price", f"${prices['BNBUSDT']:,.2f}")

st.markdown("---")

st.sidebar.header("Mission Control")
target_name = st.sidebar.text_input("Target Entity", "Global Market")
auto_mode = st.sidebar.checkbox("Enable Autopilot News", value=True)

col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("🕵️ Genie's Discovery")
    if st.button("START AUTONOMOUS SCAN"):
        with st.spinner('Accessing Global Data Scrolls...'):
            # දත්ත ලබාගැනීම
            if auto_mode:
                latest_intel = fetch_live_news()
                st.info("Live news successfully harvested from the clouds.")
            else:
                latest_intel = "Market is stable but cautious."

            # විශ්ලේෂණය
            analysis = TextBlob(latest_intel)
            vibe = round(analysis.sentiment.polarity, 2)
            
            # තීරණය
            if vibe > 0.1:
                verdict = "INSTITUTIONAL_GROWTH"
                st.success(f"PROSPERITY DETECTED: {vibe}")
                st.balloons()
            elif vibe < -0.1:
                verdict = "MARKET_CRISIS_ALERT"
                st.error(f"DANGER DETECTED: {vibe}")
            else:
                verdict = "STABLE_SYMMETRY"
                st.warning(f"BALANCE DETECTED: {vibe}")
            
            save_decision(target_name, prices['BTCUSDT'], vibe, verdict)
            
            # පද්ධතියට ලැබුණු News පෙන්වීම
            with st.expander("See Raw Intelligence Data"):
                st.write(latest_intel)

with col_right:
    st.subheader("📊 Symmetry Visualizer")
    chart_df = pd.DataFrame({
        'Resource': ['BTC Index', 'ETH Index', 'BNB Index'],
        'Power': [prices['BTCUSDT']/10, prices['ETHUSDT'], prices['BNBUSDT']*5]
    })
    st.bar_chart(chart_df.set_index('Resource'))

st.markdown("---")
st.subheader("📜 Digital Memory Logs")
st.dataframe(get_history(), use_container_width=True)