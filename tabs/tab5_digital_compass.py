# tabs/tab5_digital_compass.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import os

def create_sample_digital_compass_data():
    """Create sample digital compass data for demonstration"""
    try:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        DATA_FOLDER = os.path.join(BASE_DIR, "data")
        COMPASS_CSV = os.path.join(DATA_FOLDER, "digital_compass_data.csv")
        
        os.makedirs(DATA_FOLDER, exist_ok=True)
        
        # Create sample data for November 15-20, 2025
        sample_data = []
        
        dates = [
            "2025-11-15 09:00:00",
            "2025-11-16 10:15:00", 
            "2025-11-17 11:30:00",
            "2025-11-18 14:45:00",
            "2025-11-19 16:20:00",
            "2025-11-20 08:30:00"
        ]
        
        wellness_scores = [65.2, 58.7, 72.3, 45.8, 68.9, 75.4]
        wellness_levels = ["Concerning", "Concerning", "Moderate", "Concerning", "Moderate", "Healthy"]
        total_usage_mins = [245, 312, 189, 356, 203, 156]
        
        for i, date in enumerate(dates):
            record = {
                "date": date,
                "digital_wellness_score": wellness_scores[i],
                "wellness_level": wellness_levels[i],
                "total_fomo_score": np.random.uniform(15, 35),
                "total_daily_usage_mins": total_usage_mins[i],
                "total_platforms_used": np.random.randint(4, 8),
                # Platform breakdown
                "instagram_mins": np.random.randint(30, 90),
                "tiktok_mins": np.random.randint(20, 80),
                "youtube_mins": np.random.randint(40, 120),
                "facebook_mins": np.random.randint(10, 50),
                "twitter_mins": np.random.randint(15, 45),
                "whatsapp_mins": np.random.randint(20, 60),
                "snapchat_mins": np.random.randint(5, 30),
                "discord_mins": np.random.randint(10, 40),
                "linkedin_mins": np.random.randint(5, 25),
                "other_mins": np.random.randint(10, 50),
                # Assessment categories
                "anxiety_score": np.random.uniform(2, 6),
                "fomo_score": np.random.uniform(2, 7),
                "social_comparison_score": np.random.uniform(3, 8),
                "validation_seeking_score": np.random.uniform(2, 6),
                "habit_formation_score": np.random.uniform(1, 5),
                "mindless_consumption_score": np.random.uniform(3, 7),
                "self_esteem_score": np.random.uniform(2, 6)
            }
            sample_data.append(record)
        
        df = pd.DataFrame(sample_data)
        df.to_csv(COMPASS_CSV, index=False)
        return True
    except Exception as e:
        st.error(f"Error creating sample data: {e}")
        return False

def load_pulse_check_data():
    """Load data from pulse check CSV file"""
    try:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        DATA_FOLDER = os.path.join(BASE_DIR, "data")
        CSV_FILE = os.path.join(DATA_FOLDER, "user_daily_data.csv")
        
        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE)
            # Convert date column to datetime
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'], errors='coerce')
                df = df.dropna(subset=['date'])
                df = df.sort_values('date', ascending=False)
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading pulse check data: {e}")
        return pd.DataFrame()

def get_integrated_metrics():
    """Get integrated metrics from pulse check data"""
    df = load_pulse_check_data()
    
    if df.empty:
        return {
            'avg_screen_time': 0.0,
            'predicted_wellness': 0.0,
            'avg_stress_level': 0.0
        }
    
    try:
        # Calculate average screen time from latest 5 entries
        recent_data = df.head(5)
        
        avg_screen_time = recent_data['screen_time_hours'].mean() if 'screen_time_hours' in recent_data.columns else 0.0
        predicted_wellness = recent_data['predicted_wellness'].iloc[0] if 'predicted_wellness' in recent_data.columns else 0.0
        avg_stress_level = recent_data['stress_level'].mean() if 'stress_level' in recent_data.columns else 0.0
        
        return {
            'avg_screen_time': float(avg_screen_time),
            'predicted_wellness': float(predicted_wellness),
            'avg_stress_level': float(avg_stress_level)
        }
    except Exception as e:
        st.error(f"Error calculating metrics: {e}")
        return {
            'avg_screen_time': 0.0,
            'predicted_wellness': 0.0,
            'avg_stress_level': 0.0
        }

