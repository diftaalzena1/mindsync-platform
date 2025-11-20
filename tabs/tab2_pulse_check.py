# tab2_pulse_check.py
import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==========================
# Folder & File CSV
# ==========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(BASE_DIR, "data")
CSV_FILE = os.path.join(DATA_FOLDER, "user_daily_data.csv")

os.makedirs(DATA_FOLDER, exist_ok=True)

# ==========================
# Custom CSS & Components
# ==========================
def apply_custom_css():
    st.markdown("""
    <style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
    }
    
    /* Global text color */
    .stApp, .stMarkdown, .stText, .stNumberInput label, .stSlider label, .stButton, .stDataFrame {
        color: white !important;
    }
    
    /* Custom number input styling */
    .stNumberInput>div>div>input {
        background-color: #334155 !important;
        color: white !important;
        border: 1px solid #475569 !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    
    .stNumberInput label {
        color: #e2e8f0 !important;
        font-weight: 500;
    }
    
    /* Slider styling */
    .stSlider>div>div>div>div {
        background-color: #0EA5E9 !important;
    }
    
    .stSlider>div>div>div {
        background-color: #475569 !important;
    }
    
    .stSlider label {
        color: #e2e8f0 !important;
        font-weight: 500;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #0EA5E9 0%, #6366F1 100%) !important;
        color: white !important;
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
    }
    
    /* Metric cards */
    [data-testid="metric-container"] {
        background: rgba(30, 41, 59, 0.7) !important;
        border: 1px solid #475569 !important;
        border-radius: 12px !important;
        padding: 15px !important;
        color: white !important;
    }
    
    /* Progress bar styling */
    .stProgress>div>div>div>div {
        background: linear-gradient(90deg, #10B981 0%, #0EA5E9 100%) !important;
    }
    
    /* Table styling */
    .dataframe {
        background-color: rgba(30, 41, 59, 0.8) !important;
        color: white !important;
        border-radius: 10px;
        overflow: hidden;
    }
    
    .dataframe thead th {
        background-color: #1e293b !important;
        color: white !important;
        font-weight: 600;
        padding: 12px;
        border-bottom: 2px solid #334155;
    }
    
    .dataframe tbody tr {
        background-color: rgba(30, 41, 59, 0.6) !important;
        color: white !important;
        transition: all 0.2s ease;
    }
    
    .dataframe tbody tr:hover {
        background-color: rgba(51, 65, 85, 0.8) !important;
        transform: translateY(-1px);
    }
    
    .dataframe tbody td {
        color: white !important;
        padding: 10px 12px;
        border-bottom: 1px solid #334155;
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(90deg, rgba(14,165,233,0.2) 0%, rgba(99,102,241,0.2) 100%);
        padding: 12px 20px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 4px solid #0EA5E9;
    }
    
    /* Custom containers */
    .custom-container {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid #475569;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
    }
    
    /* Beautiful table enhancements */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    
    .stDataFrame table {
        background: transparent !important;
    }

    /* Custom beautiful table styling */
    .beautiful-table {
        background: rgba(30, 41, 59, 0.9) !important;
        border-radius: 15px !important;
        overflow: hidden !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(10px) !important;
        margin: 20px 0 !important;
    }
    
    .beautiful-table thead {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.4) 0%, rgba(99, 102, 241, 0.4) 100%) !important;
        backdrop-filter: blur(10px) !important;
        border-bottom: 2px solid rgba(14, 165, 233, 0.6) !important;
    }
    
    .beautiful-table th {
        padding: 16px 20px !important;
        text-align: left !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        color: white !important;
        border: none !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        font-family: Arial, sans-serif !important;
    }
    
    .beautiful-table tbody tr {
        background-color: rgba(30, 41, 59, 0.5) !important;
        transition: all 0.3s ease !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    .beautiful-table tbody tr:nth-child(even) {
        background-color: rgba(30, 41, 59, 0.7) !important;
    }
    
    .beautiful-table tbody tr:hover {
        background-color: rgba(51, 65, 85, 0.8) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 20px rgba(14, 165, 233, 0.3) !important;
        border-left: 3px solid #0EA5E9 !important;
    }
    
    .beautiful-table td {
        padding: 14px 20px !important;
        border: none !important;
        font-size: 13px !important;
        font-weight: 400 !important;
        color: white !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        font-family: Arial, sans-serif !important;
    }
    
    .beautiful-table td:first-child {
        font-weight: 500 !important;
        color: #0EA5E9 !important;
    }
    
    .wellness-excellent {
        background-color: rgba(16, 185, 129, 0.3) !important;
        color: white !important;
        font-weight: 600 !important;
    }
    
    .wellness-good {
        background-color: rgba(245, 158, 11, 0.3) !important;
        color: white !important;
        font-weight: 600 !important;
    }
    
    .wellness-poor {
        background-color: rgba(239, 68, 68, 0.3) !important;
        color: white !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

def metric_card(icon, label, value, delta=None, delta_color="normal"):
    colors = {
        "normal": "#10B981",
        "inverse": "#EF4444",
        "neutral": "#6B7280"
    }
    
    delta_html = f"<span style='color: {colors[delta_color]}; font-size: 14px;'>{delta}</span>" if delta else ""
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(30,41,59,0.8) 0%, rgba(15,23,42,0.8) 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease;
    ">
        <div style="font-size: 24px; margin-bottom: 0.5rem;">{icon}</div>
        <div style="color: #94A3B8; font-size: 12px; margin-bottom: 0.5rem;">{label}</div>
        <div style="color: white; font-size: 20px; font-weight: 600; margin-bottom: 0.25rem;">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def wellness_gauge(score):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Wellness Score", 'font': {'color': 'white', 'size': 20}},
        delta = {'reference': 50, 'increasing': {'color': "#10B981"}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "#0EA5E9"},
            'bgcolor': "rgba(255,255,255,0.1)",
            'borderwidth': 2,
            'bordercolor': "#334155",
            'steps': [
                {'range': [0, 40], 'color': '#EF4444'},
                {'range': [40, 70], 'color': '#F59E0B'},
                {'range': [70, 100], 'color': '#10B981'}],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': 90}}))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white", 'family': "Arial"},
        height=300,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    return fig

# ==========================
# Simpan Data User
# ==========================
def save_user_data(user_input, predicted_wellness):
    try:
        # Format date sebagai string untuk konsistensi
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df_new = pd.DataFrame([{
            "date": current_date,
            "screen_time_hours": user_input[0][0],
            "work_screen_hours": user_input[0][1],
            "leisure_screen_hours": user_input[0][2],
            "sleep_hours": user_input[0][3],
            "sleep_quality": user_input[0][4],
            "stress_level": user_input[0][5],
            "productivity": user_input[0][6],
            "predicted_wellness": predicted_wellness
        }])

        # Simpan ke CSV
        if not os.path.exists(CSV_FILE):
            df_new.to_csv(CSV_FILE, index=False)
        else:
            # Append ke file existing
            df_new.to_csv(CSV_FILE, mode='a', header=False, index=False)
        
        # Force reload data dari CSV
        st.session_state.df_user_history = load_user_data()
        
        st.success("✅ Data harian berhasil disimpan!")
        return True
    except Exception as e:
        st.error(f"⚠️ Gagal menyimpan data: {e}")
        return False

# ==========================
# Load Data User
# ==========================
def load_user_data():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            # Pastikan kolom date dalam format datetime
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'], errors='coerce')
                # Hapus row dengan date invalid
                df = df.dropna(subset=['date'])
                # Sort by date descending untuk memastikan data terbaru di atas
                df = df.sort_values('date', ascending=False)
            return df
        except Exception as e:
            st.warning(f"⚠️ Gagal membaca file CSV: {e}")
            return pd.DataFrame()
    else:
        return pd.DataFrame()

# ==========================
# Create Beautiful HTML Table Function
# ==========================
def create_beautiful_html_table(df):
    """Create a beautiful HTML table with custom styling"""
    
    # Start building the HTML
    html = """
    <div class="beautiful-table">
        <table style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr>
    """
    
    # Add header columns
    for col in df.columns:
        html += f'<th>{col}</th>'
    
    html += """
                </tr>
            </thead>
            <tbody>
    """
    
    # Add data rows
    for idx, row in df.iterrows():
        html += '<tr>'
        
        for col_idx, (col_name, value) in enumerate(row.items()):
            # Apply special formatting for wellness score
            if 'Wellness Score' in col_name:
                try:
                    score = float(value)
                    if score >= 80:
                        cell_class = "wellness-excellent"
                    elif score >= 60:
                        cell_class = "wellness-good"
                    else:
                        cell_class = "wellness-poor"
                except:
                    cell_class = ""
            else:
                cell_class = ""
                
            html += f'<td class="{cell_class}">{value}</td>'
        
        html += '</tr>'
    
    html += """
            </tbody>
        </table>
    </div>
    """
    
    return html

# ==========================
# Main Tab Function 
# ==========================
def run(model):
    apply_custom_css()
    
    # --------------------------
    # Header dengan Gradient
    # --------------------------
    st.markdown(
        """
        <div style='
            background: linear-gradient(135deg, #0EA5E9 0%, #6366F1 100%);
            padding: 2rem;
            border-radius: 16px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 8px 25px rgba(14,165,233,0.3);
        '>
            <h1 style='color: white; margin: 0; font-size: 2.5rem;'>💓 Pulse Check</h1>
            <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem; margin: 0.5rem 0;'>
                Pantau kesejahteraan mental harianmu secara real-time
            </p>
            <p style='color: rgba(255,255,255,0.8); font-style: italic; margin: 0;'>
                Semakin mendekati skor 100 berarti kesejahteraan mentalmu semakin baik 🧠✨
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------
    # Initialize Session State
    # --------------------------
    if "df_user_history" not in st.session_state:
        st.session_state.df_user_history = load_user_data()
    
    if "screen_time_hours" not in st.session_state:
        st.session_state.screen_time_hours = 8.0
    if "work_screen_hours" not in st.session_state:
        st.session_state.work_screen_hours = 4.0
    if "leisure_screen_hours" not in st.session_state:
        st.session_state.leisure_screen_hours = 4.0
    if "sleep_hours" not in st.session_state:
        st.session_state.sleep_hours = 7.0
    if "sleep_quality" not in st.session_state:
        st.session_state.sleep_quality = 8
    if "stress_level" not in st.session_state:
        st.session_state.stress_level = 5
    if "productivity" not in st.session_state:
        st.session_state.productivity = 70

    # --------------------------
    # Layout Columns
    # --------------------------
    col1, col2 = st.columns([2, 1])

    with col1:
        # --------------------------
        # Input Section
        # --------------------------
        st.markdown("""
        <div class='section-header'>
            <h3 style='color: white; margin: 0;'>📊 Input Data Harian</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown("#### ⏱️ Waktu Layar")
            screen_col1, screen_col2, screen_col3 = st.columns(3)
            
            with screen_col1:
                screen_time_hours = st.number_input(
                    "Total Waktu Layar (jam)",
                    min_value=0.0,
                    max_value=20.0,
                    value=st.session_state.screen_time_hours,
                    step=0.5,
                    help="Total waktu menggunakan gadget dalam sehari",
                    key="screen_time_input"
                )
                st.session_state.screen_time_hours = screen_time_hours
            
            with screen_col2:
                work_screen_hours = st.number_input(
                    "Waktu Kerja (jam)",
                    min_value=0.0,
                    max_value=12.0,
                    value=st.session_state.work_screen_hours,
                    step=0.5,
                    help="Waktu layar untuk pekerjaan/produktif",
                    key="work_screen_input"
                )
                st.session_state.work_screen_hours = work_screen_hours
            
            with screen_col3:
                leisure_screen_hours = st.number_input(
                    "Waktu Hiburan (jam)",
                    min_value=0.0,
                    max_value=12.0,
                    value=st.session_state.leisure_screen_hours,
                    step=0.5,
                    help="Waktu layar untuk hiburan/sosial media",
                    key="leisure_screen_input"
                )
                st.session_state.leisure_screen_hours = leisure_screen_hours

        with st.container():
            st.markdown("#### 😴 Kualitas Tidur")
            sleep_col1, sleep_col2 = st.columns(2)
            
            with sleep_col1:
                sleep_hours = st.number_input(
                    "Jam Tidur",
                    min_value=0.0,
                    max_value=12.0,
                    value=st.session_state.sleep_hours,
                    step=0.5,
                    help="Durasi tidur dalam jam",
                    key="sleep_hours_input"
                )
                st.session_state.sleep_hours = sleep_hours
            
            with sleep_col2:
                sleep_quality = st.slider(
                    "Kualitas Tidur (1-10)",
                    1, 10, st.session_state.sleep_quality,
                    help="Seberapa baik kualitas tidurmu?",
                    key="sleep_quality_input"
                )
                st.session_state.sleep_quality = sleep_quality

        with st.container():
            st.markdown("#### 🎯 Performa Harian")
            perf_col1, perf_col2 = st.columns(2)
            
            with perf_col1:
                stress_level = st.slider(
                    "Tingkat Stres (0-10)",
                    0, 10, st.session_state.stress_level,
                    help="Tingkat stres yang dirasakan hari ini",
                    key="stress_level_input"
                )
                st.session_state.stress_level = stress_level
            
            with perf_col2:
                productivity = st.slider(
                    "Produktivitas (0-100)",
                    0, 100, st.session_state.productivity,
                    help="Seberapa produktif hari ini?",
                    key="productivity_input"
                )
                st.session_state.productivity = productivity

        # --------------------------
        # Calculate Button
        # --------------------------
        calculate_col1, calculate_col2 = st.columns([2, 1])
        
        with calculate_col1:
            if st.button("🔍 Hitung Wellness Score", use_container_width=True, key="calculate_btn"):
                user_input = np.array([[ 
                    st.session_state.screen_time_hours,
                    st.session_state.work_screen_hours,
                    st.session_state.leisure_screen_hours,
                    st.session_state.sleep_hours,
                    st.session_state.sleep_quality,
                    st.session_state.stress_level,
                    st.session_state.productivity
                ]])

                try:
                    predicted_wellness = model.predict(user_input)[0]
                    st.session_state.predicted_wellness = float(predicted_wellness)
                    st.session_state.user_input = user_input
                    st.success(f"🎉 Wellness Score: {predicted_wellness:.1f}")
                except Exception as e:
                    st.error(f"⚠️ Prediksi gagal: {e}")
                    st.session_state.predicted_wellness = 0.0

    with col2:
        # --------------------------
        # Wellness Score Display
        # --------------------------
        st.markdown("""
        <div class='section-header'>
            <h3 style='color: white; margin: 0;'>🎯 Wellness Score</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if "predicted_wellness" in st.session_state:
            score = st.session_state.predicted_wellness
            
            # Gauge Chart
            fig = wellness_gauge(score)
            st.plotly_chart(fig, use_container_width=True)
            
            # Score Interpretation
            if score >= 80:
                st.success("**🎉 Excellent!** Kesejahteraan mentalmu sangat baik!")
            elif score >= 60:
                st.info("**👍 Good!** Tetap pertahankan kebiasaan sehatmu!")
            elif score >= 40:
                st.warning("**💡 Needs Improvement** Ada beberapa area yang bisa ditingkatkan")
            else:
                st.error("**🚨 Attention Needed** Perlu perhatian lebih pada kebiasaan digital")
            
            # Save Button
            if st.button("💾 Simpan Data Hari Ini", use_container_width=True, key="save_btn"):
                if save_user_data(st.session_state.user_input, st.session_state.predicted_wellness):
                    st.rerun()
        else:
            st.markdown("""
            <div style='
                background: rgba(30,41,59,0.7);
                border: 2px dashed #475569;
                border-radius: 12px;
                padding: 3rem 1rem;
                text-align: center;
                color: #94A3B8;
            '>
                <div style='font-size: 48px; margin-bottom: 1rem;'>📊</div>
                <p style='color: #94A3B8;'>Isi data harian dan klik <strong>"Hitung Wellness Score"</strong> untuk melihat hasil analisis</p>
            </div>
            """, unsafe_allow_html=True)

    # --------------------------
    # Quick Insights
    # --------------------------
    if "predicted_wellness" in st.session_state:
        st.markdown("---")
        st.markdown("### 🔍 Insights & Rekomendasi")
        
        insights = []
        recommendations = []
        
        # Screen time analysis
        if st.session_state.screen_time_hours > 10:
            insights.append("📱 Waktu layar tinggi")
            recommendations.append("Coba kurangi waktu layar 1-2 jam per hari")
        elif st.session_state.screen_time_hours < 4:
            insights.append("📱 Waktu layar optimal")
            recommendations.append("Pertahankan kebiasaan screen time yang sehat!")
        
        # Sleep analysis
        if st.session_state.sleep_hours < 6:
            insights.append("😴 Tidur kurang optimal")
            recommendations.append("Targetkan 7-9 jam tidur per malam")
        elif st.session_state.sleep_hours >= 7:
            insights.append("😴 Tidur cukup")
            recommendations.append("Kualitas tidurmu baik, pertahankan!")
        
        # Stress analysis
        if st.session_state.stress_level > 7:
            insights.append("⚠️ Stres tinggi")
            recommendations.append("Coba teknik relaksasi atau meditasi")
        elif st.session_state.stress_level < 4:
            insights.append("😊 Stres terkendali")
            recommendations.append("Bagus! Stresmu terkendali dengan baik")
        
        # Productivity analysis
        if st.session_state.productivity > 85:
            insights.append("🚀 Produktivitas tinggi")
            recommendations.append("Jangan lupa istirahat di sela produktivitas")
        
        # Display insights in columns
        if insights:
            insight_cols = st.columns(2)
            with insight_cols[0]:
                st.markdown("#### 📈 Observations")
                for insight in insights:
                    st.markdown(f"- {insight}")
            
            with insight_cols[1]:
                st.markdown("#### 💡 Recommendations")
                for rec in recommendations:
                    st.markdown(f"- {rec}")
        else:
            st.info("✨ Semua aspek seimbang! Pertahankan kebiasaan sehatmu.")

    # --------------------------
    # Historical Data - DENGAN TABEL SUPER CANTIK
    # --------------------------
    df_user_history = st.session_state.df_user_history
    
    if not df_user_history.empty:
        st.markdown("---")
        st.markdown("### 📈 Riwayat Wellness")
        
        try:
            # Validasi data sebelum diproses
            if 'predicted_wellness' not in df_user_history.columns:
                st.warning("⚠️ Kolom 'predicted_wellness' tidak ditemukan dalam data.")
                return
            
            # Pastikan tidak ada nilai NaN di predicted_wellness
            df_valid = df_user_history.dropna(subset=['predicted_wellness']).copy()
            
            if df_valid.empty:
                st.info("📊 Data wellness score masih kosong. Simpan data untuk melihat riwayat.")
                return
            
            # Ambil 5 entri teratas (karena sudah di-sort descending)
            df_display = df_valid.head(5).copy()
            
            if not df_display.empty:
                # Metrics for quick overview
                st.markdown("#### 📊 Ringkasan Terkini")
                metric_cols = st.columns(4)
                
                with metric_cols[0]:
                    latest_score = df_display.iloc[0]['predicted_wellness']
                    if pd.notna(latest_score):
                        metric_card("🎯", "Score Terakhir", f"{latest_score:.1f}")
                    else:
                        metric_card("🎯", "Score Terakhir", "N/A")
                
                with metric_cols[1]:
                    avg_score = df_display['predicted_wellness'].mean()
                    if pd.notna(avg_score):
                        metric_card("📈", "Rata-rata", f"{avg_score:.1f}")
                    else:
                        metric_card("📈", "Rata-rata", "N/A")
                
                with metric_cols[2]:
                    if len(df_display) > 1:
                        current_score = df_display.iloc[0]['predicted_wellness']
                        previous_score = df_display.iloc[1]['predicted_wellness']
                        if pd.notna(current_score) and pd.notna(previous_score):
                            trend = "🔼" if current_score > previous_score else "🔽"
                        else:
                            trend = "➡️"
                    else:
                        trend = "➡️"
                    metric_card("📊", "Trend", trend)
                
                with metric_cols[3]:
                    best_score = df_display['predicted_wellness'].max()
                    if pd.notna(best_score):
                        metric_card("⭐", "Terbaik", f"{best_score:.1f}")
                    else:
                        metric_card("⭐", "Terbaik", "N/A")

                # DETAILED TABLE - SUPER CANTIK DENGAN HTML CUSTOM
                st.write("")
                st.markdown("#### 📋 Data Detail (5 Entri Terakhir)")
                
                # Prepare display dataframe
                display_df = df_display.copy()
                
                # Format date for display only
                display_df['date_display'] = display_df['date'].dt.strftime('%Y-%m-%d %H:%M')
                
                # Select and reorder columns for display
                display_columns = ['date_display', 'screen_time_hours', 'work_screen_hours', 
                                  'leisure_screen_hours', 'sleep_hours', 'sleep_quality', 
                                  'stress_level', 'productivity', 'predicted_wellness']
                
                # Filter hanya kolom yang ada
                available_columns = [col for col in display_columns if col in display_df.columns]
                display_df = display_df[available_columns]
                
                # Rename columns for better display
                column_mapping = {
                    'date_display': '📅 Tanggal',
                    'screen_time_hours': '📱 Total Layar',
                    'work_screen_hours': '💼 Layar Kerja', 
                    'leisure_screen_hours': '🎮 Layar Hiburan',
                    'sleep_hours': '😴 Jam Tidur',
                    'sleep_quality': '⭐ Kualitas Tidur',
                    'stress_level': '😰 Tingkat Stres',
                    'productivity': '🚀 Produktivitas',
                    'predicted_wellness': '💓 Wellness Score'
                }
                
                # Hanya rename kolom yang ada
                final_columns = {}
                for old_col, new_col in column_mapping.items():
                    if old_col in display_df.columns:
                        final_columns[old_col] = new_col
                
                display_df = display_df.rename(columns=final_columns)
                
                # Format nilai numerik dengan satuan
                for col in display_df.columns:
                    if any(x in col for x in ['Layar', 'Jam Tidur']):
                        display_df[col] = display_df[col].apply(lambda x: f"{x:.1f} jam" if pd.notna(x) else "N/A")
                    elif any(x in col for x in ['Kualitas Tidur', 'Tingkat Stres']):
                        display_df[col] = display_df[col].apply(lambda x: f"{x:.0f}/10" if pd.notna(x) else "N/A")
                    elif 'Produktivitas' in col:
                        display_df[col] = display_df[col].apply(lambda x: f"{x:.0f}%" if pd.notna(x) else "N/A")
                    elif 'Wellness Score' in col:
                        display_df[col] = display_df[col].apply(lambda x: f"{x:.1f}" if pd.notna(x) else "N/A")
                
                # Create and display beautiful HTML table
                html_table = create_beautiful_html_table(display_df)
                st.markdown(html_table, unsafe_allow_html=True)
                
                # PROGRESS CHART
                st.markdown("---")
                st.markdown("#### 📊 Progress Chart")
                
                # Untuk chart, kita butuh data dalam urutan ascending
                chart_df = df_display.sort_values('date', ascending=True).copy()
                
                # Pastikan data untuk chart valid
                if len(chart_df) > 0 and 'predicted_wellness' in chart_df.columns:
                    fig = px.line(
                        chart_df,
                        x='date',
                        y='predicted_wellness',
                        title="Trend Wellness Score",
                        markers=True,
                        line_shape='spline',
                        color_discrete_sequence=['#0EA5E9']
                    )
                    
                    # Update traces for better styling
                    fig.update_traces(
                        line=dict(width=4),
                        marker=dict(
                            size=8,
                            color='#0EA5E9',
                            line=dict(width=2, color='white')
                        ),
                        hovertemplate=(
                            "<b>Tanggal:</b> %{x}<br>"
                            "<b>Wellness Score:</b> %{y:.1f}<extra></extra>"
                        )
                    )
                    
                    # Update layout for white text and beautiful design
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white', family='Arial'),
                        title=dict(
                            text="Trend Wellness Score",
                            x=0.5,
                            font=dict(size=20, color='white')
                        ),
                        xaxis=dict(
                            title="Tanggal",
                            title_font=dict(size=14, color='white'),
                            tickfont=dict(size=12, color='white'),
                            gridcolor='rgba(255,255,255,0.1)',
                            linecolor='rgba(255,255,255,0.3)',
                            showline=True
                        ),
                        yaxis=dict(
                            title="Wellness Score",
                            title_font=dict(size=14, color='white'),
                            tickfont=dict(size=12, color='white'),
                            gridcolor='rgba(255,255,255,0.1)',
                            linecolor='rgba(255,255,255,0.3)',
                            showline=True,
                            range=[0, 100]
                        ),
                        hoverlabel=dict(
                            bgcolor='rgba(30,41,59,0.9)',
                            bordercolor='#0EA5E9',
                            font=dict(color='white')
                        ),
                        showlegend=False,
                        height=400,
                        margin=dict(l=50, r=50, t=80, b=50)
                    )
                    
                    # Add target line
                    fig.add_hline(
                        y=70, 
                        line_dash="dash", 
                        line_color="#10B981",
                        annotation_text="Target Baik", 
                        annotation_font=dict(color="#10B981"),
                        annotation_position="right"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("📈 Data tidak cukup untuk menampilkan progress chart")
                    
            else:
                st.info("📊 Data yang valid tidak ditemukan. Pastikan data wellness score sudah tersimpan.")
                
        except Exception as e:
            st.error(f"⚠️ Error dalam menampilkan data historis: {str(e)}")
    else:
        st.markdown("---")
        st.markdown("### 📈 Riwayat Wellness")
        st.info("📊 Belum ada data yang tersimpan. Simpan data pertama Anda untuk melihat riwayat.")

if __name__ == "__main__":
    # For testing purposes
    class MockModel:
        def predict(self, X):
            return np.array([75.5])
    
    run(MockModel())