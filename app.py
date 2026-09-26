import streamlit as st
from src.predict import predict_job_risk
from src.risk_analyzer import analyze_risk

# --- Page Configuration ---
st.set_page_config(
    page_title="JobShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Styling ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
    }

    /* Background gradient */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Glassmorphism for inputs */
    .stTextInput > div > div > input, .stTextArea > div > textarea, .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus, .stTextArea > div > textarea:focus, .stSelectbox > div > div:focus {
        background: rgba(255, 255, 255, 0.95);
        box-shadow: 0 0 0 2px #4facfe, 0 8px 15px rgba(0,0,0,0.1);
        border-color: transparent;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(79, 172, 254, 0.6) !important;
    }

    /* Form submit button specifically */
    [data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        box-shadow: 0 4px 15px rgba(118, 75, 162, 0.4) !important;
    }
    
    [data-testid="stFormSubmitButton"] > button:hover {
        box-shadow: 0 6px 20px rgba(118, 75, 162, 0.6) !important;
    }

    /* Main content styling */
    .main .block-container {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2.5rem;
        margin-top: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.5);
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.3);
    }

    /* Headers */
    h1, h2, h3, h4 {
        color: #1a202c !important;
        font-weight: 700 !important;
    }

    h1 {
        background: -webkit-linear-gradient(45deg, #4facfe, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Alert boxes */
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    .risk-high { color: #d32f2f; font-weight: bold; }
    .risk-medium { color: #f57c00; font-weight: bold; }
    .risk-low { color: #388e3c; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("🛡️ JobShield AI")
st.subheader("Explainable Job Scam Risk Detection System")
st.markdown("Enter the details of a job posting below to estimate its legitimacy, or try one of the demonstration examples.")

# --- Demo Examples ---
st.markdown("### Demonstration Examples")
col1, col2 = st.columns(2)
with col1:
    if st.button("Load Normal-looking Example"):
        st.session_state.demo_title = "Data Analyst"
        st.session_state.demo_company = "Tech Innovations Inc."
        st.session_state.demo_desc = "We are looking for a Data Analyst to join our team and help us make data-driven decisions. You will work closely with the product and engineering teams."
        st.session_state.demo_req = "Bachelor's degree in Computer Science, Statistics, or related field. 2+ years of SQL and Python experience."
        st.session_state.demo_ben = "Health insurance, 401(k) matching, 20 days PTO."
        st.session_state.demo_loc = "New York, NY"
        st.session_state.demo_emp = "Full-time"
        st.session_state.demo_sal = "$80,000 - $100,000"
        st.session_state.demo_web = "https://www.techinnovations.example.com"
with col2:
    if st.button("Load Suspicious-looking Example"):
        st.session_state.demo_title = "DATA ENTRY WORK FROM HOME - URGENT HIRING"
        st.session_state.demo_company = ""
        st.session_state.demo_desc = "Earn thousands working from home! Easy money! We need people immediately. You must pay a $50 registration fee to cover your training materials before you start."
        st.session_state.demo_req = "No experience necessary."
        st.session_state.demo_ben = "Unlimited income potential."
        st.session_state.demo_loc = "Remote"
        st.session_state.demo_emp = "Part-time"
        st.session_state.demo_sal = "$5,000/week"
        st.session_state.demo_web = ""

# Defaults
def get_val(key):
    return st.session_state.get(key, "")

# --- Input Form ---
st.markdown("### Job Posting Details")
with st.form("job_input_form"):
    c1, c2 = st.columns(2)
    with c1:
        job_title = st.text_input("Job Title*", value=get_val("demo_title"))
        company_name = st.text_input("Company Name", value=get_val("demo_company"))
        location = st.text_input("Location", value=get_val("demo_loc"))
        employment_type = st.selectbox("Employment Type", ["Unknown", "Full-time", "Part-time", "Contract", "Temporary"], index=0 if not get_val("demo_emp") else ["Unknown", "Full-time", "Part-time", "Contract", "Temporary"].index(get_val("demo_emp")))
        
    with c2:
        salary_info = st.text_input("Salary Information", value=get_val("demo_sal"))
        company_website = st.text_input("Company Website", value=get_val("demo_web"))
        
    job_description = st.text_area("Job Description*", value=get_val("demo_desc"), height=150)
    requirements = st.text_area("Requirements", value=get_val("demo_req"), height=100)
    benefits = st.text_area("Benefits", value=get_val("demo_ben"), height=100)
    
    submitted = st.form_submit_button("🔍 Analyze Job")

# --- Processing & Results ---
if submitted:
    if not job_title.strip() or not job_description.strip():
        st.error("Please provide at least a Job Title and Job Description.")
    else:
        with st.spinner("Analyzing job posting..."):
            # Map frontend inputs to backend features
            job_data = {
                "job_title": job_title,
                "job_description": job_description,
                "requirements": requirements,
                "benefits": benefits,
                "company_profile": company_name,
                "telecommuting": 1 if "remote" in location.lower() or "work from home" in job_description.lower() or "work from home" in job_title.lower() else 0,
                "has_company_logo": 0, # Cannot determine from text alone easily
                "has_company_profile": 1 if company_name else 0,
                "employment_type": employment_type if employment_type != "Unknown" else "",
                "required_experience": "", 
                "required_education": "",
                "salary_range": salary_info,
                "location": location,
                
                # Rule-based heuristics triggers
                "payment_request": 1 if any(w in job_description.lower() for w in ['fee', 'deposit', 'pay to apply']) else 0,
                "unrealistic_salary": 1 if 'thousands' in job_description.lower() or 'week' in salary_info.lower() else 0,
                "urgency_language": 1 if 'urgent' in job_description.lower() or 'urgent' in job_title.lower() else 0,
                "suspicious_contact": 0,
                "missing_company_info": 1 if not company_name else 0
            }

            # 1. ML Prediction
            ml_result = predict_job_risk(job_data)
            
            if "error" in ml_result:
                st.error(f"System Error: {ml_result['error']}")
                st.info("Have you trained the ML model yet? Run `python src/train_model.py` first.")
            else:
                ml_prob = ml_result["risk_score"]
                
                # 2. Rule-Based Explainable Analysis
                final_analysis = analyze_risk(job_data, ml_prob)
                
                # --- Display Results ---
                st.markdown("---")
                st.markdown("## 📊 Analysis Results")
                
                score = final_analysis['risk_score']
                level = final_analysis['risk_level']
                
                # Dynamic styling
                if level == "High":
                    st.error(f"### Risk Assessment: HIGH (Score: {score}/100)")
                elif level == "Medium":
                    st.warning(f"### Risk Assessment: MEDIUM (Score: {score}/100)")
                else:
                    st.success(f"### Risk Assessment: LOW (Score: {score}/100)")
                    
                # Explanation
                st.markdown("#### Score Explanation")
                st.info(final_analysis['explanation'])
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("#### 🚨 Detected Warning Signs")
                    if final_analysis['warning_signs']:
                        for warning in final_analysis['warning_signs']:
                            st.warning(f"**{warning['indicator']}**: {warning['explanation']}")
                    else:
                        st.success("No major warning signs detected.")
                        
                with col_b:
                    st.markdown("#### ✅ Positive Indicators")
                    if final_analysis['positive_signs']:
                        for pos in final_analysis['positive_signs']:
                            st.success(pos)
                    else:
                        st.info("No strong positive indicators detected.")
                
                st.markdown("#### 🤖 ML Component Output")
                st.write(f"**Model Confidence:** {ml_prob*100:.1f}%")

                st.markdown("---")
                st.markdown("### 💡 Recommendations")
                st.markdown("""
                * **Verify the employer** through an official company website or trusted third-party directory.
                * **Avoid paying money** to apply for a job or to receive "training materials".
                * **Verify suspicious contact information** (e.g., if they ask to interview via Telegram or WhatsApp).
                * **Do not share sensitive personal or financial information** until the employer is fully verified.
                
                *(Note: JobShield AI provides risk indicators based on historical patterns. It does not definitively prove a job is a scam. Always exercise your own judgment.)*
                """)

# --- Sidebar About Section ---
with st.sidebar:
    st.header("About JobShield AI")
    st.markdown("""
    **The Problem:** 
    Job seekers are increasingly targeted by sophisticated employment scams that steal money or identity.
    
    **The Solution:** 
    JobShield AI uses a hybrid approach to detect potential fraud.
    
    **Machine Learning:** 
    A Random Forest model analyzes text patterns (via NLP/TF-IDF) and structured data to calculate a baseline probability of fraud.
    
    **Rule-based Explainability:** 
    Because ML models can be "black boxes", an overlaying rules engine explicitly flags suspicious patterns (e.g., payment requests, urgency) so the user understands *why* a job was flagged.
    
    **Limitations:** 
    This system relies on explicit text patterns and cannot verify real-world facts (like checking if a company actually exists). Scammers frequently adapt their language.
    """)