def save_digital_compass_data(assessment_data, usage_data):
    """Save digital compass data to CSV"""
    try:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        DATA_FOLDER = os.path.join(BASE_DIR, "data")
        COMPASS_CSV = os.path.join(DATA_FOLDER, "digital_compass_data.csv")
        
        os.makedirs(DATA_FOLDER, exist_ok=True)
        
        # Prepare data for saving
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Calculate total scores
        total_fomo_score = sum(data["score"] for data in assessment_data["scores"].values())
        wellness_score = assessment_data["wellness_score"]
        
        # Calculate platform usage summary
        total_usage_mins = usage_data["total_daily_mins"]
        total_platforms = sum(1 for v in usage_data["usage_data"].values() if v > 0)
        
        record = {
            "date": current_date,
            "digital_wellness_score": wellness_score,
            "wellness_level": assessment_data["wellness_level"],
            "total_fomo_score": total_fomo_score,
            "total_daily_usage_mins": total_usage_mins,
            "total_platforms_used": total_platforms,
            # Platform breakdown
            "instagram_mins": usage_data["usage_data"].get("Instagram", 0),
            "tiktok_mins": usage_data["usage_data"].get("TikTok", 0),
            "youtube_mins": usage_data["usage_data"].get("YouTube", 0),
            "facebook_mins": usage_data["usage_data"].get("Facebook", 0),
            "twitter_mins": usage_data["usage_data"].get("Twitter/X", 0),
            "whatsapp_mins": usage_data["usage_data"].get("WhatsApp", 0),
            "snapchat_mins": usage_data["usage_data"].get("Snapchat", 0),
            "discord_mins": usage_data["usage_data"].get("Discord", 0),
            "linkedin_mins": usage_data["usage_data"].get("LinkedIn", 0),
            "other_mins": usage_data["usage_data"].get("Other", 0),
            # Assessment categories
            "anxiety_score": sum(data["score"] for i, data in assessment_data["scores"].items() 
                               if assessment_data["scores"][i]["category"] == "Anxiety"),
            "fomo_score": sum(data["score"] for i, data in assessment_data["scores"].items() 
                            if assessment_data["scores"][i]["category"] == "FOMO"),
            "social_comparison_score": sum(data["score"] for i, data in assessment_data["scores"].items() 
                                         if assessment_data["scores"][i]["category"] == "Social Comparison"),
            "validation_seeking_score": sum(data["score"] for i, data in assessment_data["scores"].items() 
                                          if assessment_data["scores"][i]["category"] == "Validation Seeking"),
            "habit_formation_score": sum(data["score"] for i, data in assessment_data["scores"].items() 
                                       if assessment_data["scores"][i]["category"] == "Habit Formation"),
            "mindless_consumption_score": sum(data["score"] for i, data in assessment_data["scores"].items() 
                                            if assessment_data["scores"][i]["category"] == "Mindless Consumption"),
            "self_esteem_score": sum(data["score"] for i, data in assessment_data["scores"].items() 
                                   if assessment_data["scores"][i]["category"] == "Self-Esteem")
        }
        
        df_new = pd.DataFrame([record])
        
        if not os.path.exists(COMPASS_CSV):
            df_new.to_csv(COMPASS_CSV, index=False)
            st.success("✅ Digital Compass data saved successfully! Created new file.")
        else:
            df_new.to_csv(COMPASS_CSV, mode='a', header=False, index=False)
            st.success("✅ Digital Compass data saved successfully!")
        
        return True
    except Exception as e:
        st.error(f"❌ Error saving digital compass data: {e}")
        return False

def load_digital_compass_history():
    """Load digital compass data from CSV"""
    try:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        DATA_FOLDER = os.path.join(BASE_DIR, "data")
        COMPASS_CSV = os.path.join(DATA_FOLDER, "digital_compass_data.csv")
        
        # Create sample data if file doesn't exist
        if not os.path.exists(COMPASS_CSV):
            create_sample_digital_compass_data()
            st.info("📊 Sample Digital Compass data created for demonstration!")
        
        if os.path.exists(COMPASS_CSV):
            df = pd.read_csv(COMPASS_CSV)
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'], errors='coerce')
                df = df.dropna(subset=['date'])
                df = df.sort_values('date', ascending=False)
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading digital compass data: {e}")
        return pd.DataFrame()

