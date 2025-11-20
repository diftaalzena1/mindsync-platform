# app.py
import streamlit as st
from utils import load_data, prepare_data, train_model, calculate_metrics
import sidebar
from tabs import tab1_home_base, tab2_pulse_check, tab3_welness_map, tab4_life_balance, tab5_digital_compass, tab6_growth_journey

# -------------------------
# Page Config
# -------------------------
st.markdown("""
<style>
/* 🌈 Background utama gradasi netral gender */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to right, #6A0DAD, #2A5C7D, #40E0D0) !important;
    color: #F0F0F0 !important;
    min-height: 100vh !important;
}

/* Hilangkan header transparan */
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #2C003E !important;
    color: #F0F0F0 !important;
    padding: 10px !important;
}
[data-testid="stSidebar"] * {
    color: #F0F0F0 !important;
}

/* Layout utama */
.block-container {
    max-width: 1400px !important;
    margin: 0 auto !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}
@media (max-width: 1000px) {
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 95% !important;
    }
}

/* Judul & subheader */
h1, h2, h3, .stText, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: #F0F0F0 !important;
}

/* Tombol */
.stButton>button {
    background-color: #FF69B4 !important;  /* aksen magenta */
    color: #FFFFFF !important;
    border-radius: 8px !important;
    border: none !important;
    font-weight: 600 !important;
    transition: all 0.2s ease-in-out !important;
}
.stButton>button:hover {
    background-color: #00CED1 !important;  /* hover soft cyan */
    transform: scale(1.02) !important;
}

/* Tabel */
.stDataFrame th {
    background-color: #2C003E !important;
    color: #F0F0F0 !important;
    text-align: center !important;
}
.stDataFrame td {
    text-align: center !important;
    color: #F0F0F0 !important;
}

/* Link interaktif */
a, a:link, a:visited {
    color: #FFB6C1 !important;  /* magenta muda */
    text-decoration: none !important;
}
a:hover {
    color: #40E0D0 !important;  /* turquoise */
    text-decoration: underline !important;
}

/* Teks biasa */
.stMarkdown p, .stText {
    color: #F0F0F0 !important;
}
</style>
""", unsafe_allow_html=True)


# -------------------------
# Footer
# -------------------------
def show_footer():
    st.markdown("""
        <div style='width: 100%; font-size:13px; text-align: center; color: #CBD5E1; padding: 10px; margin-top: 80px;'>
            © 2025 Difta Alzena Sakhi · MINDSYNC Project
        </div>
    """, unsafe_allow_html=True)

# -------------------------
# Sidebar + Logo
# -------------------------
sidebar.show_sidebar()

# -------------------------
# Load & Prepare Data
# -------------------------
df = load_data()
X, y, features = prepare_data(df)

# -------------------------
# Train Model & Metrics
# -------------------------
model, X_train, X_test, y_train, y_test, y_pred = train_model(X, y)
metrics = calculate_metrics(y_test, y_pred, X_columns=features, model=model)

# -------------------------
# Navigasi Tab
# -------------------------
tab = st.sidebar.radio(
    "Choose Page:",
    [
        "Home Base",
        "Pulse Check",
        "Wellness Map",
        "Life Balance",
        "Digital Compass",
        "Growth Journey"
    ],
    key="tab_selection"
)

# -------------------------
# Routing Tab
# -------------------------
if tab == "Home Base":
    tab1_home_base.run(df, metrics)
elif tab == "Pulse Check":
    tab2_pulse_check.run(model)
elif tab == "Wellness Map":
    tab3_welness_map.run(df)
elif tab == "Life Balance":
    tab4_life_balance.run(model)
elif tab == "Digital Compass":
    tab5_digital_compass.run(df, metrics)
elif tab == "Growth Journey":
    tab6_growth_journey.run()

# -------------------------
# Footer
# -------------------------
show_footer()
