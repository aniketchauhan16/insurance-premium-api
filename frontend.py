import streamlit as st
import requests

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Premium Predictor | AI",
    page_icon="✨",
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- ADVANCED COMPACT & BOXED CSS ---
st.markdown("""
    <style>
    /* Ultra-compact global container */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
        max-width: 1400px;
    }
    
    /* Gradient Title */
    .title-highlight {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 2.5rem;
        text-align: center;
        letter-spacing: -1px;
        margin-bottom: 0.2rem;
    }
    
    .subtitle {
        color: #94a3b8;
        text-align: center;
        font-size: 1rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }

    /* --- THE PREMIUM BOX STYLING --- */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.4) 0%, rgba(15, 23, 42, 0.1) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s ease-in-out;
        height: 100%; 
    }
    
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border: 1px solid rgba(79, 172, 254, 0.3) !important;
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.6) 0%, rgba(15, 23, 42, 0.2) 100%) !important;
        box-shadow: 0 10px 30px -10px rgba(79, 172, 254, 0.15) !important;
    }

    .section-hdr {
        color: #e2e8f0;
        font-size: 1.2rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        padding-bottom: 10px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .bmi-glass {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        border-radius: 10px;
        padding: 12px 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 10px 0 20px 0;
    }
    
    /* --- UPGRADED TERMINAL RESULT CARD --- */
    .premium-result {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.95) 0%, rgba(15, 23, 42, 0.6) 100%);
        border: 1px solid rgba(79, 172, 254, 0.3);
        box-shadow: 0 8px 25px -5px rgba(79, 172, 254, 0.4), inset 0 0 15px rgba(79, 172, 254, 0.1);
        border-radius: 16px;
        padding: 2rem 1.5rem 1.5rem 1.5rem; /* Tweaked padding to fit perfectly */
        text-align: center;
        position: relative;
        overflow: hidden;
        margin-top: 25px;
        margin-bottom: 10px; /* Prevents the clipping overlap at the bottom */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 220px; /* Gives the box a solid structural height */
    }
    
    .premium-result::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, #00f2fe, #4facfe, #00f2fe);
        background-size: 200% auto;
        animation: gradient-shift 3s linear infinite;
    }
    @keyframes gradient-shift {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }
    
    .result-label {
        color: #94a3b8;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
    }
    
    .result-tier {
        font-size: 3.5rem; /* Made slightly larger */
        font-weight: 900;
        color: #ffffff;
        text-shadow: 0 0 25px rgba(79, 172, 254, 0.6);
        margin: 10px 0;
        letter-spacing: 1px;
    }
    
    .metrics-text {
        color: #64748b;
        font-size: 12px;
        margin-top: auto; 
        margin-bottom: 0;
        padding-top: 15px;
        border-top: 1px solid rgba(255, 255, 255, 0.05); /* Sleek divider line */
    }
    </style>
""", unsafe_allow_html=True)

# --- CONSTANTS ---
API_URL = "http://localhost:8000/predict"

OCCUPATION_MAP = {
    "Private Sector": "private_job",
    "Government Sector": "government_job",
    "Business Owner": "buisness_owner",
    "Freelancer": "freelancer",
    "Student": "student",
    "Retired": "retired",
    "Unemployed": "unemployed"
}

# --- HEADER SECTION ---
st.markdown('<div class="title-highlight">Insurance Premium Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Predictive risk assessment powered by demographic and biometric analysis.</div>', unsafe_allow_html=True)

# --- 3-COLUMN BOXED ARCHITECTURE ---
col_bio, col_socio, col_action = st.columns([1, 1, 1], gap="medium")

with col_bio:
    with st.container(border=True):
        st.markdown('<div class="section-hdr">🧬 Biometric Profile</div>', unsafe_allow_html=True)
        
        age = st.slider("Age (Years)", min_value=18, max_value=100, value=30)
        weight = st.slider("Weight (kg)", min_value=40.0, max_value=150.0, value=65.0, step=0.5)
        height = st.slider("Height (m)", min_value=1.40, max_value=2.20, value=1.70, step=0.01)
        
        # BMI Calculation
        bmi = weight / (height ** 2)
        if bmi < 18.5: bmi_color, bmi_status = "#fbbf24", "Underweight"
        elif bmi < 25: bmi_color, bmi_status = "#34d399", "Optimal"
        elif bmi < 30: bmi_color, bmi_status = "#fbbf24", "Overweight"
        else: bmi_color, bmi_status = "#f87171", "High Risk"
        
        st.markdown(f"""
            <div class="bmi-glass">
                <div style="color:#64748b; font-size:11px; text-transform:uppercase; letter-spacing:1px;">Calculated BMI</div>
                <div>
                    <span style="font-size:22px; font-weight:700; color:{bmi_color};">{bmi:.1f}</span>
                    <span style="color:#94a3b8; font-size:13px; font-weight:500;"> | {bmi_status}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        smoker_choice = st.radio("Tobacco Usage", options=["Non-Smoker", "Active Smoker"], horizontal=True)
        smoker = True if smoker_choice == "Active Smoker" else False

with col_socio:
    with st.container(border=True):
        st.markdown('<div class="section-hdr">💼 Socioeconomic Factors</div>', unsafe_allow_html=True)
        
        income_lpa = st.slider("Annual Income (LPA)", min_value=1.0, max_value=50.0, value=10.0, step=0.5)
        
        display_occupation = st.selectbox("Occupational Field", options=list(OCCUPATION_MAP.keys()))
        occupation = OCCUPATION_MAP[display_occupation] 
        
        city = st.text_input("Primary Residence", value="Mumbai", placeholder="e.g. Mumbai, Delhi")

with col_action:
    with st.container(border=True):
        st.markdown('<div class="section-hdr">⚡ System Terminal</div>', unsafe_allow_html=True)
        
        submit_button = st.button("Generate AI Assessment", use_container_width=True, type="primary")
        
        # --- API CONNECTION & RESULT ---
        if submit_button:
            input_data = {
                "age": age,
                "weight": weight,
                "height": height,
                "income_lpa": income_lpa,
                "smoker": smoker,
                "city": city,
                "occupation": occupation
            }

            with st.spinner("Encrypting & querying engine..."):
                try:
                    response = requests.post(API_URL, json=input_data)
                    
                    if response.status_code == 200:
                        result = response.json()
                        category = result.get('predicted_category', 'Unknown')
                        
                        st.markdown(f"""
                            <div class="premium-result">
                                <div class="result-label">Assessed Premium Tier</div>
                                <div class="result-tier">{category}</div>
                                <div class="metrics-text">Metrics applied successfully.</div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                    else:
                        st.error(f"⚠️ API Error: {response.status_code}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("🚨 Connection Failed: Ensure backend is running.")