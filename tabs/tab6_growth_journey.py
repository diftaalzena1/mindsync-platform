import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import random

def mood_selector():
    """Enhanced mood selector with better visual feedback"""
    moods = {
        "😊": {"label": "Happy & Positive", "color": "#10B981", "gradient": "linear-gradient(135deg, #10B981 0%, #059669 100%)"},
        "😌": {"label": "Calm & Peaceful", "color": "#0EA5E9", "gradient": "linear-gradient(135deg, #0EA5E9 0%, #0369A1 100%)"},
        "😢": {"label": "Sad & Down", "color": "#6366F1", "gradient": "linear-gradient(135deg, #6366F1 0%, #4F46E5 100%)"},
        "😠": {"label": "Angry & Frustrated", "color": "#EF4444", "gradient": "linear-gradient(135deg, #EF4444 0%, #DC2626 100%)"},
        "😰": {"label": "Anxious & Stressed", "color": "#F59E0B", "gradient": "linear-gradient(135deg, #F59E0B 0%, #D97706 100%)"},
        "😴": {"label": "Tired & Drained", "color": "#8B5CF6", "gradient": "linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%)"},
        "😐": {"label": "Neutral & Balanced", "color": "#64748B", "gradient": "linear-gradient(135deg, #64748B 0%, #475569 100%)"},
        "🎯": {"label": "Focused & Productive", "color": "#06B6D4", "gradient": "linear-gradient(135deg, #06B6D4 0%, #0891B2 100%)"},
        "🤔": {"label": "Reflective & Thoughtful", "color": "#84CC16", "gradient": "linear-gradient(135deg, #84CC16 0%, #65A30D 100%)"},
        "🌟": {"label": "Inspired & Motivated", "color": "#F97316", "gradient": "linear-gradient(135deg, #F97316 0%, #EA580C 100%)"}
    }
    
    st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h3 style='color: #000000; margin-bottom: 0.5rem; font-size: 1.5rem; font-weight: 600;'>🌈 How are you feeling today?</h3>
            <p style='color: #333333; font-size: 1rem;'>Select your current emotional state</p>
        </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(5)
    selected_mood = st.session_state.get('selected_mood', None)
    
    for i, (emoji, data) in enumerate(moods.items()):
        with cols[i % 5]:
            is_selected = selected_mood and selected_mood[0] == emoji
            background = data["gradient"] if is_selected else "linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%)"
            text_color = "white" if is_selected else "#000000"
            border = f"3px solid {data['color']}" if is_selected else "2px solid #E2E8F0"
            
            if st.button(f"{emoji}\n{data['label']}", key=f"mood_{i}", use_container_width=True):
                selected_mood = (emoji, data["label"])
                st.session_state.selected_mood = selected_mood
                st.rerun()
            
            # Custom styling for the selected button
            if is_selected:
                st.markdown(f"""
                    <style>
                    div[data-testid="stButton"] > button[kind="secondary"]:nth-child({i+1}) {{
                        background: {background} !important;
                        color: {text_color} !important;
                        border: {border} !important;
                        font-weight: 600 !important;
                        transform: scale(1.05);
                        transition: all 0.3s ease;
                    }}
                    </style>
                """, unsafe_allow_html=True)
    
    return selected_mood

