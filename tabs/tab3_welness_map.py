# tab3_wellness_map.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def apply_wellness_css():
    st.markdown("""
    <style>
    /* Main background */
    .main .block-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding-top: 2rem;
    }
    
    /* Wellness Card Styling */
    .wellness-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        margin: 0.5rem 0 !important;
        text-align: center !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .wellness-card::before {
        content: '' !important;
        position: absolute !important;
        left: 0 !important;
        top: 0 !important;
        bottom: 0 !important;
        width: 5px !important;
        background: var(--card-color, #0EA5E9) !important;
    }
    
    .wellness-card:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 12px 40px rgba(14, 165, 233, 0.2) !important;
        border-color: rgba(14, 165, 233, 0.3) !important;
    }
    
    .wellness-card * {
        color: white !important;
    }
    
    .wellness-card h4 {
        color: white !important;
        margin: 0.5rem 0 !important;
        font-weight: 600 !important;
    }
    
    .wellness-card .value {
        font-size: 1.8rem !important;
        font-weight: bold !important;
        margin: 0.5rem 0 !important;
        color: var(--card-color, #0EA5E9) !important;
    }
    
    .wellness-card .description {
        color: #e2e8f0 !important;
        font-size: 0.9rem !important;
        margin: 0 !important;
        opacity: 0.9 !important;
    }
    
    .wellness-icon {
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3) !important;
        display: block !important;
    }
    
    /* Insight Card Styling */
    .insight-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        margin: 0.5rem 0 !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }
    
    .insight-card:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(14, 165, 233, 0.15) !important;
    }
    
    .insight-card * {
        color: white !important;
    }
    
    /* Tip Card Styling */
    .tip-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        margin: 0.3rem 0 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
        border-left: 4px solid var(--tip-color, #0EA5E9) !important;
    }
    
    .tip-card:hover {
        transform: translateX(5px) !important;
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.1) !important;
    }
    
    .tip-card * {
        color: white !important;
    }
    
    /* Section Headers */
    .section-header {
        color: white !important;
        margin: 2rem 0 1rem 0 !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Gauge Container - DIPERBAIKI */
    .gauge-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        margin: 0.5rem 0 !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(10px) !important;
        text-align: center !important;
    }
    
    .gauge-title {
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 0.5rem !important;
    }
    
    /* Action Plan Cards */
    .action-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        margin: 0.5rem 0 !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(10px) !important;
        height: 100% !important;
        transition: all 0.3s ease !important;
    }
    
    .action-card:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 40px rgba(14, 165, 233, 0.15) !important;
    }
    
    .action-card * {
        color: white !important;
    }
    
    .action-card h4 {
        color: white !important;
        margin-bottom: 1rem !important;
        text-align: center !important;
        font-weight: 600 !important;
    }
    
    /* Custom Streamlit Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        color: white !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 0 0 8px 8px !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

def wellness_card(icon, title, value, description, color="#0EA5E9"):
    st.markdown(f"""
    <div class="wellness-card" style="--card-color: {color}">
        <div class="wellness-icon">{icon}</div>
        <h4>{title}</h4>
        <div class="value" style="color: {color} !important;">{value}</div>
        <p class="description">{description}</p>
    </div>
    """, unsafe_allow_html=True)

def insight_card(title, content, icon="💡", color="#0EA5E9"):
    st.markdown(f"""
    <div class="insight-card" style="border-left: 4px solid {color}">
        <div style="display: flex; align-items: flex-start; gap: 12px;">
            <span style="font-size: 24px; margin-top: 2px;">{icon}</span>
            <div>
                <h4 style="margin: 0 0 8px 0; color: white !important;">{title}</h4>
                <p style="margin: 0; color: #e2e8f0 !important; font-size: 14px; line-height: 1.5;">{content}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def tip_card(content, color="#0EA5E9"):
    st.markdown(f"""
    <div class="tip-card" style="--tip-color: {color}">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 14px; color: #e2e8f0 !important;">{content}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def action_plan_card(title, items, icon="🎯", color="#0EA5E9"):
    items_html = "".join([f'<li style="margin-bottom: 8px; color: #e2e8f0 !important;">{item}</li>' for item in items])
    
    st.markdown(f"""
    <div class="action-card">
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
            <h4>{title}</h4>
        </div>
        <ul style="margin: 0; padding-left: 1.2rem; color: #e2e8f0 !important;">
            {items_html}
        </ul>
    </div>
    """, unsafe_allow_html=True)

def comparison_gauge(user_value, avg_value, max_value, title, color="#0EA5E9", reverse=False):
    # PERBAIKAN: Hitung persentase dengan benar
    if reverse:
        # Untuk metrik yang lebih rendah lebih baik (screen time, stres)
        user_percent = ((max_value - user_value) / max_value) * 100
        avg_percent = ((max_value - avg_value) / max_value) * 100
    else:
        # Untuk metrik yang lebih tinggi lebih baik (tidur, olahraga)
        user_percent = (user_value / max_value) * 100
        avg_percent = (avg_value / max_value) * 100
    
    # Batasi persentase antara 0-100
    user_percent = max(0, min(100, user_percent))
    avg_percent = max(0, min(100, avg_percent))
    
    # Tentukan warna berdasarkan performa
    if reverse:
        # Untuk metrik yang lebih rendah lebih baik (screen time, stres)
        if user_value < avg_value:
            gauge_color = "#10B981"  # Hijau - lebih baik
        elif user_value > avg_value:
            gauge_color = "#EF4444"  # Merah - lebih buruk
        else:
            gauge_color = "#0EA5E9"  # Biru - sama
    else:
        # Untuk metrik yang lebih tinggi lebih baik (tidur, olahraga)
        if user_value > avg_value:
            gauge_color = "#10B981"  # Hijau - lebih baik
        elif user_value < avg_value:
            gauge_color = "#EF4444"  # Merah - lebih buruk
        else:
            gauge_color = "#0EA5E9"  # Biru - sama
    
    fig = go.Figure()
    
    # Add user value
    fig.add_trace(go.Indicator(
        mode = "gauge+number+delta",
        value = user_percent,
        delta = {'reference': avg_percent, 'relative': True, 'valueformat': '.1%', 'font': {'size': 14}},
        number = {'font': {'size': 20, 'color': 'white'}},
        domain = {'x': [0.1, 0.9], 'y': [0.2, 0.9]},
        title = {'text': f"<span style='font-size:14px;color:white'>{title}</span><br><span style='font-size:12px;color:#94a3b8'>vs Rata-rata</span>", 'font': {'size': 1}},
        gauge = {
            'axis': {
                'range': [None, 100], 
                'tickwidth': 1, 
                'tickcolor': "white", 
                'tickfont': {'color': 'white', 'size': 10}
            },
            'bar': {'color': gauge_color, 'thickness': 0.3},
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
        height=280,
        margin=dict(l=40, r=40, t=80, b=40),
        font={'color': 'white', 'family': "Arial"},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def run(df=None, model=None):
    # Apply custom CSS
    apply_wellness_css()

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
        <h1 style='color: white; margin: 0; font-size: 3rem; font-weight: 700;'>🧠 Mental Wellness Map</h1>
        <p style='color: rgba(255,255,255,0.95); font-size: 1.3rem; margin: 1rem 0; font-weight: 300;'>
            Visualisasikan & Analisis Pola Kesejahteraan Mental Anda
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
            <span style='color: #10B981; font-weight: bold;'>🟢 Optimal</span>
            <span style='color: #F59E0B; font-weight: bold;'>🟡 Sedang</span>
            <span style='color: #EF4444; font-weight: bold;'>🔴 Perlu Perhatian</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ==========================
    # Ambil data user dari st.session_state
    # ==========================
    user_data = {
        "Total Waktu Layar": st.session_state.get('screen_time_hours', 8),
        "Waktu Layar Kerja": st.session_state.get('work_screen_hours', 4),
        "Waktu Layar Hiburan": st.session_state.get('leisure_screen_hours', 4),
        "Jam Tidur": st.session_state.get('sleep_hours', 7),
        "Kualitas Tidur": st.session_state.get('sleep_quality', 4),
        "Menit Olahraga": st.session_state.get('exercise_minutes', 150),
        "Jam Bersosialisasi": st.session_state.get('social_hours', 10),
        "Tingkat Stres": st.session_state.get('stress_level', 5),
        "Produktivitas": st.session_state.get('productivity', 70)
    }
    predicted_wellness = st.session_state.get('predicted_wellness', None)

    # ==========================
    # Wellness Overview Cards
    # ==========================
    st.markdown('<div class="section-header"><h3>📊 Ringkasan Wellness Anda</h3></div>', unsafe_allow_html=True)
    
    if predicted_wellness:
        wellness_cols = st.columns(4)
        with wellness_cols[0]:
            wellness_card("🎯", "Wellness Score", f"{predicted_wellness:.1f}", 
                         "Skor Kesejahteraan Mental", "#0EA5E9")
        with wellness_cols[1]:
            status = "Optimal" if predicted_wellness >= 80 else "Baik" if predicted_wellness >= 60 else "Perlu Perhatian"
            color = "#10B981" if predicted_wellness >= 80 else "#F59E0B" if predicted_wellness >= 60 else "#EF4444"
            wellness_card("📈", "Status", status, "Kondisi Kesehatan Mental", color)
        with wellness_cols[2]:
            stress_status = "Rendah" if user_data["Tingkat Stres"] <= 4 else "Sedang" if user_data["Tingkat Stres"] <= 7 else "Tinggi"
            stress_color = "#10B981" if user_data["Tingkat Stres"] <= 4 else "#F59E0B" if user_data["Tingkat Stres"] <= 7 else "#EF4444"
            wellness_card("😌", "Tingkat Stres", stress_status, f"Skor: {user_data['Tingkat Stres']}/10", stress_color)
        with wellness_cols[3]:
            sleep_status = "Optimal" if user_data["Jam Tidur"] >= 7 else "Kurang"
            sleep_color = "#10B981" if user_data["Jam Tidur"] >= 7 else "#EF4444"
            wellness_card("😴", "Kualitas Tidur", sleep_status, f"{user_data['Jam Tidur']} jam", sleep_color)

    # ==========================
    # Main Analysis Section
    # ==========================
    analysis_cols = st.columns([2, 1])

    with analysis_cols[0]:
        # ==========================
        # Radar Chart yang Dipercantik
        # ==========================
        st.markdown('<div class="section-header"><h3>🎯 Profil Wellness Radar</h3></div>', unsafe_allow_html=True)
        
        radar_categories = ['Screen Time', 'Tidur', 'Olahraga', 'Sosialisasi', 'Stres', 'Produktivitas']
        radar_max_values = {
            "Screen Time": 16, "Tidur": 12, "Olahraga": 300, 
            "Sosialisasi": 50, "Stres": 10, "Produktivitas": 100
        }
        
        radar_tooltips = {
            "Screen Time": "🖥️ Ideal: <8 jam/hari. Kurangi waktu layar untuk kesehatan mental lebih baik",
            "Tidur": "😴 Ideal: 7-9 jam/hari. Tidur cukup meningkatkan fokus dan mood",
            "Olahraga": "💪 Ideal: 150+ menit/minggu. Olahraga rutin mengurangi stres",
            "Sosialisasi": "👥 Ideal: 5+ jam/minggu. Interaksi sosial penting untuk wellbeing",
            "Stres": "😌 Ideal: <5/10. Kelola stres dengan teknik relaksasi",
            "Produktivitas": "🎯 Ideal: 70+. Keseimbangan kerja dan istirahat"
        }

        # Calculate normalized values
        radar_user_values = [
            (user_data["Total Waktu Layar"] / radar_max_values["Screen Time"]) * 100,
            (user_data["Jam Tidur"] / radar_max_values["Tidur"]) * 100,
            (user_data["Menit Olahraga"] / radar_max_values["Olahraga"]) * 100,
            (user_data["Jam Bersosialisasi"] / radar_max_values["Sosialisasi"]) * 100,
            (user_data["Tingkat Stres"] / radar_max_values["Stres"]) * 100,
            (user_data["Produktivitas"] / radar_max_values["Produktivitas"]) * 100
        ]

        # Adjust for reverse scales (lower is better)
        radar_user_values[0] = 100 - radar_user_values[0]  # Screen Time
        radar_user_values[4] = 100 - radar_user_values[4]  # Stres

        # Get community averages if available
        if df is not None and not df.empty:
            column_mapping = {
                "Total Waktu Layar": "screen_time_hours",
                "Waktu Layar Kerja": "work_screen_hours",
                "Waktu Layar Hiburan": "leisure_screen_hours",
                "Jam Tidur": "sleep_hours",
                "Kualitas Tidur": "sleep_quality_1_5",
                "Menit Olahraga": "exercise_minutes_per_week",
                "Jam Bersosialisasi": "social_hours_per_week",
                "Tingkat Stres": "stress_level_0_10",
                "Produktivitas": "productivity_0_100"
            }
            avg_data = {k: df[col].mean() if col in df.columns else user_data[k] for k, col in column_mapping.items()}
            
            radar_avg_values = [
                (avg_data["Total Waktu Layar"] / radar_max_values["Screen Time"]) * 100,
                (avg_data["Jam Tidur"] / radar_max_values["Tidur"]) * 100,
                (avg_data["Menit Olahraga"] / radar_max_values["Olahraga"]) * 100,
                (avg_data["Jam Bersosialisasi"] / radar_max_values["Sosialisasi"]) * 100,
                (avg_data["Tingkat Stres"] / radar_max_values["Stres"]) * 100,
                (avg_data["Produktivitas"] / radar_max_values["Produktivitas"]) * 100
            ]
            
            # Adjust for reverse scales
            radar_avg_values[0] = 100 - radar_avg_values[0]  # Screen Time
            radar_avg_values[4] = 100 - radar_avg_values[4]  # Stres
        else:
            radar_avg_values = [50] * 6  # Default average

        # Create radar chart
        fig_radar = go.Figure()

        # Add user area
        fig_radar.add_trace(go.Scatterpolar(
            r=radar_user_values + [radar_user_values[0]],  # Close the polygon
            theta=radar_categories + [radar_categories[0]],
            fill='toself',
            fillcolor='rgba(14, 165, 233, 0.3)',
            line=dict(color='#0EA5E9', width=3),
            name='Profil Anda',
            hovertemplate='<b>%{theta}</b><br>Skor: %{r:.1f}%<br>%{customdata}<extra></extra>',
            customdata=[radar_tooltips[cat] for cat in radar_categories] + [radar_tooltips[radar_categories[0]]]
        ))

        # Add community average area
        fig_radar.add_trace(go.Scatterpolar(
            r=radar_avg_values + [radar_avg_values[0]],
            theta=radar_categories + [radar_categories[0]],
            fill='toself',
            fillcolor='rgba(16, 185, 129, 0.2)',
            line=dict(color='#10B981', width=2, dash='dash'),
            name='Rata-rata Komunitas',
            hovertemplate='<b>%{theta}</b><br>Rata-rata: %{r:.1f}%<extra></extra>'
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=10, color='white'),
                    gridcolor='rgba(255,255,255,0.3)',
                    linecolor='rgba(255,255,255,0.3)'
                ),
                angularaxis=dict(
                    gridcolor='rgba(255,255,255,0.3)',
                    linecolor='rgba(255,255,255,0.3)',
                    tickfont=dict(color='white')
                ),
                bgcolor='rgba(0,0,0,0)'
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                font=dict(color='white')
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=500,
            margin=dict(l=50, r=50, t=50, b=50),
            font=dict(color='white')
        )

        st.plotly_chart(fig_radar, use_container_width=True)

    with analysis_cols[1]:
        # ==========================
        # Quick Insights & Recommendations
        # ==========================
        st.markdown('<div class="section-header"><h3>💡 Insights & Rekomendasi</h3></div>', unsafe_allow_html=True)
        
        insights = []
        recommendations = []
        
        # Screen Time Analysis
        if user_data["Total Waktu Layar"] > 10:
            insights.append("Waktu Layar Tinggi Terdeteksi")
            recommendations.append("Coba teknik Pomodoro: 25 menit kerja fokus, 5 menit istirahat mata. Kurangi screen time hiburan 1 jam per hari.")
        elif user_data["Total Waktu Layar"] < 4:
            insights.append("Keseimbangan Digital Optimal")
            recommendations.append("Pertahankan kebiasaan screen time yang sehat! Anda telah menemukan keseimbangan yang baik antara dunia digital dan kehidupan nyata.")
        
        # Sleep Analysis
        if user_data["Jam Tidur"] < 6:
            insights.append("Kualitas Tidur Perlu Ditingkatkan")
            recommendations.append("Targetkan 7-9 jam tidur dengan rutinitas yang konsisten. Coba digital detox 1 jam sebelum tidur untuk kualitas tidur lebih baik.")
        elif user_data["Jam Tidur"] >= 7:
            insights.append("Pola Tidur Sehat")
            recommendations.append("Kualitas tidurmu baik, pertahankan! Konsistensi adalah kunci untuk kesehatan mental jangka panjang.")
        
        # Stress Analysis
        if user_data["Tingkat Stres"] > 7:
            insights.append("Tingkat Stres Membutuhkan Perhatian")
            recommendations.append("Coba latihan pernapasan 5-5-5 (tarik 5 detik, tahan 5 detik, buang 5 detik) sebanyak 3x sehari. Luangkan waktu untuk aktivitas yang menyenangkan.")
        elif user_data["Tingkat Stres"] < 4:
            insights.append("Manajemen Stres Optimal")
            recommendations.append("Bagus! Anda berhasil mengelola stres dengan baik. Teruskan praktik mindfulness yang sudah dilakukan.")
        
        # Exercise Analysis
        if user_data["Menit Olahraga"] < 150:
            insights.append("Aktivitas Fisik Dapat Ditingkatkan")
            recommendations.append("Targetkan 150 menit olahraga sedang per minggu. Mulai dengan jalan kaki 30 menit, 3x seminggu untuk membangun kebiasaan.")
        else:
            insights.append("Gaya Hidup Aktif")
            recommendations.append("Excellent! Aktivitas fisik yang rutin sangat baik untuk kesehatan mental. Pertahankan konsistensi ini.")

        # Display insights
        for i, (insight, rec) in enumerate(zip(insights, recommendations)):
            color = "#EF4444" if "Perhatian" in insight or "Tinggi" in insight else "#10B981" if "Optimal" in insight or "Sehat" in insight else "#F59E0B"
            icon = "⚠️" if "Perhatian" in insight else "✅" if "Optimal" in insight else "💡"
            
            with st.expander(f"{icon} {insight}", expanded=i<2):
                insight_card(insight, rec, icon, color)

        # Wellness Tips
        st.markdown('<div style="margin: 1.5rem 0 0.5rem 0; color: white; font-size: 1.1rem; font-weight: 600;">🎯 Tips Cepat Wellness</div>', unsafe_allow_html=True)
        
        tips = [
            ("💧 Minum air cukup - dehidrasi dapat mempengaruhi mood dan konsentrasi", "#0EA5E9"),
            ("🌅 10 menit sinar matahari pagi untuk meningkatkan vitamin D dan mood", "#F59E0B"),
            ("📵 Digital detox 1 jam sebelum tidur untuk kualitas tidur optimal", "#8B5CF6"),
            ("🧘 5 menit meditasi harian untuk kejernihan mental dan reduksi stres", "#10B981"),
            ("📱 Atur notifikasi penting saja untuk mengurangi distraksi digital", "#EC4899"),
            ("🎵 Dengarkan musik favorit untuk meningkatkan mood dan relaksasi", "#6366F1")
        ]
        
        for tip_content, tip_color in tips:
            tip_card(tip_content, color=tip_color)

    # ==========================
    # Detailed Comparison Section - DIPERBAIKI BESAR
    # ==========================
    if df is not None and not df.empty:
        st.markdown("---")
        st.markdown('<div class="section-header"><h3>📈 Analisis Komparatif Mendalam</h3></div>', unsafe_allow_html=True)
        
        # Comparison metrics - DIPERBAIKI: Layout yang lebih baik dengan penjelasan
        st.markdown("#### 🎯 Perbandingan Metrik Utama")
        
        # Tambahkan penjelasan tentang gauge chart
        st.markdown("""
        <div class="insight-card" style="margin-bottom: 1.5rem; border-left: 4px solid #0EA5E9">
            <p style="margin: 0; color: #e2e8f0 !important; font-size: 14px;">
                <strong>📊 Cara Membaca Gauge:</strong><br>
                • <span style="color:#10B981">Hijau</span> = Performa lebih baik dari rata-rata<br>
                • <span style="color:#EF4444">Merah</span> = Perlu perhatian (lebih rendah dari rata-rata)<br>
                • <span style="color:#0EA5E9">Biru</span> = Sama dengan rata-rata<br>
                • Angka menunjukkan persentase dari target maksimal
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        comp_cols = st.columns(3)
        
        with comp_cols[0]:
            # Screen Time Gauge - PERBAIKAN: max_value 16 jam (lebih realistis)
            gauge_fig = comparison_gauge(
                user_data["Total Waktu Layar"], 
                avg_data["Total Waktu Layar"],
                16, "Screen Time", "#0EA5E9", reverse=True
            )
            
            # Hitung persentase untuk display
            screen_percent = ((16 - user_data["Total Waktu Layar"]) / 16) * 100
            
            st.markdown("""
            <div class="gauge-container">
                <div class="gauge-title">📱 Screen Time</div>
                <div style="text-align: center; margin: 1rem 0;">
                    <div style="color: #e2e8f0; font-size: 0.9rem;">Anda: <strong>{:.1f} jam/hari</strong></div>
                    <div style="color: #94a3b8; font-size: 0.8rem;">Rata-rata: {:.1f} jam/hari</div>
                    <div style="color: #94a3b8; font-size: 0.8rem; margin-top: 0.5rem;">🟢 Ideal: &lt;8 jam/hari</div>
                    <div style="color: #94a3b8; font-size: 0.7rem; margin-top: 0.3rem;">Persentase: {:.0f}% dari batas maksimal 16 jam</div>
                </div>
            </div>
            """.format(
                user_data['Total Waktu Layar'], 
                avg_data['Total Waktu Layar'],
                screen_percent
            ), unsafe_allow_html=True)
            
            st.plotly_chart(gauge_fig, use_container_width=True, config={'displayModeBar': False})
        
        with comp_cols[1]:
            # Jam Tidur Gauge - PERBAIKAN: max_value 12 jam
            gauge_fig = comparison_gauge(
                user_data["Jam Tidur"],
                avg_data["Jam Tidur"],
                12, "Jam Tidur", "#10B981"
            )
            
            # Hitung persentase untuk display
            sleep_percent = (user_data["Jam Tidur"] / 12) * 100
            
            st.markdown("""
            <div class="gauge-container">
                <div class="gauge-title">😴 Jam Tidur</div>
                <div style="text-align: center; margin: 1rem 0;">
                    <div style="color: #e2e8f0; font-size: 0.9rem;">Anda: <strong>{:.1f} jam/malam</strong></div>
                    <div style="color: #94a3b8; font-size: 0.8rem;">Rata-rata: {:.1f} jam/malam</div>
                    <div style="color: #94a3b8; font-size: 0.8rem; margin-top: 0.5rem;">🟢 Ideal: 7-9 jam/malam</div>
                    <div style="color: #94a3b8; font-size: 0.7rem; margin-top: 0.3rem;">Persentase: {:.0f}% dari target 12 jam</div>
                </div>
            </div>
            """.format(
                user_data['Jam Tidur'], 
                avg_data['Jam Tidur'],
                sleep_percent
            ), unsafe_allow_html=True)
            
            st.plotly_chart(gauge_fig, use_container_width=True, config={'displayModeBar': False})
        
        with comp_cols[2]:
            # Tingkat Stres Gauge - PERBAIKAN: max_value 10
            gauge_fig = comparison_gauge(
                user_data["Tingkat Stres"],
                avg_data["Tingkat Stres"],
                10, "Tingkat Stres", "#F59E0B", reverse=True
            )
            
            # Hitung persentase untuk display
            stress_percent = ((10 - user_data["Tingkat Stres"]) / 10) * 100
            
            st.markdown("""
            <div class="gauge-container">
                <div class="gauge-title">😌 Tingkat Stres</div>
                <div style="text-align: center; margin: 1rem 0;">
                    <div style="color: #e2e8f0; font-size: 0.9rem;">Anda: <strong>{:.1f}/10</strong></div>
                    <div style="color: #94a3b8; font-size: 0.8rem;">Rata-rata: {:.1f}/10</div>
                    <div style="color: #94a3b8; font-size: 0.8rem; margin-top: 0.5rem;">🟢 Ideal: &lt;5/10</div>
                    <div style="color: #94a3b8; font-size: 0.7rem; margin-top: 0.3rem;">Persentase: {:.0f}% dari skala 10</div>
                </div>
            </div>
            """.format(
                user_data['Tingkat Stres'], 
                avg_data['Tingkat Stres'],
                stress_percent
            ), unsafe_allow_html=True)
            
            st.plotly_chart(gauge_fig, use_container_width=True, config={'displayModeBar': False})

        # Detailed comparison table
        st.markdown("#### 📋 Perbandingan Detail dengan Komunitas")
        
        comparison_data = []
        for k in user_data:
            user_val = user_data[k]
            avg_val = avg_data.get(k, user_val)
            diff = user_val - avg_val
            diff_percent = (diff / avg_val * 100) if avg_val != 0 else 0
            
            if k in ["Total Waktu Layar", "Tingkat Stres"]:
                status = "🟢 Lebih Baik" if diff < 0 else "🔴 Perlu Perhatian" if diff > 0 else "🟡 Sama"
                status_color = "#10B981" if diff < 0 else "#EF4444" if diff > 0 else "#F59E0B"
            else:
                status = "🟢 Lebih Baik" if diff > 0 else "🔴 Perlu Perhatian" if diff < 0 else "🟡 Sama"
                status_color = "#10B981" if diff > 0 else "#EF4444" if diff < 0 else "#F59E0B"
            
            comparison_data.append({
                "Metric": k,
                "Anda": f"{user_val:.1f}",
                "Rata-rata": f"{avg_val:.1f}",
                "Perbedaan": f"{diff:+.1f}",
                "Status": status,
                "Status Color": status_color
            })
        
        # Display as custom cards instead of dataframe
        metric_cols = st.columns(2)
        for idx, metric in enumerate(comparison_data):
            with metric_cols[idx % 2]:
                st.markdown(f"""
                <div class="insight-card" style="border-left: 4px solid {metric['Status Color']}">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <h4 style="margin: 0; font-size: 14px;">{metric['Metric']}</h4>
                        <span style="font-size: 18px;">{metric['Status'].split()[0]}</span>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 13px;">
                        <div>
                            <div style="color: #94a3b8 !important;">Nilai Anda</div>
                            <div style="font-weight: bold; color: white !important;">{metric['Anda']}</div>
                        </div>
                        <div>
                            <div style="color: #94a3b8 !important;">Rata-rata</div>
                            <div style="font-weight: bold; color: white !important;">{metric['Rata-rata']}</div>
                        </div>
                    </div>
                    <div style="margin-top: 8px; font-size: 12px; color: {metric['Status Color']} !important;">
                        {metric['Perbedaan']} dari rata-rata
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ==========================
    # Community Wellness Distribution
    # ==========================
    if df is not None and not df.empty and "mental_wellness_index_0_100" in df.columns:
        st.markdown("---")
        st.markdown('<div class="section-header"><h3>🌍 Perspektif Komunitas</h3></div>', unsafe_allow_html=True)
        
        comm_cols = st.columns([2, 1])
        
        with comm_cols[0]:
            avg_wellness = df["mental_wellness_index_0_100"].mean()
            
            fig_violin = px.violin(
                df, 
                y="mental_wellness_index_0_100", 
                box=True, 
                points="all",
                title="Distribusi Kesejahteraan Mental Komunitas"
            )
            
            if predicted_wellness is not None:
                fig_violin.add_hline(
                    y=predicted_wellness, 
                    line_dash="dash", 
                    line_color="red",
                    annotation_text="Skor Anda"
                )
            
            fig_violin.add_hline(
                y=avg_wellness, 
                line_dash="dot", 
                line_color="green",
                annotation_text="Rata-rata Komunitas"
            )
            
            fig_violin.update_layout(
                showlegend=False,
                yaxis_title="Wellness Score",
                xaxis_title="",
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                title_font_color='white'
            )
            
            st.plotly_chart(fig_violin, use_container_width=True)
        
        with comm_cols[1]:
            st.markdown("#### 📊 Posisi Anda dalam Komunitas")
            
            if predicted_wellness:
                percentile = (df["mental_wellness_index_0_100"] < predicted_wellness).mean() * 100
                
                wellness_card("🏆", "Peringkat Komunitas", f"Top {100-percentile:.1f}%", 
                            f"Lebih baik dari {percentile:.1f}% anggota", "#F59E0B")
                
                diff = predicted_wellness - avg_wellness
                diff_color = "#10B981" if diff > 0 else "#EF4444"
                diff_icon = "📈" if diff > 0 else "📉"
                
                wellness_card(diff_icon, "Vs Rata-rata", 
                            f"{diff:+.1f} poin", 
                            f"Rata-rata komunitas: {avg_wellness:.1f}", 
                            diff_color)

    # ==========================
    # Action Plan
    # ==========================
    st.markdown("---")
    st.markdown('<div class="section-header"><h3>🎯 Rencana Aksi Personal</h3></div>', unsafe_allow_html=True)
    
    action_cols = st.columns(3)
    
    with action_cols[0]:
        improvements = []
        if user_data["Total Waktu Layar"] > 10:
            improvements.append("Kurangi screen time 2 jam per hari dengan teknik Pomodoro")
        if user_data["Jam Tidur"] < 7:
            improvements.append("Tambah durasi tidur 1 jam dengan rutinitas sebelum tidur")
        if user_data["Tingkat Stres"] > 7:
            improvements.append("Latihan mindfulness dan pernapasan 10 menit sehari")
        if user_data["Menit Olahraga"] < 150:
            improvements.append("Tambah aktivitas fisik menjadi 150 menit per minggu")
        if not improvements:
            improvements.append("Pertahankan kebiasaan sehat yang sudah dilakukan")
            
        action_plan_card("🚀 Area Perbaikan", improvements, "🚀", "#EF4444")
    
    with action_cols[1]:
        strengths = []
        if user_data["Produktivitas"] > 80:
            strengths.append("Tingkat produktivitas yang sangat baik")
        if user_data["Kualitas Tidur"] >= 4:
            strengths.append("Kualitas tidur yang terjaga dengan baik")
        if user_data["Menit Olahraga"] >= 150:
            strengths.append("Gaya hidup aktif dan rutin berolahraga")
        if user_data["Tingkat Stres"] <= 4:
            strengths.append("Kemampuan manajemen stres yang efektif")
        if not strengths:
            strengths.append("Potensi untuk berkembang di semua area")
            
        action_plan_card("💪 Kekuatan", strengths, "💪", "#10B981")
    
    with action_cols[2]:
        goals = [
            "Screen time maksimal 8 jam per hari",
            "Tidur 7+ jam dengan kualitas optimal setiap malam", 
            "Olahraga minimal 3x seminggu, 30 menit per sesi",
            "Meditasi atau relaksasi 5-10 menit setiap hari",
            "Interaksi sosial minimal 5 jam per minggu"
        ]
        
        action_plan_card("🎯 Goals Mingguan", goals, "🎯", "#0EA5E9")

    # ==========================
    # Final Motivation
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
        <h3 style='color: white; margin: 0 0 1rem 0;'>Perjalanan Menuju Kesejahteraan Mental yang Lebih Baik</h3>
        <p style='color: #e2e8f0; margin: 0; font-size: 1.1rem;'>
            Setiap langkah kecil menuju kebiasaan sehat adalah investasi berharga untuk kesejahteraan mental jangka panjang Anda. 
            Terus pantau progres dan rayakan setiap pencapaian!
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    # For testing
    run()