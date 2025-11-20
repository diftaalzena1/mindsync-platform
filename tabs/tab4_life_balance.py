import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar
import os
import csv

def load_activities_from_csv():
    """Load activities from CSV file with error handling"""
    csv_file = "data/activities.csv"
    
    try:
        # Create directory if not exists
        os.makedirs("data", exist_ok=True)
        
        # Check if CSV file exists
        if not os.path.exists(csv_file):
            # Return empty list if file doesn't exist
            print(f"❌ CSV file not found: {csv_file}")
            return []
        
        # Load CSV
        df = pd.read_csv(csv_file)
        
        # Convert to list of dictionaries and ensure data types
        activities = []
        for _, row in df.iterrows():
            activity = {
                "tanggal": str(row["tanggal"]),
                "aktivitas": str(row["aktivitas"]),
                "kategori": str(row["kategori"]),
                "durasi": int(row["durasi"]),
                "intensitas": int(row["intensitas"]),
                "catatan": str(row["catatan"]) if pd.notna(row["catatan"]) else "",
                "created_at": str(row["created_at"])
            }
            activities.append(activity)
        
        print(f"✅ Loaded {len(activities)} activities from {csv_file}")
        return activities
        
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        # Return empty list if error
        return []

def save_activity_to_csv(activity):
    """Save single activity to CSV"""
    csv_file = "data/activities.csv"
    
    # Create data directory if not exists
    os.makedirs("data", exist_ok=True)
    
    # Create file with headers if not exists
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=activity.keys())
            writer.writeheader()
    
    # Append activity to CSV
    with open(csv_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=activity.keys())
        writer.writerow(activity)

def save_all_activities_to_csv(activities):
    """Save all activities to CSV (overwrite)"""
    csv_file = "data/activities.csv"
    
    # Create data directory if not exists
    os.makedirs("data", exist_ok=True)
    
    if activities:
        df = pd.DataFrame(activities)
        df.to_csv(csv_file, index=False)