def apply_digital_compass_css():
    st.markdown("""
    <style>
    /* Digital Compass Specific Styling - SEMUA TEKS PUTIH */
    * {
        color: white !important;
    }
    
    .compass-hero {
        background: linear-gradient(135deg, #10B981 0%, #0EA5E9 100%) !important;
        padding: 2rem 1.5rem !important;
        border-radius: 16px !important;
        text-align: center !important;
        margin-bottom: 2rem !important;
        box-shadow: 0 8px 32px rgba(16, 185, 129, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .compass-card {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(14, 165, 233, 0.15) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .assessment-question {
        background: linear-gradient(135deg, rgba(14, 165, 233, 0.1) 0%, rgba(99, 102, 241, 0.1) 100%) !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        margin: 0.8rem 0 !important;
        border-left: 4px solid #0EA5E9 !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
    }
    
    .platform-card {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(14, 165, 233, 0.1) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
        transition: all 0.3s ease !important;
    }
    
    .platform-card:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.3) !important;
        border-color: rgba(14, 165, 233, 0.4) !important;
    }
    
    .recommendation-high {
        border-left: 4px solid #EF4444 !important;
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(245, 158, 11, 0.1) 100%) !important;
    }
    
    .recommendation-medium {
        border-left: 4px solid #F59E0B !important;
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(16, 185, 129, 0.1) 100%) !important;
    }
    
    .recommendation-low {
        border-left: 4px solid #10B981 !important;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(14, 165, 233, 0.1) 100%) !important;
    }
    
    .challenge-day {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(14, 165, 233, 0.1) 100%) !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        margin: 0.5rem 0 !important;
    }
    
    /* Button Styling - TEKS PUTIH */
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
        color: white !important;
        background: linear-gradient(135deg, #0EA5E9 0%, #6366F1 100%) !important;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%) !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 12px 24px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        color: white !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0EA5E9 0%, #6366F1 100%) !important;
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* Metric Cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(14, 165, 233, 0.15) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    [data-testid="metric-container"] * {
        color: white !important;
    }
    
    /* Slider Styling */
    .stSlider {
        background: rgba(15, 23, 42, 0.6) !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .stSlider label {
        color: white !important;
        font-weight: 500 !important;
    }
    
    .stSlider [data-testid="stMarkdown"] p {
        color: white !important;
    }
    
    /* Number Input Styling */
    .stNumberInput input {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 8px !important;
        color: white !important;
    }
    
    .stNumberInput label {
        color: white !important;
    }
    
    /* Selectbox Styling */
    .stSelectbox label {
        color: white !important;
    }
    
    .stSelectbox [data-baseweb="select"] {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 8px !important;
        color: white !important;
    }
    
    .stSelectbox [data-baseweb="select"] div {
        color: white !important;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        color: white !important;
        background: rgba(30, 41, 59, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 8px !important;
    }
    
    .streamlit-expanderContent {
        color: white !important;
    }
    
    /* Radio Styling */
    .stRadio label {
        color: white !important;
    }
    
    .stRadio [role="radiogroup"] {
        color: white !important;
    }
    
    /* Checkbox Styling */
    .stCheckbox label {
        color: white !important;
    }
    
    /* Text Input Styling */
    .stTextInput input {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 8px !important;
        color: white !important;
    }
    
    .stTextInput label {
        color: white !important;
    }
    
    /* ALL TEXT WHITE - GLOBAL OVERRIDE */
    body, html, .stApp, .stApp * {
        color: white !important;
    }
    
    .compass-hero h1, .compass-hero h2, .compass-hero h3, .compass-hero h4,
    .compass-hero p, .compass-hero span, .compass-hero div {
        color: white !important;
    }
    
    .compass-card h1, .compass-card h2, .compass-card h3, .compass-card h4,
    .compass-card h5, .compass-card h6, .compass-card p, .compass-card li, 
    .compass-card span, .compass-card div, .compass-card strong, .compass-card small {
        color: white !important;
    }
    
    .assessment-question * {
        color: white !important;
    }
    
    .platform-card * {
        color: white !important;
    }
    
    .recommendation-high *, .recommendation-medium *, .recommendation-low * {
        color: white !important;
    }
    
    .challenge-day * {
        color: white !important;
    }
    
    /* Streamlit specific elements */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4,
    .stMarkdown h5, .stMarkdown h6, .stMarkdown p, .stMarkdown span, 
    .stMarkdown div, .stMarkdown li, .stMarkdown ul, .stMarkdown ol {
        color: white !important;
    }
    
    .stExpander * {
        color: white !important;
    }
    
    /* Ensure all text in tabs is white */
    .stTabs [data-baseweb="tab"] {
        color: white !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: white !important;
    }
    
    /* Warning, Info, Success messages */
    .stWarning, .stInfo, .stSuccess, .stError {
        color: white !important;
    }
    
    .stWarning *,
    .stInfo *,
    .stSuccess *,
    .stError * {
        color: white !important;
    }
    
    /* Progress bars and other elements */
    .stProgress > div > div {
        background: linear-gradient(135deg, #0EA5E9 0%, #6366F1 100%) !important;
    }
    
    /* Plotly chart text */
    .js-plotly-plot .plotly .main-svg {
        color: white !important;
    }
    
    /* Dataframe styling */
    .dataframe {
        color: white !important;
    }
    
    .dataframe th {
        color: white !important;
        background: rgba(30, 41, 59, 0.8) !important;
    }
    
    .dataframe td {
        color: white !important;
        background: rgba(30, 41, 59, 0.6) !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def fomo_assessment_questionnaire():
    st.markdown("""
    <div class='compass-card'>
        <h3 style='margin: 0 0 1rem 0; text-align: center; color: white;'>🧭 Digital Wellness Assessment</h3>
        <p style='text-align: center; margin: 0; color: white;'>
        Measure how digital habits affect your mental wellbeing</p>
    </div>
    """, unsafe_allow_html=True)
    
    questions = [
        {
            "question": "How often do you feel anxious when you can't check your social media?",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Always"],
            "weight": 1.2,
            "category": "Anxiety"
        },
        {
            "question": "Do you feel left out when you see others having fun without you?",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Always"],
            "weight": 1.0,
            "category": "FOMO"
        },
        {
            "question": "How often do you compare your life to others' social media posts?",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Constantly"],
            "weight": 1.3,
            "category": "Social Comparison"
        },
        {
            "question": "Do you feel pressured to post about your life to keep up appearances?",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Always"],
            "weight": 1.1,
            "category": "Validation Seeking"
        },
        {
            "question": "How often do you check social media first thing in the morning?",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Always"],
            "weight": 0.9,
            "category": "Habit Formation"
        },
        {
            "question": "Do you feel your posts don't get enough likes/comments?",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Always"],
            "weight": 1.0,
            "category": "Validation Seeking"
        },
        {
            "question": "How often do you scroll through feeds mindlessly?",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Constantly"],
            "weight": 0.8,
            "category": "Mindless Consumption"
        },
        {
            "question": "Do you feel inadequate when seeing others' achievements?",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Always"],
            "weight": 1.4,
            "category": "Self-Esteem"
        }
    ]
    
    scores = {}
    st.markdown("### 📝 Digital Wellness Questionnaire")
    st.markdown("<p style='color: white;'>Rate how often you experience these feelings (0 = Never, 4 = Always):</p>", unsafe_allow_html=True)
    
    for i, q in enumerate(questions):
        st.markdown(f"<div class='assessment-question'>", unsafe_allow_html=True)
        score = st.slider(
            f"**{i+1}. {q['question']}**",
            0, 4, 2,
            key=f"fomo_q_{i}",
            help="0: Never, 1: Rarely, 2: Sometimes, 3: Often, 4: Always"
        )
        st.markdown(f"<small style='color: white;'>Category: {q['category']}</small>", unsafe_allow_html=True)
        st.markdown(f"</div>", unsafe_allow_html=True)
        
        scores[i] = {
            "score": score * q['weight'],
            "category": q['category']
        }
    
    return scores, questions

def platform_usage_tracker():
    st.markdown("### 📊 Digital Habit Tracking")
    st.markdown("<p style='color: white;'>Track your daily usage across different platforms:</p>", unsafe_allow_html=True)
    
    platforms = {
        "Instagram": "📷",
        "TikTok": "🎵", 
        "Facebook": "👥",
        "Twitter/X": "🐦",
        "YouTube": "📺",
        "Snapchat": "👻",
        "WhatsApp": "💬",
        "Discord": "🎮",
        "LinkedIn": "💼",
        "Other": "📱"
    }
    
    usage_data = {}
    
    # Create two columns for better layout
    cols = st.columns(2)
    
    for i, (platform, icon) in enumerate(platforms.items()):
        with cols[i % 2]:
            st.markdown(f"<div class='platform-card'>", unsafe_allow_html=True)
            usage_data[platform] = st.number_input(
                f"{icon} {platform} (minutes/day)",
                min_value=0,
                max_value=480,
                value=30,
                key=f"usage_{platform}",
                help=f"Daily usage time for {platform}"
            )
            st.markdown(f"</div>", unsafe_allow_html=True)
    
    return usage_data

def calculate_digital_wellness_score(scores):
    if not scores:
        return 0, "Unknown", "#FFFFFF", "Complete the assessment to get your score"
    
    total_score = sum(data["score"] for data in scores.values())
    max_possible = sum(4 * q['weight'] for q in st.session_state.get('fomo_questions', []))
    
    if max_possible > 0:
        normalized_score = (total_score / max_possible) * 100
    else:
        normalized_score = 0
    
    # Categorize digital wellness level
    if normalized_score < 25:
        level = "Healthy"
        color = "#10B981"
        description = "You have a balanced relationship with digital technology"
    elif normalized_score < 50:
        level = "Moderate" 
        color = "#F59E0B"
        description = "Some signs of digital stress - good awareness needed"
    elif normalized_score < 75:
        level = "Concerning"
        color = "#EF4444"
        description = "Significant digital impact - consider digital detox"
    else:
        level = "Critical"
        color = "#DC2626"
        description = "Urgent need to address digital habits for mental health"
    
    return normalized_score, level, color, description

def create_platform_analysis_chart(usage_data):
    # Filter platforms with usage > 0
    active_platforms = {k: v for k, v in usage_data.items() if v > 0}
    
    if not active_platforms:
        return None
    
    fig = px.pie(
        values=list(active_platforms.values()),
        names=list(active_platforms.keys()),
        title="Digital Time Distribution",
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        marker=dict(line=dict(color='rgba(255,255,255,0.3)', width=2))
    )
    
    fig.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        title_font_color='white'
    )
    
    return fig

def create_wellness_radar(scores, questions):
    if not scores or not questions:
        # Return empty radar if no data
        fig = go.Figure()
        fig.update_layout(
            title="Complete assessment to see radar chart",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        return fig
    
    categories = list(set([q['category'] for q in questions]))
    category_scores = {}
    
    # Calculate average score for each category
    for category in categories:
        category_scores[category] = []
    
    for i, data in scores.items():
        category_scores[data['category']].append(data['score'])
    
    # Average scores per category (normalized to 0-100)
    values = []
    for category in categories:
        if category_scores[category]:
            avg_score = sum(category_scores[category]) / len(category_scores[category])
            normalized_score = (avg_score / (4 * max(q['weight'] for q in questions if q['category'] == category))) * 100
            values.append(min(normalized_score, 100))
        else:
            values.append(0)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor='rgba(239, 68, 68, 0.3)',
        line=dict(color='#EF4444', width=2),
        name='Digital Impact Areas'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10, color='white'),
                gridcolor='rgba(255,255,255,0.2)',
                linecolor='rgba(255,255,255,0.3)'
            ),
            angularaxis=dict(
                gridcolor='rgba(255,255,255,0.2)',
                linecolor='rgba(255,255,255,0.3)',
                tickfont=dict(color='white')
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=False,
        title="Digital Wellness Impact Radar",
        title_font_color='white',
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig

def generate_personalized_recommendations(wellness_score, wellness_level, usage_data, scores, questions):
    recommendations = []
    
    # Based on wellness level
    if wellness_level in ["Concerning", "Critical"]:
        recommendations.append({
            "icon": "📵",
            "title": "Digital Detox Challenge",
            "description": "Start with 1 hour of no social media daily, gradually increasing to 4 hours",
            "priority": "High",
            "category": "Immediate Action"
        })
    
    # Based on usage patterns
    total_daily_usage = sum(usage_data.values()) if usage_data else 0
    if total_daily_usage > 180:  # More than 3 hours
        recommendations.append({
            "icon": "⏰",
            "title": "Usage Time Limits",
            "description": f"Set app limits to reduce from {total_daily_usage} to 120 minutes daily",
            "priority": "High",
            "category": "Usage Management"
        })
    
    # Category-based recommendations
    if scores and questions:
        category_scores = {}
        for i, data in scores.items():
            category = data["category"]
            if category not in category_scores:
                category_scores[category] = []
            category_scores[category].append(data["score"])
        
        # Average scores per category
        for category, scores_list in category_scores.items():
            avg_score = sum(scores_list) / len(scores_list)
            if avg_score > 3.0:  # High impact
                if category == "Social Comparison":
                    recommendations.append({
                        "icon": "🤔",
                        "title": "Reality Check Practice",
                        "description": "Remember: Social media shows highlights, not reality. Practice gratitude journaling",
                        "priority": "Medium",
                        "category": "Mindset Shift"
                    })
                elif category == "Anxiety":
                    recommendations.append({
                        "icon": "🧘",
                        "title": "Mindfulness Training",
                        "description": "Try 5-minute meditation before checking social media",
                        "priority": "Medium",
                        "category": "Anxiety Management"
                    })
    
    # Default recommendations
    if not recommendations:
        recommendations.extend([
            {
                "icon": "📚",
                "title": "Digital Literacy",
                "description": "Educate yourself about algorithm manipulation and curated content",
                "priority": "Low",
                "category": "Education"
            },
            {
                "icon": "🎯",
                "title": "Intentional Usage",
                "description": "Set specific purposes for digital use instead of mindless scrolling",
                "priority": "Medium",
                "category": "Habit Building"
            }
        ])
    
    return recommendations

def recommendation_card(rec):
    priority_classes = {
        "High": "recommendation-high",
        "Medium": "recommendation-medium", 
        "Low": "recommendation-low"
    }
    
    priority_colors = {
        "High": "#EF4444",
        "Medium": "#F59E0B",
        "Low": "#10B981"
    }
    
    st.markdown(f"""
    <div class='compass-card {priority_classes[rec['priority']]}'>
        <div style="display: flex; align-items: flex-start; gap: 12px;">
            <span style="font-size: 1.8rem;">{rec['icon']}</span>
            <div style="flex: 1;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                    <h4 style="margin: 0; font-size: 1.1rem; color: white;">{rec['title']}</h4>
                    <span style="background: {priority_colors[rec['priority']]}20; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
                        {rec['priority']} Priority
                    </span>
                </div>
                <p style="margin: 0 0 0.5rem 0; font-size: 0.95rem; color: white;">{rec['description']}</p>
                <div style="font-size: 0.85rem; font-weight: 500; color: white;">{rec['category']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def run(df=None, metrics=None):
    # Apply custom CSS
    apply_digital_compass_css()

    # Initialize session state
    if 'digital_wellness_history' not in st.session_state:
        st.session_state.digital_wellness_history = []
    if 'digital_usage_history' not in st.session_state:
        st.session_state.digital_usage_history = []
    if 'fomo_questions' not in st.session_state:
        st.session_state.fomo_questions = []
    if 'compass_df' not in st.session_state:
        st.session_state.compass_df = load_digital_compass_history()
    
    # Load integrated metrics from pulse check
    pulse_metrics = get_integrated_metrics()
    
    # Hero Header
    st.markdown(
        """
        <div class='compass-hero'>
            <h1 style='margin: 0; font-size: 2.5rem; font-weight: 700; color: white;'>🧭 Digital Wellness Compass</h1>
            <p style='
                font-size: 1.1rem;
                margin: 0.5rem 0;
                font-weight: 300;
                color: white;
            '>
                Navigate Your Path to Digital Balance & Mental Wellbeing
            </p>
            <p style='
                font-style: italic;
                font-size: 0.95rem;
                margin: 0;
                color: white;
            '>
                "Find Your Balance in the Digital World" 🌐
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Introduction
    st.markdown("""
    <div class='compass-card'>
        <h3 style='margin: 0 0 1rem 0; color: white;'>🎯 Your Digital Wellness Journey</h3>
        <p style='margin: 0 0 1rem 0; color: white;'>This compass helps you navigate the challenges of digital life:</p>
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;'>
            <div>
                <span style='font-weight: bold; color: white;'>• FOMO</span>
                <p style='margin: 0.2rem 0; font-size: 0.9rem; color: white;'>Anxiety from digital social pressure</p>
            </div>
            <div>
                <span style='font-weight: bold; color: white;'>• Social Comparison</span>
                <p style='margin: 0.2rem 0; font-size: 0.9rem; color: white;'>Measuring against curated online lives</p>
            </div>
            <div>
                <span style='font-weight: bold; color: white;'>• Digital Overload</span>
                <p style='margin: 0.2rem 0; font-size: 0.9rem; color: white;'>Information and notification fatigue</p>
            </div>
            <div>
                <span style='font-weight: bold; color: white;'>• Attention Fragmentation</span>
                <p style='margin: 0.2rem 0; font-size: 0.9rem; color: white;'>Constant switching between apps and tasks</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Integrate with existing metrics from pulse check
    st.markdown("### 📈 Your Current Digital Profile")
    metric_cols = st.columns(3)
    
    with metric_cols[0]:
        avg_screen_time = pulse_metrics.get('avg_screen_time', 0)
        st.metric(
            "Average Screen Time", 
            f"{avg_screen_time:.1f} hrs/day",
            help="Based on your recent Pulse Check data"
        )
    
    with metric_cols[1]:
        wellness_score = pulse_metrics.get('predicted_wellness', 0)
        st.metric(
            "Wellness Score", 
            f"{wellness_score:.1f}/100",
            help="Your latest wellness score from Pulse Check"
        )
    
    with metric_cols[2]:
        stress_level = pulse_metrics.get('avg_stress_level', 0)
        st.metric(
            "Stress Level", 
            f"{stress_level:.1f}/10",
            help="Average stress level from recent data"
        )

    # Data source information
    if pulse_metrics['avg_screen_time'] > 0:
        st.info("📊 **Data Source**: These metrics are integrated from your Pulse Check history. Visit the Pulse Check tab to update your data.")
    else:
        st.warning("📊 **No Data Available**: Complete the Pulse Check assessment first to see your integrated metrics here.")

    # Main Analysis Section
    tab1, tab2, tab3 = st.tabs(["🧭 Self-Assessment", "📊 Digital Habits", "💡 Action Plan"])
    
    with tab1:
        st.markdown("### 🔍 Digital Wellness Self-Assessment")
        
        # Wellness Questionnaire
        scores, questions = fomo_assessment_questionnaire()
        st.session_state.fomo_questions = questions
        
        if st.button("🧮 Calculate Digital Wellness Score", use_container_width=True):
            if scores:
                wellness_score, wellness_level, color, description = calculate_digital_wellness_score(scores)
                
                # Save to session state
                assessment_data = {
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "wellness_score": wellness_score,
                    "wellness_level": wellness_level,
                    "scores": scores
                }
                st.session_state.digital_wellness_history.append(assessment_data)
                
                # Display Results
                st.markdown(f"""
                <div class='compass-card' style='border-left: 6px solid {color};'>
                    <div style='text-align: center;'>
                        <h2 style='color: {color}; margin: 0 0 0.5rem 0; font-size: 2rem;'>Digital Wellness Score: {wellness_score:.1f}/100</h2>
                        <h3 style='color: {color}; margin: 0 0 1rem 0;'>{wellness_level} Level</h3>
                        <p style='margin: 0; font-size: 1.1rem; color: white;'>{description}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Radar Chart
                radar_fig = create_wellness_radar(scores, questions)
                st.plotly_chart(radar_fig, use_container_width=True)
            else:
                st.warning("Please complete the assessment questions first.")
    
    with tab2:
        st.markdown("### 📱 Your Digital Habit Patterns")
        
        usage_data = platform_usage_tracker()
        
        if st.button("📈 Analyze Digital Habits", use_container_width=True):
            if usage_data:
                # Save to session state
                usage_record = {
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "usage_data": usage_data,
                    "total_daily_mins": sum(usage_data.values())
                }
                st.session_state.digital_usage_history.append(usage_record)
                
                # Usage Analysis
                total_usage = sum(usage_data.values())
                usage_hours = total_usage / 60
                
                st.markdown(f"""
                <div class='compass-card'>
                    <h3 style='margin: 0 0 1rem 0; color: white;'>📊 Daily Digital Usage Summary</h3>
                    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;'>
                        <div style='text-align: center; padding: 1rem; background: rgba(14, 165, 233, 0.2); border-radius: 12px;'>
                            <div style='font-size: 2.5rem; font-weight: bold; color: #0EA5E9;'>{total_usage}</div>
                            <div style='font-weight: 600; color: white;'>Total Minutes/Day</div>
                        </div>
                        <div style='text-align: center; padding: 1rem; background: rgba(14, 165, 233, 0.2); border-radius: 12px;'>
                            <div style='font-size: 2.5rem; font-weight: bold; color: #0EA5E9;'>{usage_hours:.1f}</div>
                            <div style='font-weight: 600; color: white;'>Hours/Day</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Platform Distribution
                fig = create_platform_analysis_chart(usage_data)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                
                # Check if we have both assessment and usage data to save
                if (st.session_state.digital_wellness_history and 
                    len(st.session_state.digital_wellness_history) > 0 and
                    len(st.session_state.digital_usage_history) > 0):
                    
                    latest_assessment = st.session_state.digital_wellness_history[-1]
                    latest_usage = st.session_state.digital_usage_history[-1]
                    
                    # Save button
                    if st.button("💾 Save Complete Session Data", use_container_width=True, key="save_session_btn"):
                        if save_digital_compass_data(latest_assessment, latest_usage):
                            # Reload the history
                            st.session_state.compass_df = load_digital_compass_history()
                            st.rerun()
                
                # Usage Recommendations
                if usage_hours > 4:
                    st.error(f"⚠️ You're spending {usage_hours:.1f} hours daily on digital platforms. Consider setting healthy boundaries.")
                elif usage_hours > 2:
                    st.warning(f"ℹ️ Your digital usage of {usage_hours:.1f} hours is moderate. Maintain conscious awareness of your habits.")
                else:
                    st.success(f"✅ Your digital usage of {usage_hours:.1f} hours shows good balance. Keep it up!")
            else:
                st.warning("Please fill in your platform usage data first.")
    
    with tab3:
        st.markdown("### 💡 Your Personalized Action Plan")
        
        # Check if we have data to show recommendations
        if st.session_state.digital_wellness_history and st.session_state.digital_usage_history:
            latest_wellness = st.session_state.digital_wellness_history[-1]
            latest_usage = st.session_state.digital_usage_history[-1]
            
            recommendations = generate_personalized_recommendations(
                latest_wellness['wellness_score'],
                latest_wellness['wellness_level'],
                latest_usage['usage_data'],
                latest_wellness['scores'],
                st.session_state.fomo_questions
            )
            
            st.markdown(f"""
            <div class='compass-card'>
                <h3 style='margin: 0 0 1rem 0; color: white;'>🎯 Your Digital Balance Roadmap</h3>
                <p style='margin: 0; color: white;'>
                Based on your Digital Wellness Score of <strong>{latest_wellness['wellness_score']:.1f}/100</strong> 
                and <strong>{latest_usage['total_daily_mins']} minutes</strong> of daily digital usage
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Sort recommendations by priority
            priority_order = {"High": 3, "Medium": 2, "Low": 1}
            recommendations.sort(key=lambda x: priority_order[x['priority']], reverse=True)
            
            for rec in recommendations:
                recommendation_card(rec)
            
            # 7-Day Digital Balance Challenge
            st.markdown("### 🌟 7-Day Digital Balance Challenge")
            
            challenge_steps = [
                {"day": 1, "task": "Digital Sunset - No screens 1 hour before bed", "benefit": "Improve sleep quality", "icon": "😴"},
                {"day": 2, "task": "Notification Cleanse - Turn off non-essential alerts", "benefit": "Reduce interruptions", "icon": "🔕"},
                {"day": 3, "task": "Single-Tasking Focus - One app at a time", "benefit": "Improve concentration", "icon": "🎯"},
                {"day": 4, "task": "Digital Minimalism - Delete one unused app", "benefit": "Reduce digital clutter", "icon": "🧹"},
                {"day": 5, "task": "Analog Hour - Engage in offline hobby", "benefit": "Rediscover real-world joy", "icon": "🎨"},
                {"day": 6, "task": "Mindful Scrolling - Set intention before opening apps", "benefit": "Conscious consumption", "icon": "🧠"},
                {"day": 7, "task": "Digital Sabbath - 4 hours completely offline", "benefit": "Mental reset", "icon": "🌿"}
            ]
            
            for step in challenge_steps:
                with st.expander(f"{step['icon']} Day {step['day']}: {step['task']}", expanded=False):
                    st.markdown(f"<div class='challenge-day'>", unsafe_allow_html=True)
                    st.write(f"**Benefit**: {step['benefit']}")
                    if st.button(f"Start Day {step['day']}", key=f"challenge_day_{step['day']}"):
                        st.success(f"Day {step['day']} challenge started! 🚀")
                    st.markdown(f"</div>", unsafe_allow_html=True)
        
        else:
            st.markdown("""
            <div class='compass-card'>
                <div style='text-align: center; padding: 2rem;'>
                    <span style='font-size: 3rem;'>📝</span>
                    <h3 style='margin: 1rem 0; color: white;'>Complete Your Assessment First</h3>
                    <p style='color: white;'>Complete the Digital Wellness Assessment and Habit Analysis first to get your personalized action plan.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Progress Tracking - Now using CSV data
    if not st.session_state.compass_df.empty:
        st.markdown("### 📈 Your Progress Journey")
        
        # Get the latest 10 entries for display
        display_df = st.session_state.compass_df.head(10).sort_values('date', ascending=True)
        
        if len(display_df) > 1:
            # Create trend chart
            fig = px.line(
                display_df,
                x='date',
                y='digital_wellness_score',
                title="Digital Wellness Progress Over Time",
                markers=True,
                line_shape="spline"
            )
            
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Wellness Score",
                yaxis_range=[0, 100],
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                title_font_color='white'
            )
            
            # Add colored zones
            fig.add_hrect(y0=0, y1=25, line_width=0, fillcolor="green", opacity=0.1, annotation_text="Healthy")
            fig.add_hrect(y0=25, y1=50, line_width=0, fillcolor="yellow", opacity=0.1, annotation_text="Moderate")
            fig.add_hrect(y0=50, y1=75, line_width=0, fillcolor="orange", opacity=0.1, annotation_text="Concerning")
            fig.add_hrect(y0=75, y1=100, line_width=0, fillcolor="red", opacity=0.1, annotation_text="Critical")
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show recent history
            st.markdown("#### 📋 Recent Assessments")
            recent_data = st.session_state.compass_df.head(5)[['date', 'digital_wellness_score', 'wellness_level', 'total_daily_usage_mins']].copy()
            recent_data['date'] = recent_data['date'].dt.strftime('%Y-%m-%d %H:%M')
            recent_data['digital_wellness_score'] = recent_data['digital_wellness_score'].round(1)
            recent_data['total_daily_usage_mins'] = recent_data['total_daily_usage_mins'].astype(int)
            recent_data = recent_data.rename(columns={
                'date': '📅 Date',
                'digital_wellness_score': '💓 Wellness Score',
                'wellness_level': '📊 Level',
                'total_daily_usage_mins': '⏱️ Usage (mins)'
            })
            
            st.dataframe(recent_data, use_container_width=True)
        else:
            st.info("Complete more assessments to see your progress journey!")
    
    # Display 5 Latest Records before Educational Content
    if not st.session_state.compass_df.empty:
        st.markdown("---")
        st.markdown("### 📊 Latest Digital Wellness Records")
        
        # Get the 5 most recent records
        latest_records = st.session_state.compass_df.head(5).copy()
        
        # Format the data for display
        display_data = latest_records[['date', 'digital_wellness_score', 'wellness_level', 'total_daily_usage_mins', 'total_platforms_used']].copy()
        display_data['date'] = display_data['date'].dt.strftime('%Y-%m-%d %H:%M')
        display_data['digital_wellness_score'] = display_data['digital_wellness_score'].round(1)
        display_data['total_daily_usage_mins'] = display_data['total_daily_usage_mins'].astype(int)
        
        # Add color coding for wellness levels
        def get_level_color(level):
            if level == "Healthy":
                return "#10B981"
            elif level == "Moderate":
                return "#F59E0B"
            elif level == "Concerning":
                return "#EF4444"
            else:
                return "#DC2626"
        
        # Create a beautiful display
        for idx, record in display_data.iterrows():
            color = get_level_color(record['wellness_level'])
            st.markdown(f"""
            <div class='compass-card' style='border-left: 6px solid {color}; margin: 0.5rem 0;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <h4 style='margin: 0 0 0.5rem 0; color: white;'>{record['date']}</h4>
                        <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem;'>
                            <div>
                                <div style='font-size: 1.8rem; font-weight: bold; color: {color};'>{record['digital_wellness_score']}</div>
                                <div style='font-size: 0.9rem; color: white;'>Wellness Score</div>
                            </div>
                            <div>
                                <div style='font-size: 1.2rem; font-weight: bold; color: {color};'>{record['wellness_level']}</div>
                                <div style='font-size: 0.9rem; color: white;'>Level</div>
                            </div>
                            <div>
                                <div style='font-size: 1.2rem; font-weight: bold; color: #0EA5E9;'>{record['total_daily_usage_mins']}m</div>
                                <div style='font-size: 0.9rem; color: white;'>Daily Usage</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Educational Content
    st.markdown("---")
    st.markdown("### 📚 Digital Wellness Education")
    
    edu_cols = st.columns(2)
    
    with edu_cols[0]:
        st.markdown("""
        <div class='compass-card'>
            <h4 style='margin: 0 0 1rem 0; color: white;'>🧠 The Science Behind Digital Wellness</h4>
            <div>
                <div style='display: flex; align-items: center; gap: 8px; margin: 0.5rem 0;'>
                    <span style='color: white;'>•</span>
                    <span style='color: white;'><strong>Dopamine Loops</strong>: Social media triggers reward pathways</span>
                </div>
                <div style='display: flex; align-items: center; gap: 8px; margin: 0.5rem 0;'>
                    <span style='color: white;'>•</span>
                    <span style='color: white;'><strong>Attention Economy</strong>: Platforms compete for your focus</span>
                </div>
                <div style='display: flex; align-items: center; gap: 8px; margin: 0.5rem 0;'>
                    <span style='color: white;'>•</span>
                    <span style='color: white;'><strong>Comparison Culture</strong>: Curated lives vs reality</span>
                </div>
                <div style='display: flex; align-items: center; gap: 8px; margin: 0.5rem 0;'>
                    <span style='color: white;'>•</span>
                    <span style='color: white;'><strong>Digital Minimalism</strong>: Intentional technology use</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with edu_cols[1]:
        st.markdown("""
        <div class='compass-card'>
            <h4 style='margin: 0 0 1rem 0; color: white;'>🛡️ Building Digital Resilience</h4>
            <div>
                <div style='display: flex; align-items: center; gap: 8px; margin: 0.5rem 0;'>
                    <span style='color: white;'>•</span>
                    <span style='color: white;'><strong>Digital Boundaries</strong>: Set clear usage limits</span>
                </div>
                <div style='display: flex; align-items: center; gap: 8px; margin: 0.5rem 0;'>
                    <span style='color: white;'>•</span>
                    <span style='color: white;'><strong>Mindful Consumption</strong>: Curate your digital diet</span>
                </div>
                <div style='display: flex; align-items: center; gap: 8px; margin: 0.5rem 0;'>
                    <span style='color: white;'>•</span>
                    <span style='color: white;'><strong>Analog Balance</strong>: Nurture offline connections</span>
                </div>
                <div style='display: flex; align-items: center; gap: 8px; margin: 0.5rem 0;'>
                    <span style='color: white;'>•</span>
                    <span style='color: white;'><strong>Tech Intentionality</strong>: Use tools, don't be used by them</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div class='compass-card' style='text-align: center; padding: 1.5rem;'>
            <strong style='font-size: 1.1rem; color: white;'>MindSync — Your Digital Compass</strong><br>
            <span style='color: white;'>"Navigate your digital life with intention, not impulse" 🧭✨</span>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    run()