def create_goal_card(goal, progress, deadline, category, priority):
    """Create beautiful goal card with enhanced visuals"""
    priority_colors = {
        "High": {"color": "#EF4444", "gradient": "linear-gradient(135deg, #EF4444 0%, #DC2626 100%)"},
        "Medium": {"color": "#F59E0B", "gradient": "linear-gradient(135deg, #F59E0B 0%, #D97706 100%)"}, 
        "Low": {"color": "#10B981", "gradient": "linear-gradient(135deg, #10B981 0%, #059669 100%)"}
    }
    
    category_icons = {
        "Digital Wellness": "📱",
        "Mental Health": "🧠", 
        "Physical Health": "💪",
        "Social": "👥",
        "Productivity": "🎯",
        "Sleep": "😴",
        "Lifestyle": "🌱"
    }
    
    # Progress styling
    if progress >= 80:
        progress_style = {"color": "#10B981", "emoji": "🎉", "class": "excellent"}
    elif progress >= 50:
        progress_style = {"color": "#F59E0B", "emoji": "🔥", "class": "good"}
    else:
        progress_style = {"color": "#EF4444", "emoji": "🚀", "class": "needs-work"}
    
    # Days remaining calculation
    try:
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
        days_remaining = (deadline_date - datetime.now()).days
        
        if days_remaining < 0:
            days_style = {"text": "Deadline passed", "emoji": "❌", "color": "#EF4444"}
        elif days_remaining == 0:
            days_style = {"text": "Due today", "emoji": "⚠️", "color": "#F59E0B"}
        elif days_remaining <= 7:
            days_style = {"text": f"{days_remaining} days left", "emoji": "⏳", "color": "#F59E0B"}
        else:
            days_style = {"text": f"{days_remaining} days left", "emoji": "⏱️", "color": "#10B981"}
    except:
        days_style = {"text": "Invalid date", "emoji": "❓", "color": "#64748B"}
    
    # Create the card
    with st.container():
        st.markdown(f"""
        <div class="goal-card {progress_style['class']}">
            <div class="goal-header">
                <div class="goal-icon">{category_icons.get(category, '🎯')}</div>
                <div class="goal-content">
                    <h3 style="color: #000000 !important;">{goal}</h3>
                    <div class="goal-meta">
                        <span style="color: #000000 !important;">📅 {deadline}</span>
                        <span style="color: {days_style['color']} !important;">{days_style['emoji']} {days_style['text']}</span>
                        <span class="priority-badge" style="background: {priority_colors[priority]['gradient']}">{priority} Priority</span>
                    </div>
                </div>
            </div>
            <div class="progress-section">
                <div class="progress-header">
                    <span style="color: #000000 !important;">Progress {progress_style['emoji']}</span>
                    <span style="color: {progress_style['color']} !important; font-weight: bold;">{progress}%</span>
                </div>
                <div class="progress-container">
                    <div class="progress-bar" style="width: {progress}%; background: {progress_style['color']};">
                        <div class="progress-fill"></div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_reflection_card(date, mood, reflection, tags):
    """Create beautiful reflection card with enhanced visuals"""
    mood_colors = {
        "😊": {"color": "#10B981", "gradient": "linear-gradient(135deg, #10B981 0%, #059669 100%)"},
        "😌": {"color": "#0EA5E9", "gradient": "linear-gradient(135deg, #0EA5E9 0%, #0369A1 100%)"},
        "😢": {"color": "#6366F1", "gradient": "linear-gradient(135deg, #6366F1 0%, #4F46E5 100%)"},
        "😠": {"color": "#EF4444", "gradient": "linear-gradient(135deg, #EF4444 0%, #DC2626 100%)"},
        "😰": {"color": "#F59E0B", "gradient": "linear-gradient(135deg, #F59E0B 0%, #D97706 100%)"},
        "😴": {"color": "#8B5CF6", "gradient": "linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%)"},
        "😐": {"color": "#64748B", "gradient": "linear-gradient(135deg, #64748B 0%, #475569 100%)"},
        "🎯": {"color": "#06B6D4", "gradient": "linear-gradient(135deg, #06B6D4 0%, #0891B2 100%)"},
        "🤔": {"color": "#84CC16", "gradient": "linear-gradient(135deg, #84CC16 0%, #65A30D 100%)"},
        "🌟": {"color": "#F97316", "gradient": "linear-gradient(135deg, #F97316 0%, #EA580C 100%)"}
    }
    
    mood_data = mood_colors.get(mood[0], {"color": "#64748B", "gradient": "linear-gradient(135deg, #64748B 0%, #475569 100%)"})
    
    with st.container():
        st.markdown(f"""
        <div class="reflection-card">
            <div class="reflection-header">
                <div class="mood-icon" style="background: {mood_data['gradient']}">
                    {mood[0]}
                </div>
                <div class="reflection-content">
                    <h3 style="color: #000000 !important;">{mood[1]}</h3>
                    <div class="reflection-meta">
                        <span style="color: #000000 !important;">📅 {date}</span>
                    </div>
                </div>
            </div>
            <div class="reflection-body" style="color: #000000 !important;">
                {reflection}
            </div>
            <div class="reflection-tags">
        """, unsafe_allow_html=True)
        
        # Display tags
        if tags:
            tag_html = "".join([f'<span class="reflection-tag" style="background: {mood_data["color"]}30; color: #000000 !important; border-color: {mood_data["color"]}50;">{tag}</span>' for tag in tags])
            st.markdown(f'<div class="tags-container">{tag_html}</div>', unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)

def create_mood_distribution(entries):
    """Create a beautiful mood distribution chart"""
    if not entries:
        return None
        
    mood_counts = {}
    for entry in entries:
        mood_emoji = entry["mood"][0]
        mood_counts[mood_emoji] = mood_counts.get(mood_emoji, 0) + 1
    
    if not mood_counts:
        return None
        
    mood_colors = {
        "😊": "#10B981", "😌": "#0EA5E9", "😢": "#6366F1", 
        "😠": "#EF4444", "😰": "#F59E0B", "😴": "#8B5CF6",
        "😐": "#64748B", "🎯": "#06B6D4", "🤔": "#84CC16", "🌟": "#F97316"
    }
    
    labels = list(mood_counts.keys())
    values = list(mood_counts.values())
    colors = [mood_colors.get(mood, "#64748B") for mood in labels]
    
    fig = px.pie(
        names=labels, 
        values=values,
        color=labels,
        color_discrete_map=mood_colors,
        title="🎭 Your Mood Distribution"
    )
    
    fig.update_layout(
        height=400,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#000000', family="Arial"),
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.1
        )
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        marker=dict(line=dict(color='white', width=2))
    )
    
    return fig

def run():
    # Enhanced Custom CSS with Black Text
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.2);
    }
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 100" fill="%23ffffff10"><polygon points="0,0 1000,100 1000,0"></polygon></svg>');
        background-size: cover;
    }
    
    /* Goal Cards */
    .goal-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border-left: 5px solid;
    }
    .goal-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }
    .goal-card.excellent { border-left-color: #10B981; }
    .goal-card.good { border-left-color: #F59E0B; }
    .goal-card.needs-work { border-left-color: #EF4444; }
    
    .goal-header {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    .goal-icon {
        font-size: 2.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0.8rem;
        border-radius: 15px;
        color: white;
    }
    .goal-content h3 {
        margin: 0 0 0.5rem 0;
        color: #000000 !important;
        font-size: 1.2rem;
        font-weight: 600;
    }
    .goal-meta {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        color: #000000 !important;
        font-size: 0.9rem;
    }
    .priority-badge {
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        color: white;
        font-weight: 600;
        font-size: 0.8rem;
    }
    
    .progress-section {
        margin-top: 1rem;
    }
    .progress-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
        color: #000000 !important;
    }
    .progress-container {
        width: 100%;
        height: 12px;
        background: rgba(0,0,0,0.1);
        border-radius: 10px;
        overflow: hidden;
    }
    .progress-bar {
        height: 100%;
        border-radius: 10px;
        position: relative;
        transition: all 0.5s ease;
    }
    .progress-fill {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Reflection Cards */
    .reflection-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .reflection-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }
    
    .reflection-header {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    .mood-icon {
        font-size: 2rem;
        padding: 0.8rem;
        border-radius: 15px;
        color: white;
        min-width: 60px;
        text-align: center;
    }
    .reflection-content h3 {
        margin: 0 0 0.3rem 0;
        color: #000000 !important;
        font-size: 1.1rem;
        font-weight: 600;
    }
    .reflection-meta {
        color: #000000 !important;
        font-size: 0.9rem;
    }
    
    .reflection-body {
        color: #000000 !important;
        line-height: 1.7;
        margin: 1.2rem 0;
        padding: 1.2rem;
        background: rgba(0,0,0,0.02);
        border-radius: 12px;
        border-left: 4px solid;
        font-size: 1rem;
    }
    
    .reflection-tags {
        margin-top: 1rem;
    }
    .tags-container {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    .reflection-tag {
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        border: 1px solid;
    }
    
    /* Stats Cards */
    .stats-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.3);
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    .stats-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.12);
    }
    
    /* Section Headers */
    .section-header {
        background: linear-gradient(135deg, #8B5CF6 0%, #0EA5E9 100%);
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.2);
    }
    
    /* Custom buttons */
    .stButton button {
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
    }
    
    /* Streamlit component text colors */
    .stTextInput input, .stTextArea textarea, .stSelectbox label, .stSlider label {
        color: #000000 !important;
    }
    
    .stExpander {
        border: 1px solid rgba(0,0,0,0.1) !important;
        border-radius: 10px !important;
    }
    
    .stExpander label {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    /* FIXED: Data management buttons styling */
    .stDownloadButton button,
    div[data-testid="stDownloadButton"] button,
    div[data-testid="baseButton-secondary"] {
        background-color: #f0f2f6 !important;
        color: #000000 !important;
        border: 1px solid #d0d0d0 !important;
    }
    
    .stDownloadButton button:hover,
    div[data-testid="stDownloadButton"] button:hover,
    div[data-testid="baseButton-secondary"]:hover {
        background-color: #e6e8eb !important;
        color: #000000 !important;
        border: 1px solid #b0b0b0 !important;
    }
    
    /* Reset button specific styling */
    div[data-testid="stButton"] > button[kind="secondary"] {
        background-color: #f0f2f6 !important;
        color: #000000 !important;
        border: 1px solid #d0d0d0 !important;
    }
    
    div[data-testid="stButton"] > button[kind="secondary"]:hover {
        background-color: #e6e8eb !important;
        color: #000000 !important;
        border: 1px solid #b0b0b0 !important;
    }
    
    /* Force black text in empty state */
    .empty-state-title, .empty-state-description {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Enhanced Hero Header
    st.markdown("""
        <div class='main-header'>
            <div style='position: relative; z-index: 2;'>
                <h1 style='color: white; margin: 0; font-size: 3.2rem; font-weight: 800;'>🌱 Growth Journey</h1>
                <p style='color: rgba(255,255,255,0.95); font-size: 1.4rem; margin: 1rem 0; font-weight: 300;'>
                    Your Personal Path to Mental Wellness & Self-Discovery
                </p>
                <div style='display: flex; justify-content: center; gap: 12px; margin-top: 1.5rem;'>
                    <span style='background: rgba(255,255,255,0.25); color: white; padding: 10px 20px; border-radius: 25px; font-size: 0.95rem; font-weight: 500; backdrop-filter: blur(10px);'>Reflect</span>
                    <span style='background: rgba(255,255,255,0.25); color: white; padding: 10px 20px; border-radius: 25px; font-size: 0.95rem; font-weight: 500; backdrop-filter: blur(10px);'>Grow</span>
                    <span style='background: rgba(255,255,255,0.25); color: white; padding: 10px 20px; border-radius: 25px; font-size: 0.95rem; font-weight: 500; backdrop-filter: blur(10px);'>Thrive</span>
                    <span style='background: rgba(255,255,255,0.25); color: white; padding: 10px 20px; border-radius: 25px; font-size: 0.95rem; font-weight: 500; backdrop-filter: blur(10px);'>Transform</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Initialize Session State
    if 'journal_entries' not in st.session_state:
        st.session_state.journal_entries = []
    
    if 'goals' not in st.session_state:
        future_date1 = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        future_date2 = (datetime.now() + timedelta(days=45)).strftime("%Y-%m-%d")
        future_date3 = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")
        
        st.session_state.goals = [
            {
                "goal": "Reduce screen time to 6 hours daily",
                "progress": 65,
                "deadline": future_date1,
                "category": "Digital Wellness",
                "priority": "High"
            },
            {
                "goal": "🧠 Meditate for 10 minutes every morning",
                "progress": 40,
                "deadline": future_date2, 
                "category": "Mental Health",
                "priority": "Medium"
            },
            {
                "goal": "Exercise 3 times per week",
                "progress": 80,
                "deadline": future_date3,
                "category": "Physical Health",
                "priority": "Medium"
            }
        ]

    # Main Content Layout
    col1, col2 = st.columns([2, 1])

    with col1:
        # Daily Reflection Section
        st.markdown("""
            <div class='section-header'>
                <h2 style='color: white; margin: 0; font-size: 1.8rem;'>📖 Daily Reflection</h2>
                <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 1rem;'>
                    Take a moment to reflect on your day and emotions
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        selected_mood = mood_selector()
        
        st.markdown("#### ✍️ Your Reflection")
        reflection = st.text_area(
            "Share your thoughts...",
            placeholder="✨ What made you smile today?\n🌧️ What challenges did you face?\n🙏 What are you grateful for?\n💭 Any insights or learnings?",
            height=180,
            label_visibility="collapsed",
            help="This is your safe space to express your thoughts and feelings"
        )
        
        st.markdown("#### 🏷️ Add Tags")
        tag_options = {
            "Gratitude": "🙏", "Challenge": "🌧️", "Achievement": "🏆", 
            "Learning": "📚", "Breakthrough": "💡", "Self-Care": "💆",
            "Connection": "🤝", "Growth": "🌱", "Mindfulness": "🧘"
        }
        
        selected_tags = []
        tag_cols = st.columns(3)
        for i, (tag, emoji) in enumerate(tag_options.items()):
            with tag_cols[i % 3]:
                if st.checkbox(f"{emoji} {tag}", key=f"tag_{tag}"):
                    selected_tags.append(tag)
        
        # Custom tag
        custom_col1, custom_col2 = st.columns([3, 1])
        with custom_col1:
            custom_tag = st.text_input("Add custom tag:", placeholder="Your custom tag...")
        with custom_col2:
            if st.button("➕ Add", use_container_width=True) and custom_tag.strip():
                selected_tags.append(custom_tag.strip())
                st.rerun()
        
        # Save Reflection Button
        st.markdown("<br>", unsafe_allow_html=True)
        save_col1, save_col2, save_col3 = st.columns([1, 2, 1])
        with save_col2:
            if st.button("💾 Save Reflection", use_container_width=True, type="primary"):
                if reflection.strip() and selected_mood:
                    entry = {
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "mood": selected_mood,
                        "reflection": reflection.strip(),
                        "tags": selected_tags
                    }
                    st.session_state.journal_entries.append(entry)
                    st.session_state.selected_mood = None
                    st.success("✨ Reflection saved successfully!")
                    st.balloons()
                    st.rerun()
                else:
                    if not selected_mood:
                        st.warning("🎭 Please select your mood first!")
                    else:
                        st.warning("📝 Write something meaningful before saving!")

    with col2:
        # Quick Stats Section
        st.markdown("""
            <div style='
                background: linear-gradient(135deg, #10B981 0%, #059669 100%);
                padding: 1.5rem;
                border-radius: 16px;
                margin-bottom: 1.5rem;
                text-align: center;
                box-shadow: 0 8px 25px rgba(16, 185, 129, 0.2);
            '>
                <h3 style='color: white; margin: 0; font-size: 1.4rem;'>📊 Your Journey Stats</h3>
            </div>
        """, unsafe_allow_html=True)
        
        total_reflections = len(st.session_state.journal_entries)
        total_goals = len(st.session_state.goals)
        completed_goals = len([g for g in st.session_state.goals if g["progress"] >= 100])
        
        # Enhanced Stats Cards
        stats_col1, stats_col2 = st.columns(2)
        
        with stats_col1:
            st.markdown(f"""
                <div class='stats-card'>
                    <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>📝</div>
                    <div style='font-size: 1.8rem; font-weight: bold; color: #000000;'>{total_reflections}</div>
                    <div style='color: #000000; font-size: 0.9rem; font-weight: 500;'>Reflections</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class='stats-card'>
                    <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>✅</div>
                    <div style='font-size: 1.8rem; font-weight: bold; color: #000000;'>{completed_goals}</div>
                    <div style='color: #000000; font-size: 0.9rem; font-weight: 500;'>Completed Goals</div>
                </div>
            """, unsafe_allow_html=True)
        
        with stats_col2:
            st.markdown(f"""
                <div class='stats-card'>
                    <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>🎯</div>
                    <div style='font-size: 1.8rem; font-weight: bold; color: #000000;'>{total_goals}</div>
                    <div style='color: #000000; font-size: 0.9rem; font-weight: 500;'>Active Goals</div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.journal_entries:
                # Calculate average mood score for last 7 days
                mood_scores = {
                    "😊": 10, "😌": 9, "🎯": 8, "🌟": 8, "🤔": 7, 
                    "😐": 6, "😴": 5, "😰": 4, "😢": 3, "😠": 2
                }
                recent_entries = st.session_state.journal_entries[-7:]
                if recent_entries:
                    avg_score = sum(mood_scores.get(entry["mood"][0], 5) for entry in recent_entries) / len(recent_entries)
                    mood_emoji = "😊" if avg_score >= 8 else "😌" if avg_score >= 6 else "😐"
                    
                    st.markdown(f"""
                        <div class='stats-card'>
                            <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>{mood_emoji}</div>
                            <div style='font-size: 1.8rem; font-weight: bold; color: #000000;'>{avg_score:.1f}/10</div>
                            <div style='color: #000000; font-size: 0.9rem; font-weight: 500;'>Avg Mood (7d)</div>
                        </div>
                    """, unsafe_allow_html=True)

        # Quick Actions
        st.markdown("""
            <div style='
                background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
                padding: 1.5rem;
                border-radius: 16px;
                margin: 1.5rem 0;
                text-align: center;
                box-shadow: 0 8px 25px rgba(245, 158, 11, 0.2);
            '>
                <h3 style='color: white; margin: 0; font-size: 1.4rem;'>⚡ Quick Actions</h3>
            </div>
        """, unsafe_allow_html=True)
        
        action_col1, action_col2 = st.columns(2)
        with action_col1:
            if st.button("📋 View Reflections", use_container_width=True, key="view_reflections"):
                st.session_state.show_reflections = True
        with action_col2:
            if st.button("🎯 Manage Goals", use_container_width=True, key="manage_goals"):
                st.session_state.show_goals = True

    # Goals Management Section
    st.markdown("""
        <div style='
            background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
            padding: 1.5rem;
            border-radius: 16px;
            margin: 2rem 0 1.5rem 0;
            box-shadow: 0 8px 25px rgba(239, 68, 68, 0.2);
        '>
            <h2 style='color: white; margin: 0; text-align: center; font-size: 1.8rem;'>🎯 Personal Goals</h2>
            <p style='color: rgba(255,255,255,0.9); text-align: center; margin: 0.5rem 0 0 0; font-size: 1rem;'>
                Set meaningful goals and track your progress
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    goal_cols = st.columns(2)
    
    with goal_cols[0]:
        st.markdown("#### 🚀 Set New Goal")
        with st.form("goal_form", clear_on_submit=True):
            goal = st.text_input("🎯 Goal Description", placeholder="What do you want to achieve?")
            
            colA, colB = st.columns(2)
            with colA:
                category = st.selectbox(
                    "Category",
                    ["Digital Wellness", "Mental Health", "Physical Health", "Social", "Productivity", "Sleep", "Lifestyle"]
                )
                deadline = st.date_input("📅 Deadline", datetime.now() + timedelta(days=30))
            with colB:
                priority = st.selectbox("🎯 Priority", ["High", "Medium", "Low"])
                initial_progress = st.slider("📊 Initial Progress", 0, 100, 0)
            
            if st.form_submit_button("🎯 Add Goal", use_container_width=True):
                if goal.strip():
                    new_goal = {
                        "goal": goal.strip(),
                        "progress": initial_progress,
                        "deadline": deadline.strftime("%Y-%m-%d"),
                        "category": category,
                        "priority": priority
                    }
                    st.session_state.goals.append(new_goal)
                    st.success("🎉 New goal added successfully!")
                    st.rerun()

    with goal_cols[1]:
        st.markdown("#### 📈 Goals Overview")
        if st.session_state.goals:
            total_goals = len(st.session_state.goals)
            completed_goals = len([g for g in st.session_state.goals if g["progress"] >= 100])
            avg_progress = sum(g["progress"] for g in st.session_state.goals) / total_goals
            
            # Enhanced metrics display
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            with metric_col1:
                st.metric("Total Goals", total_goals, delta=f"{total_goals} active")
            with metric_col2:
                st.metric("Completed", completed_goals, delta=f"{completed_goals} done")
            with metric_col3:
                st.metric("Avg Progress", f"{avg_progress:.1f}%")
            
            # Progress chart
            goal_data = []
            for goal in st.session_state.goals:
                goal_data.append({
                    "Goal": goal["goal"][:25] + "..." if len(goal["goal"]) > 25 else goal["goal"],
                    "Progress": goal["progress"],
                    "Category": goal["category"]
                })
            
            df_goals = pd.DataFrame(goal_data)
            fig = px.bar(
                df_goals, 
                y="Goal", 
                x="Progress",
                color="Category",
                orientation='h',
                title="<b>Goal Progress Overview</b>",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_layout(
                height=350,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#000000', family="Arial"),
                title_font=dict(size=18, color='#000000')
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("🌟 No goals set yet. Start by adding your first goal!")

    # Display Goals with Enhanced Filters
    if st.session_state.goals:
        st.markdown("#### 📋 Your Goals")
        
        # Enhanced Filtering
        filter_cols = st.columns(4)
        with filter_cols[0]:
            category_filter = st.selectbox("Filter by Category", ["All"] + list(set(g["category"] for g in st.session_state.goals)), key="cat_filter")
        with filter_cols[1]:
            priority_filter = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"], key="pri_filter")
        with filter_cols[2]:
            progress_filter = st.selectbox("Filter by Progress", ["All", "Not Started (0%)", "In Progress (1-99%)", "Completed (100%)"], key="prog_filter")
        with filter_cols[3]:
            sort_by = st.selectbox("Sort by", ["Priority", "Progress", "Deadline", "Category"], key="sort_filter")
        
        filtered_goals = st.session_state.goals.copy()
        
        if category_filter != "All":
            filtered_goals = [g for g in filtered_goals if g["category"] == category_filter]
        if priority_filter != "All":
            filtered_goals = [g for g in filtered_goals if g["priority"] == priority_filter]
        if progress_filter != "All":
            if progress_filter == "Not Started (0%)":
                filtered_goals = [g for g in filtered_goals if g["progress"] == 0]
            elif progress_filter == "In Progress (1-99%)":
                filtered_goals = [g for g in filtered_goals if 0 < g["progress"] < 100]
            elif progress_filter == "Completed (100%)":
                filtered_goals = [g for g in filtered_goals if g["progress"] == 100]
        
        # Sort goals
        if sort_by == "Priority":
            priority_order = {"High": 3, "Medium": 2, "Low": 1}
            filtered_goals.sort(key=lambda x: priority_order[x["priority"]], reverse=True)
        elif sort_by == "Progress":
            filtered_goals.sort(key=lambda x: x["progress"], reverse=True)
        elif sort_by == "Deadline":
            filtered_goals.sort(key=lambda x: x["deadline"])
        elif sort_by == "Category":
            filtered_goals.sort(key=lambda x: x["category"])
        
        # Display enhanced goal cards
        for i, goal in enumerate(filtered_goals):
            create_goal_card(
                goal["goal"],
                goal["progress"],
                goal["deadline"],
                goal["category"],
                goal["priority"]
            )
            
            # Enhanced progress update section
            with st.expander(f"📊 Update Progress: {goal['goal'][:35]}{'...' if len(goal['goal']) > 35 else ''}"):
                update_col1, update_col2, update_col3 = st.columns([3, 1, 1])
                with update_col1:
                    new_progress = st.slider(
                        "Progress",
                        0, 100, goal["progress"],
                        key=f"slider_{i}",
                        help="Adjust the progress percentage"
                    )
                with update_col2:
                    if st.button("Update", key=f"update_{i}", use_container_width=True, type="primary"):
                        goal["progress"] = new_progress
                        st.success("✅ Progress updated successfully!")
                        st.rerun()
                with update_col3:
                    if st.button("Delete", key=f"delete_{i}", use_container_width=True, type="secondary"):
                        st.session_state.goals.remove(goal)
                        st.success("🗑️ Goal deleted successfully!")
                        st.rerun()

    # Reflection History & Analytics
    if st.session_state.journal_entries:
        st.markdown("""
            <div style='
                background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
                padding: 1.5rem;
                border-radius: 16px;
                margin: 2rem 0 1.5rem 0;
                box-shadow: 0 8px 25px rgba(99, 102, 241, 0.2);
            '>
                <h2 style='color: white; margin: 0; text-align: center; font-size: 1.8rem;'>📚 Reflection History</h2>
                <p style='color: rgba(255,255,255,0.9); text-align: center; margin: 0.5rem 0 0 0; font-size: 1rem;'>
                    Review your journey and track your emotional patterns
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Mood Distribution Only (No Timeline)
        st.markdown("#### 🎭 Mood Distribution")
        distribution_fig = create_mood_distribution(st.session_state.journal_entries)
        if distribution_fig:
            st.plotly_chart(distribution_fig, use_container_width=True)
        
        # Recent Reflections with Enhanced Filtering
        st.markdown("#### 📖 Recent Reflections")
        
        ref_filter_cols = st.columns(3)
        with ref_filter_cols[0]:
            show_count = st.slider("Show entries", 1, 10, 5, key="reflection_count")
        with ref_filter_cols[1]:
            sort_reflections = st.selectbox("Sort order", ["Newest First", "Oldest First"], key="reflection_sort")
        with ref_filter_cols[2]:
            mood_filter = st.selectbox("Filter by mood", ["All"] + list(set(entry["mood"][1] for entry in st.session_state.journal_entries)), key="mood_filter")
        
        display_entries = st.session_state.journal_entries.copy()
        
        if mood_filter != "All":
            display_entries = [entry for entry in display_entries if entry["mood"][1] == mood_filter]
        
        display_entries = display_entries[-show_count:]
        if sort_reflections == "Newest First":
            display_entries = display_entries[::-1]
        
        for i, entry in enumerate(display_entries):
            create_reflection_card(
                entry["date"],
                entry["mood"],
                entry["reflection"],
                entry["tags"]
            )

    else:
        # FIXED: Empty State with BLACK TEXT
        st.markdown("""
        <div style='
            background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%);
            border: 2px dashed #94a3b8;
            border-radius: 20px;
            padding: 4rem 2rem;
            text-align: center;
            margin: 2rem 0;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        '>
            <div style='font-size: 5rem; margin-bottom: 1.5rem;'>📝</div>
            <h3 class="empty-state-title" style='color: #000000 !important; margin-bottom: 1rem; font-size: 1.5rem; font-weight: 600;'>Your Reflection Journey Awaits</h3>
            <p class="empty-state-description" style='color: #000000 !important; max-width: 500px; margin: 0 auto 2rem auto; font-size: 1rem; line-height: 1.6;'>
                Start your wellness journey by writing your first reflection. 
                Track your moods, set goals, and watch yourself grow day by day.
            </p>
            <div style='
                background: linear-gradient(135deg, #8B5CF6 0%, #0EA5E9 100%);
                color: white;
                padding: 12px 30px;
                border-radius: 25px;
                display: inline-block;
                font-weight: 600;
                font-size: 1rem;
                box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
            '>
                ✨ Begin Your Journey
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Enhanced Data Management Section
    st.markdown("---")
    st.markdown("### 💾 Your Data")
    
    data_cols = st.columns(3)
    
    with data_cols[0]:
        if st.session_state.journal_entries:
            reflections_json = json.dumps(st.session_state.journal_entries, indent=2, ensure_ascii=False)
            st.download_button(
                label="📄 Export Reflections",
                data=reflections_json,
                file_name=f"mindspace_reflections_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True,
                help="Download all your reflections as a JSON file"
            )
        else:
            st.button("📄 Export Reflections", disabled=True, use_container_width=True)
    
    with data_cols[1]:
        if st.session_state.goals:
            goals_json = json.dumps(st.session_state.goals, indent=2, ensure_ascii=False)
            st.download_button(
                label="📊 Export Goals", 
                data=goals_json,
                file_name=f"mindspace_goals_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True,
                help="Download all your goals as a JSON file"
            )
        else:
            st.button("📊 Export Goals", disabled=True, use_container_width=True)
    
    with data_cols[2]:
        if st.button("🔄 Reset All Data", use_container_width=True, key="reset_data"):
            if st.checkbox("I understand this will delete all my reflections and goals", key="reset_confirm"):
                st.session_state.journal_entries = []
                st.session_state.goals = []
                st.session_state.selected_mood = None
                st.success("🗑️ All data has been reset successfully!")
                st.rerun()

    # FIXED: Additional CSS to ensure button styling works
    st.markdown("""
    <style>
    /* FIXED: Ensure all data management buttons have consistent styling */
    .stDownloadButton button,
    div[data-testid="stDownloadButton"] button,
    div[data-testid="baseButton-secondary"] {
        background-color: #f0f2f6 !important;
        color: #000000 !important;
        border: 1px solid #d0d0d0 !important;
    }
    
    .stDownloadButton button:hover,
    div[data-testid="stDownloadButton"] button:hover,
    div[data-testid="baseButton-secondary"]:hover {
        background-color: #e6e8eb !important;
        color: #000000 !important;
        border: 1px solid #b0b0b0 !important;
    }
    
    /* FIXED: Reset button specific styling */
    div[data-testid="stButton"] > button[kind="secondary"] {
        background-color: #f0f2f6 !important;
        color: #000000 !important;
        border: 1px solid #d0d0d0 !important;
    }
    
    div[data-testid="stButton"] > button[kind="secondary"]:hover {
        background-color: #e6e8eb !important;
        color: #000000 !important;
        border: 1px solid #b0b0b0 !important;
    }
    
    /* FIXED: Empty state text color */
    .empty-state-title, .empty-state-description {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Enhanced Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='
            text-align: center; 
            color: #000000; 
            padding: 2rem 1rem;
            background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.7) 100%);
            border-radius: 16px;
            margin-top: 2rem;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.3);
        '>
            <div style='font-size: 2.5rem; margin-bottom: 1rem;'>🌿</div>
            <h4 style='color: #000000 !important; margin-bottom: 0.5rem; font-size: 1.3rem; font-weight: 600;'>MindSync Growth Journey</h4>
            <p style='margin: 0; font-size: 1rem; line-height: 1.6; color: #000000 !important;'>
                Every reflection is a step forward. Every goal is a dream in motion.<br>
                Your journey to wellness is unique and beautiful. Keep growing! 🌟
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    run()