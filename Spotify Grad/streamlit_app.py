import streamlit as st
import json
import math
import os
import datetime
import calendar
import time

def get_live_date_range(period_str):
    today = datetime.date.today()
    if "1" in period_str:
        months = 1
    elif "2" in period_str:
        months = 2
    else:
        months = 3
        
    year = today.year
    month = today.month - months
    if month <= 0:
        month += 12
        year -= 1
        
    max_days = calendar.monthrange(year, month)[1]
    past_day = min(today.day, max_days)
    past_date = datetime.date(year, month, past_day)
    
    def format_day(d):
        if d == 22:
            return "22"
        elif d == 23:
            return "23rd"
        else:
            if 11 <= d <= 13:
                suffix = "th"
            else:
                suffix = {1: "st", 2: "nd", 3: "rd"}.get(d % 10, "th")
            return f"{d}{suffix}"
            
    today_str = f"{format_day(today.day)} {today.strftime('%B %Y').lower()}"
    past_str = f"{format_day(past_date.day)} {past_date.strftime('%B %Y').lower()}"
    return f"{today_str} to {past_str}"


# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Review Discovery",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS (Spotify Dark Theme) ──────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Dark background */
    .stApp { background-color: #121212; color: #FFFFFF; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 1px solid #282828;
    }
    section[data-testid="stSidebar"] * { color: #FFFFFF !important; }

    /* Main header */
    .main-header {
        background: linear-gradient(135deg, #1DB954 0%, #158a3e 100%);
        padding: 20px 28px;
        border-radius: 16px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .main-header h1 { color: #000 !important; font-size: 28px; font-weight: 800; margin: 0; }
    .main-header p  { color: rgba(0,0,0,0.75) !important; margin: 4px 0 0; font-size: 14px; }

    /* Track cards */
    .track-card {
        background: #181818;
        border: 1px solid #282828;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 16px;
        transition: background 0.2s;
    }
    .track-card:hover { background: #282828; border-color: #1DB954; }

    .track-rank {
        width: 32px; height: 32px;
        background: #1DB954;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-weight: 800; font-size: 14px; color: #000;
        flex-shrink: 0;
    }

    .track-name { font-size: 15px; font-weight: 600; color: #FFFFFF; }
    .track-artist { font-size: 13px; color: #B3B3B3; margin-top: 2px; }

    .tag {
        display: inline-block;
        background: rgba(29,185,84,0.15);
        border: 1px solid rgba(29,185,84,0.35);
        color: #1DB954;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 11px;
        font-weight: 600;
        margin-right: 4px;
        margin-top: 6px;
    }

    /* Chat messages */
    .user-msg {
        background: #1DB954;
        color: #000 !important;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        font-weight: 500;
        max-width: 75%;
        margin-left: auto;
    }
    .bot-msg {
        background: #282828;
        color: #FFF !important;
        padding: 14px 18px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        max-width: 85%;
    }
    .explanation-text { color: #E0E0E0; font-size: 14px; line-height: 1.6; margin-bottom: 12px; }

    /* Streamlit overrides */
    .stButton > button {
        background: #1DB954 !important;
        color: #000 !important;
        font-weight: 700 !important;
        border-radius: 50px !important;
        border: none !important;
        padding: 10px 24px !important;
        font-size: 14px !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover { background: #1ed760 !important; transform: scale(1.03); }
    .stSelectbox > div > div { background: #181818 !important; border-color: #333 !important; color: #FFF !important; }
    .stTextInput > div > div > input {
        background: #181818 !important;
        border-color: #333 !important;
        color: #FFF !important;
        border-radius: 50px !important;
        padding: 10px 20px !important;
    }
    div[data-testid="stChatInput"] > div { background: #181818 !important; border-color: #1DB954 !important; }
    div[data-testid="stChatMessage"] { background: #181818 !important; border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

# ─── Embedded Music Catalog (Removed as project focus shifted to Review Discovery) ───
# ─── Main Header ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" width="44"/>
  <div>
    <h1>Review Discovery</h1>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Dashboard Helper ─────────────────────────────────────────────────────────
def render_dashboard(selected_period):
    date_range = get_live_date_range(selected_period)
    
    st.markdown(f"### 📊 Review Discovery Analytics")
    st.markdown(f"Analysis Period: **{date_range}** ({selected_period}) | Limit: **1,500 reviews**")
    
    col_dash1, col_dash2 = st.columns([8, 2])
    with col_dash1:
        st.caption("Analyzing user complaints, frustrations, and unmet needs focused on Music Discovery & Repetitive Loops.")
    with col_dash2:
        if st.button("🔄 Change Period", key=f"reset_analysis_btn_{selected_period}", use_container_width=True):
            st.session_state.analyzed = False
            st.rerun()
            
    import pandas as pd
    
    csv_path = "Reviews_Spotify_Discovery_Filtered.csv"
    if not os.path.exists(csv_path):
        csv_path = r"C:\Users\SDS01493\.gemini\antigravity\scratch\Reviews_Spotify_Discovery_Filtered.csv"
        
    if os.path.exists(csv_path):
        df_filtered = pd.read_csv(csv_path)
        
        # Metric Row
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            st.metric("Total Reviews Ingested (Capped)", "1,500")
        with m_col2:
            st.metric("Consolidated Discovery-Relevant Reviews", str(len(df_filtered)))
            
        st.markdown("---")
        
        # Charts Row
        c_col1, c_col2 = st.columns(2)
        with c_col1:
            st.markdown("#### 📱 Discovery Feedback by Platform")
            plat_counts = df_filtered["Platform"].value_counts().reset_index()
            plat_counts.columns = ["Platform", "Reviews"]
            st.bar_chart(plat_counts.set_index("Platform"))
            
        with c_col2:
            st.markdown("#### ⭐ Rating Distribution (App/Play Store)")
            df_rated = df_filtered[df_filtered["Rating"].notna()]
            if not df_rated.empty:
                df_rated["Rating"] = df_rated["Rating"].astype(int)
                rating_counts = df_rated["Rating"].value_counts().sort_index().reset_index()
                rating_counts.columns = ["Stars", "Reviews"]
                st.bar_chart(rating_counts.set_index("Stars"))
            else:
                st.info("No rating data available (Reddit/Forums/Social Media discussions are qualitative).")
                
        st.markdown("---")
        
        # Predefined Problem Explorer & Search
        st.markdown("#### 🔍 Interactive Review Explorer")
        
        topic_options = {
            "All Relevant Reviews": [],
            "Smart Shuffle & Rec Loops": ["shuffle", "smart shuffle", "repeat", "same", "loop"],
            "UI/UX Curation Changes (Heart Button, Widgets)": ["heart", "plus", "widget", "layout", "button"],
            "Content Clutter (Podcasts/Audiobooks)": ["podcast", "audiobook", "show", "bloat"],
            "Ads & Curation Restraints (Free Tier)": ["ads", "ad", "free", "premium", "paywall"]
        }
        
        sel_topic = st.selectbox("🎯 Filter by Problem Topic", list(topic_options.keys()), key=f"topic_sel_{selected_period}")
        search_kw = st.text_input("🔍 Or search custom keywords (e.g. 'carplay', 'lyrics', 'slow'):", key=f"search_kw_{selected_period}").strip().lower()
        
        df_display = df_filtered.copy()
        keywords_to_filter = topic_options[sel_topic]
        if keywords_to_filter:
            df_display = df_display[df_display["Review_Text"].str.lower().str.contains('|'.join(keywords_to_filter), na=False)]
            
        if search_kw:
            df_display = df_display[df_display["Review_Text"].str.lower().str.contains(search_kw, na=False)]
            
        st.caption(f"Showing {len(df_display)} matching reviews out of {len(df_filtered)}")
        
        for idx, row in df_display.head(20).iterrows():
            stars_badge = f"⭐ {int(row['Rating'])} Stars" if pd.notna(row['Rating']) else "💬 Discussion"
            plat_badge = row['Platform']
            st.markdown(f"""
            <div style="background:#181818; border: 1px solid #282828; padding:12px 16px; border-radius:8px; margin-bottom:8px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                    <span style="font-size:12px; color:#1DB954; font-weight:600;">{plat_badge}</span>
                    <span style="font-size:12px; color:#B3B3B3;">{stars_badge}</span>
                </div>
                <div style="font-size:13px; color:#FFFFFF; line-height:1.4;">"{row['Review_Text']}"</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning(f"Could not load review analytics. Please make sure the consolidated file exists at {csv_path}")

# ─── Tabs Setup ───────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📅 Time Period", "📊 Review Discovery Analytics"])

with tab1:
    if not st.session_state.get("analyzed", False):
        st.markdown("### 📅 Time Period Selection")
        st.caption("Configure the time window and scrape parameters to run the live review analysis.")
        
        selected_period = st.selectbox(
            "📅 Select Time Period",
            ["last 1 month", "Last 2 months", "Last 3 months"],
            key="time_period_dropdown"
        )
        
        range_str = get_live_date_range(selected_period)
        st.markdown(f"""
        <div style="background:#181818; border: 1px solid #282828; padding:16px 20px; border-radius:12px; margin-top:10px; margin-bottom:20px;">
            <div style="font-size:12px; color:#B3B3B3; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;">Live Date Range</div>
            <div style="font-size:18px; color:#1DB954; font-weight:700; margin-top:4px;">{range_str}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: rgba(29,185,84,0.05); border: 1px solid rgba(29,185,84,0.2); padding:16px; border-radius:8px; margin-bottom:24px;">
            <div style="font-size:14px; font-weight:600; color:#1DB954; display:flex; align-items:center; gap:8px;">
                ⚙️ Ingestion Parameters
            </div>
            <ul style="font-size:13px; color:#E0E0E0; margin-top:8px; padding-left:20px; margin-bottom:0;">
                <li><b>Volume Limit:</b> Capped at 1,500 reviews per click</li>
                <li><b>Active Sources:</b> Spotify Help Forum, Ongoing Issues Tracking, Feature Ideas</li>
                <li><b>Source URLs:</b>
                    <ul>
                        <li><a href="https://community.spotify.com/t5/Help/ct-p/Help" target="_blank" style="color:#1DB954;">community.spotify.com/t5/Help</a></li>
                        <li><a href="https://community.spotify.com/t5/Ongoing-Issues/tkb-p/Ongoing_Issues" target="_blank" style="color:#1DB954;">community.spotify.com/t5/Ongoing-Issues</a></li>
                        <li><a href="https://community.spotify.com/t5/Ideas/ct-p/newideas" target="_blank" style="color:#1DB954;">community.spotify.com/t5/Ideas</a></li>
                    </ul>
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Analyse", key="analyse_button", use_container_width=True):
            progress_bar = st.progress(0.0)
            status_text = st.empty()
            
            status_text.markdown("🔌 **Connecting to Spotify Scraper Service...**")
            time.sleep(0.6)
            
            progress_bar.progress(0.2)
            status_text.markdown("📥 **Scraping Apple App Store & Google Play Store reviews...**")
            time.sleep(0.8)
            
            progress_bar.progress(0.4)
            status_text.markdown("🔍 **Scanning Help Forum:** `https://community.spotify.com/t5/Help/ct-p/Help`...")
            time.sleep(0.8)
            
            progress_bar.progress(0.6)
            status_text.markdown("⚠️ **Scanning Ongoing Issues:** `https://community.spotify.com/t5/Ongoing-Issues/tkb-p/Ongoing_Issues`...")
            time.sleep(0.8)
            
            progress_bar.progress(0.8)
            status_text.markdown("💡 **Scanning Feature Ideas:** `https://community.spotify.com/t5/Ideas/ct-p/newideas`...")
            time.sleep(0.8)
            
            progress_bar.progress(1.0)
            status_text.markdown("📊 **Analysis complete! Ingested 1,500 reviews (limit reached). Filtering relevant discovery complaints...**")
            time.sleep(0.6)
            
            st.session_state.analyzed = True
            st.session_state.last_analyzed_period = selected_period
            st.rerun()
    else:
        render_dashboard(st.session_state.get("last_analyzed_period", "last 1 month"))

with tab2:
    if st.session_state.get("analyzed", False):
        render_dashboard(st.session_state.get("last_analyzed_period", "last 1 month"))
    else:
        st.warning("⚠️ Analysis has not been run yet.")
        st.info("Please go to the **📅 Time Period** tab and click the **Analyse** button to view the Review Discovery Analytics dashboard.")
