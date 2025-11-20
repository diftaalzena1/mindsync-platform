# Revised tabs/home_base.py
# Tujuan: memastikan warna per-card (border, icon background, gradient) tidak tertimpa global CSS

import streamlit as st
import pandas as pd
import plotly.express as px


def hex_to_rgb(hex_color: str) -> str:
    """Convert hex color (#RRGGBB or #RGB) to an "r,g,b" string for CSS rgba()."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    try:
        r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    except Exception:
        # fallback to a blue tint
        r, g, b = (14, 165, 233)
    return f"{r},{g},{b}"


def apply_home_css():
    st.markdown("""
    <style>
    /* Main container styling untuk home */
    .main .block-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }

    /* Feature card styling (keystyle tetap, tapi background & border-left DISET inline per-card) */
    .feature-card {
        /* make generic card shell, but don't force background or border colors here */
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 1.2rem !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(6px) !important;
        transition: all 0.24s ease !important;
        height: 100% !important;
        color: white !important;
        overflow: hidden !important;
    }

    .feature-card:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 12px 40px rgba(14, 165, 233, 0.12) !important;
    }

    .feature-card * {
        color: white !important;
    }

    .feature-card h4 {
        color: white !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }

    .feature-card p {
        color: #e2e8f0 !important;
        font-size: 14px !important;
        line-height: 1.5 !important;
        opacity: 0.95 !important;
        margin: 0 !important;
    }

    /* Icon container styling */
    .icon-container {
        width: 70px !important;
        height: 70px !important;
        border-radius: 50% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 auto 1rem auto !important;
        font-size: 28px !important;
        border: 2px solid rgba(255, 255, 255, 0.06) !important;
        backdrop-filter: blur(6px) !important;
    }

    /* Info box styling */
    .info-box {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.12) 0%, rgba(99, 102, 241, 0.08) 100%) !important;
        border-left: 4px solid #0EA5E9 !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        margin: 1.5rem 0 !important;
        color: white !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
    }

    .info-box * {
        color: white !important;
    }

    /* Tip card styling */
    .tip-card {
        background: rgba(30, 41, 59, 0.78) !important;
        padding: 1.2rem !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        text-align: center !important;
        height: 140px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        transition: all 0.24s ease !important;
        backdrop-filter: blur(6px) !important;
    }

    .tip-card:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(14, 165, 233, 0.08) !important;
    }

    .tip-card * {
        color: white !important;
    }

    /* Section headers */
    .section-header {
        color: white !important;
        margin: 2rem 0 1.5rem 0 !important;
    }

    .section-header h3 {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)


