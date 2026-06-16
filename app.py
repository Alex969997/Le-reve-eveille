import streamlit as st
import pandas as pd
import plotly.express as px
from backend.main import BackendService

# 1. Page Configuration
st.set_page_config(
    page_title="Streamlit Boilerplate App",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS to inject for modern styling (Premium aesthetic)
st.markdown("""
<style>
    /* Main container adjustments */
    .reportview-container {
        background: #0f172a;
    }
    /* Sleek card containers */
    .metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        margin-bottom: 16px;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
    }
    .metric-title {
        color: #94a3b8;
        font-size: 0.875rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .metric-value {
        color: #f8fafc;
        font-size: 1.875rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar Navigation & Controls
with st.sidebar:
    st.image("https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png", width=200)
    st.title("Settings")
    st.write("Control your app properties below:")
    
    # Input parameter to pass to backend query
    days_to_plot = st.slider("Select Days of History", min_value=7, max_value=90, value=30)
    
    st.divider()
    st.info("💡 Tip: This project separates frontend layout (`app.py`) from business logic (`backend/main.py`).")

# 4. Main Layout & Title
st.title("⚡ Python + Streamlit Boilerplate")
st.caption("A modern, clean, and production-ready boilerplate template.")

# Tabs for different features
tab_dashboard, tab_tools, tab_about = st.tabs(["📊 Dashboard", "⚙️ Backend Tools", "📖 Code Structure"])

# --- TAB 1: Dashboard ---
with tab_dashboard:
    st.subheader("Key Performance Indicators")
    
    # Call backend layer for statistics
    stats = BackendService.get_dashboard_stats()
    
    # Create clean metric layout
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">TOTAL RECORDS</div>
            <div class="metric-value">{stats.total_records:,}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">ACTIVE USERS</div>
            <div class="metric-value">{stats.active_users:,}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">CONVERSION RATE</div>
            <div class="metric-value">{stats.conversion_rate}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">GROWTH</div>
            <div class="metric-value">+{stats.growth_percentage}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("Interactive Insights")
    
    # Call backend layer for plot data based on user input
    df_data = BackendService.get_time_series_data(days=days_to_plot)
    
    col_chart, col_table = st.columns([2, 1])
    
    with col_chart:
        fig = px.line(
            df_data, 
            x="Date", 
            y=["Revenue", "Signups"], 
            title=f"Revenue & Signups over the last {days_to_plot} days",
            template="plotly_dark",
            color_discrete_sequence=["#38bdf8", "#34d399"]
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col_table:
        st.write("Raw Backend Dataset (Tail)")
        st.dataframe(df_data.tail(10), use_container_width=True)

# --- TAB 2: Backend Tools ---
with tab_tools:
    st.subheader("Simulate Backend Computations")
    st.write("Type a sentence below to send it to the Python backend service for processing.")
    
    user_text = st.text_input("Enter text to process:", value="This is an awesome and good starting template!")
    
    if st.button("Process with Backend"):
        result = BackendService.process_user_input(user_text)
        
        if result["status"] == "success":
            st.success("Successfully processed by the backend!")
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Word Count", result["word_count"])
            c2.metric("Character Count", result["char_count"])
            c3.metric("Detected Sentiment", result["sentiment"])
        else:
            st.warning(result["message"])

# --- TAB 3: Code Structure ---
with tab_about:
    st.subheader("Project Structure")
    st.code("""
.
├── app.py                # Main Frontend / Presentation Layer
├── requirements.txt      # Application dependencies
├── README.md             # Documentation
└── backend/
    ├── __init__.py       # Package marker
    └── main.py           # Backend business logic, state and API calls
    """, language="text")
    
    st.info("🚀 **Ready to scale!** You can easily wrap `backend/main.py` with FastAPI if you decide to separate them into standalone HTTP microservices in the future.")
st.divider()
st.caption("Developed with ❤️ using Python and Streamlit.")