def apply_balance_css():
    st.markdown("""
    <style>
    /* Main background */
    .main .block-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding-top: 2rem;
    }
    
    /* Activity Card Styling */
    .activity-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        margin: 0.5rem 0 !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .activity-card::before {
        content: '' !important;
        position: absolute !important;
        left: 0 !important;
        top: 0 !important;
        bottom: 0 !important;
        width: 5px !important;
        background: var(--card-color, #0EA5E9) !important;
    }
    
    .activity-card:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 12px 40px rgba(14, 165, 233, 0.2) !important;
        border-color: rgba(14, 165, 233, 0.3) !important;
    }
    
    .activity-card * {
        color: white !important;
    }
    
    /* Score Card Styling */
    .score-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        margin: 0.5rem 0 !important;
        text-align: center !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }
    
    .score-card:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 40px rgba(14, 165, 233, 0.15) !important;
    }
    
    /* Recommendation Card Styling */
    .recommendation-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        margin: 0.5rem 0 !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
        border-left: 4px solid var(--rec-color, #0EA5E9) !important;
    }
    
    .recommendation-card:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(14, 165, 233, 0.15) !important;
    }
    
    .recommendation-card * {
        color: white !important;
    }
    
    /* Progress Card Styling */
    .progress-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        margin: 0.5rem 0 !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(10px) !important;
        text-align: center !important;
    }
    
    /* Section Headers */
    .section-header {
        color: white !important;
        margin: 2rem 0 1rem 0 !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Calendar Day Styling */
    .calendar-day {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.7) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        margin: 0.25rem 0 !important;
        min-height: 120px !important;
    }
    
    .calendar-today {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.2) 0%, rgba(15, 23, 42, 0.8) 100%) !important;
        border: 1px solid rgba(14, 165, 233, 0.3) !important;
    }
    
    /* Empty State Styling */
    .empty-state {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.7) 100%) !important;
        border: 2px dashed rgba(255, 255, 255, 0.2) !important;
        border-radius: 16px !important;
        padding: 3rem 2rem !important;
        text-align: center !important;
        margin: 1rem 0 !important;
    }
    
    /* Form Styling */
    .stForm {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Button Styling - BLACK TEXT */
    .stButton>button {
        background: linear-gradient(135deg, #0EA5E9 0%, #6366F1 100%) !important;
        color: #000000 !important; /* Changed to black as requested */
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.4) !important;
        color: #000000 !important; /* Black text on hover */
    }
    
    /* Form Submit Button - BLACK TEXT */
    .stForm .stButton>button {
        color: #000000 !important;
        font-weight: 700 !important;
    }
    
    .stForm .stButton>button:hover {
        color: #000000 !important;
    }
    
    /* Metric Styling */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        color: white !important;
    }
    
    [data-testid="metric-container"] * {
        color: white !important;
    }
    
    /* Custom Streamlit Components - WHITE TEXT */
    .stDateInput, .stSelectbox, .stSlider, .stTextArea {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        color: white !important;
    }
    
    .stDateInput>div>div>input, .stSelectbox>div>div>select, .stTextArea>div>textarea {
        color: white !important;
        background: transparent !important;
    }
    
    /* Form Labels - WHITE TEXT */
    .stForm label, .stForm span, .stForm div {
        color: white !important;
    }
    
    /* Slider Labels - WHITE TEXT */
    .stSlider label {
        color: white !important;
    }
    
    /* Selectbox Options - WHITE TEXT */
    .stSelectbox option {
        color: white !important;
        background: #1e293b !important;
    }
    
    /* Text Input - WHITE TEXT */
    .stTextInput input {
        color: white !important;
    }
    
    /* Search Input - WHITE TEXT */
    input[type="text"] {
        color: white !important;
    }
    
    /* Filter Section - WHITE TEXT */
    .stTextInput label, .stSelectbox label {
        color: white !important;
    }
    
    /* Activity Summary - WHITE TEXT */
    .summary-section * {
        color: white !important;
    }
    
    /* Gauge Title Styling - FIXED */
    .gauge-title {
        font-size: 16px !important;
        font-weight: bold !important;
        color: white !important;
        text-align: center !important;
        margin-bottom: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

def activity_card(activity, duration, intensity, date, category):
    intensity_colors = {
        1: "#10B981",  # Green
        2: "#34D399",  # Light Green
        3: "#F59E0B",  # Yellow
        4: "#F97316",  # Orange
        5: "#EF4444"   # Red
    }
    
    category_icons = {
        "Relaxation": "🧘",
        "Physical": "💪", 
        "Social": "👥",
        "Digital": "📱",
        "Creative": "🎨",
        "Sleep": "😴"
    }
    
    st.markdown(f"""
    <div class="activity-card" style="--card-color: {intensity_colors[intensity]}">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div style="flex: 1;">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 1rem;">
                    <span style="font-size: 1.5rem;">{category_icons.get(category, '📝')}</span>
                    <div>
                        <h4 style="margin: 0; color: white !important; font-size: 1.1rem;">{activity}</h4>
                        <p style="margin: 0; color: #94a3b8 !important; font-size: 0.9rem;">{category} • {date}</p>
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="color: #e2e8f0; font-size: 0.9rem;">
                        ⏱️ <strong>{duration} menit</strong>
                    </div>
                    <div style="color: {intensity_colors[intensity]}; font-size: 0.9rem;">
                        {'⭐' * intensity}{'☆' * (5-intensity)}
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def progress_chart(current, target, label, color="#0EA5E9"):
    progress = min(current / target * 100, 100) if target > 0 else 0
    chart_color = "#10B981" if progress >= 80 else "#F59E0B" if progress >= 50 else "#EF4444"
    
    fig = go.Figure()
    
    fig.add_trace(go.Indicator(
        mode = "gauge+number",
        value = progress,
        number = {'suffix': "%", 'font': {'size': 20, 'color': 'white'}},
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': label, 'font': {'size': 16, 'color': 'white', 'family': 'Arial'}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white", 'tickfont': {'color': 'white', 'size': 12}},
            'bar': {'color': chart_color, 'thickness': 0.3},
            'bgcolor': "rgba(255,255,255,0.1)",
            'borderwidth': 2,
            'bordercolor': "rgba(255,255,255,0.2)",
            'steps': [
                {'range': [0, 40], 'color': "rgba(239, 68, 68, 0.2)"},
                {'range': [40, 70], 'color': "rgba(245, 158, 11, 0.2)"},
                {'range': [70, 100], 'color': "rgba(16, 185, 129, 0.2)"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90}}))
    
    fig.update_layout(
        height=200,
        margin=dict(l=20, r=20, t=60, b=20),  # Increased top margin for title
        font={'color': "white", 'family': "Arial"},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def calculate_dsi_from_data(screen_time, stress_level, sleep_quality, productivity):
    """
    Calculate Digital Stress Index (DSI) from user data
    Formula: Higher screen time + higher stress + lower sleep quality = higher DSI
    """
    # Normalize components (0-100 scale)
    screen_component = min(screen_time / 12 * 100, 100)  # 12 hours max
    stress_component = stress_level * 10  # 0-10 to 0-100
    sleep_component = (5 - sleep_quality) * 20  # Inverse: lower sleep quality = higher stress
    productivity_component = (100 - productivity)  # Inverse: lower productivity = higher stress
    
    # Weighted average
    dsi = (
        screen_component * 0.3 +
        stress_component * 0.3 + 
        sleep_component * 0.2 +
        productivity_component * 0.2
    )
    
    return min(max(dsi, 0), 100)  # Ensure between 0-100

def calculate_dbi_from_data(screen_time, work_screen, leisure_screen, sleep_hours, productivity):
    """
    Calculate Digital Balance Index (DBI) from user data
    Formula: Balance between work/leisure + good sleep + high productivity = higher DBI
    """
    # Work-leisure balance component (0-100)
    if screen_time > 0:
        work_balance = (1 - abs(work_screen - leisure_screen) / screen_time) * 100
    else:
        work_balance = 100
    
    # Sleep component (7-9 hours optimal)
    if sleep_hours >= 7 and sleep_hours <= 9:
        sleep_component = 100
    else:
        sleep_component = 100 - abs(sleep_hours - 8) * 12.5  # Penalize deviation from 8 hours
    
    # Productivity component
    productivity_component = productivity
    
    # Screen time health component
    if screen_time <= 6:
        screen_component = 100
    else:
        screen_component = max(100 - (screen_time - 6) * 10, 0)
    
    # Weighted average
    dbi = (
        work_balance * 0.25 +
        sleep_component * 0.25 +
        productivity_component * 0.25 +
        screen_component * 0.25
    )
    
    return min(max(dbi, 0), 100)

def run(model=None):
    # Apply custom CSS
    apply_balance_css()

    # ==========================
    # Initialize Session State
    # ==========================
    if "planner" not in st.session_state:
        st.session_state["planner"] = load_activities_from_csv()

    # ==========================
    # Hero Header
    # ==========================
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, #8B5CF6 0%, #0EA5E9 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(139, 92, 246, 0.3);
        position: relative;
        overflow: hidden;
    '>
        <div style='
            position: absolute;
            top: -50%;
            right: -10%;
            width: 300px;
            height: 300px;
            background: rgba(255,255,255,0.1);
            border-radius: 50%;
            filter: blur(40px);
        '></div>
        <h1 style='color: white; margin: 0; font-size: 3rem; font-weight: 700;'>🧭 Life Balance</h1>
        <p style='color: rgba(255,255,255,0.95); font-size: 1.3rem; margin: 1rem 0; font-weight: 300;'>
            Rencanakan Perjalanan Menuju Keseimbangan Digital yang Lebih Sehat
        </p>
        <div style='
            display: inline-flex;
            gap: 1rem;
            margin-top: 1rem;
            align-items: center;
            background: rgba(255,255,255,0.15);
            padding: 0.5rem 1.5rem;
            border-radius: 50px;
            backdrop-filter: blur(10px);
        '>
            <span style='color: #059669; font-weight: bold;'>🧠 MWI</span>
            <span style='color: #B91C1C; font-weight: bold;'>😰 DSI</span>
            <span style='color: #0369A1; font-weight: bold;'>⚖️ DBI</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ==========================
    # Data Management Section
    # ==========================
    st.markdown('<div class="section-header"><h3>💾 Manajemen Data Aktivitas</h3></div>', unsafe_allow_html=True)
    
    data_cols = st.columns(3)
    
    with data_cols[0]:
        total_activities = len(st.session_state.planner)
        st.metric("Total Aktivitas Tersimpan", total_activities)
    
    with data_cols[1]:
        if st.button("📥 Export ke CSV", use_container_width=True):
            if st.session_state.planner:
                df = pd.DataFrame(st.session_state.planner)
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv_data,
                    file_name=f"aktivitas_digital_balance_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.warning("Tidak ada data untuk di-export")
    
    with data_cols[2]:
        if st.button("🔄 Sync dengan CSV", use_container_width=True):
            st.session_state.planner = load_activities_from_csv()
            st.success("✅ Data berhasil disinkronisasi dengan CSV!")
            st.rerun()

    # ==========================
    # Wellness Scores Dashboard
    # ==========================
    st.markdown('<div class="section-header"><h3>📊 Dashboard Kesejahteraan Digital</h3></div>', unsafe_allow_html=True)
    
    # Initialize session state for score history if not exists
    if 'score_history' not in st.session_state:
        st.session_state.score_history = []
    
    # Get scores from model or calculate from session data
    if model and hasattr(model, 'get_scores'):
        scores = model.get_scores()
        mwi = scores.get("MWI", 65)
        dsi = scores.get("DSI", 45) 
        dbi = scores.get("DBI", 70)
    else:
        # Calculate from Tab 2 data if available
        try:
            # Get data from Tab 2 (Daily Pulse)
            screen_time = st.session_state.get('screen_time_hours', 8)
            work_screen = st.session_state.get('work_screen_hours', 4)
            leisure_screen = st.session_state.get('leisure_screen_hours', 4)
            sleep_hours = st.session_state.get('sleep_hours', 7)
            sleep_quality = st.session_state.get('sleep_quality', 4)
            stress_level = st.session_state.get('stress_level', 5)
            productivity = st.session_state.get('productivity', 70)
            
            # MWI from Tab 2 prediction (if available)
            mwi = st.session_state.get('predicted_wellness', 65)
            
            # Calculate DSI and DBI using actual formulas
            dsi = calculate_dsi_from_data(
                screen_time=screen_time,
                stress_level=stress_level,
                sleep_quality=sleep_quality,
                productivity=productivity
            )
            
            dbi = calculate_dbi_from_data(
                screen_time=screen_time,
                work_screen=work_screen,
                leisure_screen=leisure_screen,
                sleep_hours=sleep_hours,
                productivity=productivity
            )
            
            # Show data source info
            st.markdown("""
            <div class="recommendation-card" style="--rec-color: #10B981">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                    <span style="font-size: 24px;">✅</span>
                    <div>
                        <strong>Skor dihitung dari data Pulse Check terbaru!</strong>
                        <p style="margin: 0; color: #94a3b8 !important; font-size: 14px;">Berdasarkan input screen time, stres, tidur, dan produktivitas Anda</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.warning(f"⚠️ Menggunakan data default: {e}")
            # Fallback to default calculations
            mwi = st.session_state.get('predicted_wellness', 65) or 65
            dsi = max(0, 100 - mwi + 20)
            dbi = (mwi + (100 - dsi)) / 2

    # Display scores in columns
    score_cols = st.columns(3)
    
    with score_cols[0]:
        status = "Optimal" if mwi >= 70 else "Baik" if mwi >= 50 else "Perlu Perhatian"
        status_color = "#10B981" if mwi >= 70 else "#F59E0B" if mwi >= 50 else "#EF4444"
        st.markdown(f"""
        <div class="score-card">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🧠</div>
            <h3 style="margin: 0.5rem 0; color: white !important;">MWI</h3>
            <div style="font-size: 2.5rem; font-weight: bold; color: #0EA5E9; margin: 0.5rem 0;">{mwi:.1f}</div>
            <div style="color: {status_color}; font-weight: bold; margin: 0.5rem 0; font-size: 1.1rem;">{status}</div>
            <p style="color: #94a3b8; margin: 0;">Mental Wellness Index</p>
        </div>
        """, unsafe_allow_html=True)
    
    with score_cols[1]:
        status = "Rendah" if dsi <= 40 else "Sedang" if dsi <= 70 else "Tinggi"
        status_color = "#10B981" if dsi <= 40 else "#F59E0B" if dsi <= 70 else "#EF4444"
        st.markdown(f"""
        <div class="score-card">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">😰</div>
            <h3 style="margin: 0.5rem 0; color: white !important;">DSI</h3>
            <div style="font-size: 2.5rem; font-weight: bold; color: #EF4444; margin: 0.5rem 0;">{dsi:.1f}</div>
            <div style="color: {status_color}; font-weight: bold; margin: 0.5rem 0; font-size: 1.1rem;">{status}</div>
            <p style="color: #94a3b8; margin: 0;">Digital Stress Index</p>
        </div>
        """, unsafe_allow_html=True)
    
    with score_cols[2]:
        status = "Seimbang" if dbi >= 70 else "Cukup" if dbi >= 50 else "Tidak Seimbang"
        status_color = "#10B981" if dbi >= 70 else "#F59E0B" if dbi >= 50 else "#EF4444"
        st.markdown(f"""
        <div class="score-card">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">⚖️</div>
            <h3 style="margin: 0.5rem 0; color: white !important;">DBI</h3>
            <div style="font-size: 2.5rem; font-weight: bold; color: #10B981; margin: 0.5rem 0;">{dbi:.1f}</div>
            <div style="color: {status_color}; font-weight: bold; margin: 0.5rem 0; font-size: 1.1rem;">{status}</div>
            <p style="color: #94a3b8; margin: 0;">Digital Balance Index</p>
        </div>
        """, unsafe_allow_html=True)

    # Score interpretation and recommendations
    st.markdown('<div class="section-header"><h3>📈 Interpretasi Skor Anda</h3></div>', unsafe_allow_html=True)
    
    interpret_cols = st.columns(3)
    
    with interpret_cols[0]:
        if mwi >= 70:
            st.markdown("""
            <div class="recommendation-card" style="--rec-color: #10B981">
                <strong>🧠 MWI Optimal</strong><br>
                <span style="color: #94a3b8">Kesejahteraan mental Anda dalam kondisi baik!</span>
            </div>
            """, unsafe_allow_html=True)
        elif mwi >= 50:
            st.markdown("""
            <div class="recommendation-card" style="--rec-color: #F59E0B">
                <strong>🧠 MWI Cukup</strong><br>
                <span style="color: #94a3b8">Ada ruang untuk peningkatan kesejahteraan mental.</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="recommendation-card" style="--rec-color: #EF4444">
                <strong>🧠 MWI Perlu Perhatian</strong><br>
                <span style="color: #94a3b8">Prioritaskan kesehatan mental Anda.</span>
            </div>
            """, unsafe_allow_html=True)
    
    with interpret_cols[1]:
        if dsi <= 40:
            st.markdown("""
            <div class="recommendation-card" style="--rec-color: #10B981">
                <strong>😰 DSI Rendah</strong><br>
                <span style="color: #94a3b8">Stres digital terkendali dengan baik!</span>
            </div>
            """, unsafe_allow_html=True)
        elif dsi <= 70:
            st.markdown("""
            <div class="recommendation-card" style="--rec-color: #F59E0B">
                <strong>😰 DSI Sedang</strong><br>
                <span style="color: #94a3b8">Waspada terhadap potensi stres digital.</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="recommendation-card" style="--rec-color: #EF4444">
                <strong>😰 DSI Tinggi</strong><br>
                <span style="color: #94a3b8">Perlu tindakan untuk mengurangi stres digital.</span>
            </div>
            """, unsafe_allow_html=True)
    
    with interpret_cols[2]:
        if dbi >= 70:
            st.markdown("""
            <div class="recommendation-card" style="--rec-color: #10B981">
                <strong>⚖️ DBI Seimbang</strong><br>
                <span style="color: #94a3b8">Hidup digital Anda sudah seimbang!</span>
            </div>
            """, unsafe_allow_html=True)
        elif dbi >= 50:
            st.markdown("""
            <div class="recommendation-card" style="--rec-color: #F59E0B">
                <strong>⚖️ DBI Cukup</strong><br>
                <span style="color: #94a3b8">Terus usahakan keseimbangan yang lebih baik.</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="recommendation-card" style="--rec-color: #EF4444">
                <strong>⚖️ DBI Tidak Seimbang</strong><br>
                <span style="color: #94a3b8">Fokus pada penciptaan keseimbangan digital.</span>
            </div>
            """, unsafe_allow_html=True)

    # ==========================
    # Progress Tracking - WITH VISIBLE GAUGE TITLES
    # ==========================
    st.markdown('<div class="section-header"><h3>🎯 Progress Mingguan</h3></div>', unsafe_allow_html=True)
    
    # Calculate weekly progress
    weekly_activities = [act for act in st.session_state.get("planner", []) 
                        if datetime.strptime(act["tanggal"], "%Y-%m-%d") >= datetime.now() - timedelta(days=7)]
    
    total_weekly_minutes = sum(act["durasi"] for act in weekly_activities)
    weekly_goal = 300  # 5 hours per week
    
    progress_cols = st.columns(3)
    
    with progress_cols[0]:
        st.markdown('<div class="gauge-title">Aktivitas Sehat</div>', unsafe_allow_html=True)
        st.markdown('<div class="progress-card">', unsafe_allow_html=True)
        st.plotly_chart(progress_chart(
            total_weekly_minutes, weekly_goal, "Aktivitas Sehat"
        ), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with progress_cols[1]:
        st.markdown('<div class="gauge-title">Relaksasi</div>', unsafe_allow_html=True)
        st.markdown('<div class="progress-card">', unsafe_allow_html=True)
        relaxation_activities = [act for act in weekly_activities if act["kategori"] in ["Relaxation", "Sleep"]]
        relaxation_minutes = sum(act["durasi"] for act in relaxation_activities)
        st.plotly_chart(progress_chart(
            relaxation_minutes, 180, "Relaksasi"
        ), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with progress_cols[2]:
        st.markdown('<div class="gauge-title">Aktivitas Fisik</div>', unsafe_allow_html=True)
        st.markdown('<div class="progress-card">', unsafe_allow_html=True)
        physical_activities = [act for act in weekly_activities if act["kategori"] in ["Physical"]]
        physical_minutes = sum(act["durasi"] for act in physical_activities)
        st.plotly_chart(progress_chart(
            physical_minutes, 150, "Aktivitas Fisik"
        ), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Progress summary
    if weekly_activities:
        completion_rate = (total_weekly_minutes / weekly_goal * 100) if weekly_goal > 0 else 0
        st.markdown(f"""
        <div class="recommendation-card" style="--rec-color: #0EA5E9">
            <div style="text-align: center;">
                <strong>📊 Ringkasan Minggu Ini</strong><br>
                <span style="color: #94a3b8">
                    {len(weekly_activities)} aktivitas • {total_weekly_minutes} menit • 
                    <span style='color: {"#10B981" if completion_rate >= 80 else "#F59E0B" if completion_rate >= 50 else "#EF4444"}'>
                        {completion_rate:.1f}% tercapai
                    </span>
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ==========================
    # Activity Planner Form - WHITE TEXT
    # ==========================
    st.markdown('<div class="section-header"><h3 style="color: white !important;">📅 Rencanakan Aktivitas Sehat</h3></div>', unsafe_allow_html=True)
    
    with st.form("planner_form", clear_on_submit=True):
        colA, colB = st.columns(2)

        with colA:
            tanggal = st.date_input(
                "📅 Tanggal Aktivitas",
                datetime.today(),
                help="Pilih tanggal untuk aktivitas ini"
            )
            
            aktivitas = st.selectbox(
                "🎯 Jenis Aktivitas",
                [
                    "Meditasi & Mindfulness",
                    "Digital Detox (no gadget)",
                    "Olahraga Ringan (jalan, yoga)",
                    "Olahraga Intens (lari, gym)",
                    "Jurnal Emosi & Refleksi",
                    "Quality Time dengan Keluarga/Teman",
                    "Membaca Buku (non-digital)",
                    "Hobi Kreatif Offline",
                    "Tidur Berkualitas",
                    "Nature Time (jalan di alam)",
                    "Teknik Relaksasi (pernapasan)",
                    "Batasan Screen Time"
                ]
            )
            
            durasi = st.slider(
                "⏱️ Durasi (menit)",
                min_value=5,
                max_value=240,
                value=30,
                step=5,
                help="Durasi aktivitas dalam menit"
            )

        with colB:
            # Map activities to categories
            activity_categories = {
                "Meditasi & Mindfulness": "Relaxation",
                "Digital Detox (no gadget)": "Digital", 
                "Olahraga Ringan (jalan, yoga)": "Physical",
                "Olahraga Intens (lari, gym)": "Physical",
                "Jurnal Emosi & Refleksi": "Relaxation",
                "Quality Time dengan Keluarga/Teman": "Social",
                "Membaca Buku (non-digital)": "Creative",
                "Hobi Kreatif Offline": "Creative",
                "Tidur Berkualitas": "Sleep",
                "Nature Time (jalan di alam)": "Physical",
                "Teknik Relaksasi (pernapasan)": "Relaxation",
                "Batasan Screen Time": "Digital"
            }
            
            kategori = activity_categories.get(aktivitas, "Relaxation")
            
            intensitas = st.slider(
                "🔥 Intensitas Manfaat (1-5)",
                1, 5, 3,
                help="Seberapa besar manfaat aktivitas ini untuk keseimbangan digital Anda"
            )
            
            catatan = st.text_area(
                "📝 Catatan Tambahan (opsional)",
                placeholder="Tulis detail atau tujuan spesifik aktivitas ini...",
                height=80
            )

        submitted = st.form_submit_button(
            "💾 Simpan Aktivitas ke CSV",
            use_container_width=True
        )

    # ==========================
    # Save Activity to CSV dan Session State
    # ==========================
    if submitted:
        new_activity = {
            "tanggal": tanggal.strftime("%Y-%m-%d"),
            "aktivitas": aktivitas,
            "kategori": kategori,
            "durasi": durasi,
            "intensitas": intensitas,
            "catatan": catatan,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Save to session state
        st.session_state["planner"].append(new_activity)
        
        # Save to CSV
        save_activity_to_csv(new_activity)
        
        st.success("🎉 Aktivitas berhasil ditambahkan dan disimpan ke CSV!")
        st.balloons()

    # ==========================
    # Activities Overview - WHITE TEXT
    # ==========================
    st.markdown('<div class="section-header"><h3 style="color: white !important;">📋 Aktivitas Terencana</h3></div>', unsafe_allow_html=True)
    
    if len(st.session_state["planner"]) == 0:
        st.markdown("""
        <div class="empty-state">
            <div style='font-size: 4rem; margin-bottom: 1rem;'>📅</div>
            <h3 style='color: #e2e8f0; margin-bottom: 1rem;'>Belum ada aktivitas yang direncanakan</h3>
            <p style='color: #94a3b8; margin: 0;'>Mulai rencanakan perjalanan menuju keseimbangan digital dengan menambahkan aktivitas pertama Anda!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Filter options - WHITE TEXT
        filter_cols = st.columns([2, 1, 1])
        with filter_cols[0]:
            search_term = st.text_input("🔍 Cari aktivitas...", placeholder="Ketik nama aktivitas...")
        with filter_cols[1]:
            categories = list(set(act["kategori"] for act in st.session_state["planner"]))
            category_filter = st.selectbox("Kategori", ["Semua"] + categories)
        with filter_cols[2]:
            intensity_filter = st.selectbox("Intensitas", ["Semua", "1", "2", "3", "4", "5"])

        # Filter activities
        filtered_activities = st.session_state["planner"]
        if search_term:
            filtered_activities = [act for act in filtered_activities if search_term.lower() in act["aktivitas"].lower()]
        if category_filter != "Semua":
            filtered_activities = [act for act in filtered_activities if act["kategori"] == category_filter]
        if intensity_filter != "Semua":
            filtered_activities = [act for act in filtered_activities if act["intensitas"] == int(intensity_filter)]

        # Sort by date
        filtered_activities.sort(key=lambda x: x["tanggal"], reverse=True)

        # Display activities
        for activity in filtered_activities:
            activity_card(
                activity["aktivitas"],
                activity["durasi"],
                activity["intensitas"],
                activity["tanggal"],
                activity["kategori"]
            )

        # Summary statistics - WHITE TEXT
        st.markdown('<div class="section-header"><h3 style="color: white !important;">📊 Ringkasan Aktivitas</h3></div>', unsafe_allow_html=True)
        summary_cols = st.columns(4)
        
        with summary_cols[0]:
            total_activities = len(filtered_activities)
            st.metric("Total Aktivitas", total_activities)
        
        with summary_cols[1]:
            total_minutes = sum(act["durasi"] for act in filtered_activities)
            st.metric("Total Menit", total_minutes)
        
        with summary_cols[2]:
            avg_intensity = sum(act["intensitas"] for act in filtered_activities) / len(filtered_activities) if filtered_activities else 0
            st.metric("Rata-rata Intensitas", f"{avg_intensity:.1f}")
        
        with summary_cols[3]:
            upcoming_activities = len([act for act in filtered_activities if act["tanggal"] >= datetime.now().strftime("%Y-%m-%d")])
            st.metric("Aktivitas Mendatang", upcoming_activities)

    # ==========================
    # Smart Recommendations
    # ==========================
    st.markdown('<div class="section-header"><h3>🤖 Rekomendasi Personal</h3></div>', unsafe_allow_html=True)
    
    rec_cols = st.columns(2)
    
    with rec_cols[0]:
        st.markdown("#### 💡 Berdasarkan Skor Anda")
        
        recommendations = []
        
        # MWI-based recommendations
        if mwi < 50:
            recommendations.append("""
            <div class="recommendation-card" style="--rec-color: #EF4444">
                <div style="display: flex; align-items: flex-start; gap: 12px;">
                    <span style="font-size: 24px;">🧠</span>
                    <div>
                        <strong>Tingkatkan Kesejahteraan Mental</strong>
                        <p style="margin: 8px 0 0 0; color: #94a3b8 !important; font-size: 14px;">Tambahkan 15 menit meditasi harian dan jurnal emosi untuk refleksi.</p>
                    </div>
                </div>
            </div>
            """)
        elif mwi < 70:
            recommendations.append("""
            <div class="recommendation-card" style="--rec-color: #F59E0B">
                <div style="display: flex; align-items: flex-start; gap: 12px;">
                    <span style="font-size: 24px;">🧠</span>
                    <div>
                        <strong>Pertahankan Kesejahteraan Mental</strong>
                        <p style="margin: 8px 0 0 0; color: #94a3b8 !important; font-size: 14px;">Lanjutkan kebiasaan sehat dan tambahkan variasi aktivitas relaksasi.</p>
                    </div>
                </div>
            </div>
            """)
        
        # DSI-based recommendations
        if dsi > 70:
            recommendations.append("""
            <div class="recommendation-card" style="--rec-color: #EF4444">
                <div style="display: flex; align-items: flex-start; gap: 12px;">
                    <span style="font-size: 24px;">😰</span>
                    <div>
                        <strong>Kurangi Stres Digital</strong>
                        <p style="margin: 8px 0 0 0; color: #94a3b8 !important; font-size: 14px;">Rencanakan digital detox 1 jam sebelum tidur dan batasi notifikasi.</p>
                    </div>
                </div>
            </div>
            """)
        elif dsi > 50:
            recommendations.append("""
            <div class="recommendation-card" style="--rec-color: #F59E0B">
                <div style="display: flex; align-items: flex-start; gap: 12px;">
                    <span style="font-size: 24px;">😰</span>
                    <div>
                        <strong>Kelola Stres Digital</strong>
                        <p style="margin: 8px 0 0 0; color: #94a3b8 !important; font-size: 14px;">Practice mindful scrolling dan set batasan waktu untuk media sosial.</p>
                    </div>
                </div>
            </div>
            """)
        
        # DBI-based recommendations
        if dbi < 50:
            recommendations.append("""
            <div class="recommendation-card" style="--rec-color: #EF4444">
                <div style="display: flex; align-items: flex-start; gap: 12px;">
                    <span style="font-size: 24px;">⚖️</span>
                    <div>
                        <strong>Perbaiki Keseimbangan Digital</strong>
                        <p style="margin: 8px 0 0 0; color: #94a3b8 !important; font-size: 14px;">Kombinasikan aktivitas offline dengan screen time yang terukur.</p>
                    </div>
                </div>
            </div>
            """)
        elif dbi < 70:
            recommendations.append("""
            <div class="recommendation-card" style="--rec-color: #F59E0B">
                <div style="display: flex; align-items: flex-start; gap: 12px;">
                    <span style="font-size: 24px;">⚖️</span>
                    <div>
                        <strong>Optimalkan Keseimbangan</strong>
                        <p style="margin: 8px 0 0 0; color: #94a3b8 !important; font-size: 14px;">Fokus pada kualitas interaksi digital daripada kuantitas.</p>
                    </div>
                </div>
            </div>
            """)
        
        if not recommendations:
            recommendations.append("""
            <div class="recommendation-card" style="--rec-color: #10B981">
                <div style="display: flex; align-items: flex-start; gap: 12px;">
                    <span style="font-size: 24px;">🎉</span>
                    <div>
                        <strong>Kondisi Optimal!</strong>
                        <p style="margin: 8px 0 0 0; color: #94a3b8 !important; font-size: 14px;">Pertahankan kebiasaan sehat dan eksplorasi aktivitas baru untuk variasi.</p>
                    </div>
                </div>
            </div>
            """)
        
        for rec in recommendations:
            st.markdown(rec, unsafe_allow_html=True)
    
    with rec_cols[1]:
        st.markdown("#### 🎯 Aktivitas yang Disarankan")
        
        suggested_activities = []
        
        # Suggest based on current activities distribution
        if st.session_state["planner"]:
            categories = [act["kategori"] for act in st.session_state["planner"]]
            category_count = {cat: categories.count(cat) for cat in set(categories)}
            
            # Find least frequent category
            if category_count:
                least_category = min(category_count, key=category_count.get)
                if least_category == "Physical":
                    suggested_activities.append("💪 Coba tambahkan olahraga ringan 3x seminggu")
                elif least_category == "Social":
                    suggested_activities.append("👥 Rencanakan quality time dengan teman/keluarga")
                elif least_category == "Relaxation":
                    suggested_activities.append("🧘 Tambahkan sesi meditasi 10 menit harian")
                elif least_category == "Creative":
                    suggested_activities.append("🎨 Eksplorasi hobi kreatif offline")
                elif least_category == "Sleep":
                    suggested_activities.append("😴 Prioritaskan tidur 7-8 jam berkualitas")
        
        # Score-based additional suggestions
        if dsi > 60:
            suggested_activities.extend([
                "📵 Digital detox 2 jam sehari",
                "🧘‍♂️ Teknik pernapasan untuk reduksi stres",
                "🌳 Time in nature tanpa gadget"
            ])
        
        if dbi < 60:
            suggested_activities.extend([
                "⚖️ Audit waktu layar harian",
                "📊 Track work-life balance",
                "🎯 Set batasan waktu aplikasi"
            ])
        
        # Default suggestions
        if not suggested_activities:
            suggested_activities = [
                "🌅 Morning routine tanpa gadget 30 menit",
                "📵 Digital detox selama makan",
                "💤 Tidur 7-8 jam dengan kualitas baik", 
                "🚶 Jalan kaki 30 menit di alam terbuka",
                "🎨 Eksplorasi hobi kreatif offline"
            ]
        
        for suggestion in suggested_activities:
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 10px; margin: 8px 0; padding: 12px; background: rgba(255,255,255,0.05); border-radius: 8px;">
                <span style="font-size: 1.2rem;">{suggestion.split(' ')[0]}</span>
                <span style="color: #e2e8f0;">{' '.join(suggestion.split(' ')[1:])}</span>
            </div>
            """, unsafe_allow_html=True)

    # ==========================
    # Weekly Calendar View
    # ==========================
    if st.session_state["planner"]:
        st.markdown('<div class="section-header"><h3>📅 Kalender Mingguan</h3></div>', unsafe_allow_html=True)
        
        # Get activities for current week
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        week_dates = [(start_of_week + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
        
        week_activities = {}
        for date in week_dates:
            week_activities[date] = [act for act in st.session_state["planner"] if act["tanggal"] == date]
        
        # Create weekly calendar
        days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
        
        cal_cols = st.columns(7)
        for i, (col, day, date) in enumerate(zip(cal_cols, days, week_dates)):
            with col:
                day_activities = week_activities.get(date, [])
                is_today = date == datetime.now().strftime("%Y-%m-%d")
                
                # Day header
                day_class = "calendar-day calendar-today" if is_today else "calendar-day"
                st.markdown(f"""
                <div class="{day_class}">
                    <div style="text-align: center; margin-bottom: 1rem;">
                        <div style="color: {'#0EA5E9' if is_today else '#e2e8f0'}; font-weight: {'bold' if is_today else 'normal'};">{day}</div>
                        <div style="color: #94a3b8; font-size: 0.9rem;">{date[8:]}/{date[5:7]}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Activities for the day
                for activity in day_activities:
                    intensity_color = ["#10B981", "#34D399", "#F59E0B", "#F97316", "#EF4444"][activity["intensitas"]-1]
                    st.markdown(f"""
                    <div style="
                        background: {intensity_color}15;
                        border-left: 3px solid {intensity_color};
                        padding: 0.5rem;
                        margin: 0.25rem 0;
                        border-radius: 4px;
                        font-size: 0.8rem;
                    ">
                        <div style="font-weight: bold; color: white;">{activity['aktivitas'][:15]}...</div>
                        <div style="color: #94a3b8;">⏱️ {activity['durasi']}m • {'⭐' * activity['intensitas']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)

    # ==========================
    # Score Improvement Tips
    # ==========================
    st.markdown('<div class="section-header"><h3>💪 Tips Peningkatan Skor</h3></div>', unsafe_allow_html=True)
    
    tip_cols = st.columns(2)
    
    with tip_cols[0]:
        st.markdown("#### 🧠 Tingkatkan MWI")
        mwi_tips = [
            "Prioritaskan tidur 7-9 jam per malam",
            "Practice gratitude journaling setiap hari",
            "Lakukan aktivitas fisik 30 menit, 3x seminggu",
            "Batasi screen time 1 jam sebelum tidur",
            "Social connection yang meaningful"
        ]
        for tip in mwi_tips:
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 10px; margin: 8px 0; padding: 8px 12px; background: rgba(14, 165, 233, 0.1); border-radius: 8px;">
                <span style="color: #0EA5E9;">•</span>
                <span style="color: #e2e8f0;">{tip}</span>
            </div>
            """, unsafe_allow_html=True)
    
    with tip_cols[1]:
        st.markdown("#### ⚖️ Optimalkan DBI")
        dbi_tips = [
            "Work-life balance: 50% kerja, 50% hiburan",
            "Digital Sabbath: 1 hari tanpa gadget per minggu",
            "Mindful consumption: intent sebelum buka app",
            "Physical-digital balance: setiap 1 jam online, 15 menit offline",
            "Quality over quantity screen time"
        ]
        for tip in dbi_tips:
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 10px; margin: 8px 0; padding: 8px 12px; background: rgba(16, 185, 129, 0.1); border-radius: 8px;">
                <span style="color: #10B981;">•</span>
                <span style="color: #e2e8f0;">{tip}</span>
            </div>
            """, unsafe_allow_html=True)

    # ==========================
    # Footer
    # ==========================
    st.markdown("---")
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
    '>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>🌟</div>
        <h3 style='color: white; margin: 0 0 1rem 0;'>MindSync — Digital Wellbeing Intelligence</h3>
        <p style='color: #e2e8f0; margin: 0; font-size: 1.1rem;'>
            Setiap langkah kecil menuju keseimbangan digital adalah pencapaian besar untuk kesehatan mental Anda 🧠✨
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    # For testing
    class MockModel:
        def get_scores(self):
            return {"MWI": 72, "DSI": 38, "DBI": 75}
    
    run(MockModel())