def info_box(html_content, icon="💡", bg_color="linear-gradient(135deg, rgba(14, 165, 233, 0.12) 0%, rgba(16, 185, 129, 0.08) 100%)"):
    st.markdown(f"""
    <div class="info-box" style="background: {bg_color} !important;">
        <div style="display: flex; align-items: flex-start; gap: 12px;">
            <span style="font-size: 20px; margin-top: 2px;">{icon}</span>
            <div style="font-size: 15px; line-height: 1.6;">{html_content}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def feature_card(icon, title, description, color="#0EA5E9"):
    """Render a feature card where the visible color accents are set inline
    so they won't be overwritten by global CSS.

    color: hex string like '#0EA5E9'
    """
    rgb = hex_to_rgb(color)
    # subtle gradient using the color and a dark fallback
    card_bg = f"linear-gradient(135deg, rgba({rgb},0.12) 0%, rgba(15,23,42,0.86) 100%)"
    icon_bg = f"rgba({rgb},0.12)"
    icon_border = f"rgba({rgb},0.22)"

    st.markdown(f"""
    <div class="feature-card" style="background: {card_bg} !important; border-left: 4px solid {color} !important;">
        <div style="text-align: center; margin-bottom: 1rem;">
            <div class="icon-container" style="background: {icon_bg} !important; border-color: {icon_border} !important;">
                {icon}
            </div>
        </div>
        <h4 style="text-align: center; margin-bottom: 0.6rem; font-size: 18px;">{title}</h4>
        <p style="text-align: center; margin: 0; font-size: 14px; line-height: 1.5;">{description}</p>
    </div>
    """, unsafe_allow_html=True)


def run(df, metrics, username=None):
    if username is None:
        username = st.session_state.get('username', 'Pengguna')

    # Apply custom CSS untuk home page
    apply_home_css()

    # =========================
    # Header Hero dengan Gradient
    # =========================
    st.markdown(f"""
    <div style="
        text-align: center;
        margin: 2rem 0 3rem 0;
        padding: 2.5rem 2rem;
        background: linear-gradient(135deg, #10B981 0%, #0EA5E9 100%);
        border-radius: 16px;
        color: white;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.18);
    ">
        <div style="font-size: 48px; margin-bottom: 1rem;">👋</div>
        <h1 style="color: white; font-size: 2.5rem; margin-bottom: 0.5rem;">
            Selamat Datang, {username}!
        </h1>
        <h3 style="color: rgba(255,255,255,0.95); font-weight: 400; margin: 0;">
            di MINDSYNC — Your Digital Wellness Companion
        </h3>
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # Fitur Utama MindSync
    # =========================
    st.markdown("### 🚀 Fitur Unggulan MINDSYNC")

    # ------ 3 Kolom ------
    features_cols = st.columns(3)

    with features_cols[0]:
        feature_card(
            "💓",
            "Pulse Check",
            "Monitor kesejahteraan mental harian melalui pencatatan screen time, tidur, stres, dan produktivitas, lalu dapatkan skor wellness berbasis AI lengkap dengan insight otomatis dan tracking.",
            "#0EA5E9",
        )

    with features_cols[1]:
        feature_card(
            "🗺️",
            "Wellness Map",
            "Visualisasi interaktif yang memetakan pola perilaku, emosi, dan aktivitas Anda serta membandingkannya dengan tren komunitas untuk memahami faktor-faktor kunci kesejahteraan mental.",
            "#10B981"
        )

    with features_cols[2]:
        feature_card(
            "⚖️",
            "Life Balance",
            "Planner keseimbangan digital yang menghitung indeks MWI, DSI, dan DBI, dilengkapi dashboard mingguan dan habit planner untuk menjaga pola hidup yang lebih sehat.",
            "#F59E0B"
        )

    st.markdown("---")

    # ------ 2 Kolom ------
    features_cols2 = st.columns(2)

    with features_cols2[0]:
        feature_card(
            "🧭",
            "Wellness Compass",
            "Asesmen digital wellness yang mengukur tingkat FOMO dan pola konsumsi digital, kemudian memberikan rencana aksi personalisasi dan tantangan 7 hari.",
            "#6366F1"
        )

    with features_cols2[1]:
        feature_card(
            "🌱",
            "Growth Journey",
            "Jurnal refleksi dan goal-setting berbasis SMART untuk melacak mood, menuliskan refleksi harian, menetapkan tujuan, dan memantau pertumbuhan mental secara konsisten.",
            "#EC4899"
        )

    # ========================= 
    # Tantangan & Solusi (Feature Cards)
    # =========================
    st.markdown("---")
    st.markdown("### 🌟 Transformasi Wellness Digital Anda")

    ts_cols = st.columns(2)

    with ts_cols[0]:
        feature_card(
            "⚠️",
            "Tantangan Digital Modern",
            "Screen time berlebihan, kualitas tidur menurun akibat blue light, stres karena banjir informasi, penurunan fokus & produktivitas, serta kesulitan menjaga batas sehat antara dunia digital dan kehidupan nyata.",
            "#EF4444"
        )

    with ts_cols[1]:
        feature_card(
            "✨",
            "Solusi MINDSYNC",
            "Pemantauan screen time sehat, rekomendasi rutinitas tidur optimal, latihan mindfulness & digital detox, perencanaan work-life balance personalisasi, serta sistem goal-setting & progress tracking untuk perubahan kebiasaan berkelanjutan.",
            "#10B981"
        )

    # =========================
    # Call to Action
    # =========================
    st.markdown("---")

    info_box(
        """
        <div style="line-height: 1.6;">
            <h4 style="margin: 0 0 8px 0; color: white !important;">🚀 Mulai Perjalanan Wellness Anda!</h4>
            Jelajahi semua fitur MINDSYNC untuk transformasi digital yang lebih sehat — mulai dari <strong>Daily Pulse</strong> untuk monitoring harian, 
            <strong>Wellness Map</strong> untuk memahami pola perilaku, <strong>Life Balance</strong> untuk perencanaan keseimbangan, 
            <strong>Wellness Compass</strong> untuk asesmen digital, hingga <strong>Growth Journey</strong> untuk pengembangan diri yang konsisten.
        </div>
        """,
        "",
        "linear-gradient(135deg, rgba(14, 165, 233, 0.2) 0%, rgba(16, 185, 129, 0.2) 100%)"
    )

    # =========================
    # Quick Tips
    # =========================
    st.markdown("---")
    st.markdown("### 💫 Tips Cepat Hari Ini")

    tips = [
        ("🌅", "Mulai hari tanpa gadget 30 menit setelah bangun tidur", "#0EA5E9"),
        ("⏰", "Setel reminder untuk istirahat mata setiap 45 menit", "#10B981"),
        ("📵", "Digital detox 1 jam sebelum tidur untuk kualitas tidur lebih baik", "#6366F1"),
        ("🎯", "Tetapkan 3 goals produktif harian yang realistis", "#EC4899")
    ]

    tip_cols = st.columns(4)
    for col, (icon, tip, color) in zip(tip_cols, tips):
        with col:
            rgb = hex_to_rgb(color)
            border = f"4px solid {color}"
            bg = f"linear-gradient(135deg, rgba({rgb},0.08) 0%, rgba(15,23,42,0.78) 100%)"
            st.markdown(f"""
            <div class="tip-card" style="border-left: {border} !important; background: {bg} !important;">
                <div style="font-size: 32px; margin-bottom: 0.8rem; text-shadow: 0 2px 4px rgba(0,0,0,0.2);">{icon}</div>
                <div style="font-size: 13px; line-height: 1.4; color: #e2e8f0 !important;">{tip}</div>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    # For testing purposes
    sample_metrics = {
        'avg_screen_time': 5.2,
        'avg_sleep_quality': 7.8,
        'avg_mood': 8.1,
        'productive_sessions': 12
    }
    run(pd.DataFrame(), sample_metrics, "John Doe")
