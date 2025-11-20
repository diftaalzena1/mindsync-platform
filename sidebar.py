import streamlit as st
import os

def show_sidebar():
    logo_path = "assets/logo.jpg"

    st.sidebar.markdown("""
        <style>
        /* Sidebar background dengan gradient */
        [data-testid="stSidebar"] { 
            background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
            padding: 16px 12px;
        }

        /* Logo image directly (no background wrapper) */
        .logo-img img { 
            border-radius: 12px; 
            max-height: 80px;
            object-fit: contain;
        }

        /* User greeting dengan glassmorphism */
        .greeting-box {
            background: linear-gradient(135deg, rgba(14, 165, 233, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            color: #F8FAFC;
            padding: 16px;
            border-radius: 12px;
            font-weight: 600;
            margin-bottom: 20px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        /* Section headers */
        .section-header {
            font-weight: 700;
            font-size: 14px;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin: 20px 0 12px 0;
            padding-left: 8px;
        }

        /* Profile cards */
        .profile-card {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 12px;
            margin-bottom: 8px;
        }
        .profile-label {
            font-size: 12px;
            color: #94A3B8;
            margin-bottom: 4px;
        }
        .profile-value {
            font-size: 14px;
            color: #F8FAFC;
            font-weight: 600;
        }

        /* Quick stats */
        .stats-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            margin: 15px 0;
        }
        .stat-card {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 8px;
            padding: 10px;
            text-align: center;
        }
        .stat-value {
            font-size: 16px;
            font-weight: 700;
            color: #0EA5E9;
            margin-bottom: 2px;
        }
        .stat-label {
            font-size: 10px;
            color: #94A3B8;
        }

        /* FIXED: Input styling - BLACK TEXT FOR ALL FORM INPUTS */
        [data-testid="stSidebar"] .stNumberInput input,
        [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div,
        [data-testid="stSidebar"] .stTextInput input {
            color: #000000 !important;
            background-color: rgba(255,255,255,0.9) !important;
        }

        /* FIXED: Number input specific styling */
        [data-testid="stSidebar"] .stNumberInput input {
            color: #000000 !important;
            background-color: rgba(255,255,255,0.9) !important;
            border: 1px solid rgba(255,255,255,0.3) !important;
            border-radius: 8px !important;
        }

        /* FIXED: Selectbox specific styling */
        [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
            color: #000000 !important;
            background-color: rgba(255,255,255,0.9) !important;
        }

        /* FIXED: Button styling - BLACK TEXT FOR ALL BUTTONS */
        [data-testid="stSidebar"] .stButton button,
        [data-testid="stSidebar"] .stFormSubmitButton button,
        [data-testid="stSidebar"] form .stButton button {
            background: linear-gradient(135deg, #0EA5E9 0%, #6366F1 100%) !important;
            color: #000000 !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 8px 16px !important;
            width: 100% !important;
            transition: all 0.3s ease !important;
        }

        [data-testid="stSidebar"] .stButton button:hover,
        [data-testid="stSidebar"] .stFormSubmitButton button:hover,
        [data-testid="stSidebar"] form .stButton button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(14, 165, 233, 0.4) !important;
        }

        /* FIXED: Specific styling untuk form submit button text */
        [data-testid="stSidebar"] .stButton button p,
        [data-testid="stSidebar"] .stFormSubmitButton button p,
        [data-testid="stSidebar"] form .stButton button p {
            color: #000000 !important;
            font-weight: 600 !important;
        }

        /* FIXED: Ensure all button text is black */
        [data-testid="stSidebar"] .stButton button span,
        [data-testid="stSidebar"] .stFormSubmitButton button span,
        [data-testid="stSidebar"] form .stButton button span {
            color: #000000 !important;
            font-weight: 600 !important;
        }

        /* Label styling untuk form - WHITE TEXT */
        [data-testid="stSidebar"] .stNumberInput label,
        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stTextInput label {
            color: #F8FAFC !important;
        }

        /* Footer */
        .sidebar-footer {
            font-size: 11px;
            color: #64748B;
            text-align: center;
            padding: 15px 0 5px 0;
            border-top: 1px solid rgba(255,255,255,0.1);
            margin-top: 20px;
        }

        /* Hide streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Additional styling untuk form di expander */
        .streamlit-expander {
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 8px !important;
        }
        
        .streamlit-expanderHeader {
            color: #F8FAFC !important;
            font-weight: 600 !important;
        }
        
        /* FIXED: Dropdown options styling */
        [data-baseweb="select"] div {
            color: #000000 !important;
        }
        
        [data-baseweb="popover"] div {
            color: #000000 !important;
            background-color: white !important;
        }
        
        /* FIXED: Placeholder text */
        [data-testid="stSidebar"] .stTextInput input::placeholder {
            color: #666666 !important;
        }

        /* FIXED: Ensure all text in form inputs is black */
        [data-testid="stSidebar"] input, 
        [data-testid="stSidebar"] select,
        [data-testid="stSidebar"] .st-bb,
        [data-testid="stSidebar"] .st-bj {
            color: #000000 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # ❗ LOGO tanpa background, langsung tampil clean
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, use_container_width=True)
    else:
        st.sidebar.markdown("""
            <div style='text-align: center; color: #64748B; padding: 20px;'>
                <div style='font-size: 2rem;'>🧠</div>
                <strong>MindSync</strong>
            </div>
        """, unsafe_allow_html=True)

    # User Greeting Section
    if "username" not in st.session_state:
        username = st.sidebar.text_input("✨ Masukkan nama panggilan:", placeholder="Ketik nama kamu...")
        col1, col2 = st.sidebar.columns([2, 1])
        with col1:
            if st.button("🚀 Mulai Journey", use_container_width=True):
                if username.strip() != "":
                    st.session_state.username = username.strip()
                    st.rerun()
                else:
                    st.sidebar.warning("Masukkan nama dulu ya! ✨")
    else:
        st.sidebar.markdown(
            f'''
            <div class="greeting-box">
                <div style="font-size: 2rem; margin-bottom: 8px;">👋</div>
                <div style="font-size: 16px; margin-bottom: 4px;">Halo, {st.session_state.username}!</div>
                <div style="font-size: 12px; opacity: 0.8;">Siap sync digital wellbeing-mu?</div>
            </div>
            ''', 
            unsafe_allow_html=True
        )
        
        if st.sidebar.button("🔄 Ganti Nama", use_container_width=True):
            del st.session_state.username
            st.rerun()

    # Quick Stats Section
    if "username" in st.session_state:
        st.sidebar.markdown('<div class="section-header">📊 Progress Hari Ini</div>', unsafe_allow_html=True)
        
        wellness_score = st.session_state.get('predicted_wellness', 65)
        screen_time = st.session_state.get('screen_time_hours', 0)
        
        st.sidebar.markdown('''
            <div class="stats-container">
                <div class="stat-card">
                    <div class="stat-value">''' + f"{wellness_score:.0f}" + '''</div>
                    <div class="stat-label">Wellness</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">''' + f"{screen_time:.0f}" + '''h</div>
                    <div class="stat-label">Screen Time</div>
                </div>
            </div>
        ''', unsafe_allow_html=True)

    # Profile Section
    st.sidebar.markdown('<div class="section-header">👤 Profil Digital</div>', unsafe_allow_html=True)
    
    # Initialize user profile if not exists
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            'age': 25, 
            'gender': "Female", 
            'occupation': "Student",
            'work_mode': "In-person"
        }
    
    # Edit Profile Form
    with st.sidebar.expander("📝 Edit Profil", expanded=False):
        with st.form(key='profile_form'):
            col1, col2 = st.columns(2)
            with col1:
                new_age = st.number_input(
                    "Usia", 
                    min_value=10, 
                    max_value=80, 
                    value=st.session_state.user_profile['age'],
                    key="age_input"
                )
            with col2:
                new_gender = st.selectbox(
                    "Gender",
                    ["Female", "Male", "Other"],
                    index=["Female", "Male", "Other"].index(st.session_state.user_profile['gender']),
                    key="gender_select"
                )
            
            new_occupation = st.selectbox(
                "Pekerjaan",
                ["Student", "Employed", "Self-employed", "Freelancer", "Retired"],
                index=["Student", "Employed", "Self-employed", "Freelancer", "Retired"].index(st.session_state.user_profile['occupation']),
                key="occupation_select"
            )
            
            new_work_mode = st.selectbox(
                "Mode Kerja/Belajar",
                ["Remote", "In-person", "Hybrid"],
                index=["Remote", "In-person", "Hybrid"].index(st.session_state.user_profile['work_mode']),
                key="work_mode_select"
            )
            
            # Submit button untuk update profile - DENGAN STYLING KHUSUS
            submitted = st.form_submit_button("💾 Update Profil", use_container_width=True)
            if submitted:
                st.session_state.user_profile['age'] = new_age
                st.session_state.user_profile['gender'] = new_gender
                st.session_state.user_profile['occupation'] = new_occupation
                st.session_state.user_profile['work_mode'] = new_work_mode
                st.success("✅ Profil berhasil diupdate!")
                st.rerun()

    # Display Current Profile (akan update otomatis setelah form disubmit)
    st.sidebar.markdown(f'''
        <div class="profile-card">
            <div class="profile-label">👤 Profil Singkat</div>
            <div class="profile-value">{st.session_state.user_profile['age']} tahun • {st.session_state.user_profile['occupation']}</div>
            <div style="font-size: 11px; color: #94A3B8; margin-top: 4px;">
                {st.session_state.user_profile['gender']} • {st.session_state.user_profile['work_mode']}
            </div>
        </div>
    ''', unsafe_allow_html=True)
    st.sidebar.write("")
