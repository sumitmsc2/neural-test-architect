import streamlit as st
import requests
import time
import json

# Configuration
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Neural Test Architect",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern QA look
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .main-header {
        font-family: 'Roboto', sans-serif;
        color: #1f2937;
    }
    .stTextArea > div > div > textarea {
        background-color: #f8f9fa;
        border-radius: 8px;
    }
    .stCodeBlock {
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
    st.title("Neural Architect")
    st.markdown("---")
    
    st.subheader("⚙️ Engine Settings")
    model_choice = st.selectbox("LLM Model", ["GPT-4 Turbo", "Claude 3 Opus", "Llama 2 QA-Tuned"])
    confidence_threshold = st.slider("Min Confidence", 0.0, 1.0, 0.85)
    
    st.markdown("---")
    st.info("💡 **Tip:** Describe user stories clearly for best results.")

# Main Interface
st.title("🤖 Neural Test Architect")
st.markdown("### AI-Powered Quality Assurance & Self-Healing Automation")

tab1, tab2, tab3 = st.tabs(["✨ Test Generator", "❤️‍🩹 Self-Healing", "📊 Defect Analytics"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Feature Description")
        feature_desc = st.text_area("Enter User Story / Requirement", height=200, placeholder="As a user, I want to login with valid credentials so that I can access my dashboard.")
        
        if st.button("Generate Test Suite"):
            if feature_desc:
                with st.spinner("Analyzing Requirements & Generating Tests..."):
                    try:
                        response = requests.post(f"{API_URL}/generate", json={"feature_description": feature_desc})
                        if response.status_code == 200:
                            st.session_state.generated_test = response.json()
                            st.success("Test Suite Generated Successfully!")
                        else:
                            st.error("Generation Failed.")
                    except Exception as e:
                        st.error(f"Connection Error: {e}")
            else:
                st.warning("Please enter a feature description.")

    with col2:
        st.subheader("✅ Generated Output")
        if "generated_test" in st.session_state:
            test_data = st.session_state.generated_test
            st.markdown(f"**Test ID:** {test_data['id']}")
            st.markdown(f"**Title:** {test_data['title']}")
            
            with st.expander("Show Gherkin Steps", expanded=True):
                for step in test_data['steps']:
                    st.markdown(f"- {step}")
            
            st.markdown("**Automation Script (Python/Selenium):**")
            st.code(test_data['automation_script'], language="python")
            
            st.metric("AI Confidence Score", f"{test_data['ai_confidence']*100:.1f}%", "+2.4%")

with tab2:
    st.subheader("🔧 Self-Healing Automation")
    st.markdown("Repair broken test scripts automatically by analyzing error logs.")
    
    col_heal_1, col_heal_2 = st.columns(2)
    
    with col_heal_1:
        broken_script = st.text_area("Broken Script", height=150, value="driver.find_element(By.ID, 'login-btn').click()")
        error_log = st.text_area("Error Log", height=100, value="NoSuchElementException: Unable to locate element: {'method':'id','selector':'login-btn'}")
        
        if st.button("Heal Script"):
            with st.spinner("Diagnosing & Repairing..."):
                time.sleep(1.5) # Simulate API call
                st.session_state.healed_script = "driver.find_element(By.ID, 'submit-btn-v2').click() # Healed by AI"
                st.success("Script Healed!")

    with col_heal_2:
        if "healed_script" in st.session_state:
            st.markdown("**Healed Script:**")
            st.code(st.session_state.healed_script, language="python")
            st.info("AI detected ID change from 'login-btn' to 'submit-btn-v2'.")

with tab3:
    st.subheader("📈 Defect Prediction Analytics")
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Predicted Bug Density", "1.2 / KLOC", "-0.3")
    col_b.metric("Flaky Tests Detected", "4", "-2")
    col_c.metric("Test Coverage", "94.5%", "+1.2%")
    
    st.markdown("#### High-Risk Modules")
    st.table({
        "Module": ["Authentication", "Payment Gateway", "User Profile"],
        "Risk Score": ["High (85%)", "Critical (92%)", "Low (20%)"],
        "Recommended Action": ["Increase Unit Tests", "Manual Review Required", "Automated Regression"]
    })