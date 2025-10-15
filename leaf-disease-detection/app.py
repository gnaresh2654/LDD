import streamlit as st
import requests
from PIL import Image
import io
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Leaf Disease Detection System",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #558B2F;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .result-card {
        background-color: #F1F8E9;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #4CAF50;
    }
    .symptom-item {
        background-color: #FFF3E0;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        border-left: 3px solid #FF9800;
    }
    .treatment-item {
        background-color: #E3F2FD;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        border-left: 3px solid #2196F3;
    }
    .prevention-item {
        background-color: #F3E5F5;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        border-left: 3px solid #9C27B0;
    }
    .severity-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .severity-healthy {
        background-color: #4CAF50;
        color: white;
    }
    .severity-mild {
        background-color: #FFEB3B;
        color: #000;
    }
    .severity-moderate {
        background-color: #FF9800;
        color: white;
    }
    .severity-severe {
        background-color: #F44336;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# API configuration
API_BASE_URL = st.secrets.get("API_BASE_URL", "http://localhost:8000")

# Initialize session state
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

def check_api_health():
    """Check if the API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def analyze_image(image_file):
    """Send image to API for analysis"""
    try:
        files = {"file": ("leaf.jpg", image_file, "image/jpeg")}
        response = requests.post(
            f"{API_BASE_URL}/analyze",
            files=files,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            return None
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
        return None
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return None

def get_severity_class(severity):
    """Get CSS class for severity badge"""
    severity_lower = severity.lower()
    if "healthy" in severity_lower:
        return "severity-healthy"
    elif "mild" in severity_lower:
        return "severity-mild"
    elif "moderate" in severity_lower:
        return "severity-moderate"
    elif "severe" in severity_lower:
        return "severity-severe"
    else:
        return "severity-mild"

# Main app
def main():
    # Header
    st.markdown('<p class="main-header">🍃 Leaf Disease Detection System</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("""
        This system uses advanced AI vision models to detect and diagnose plant diseases from leaf images.
        
        **Features:**
        - Real-time disease detection
        - Detailed symptom analysis
        - Treatment recommendations
        - Prevention strategies
        """)
        
        st.divider()
        
        # API Status
        st.subheader("🔌 API Status")
        if check_api_health():
            st.success("✅ Connected")
        else:
            st.error("❌ Disconnected")
            st.warning(f"Make sure the API is running at {API_BASE_URL}")
        
        st.divider()
        
        # History
        st.subheader("📜 Analysis History")
        if st.session_state.analysis_history:
            st.write(f"Total analyses: {len(st.session_state.analysis_history)}")
            if st.button("Clear History"):
                st.session_state.analysis_history = []
                st.rerun()
        else:
            st.write("No analyses yet")
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<p class="sub-header">📸 Upload Leaf Image</p>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose a leaf image...",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear image of a plant leaf for disease detection"
        )
        
        if uploaded_file is not None:
            # Display image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
            
            # Analyze button
            if st.button("🔍 Analyze Leaf", type="primary", use_container_width=True):
                with st.spinner("🔬 Analyzing leaf... This may take a few moments..."):
                    # Reset file pointer
                    uploaded_file.seek(0)
                    
                    # Analyze
                    result = analyze_image(uploaded_file)
                    
                    if result:
                        st.session_state.current_result = result
                        st.session_state.analysis_history.append({
                            "timestamp": result["timestamp"],
                            "disease": result["disease_name"],
                            "severity": result["severity"]
                        })
                        st.success("✅ Analysis complete!")
                        st.rerun()
    
    with col2:
        st.markdown('<p class="sub-header">📊 Analysis Results</p>', unsafe_allow_html=True)
        
        if hasattr(st.session_state, 'current_result'):
            result = st.session_state.current_result
            
            # Disease name and confidence
            st.markdown(f"""
                <div class="result-card">
                    <h2 style="color: #2E7D32; margin-bottom: 1rem;">{result['disease_name']}</h2>
                    <p><strong>Confidence:</strong> {result['confidence']}</p>
                    <div class="severity-badge {get_severity_class(result['severity'])}">
                        Severity: {result['severity']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Description
            with st.expander("📝 Description", expanded=True):
                st.write(result['description'])
            
            # Symptoms
            with st.expander("🔍 Symptoms Detected", expanded=True):
                for symptom in result['symptoms']:
                    st.markdown(f'<div class="symptom-item">• {symptom}</div>', unsafe_allow_html=True)
            
            # Treatment
            with st.expander("💊 Treatment Recommendations", expanded=True):
                for i, treatment in enumerate(result['treatment'], 1):
                    st.markdown(f'<div class="treatment-item">{i}. {treatment}</div>', unsafe_allow_html=True)
            
            # Prevention
            with st.expander("🛡️ Prevention Measures", expanded=True):
                for i, prevention in enumerate(result['prevention'], 1):
                    st.markdown(f'<div class="prevention-item">{i}. {prevention}</div>', unsafe_allow_html=True)
            
            # Download report
            st.divider()
            report_data = json.dumps(result, indent=2)
            st.download_button(
                label="📥 Download Report (JSON)",
                data=report_data,
                file_name=f"leaf_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        else:
            st.info("👆 Upload a leaf image and click 'Analyze Leaf' to get started!")
            
            # Instructions
            st.markdown("""
            ### 📋 How to Use:
            1. Upload a clear image of a plant leaf
            2. Click the 'Analyze Leaf' button
            3. Review the detailed analysis results
            4. Follow treatment and prevention recommendations
            
            ### 💡 Tips for Best Results:
            - Use well-lit images
            - Ensure the leaf fills most of the frame
            - Avoid blurry or unclear images
            - Capture any visible symptoms clearly
            """)

if __name__ == "__main__":
    main()
