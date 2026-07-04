import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Config
MODEL_NAME = "ufoblivr/docforge-codet5-base-v1"

# Load model
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    model.eval()
    return tokenizer, model

tokenizer, model = load_model()

st.set_page_config(
    page_title="DocForge",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 20px 0;
    }
    .doc-section {
        background-color: #f0f2f6;
        border-left: 4px solid #1f77e6;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .success-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px 30px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.25);
        margin-bottom: 25px;
    }
    
    .success-section h3 {
        margin: 0;
        font-size: 1.5em;
        font-weight: 800;
        letter-spacing: 0.5px;
    }
    
    .code-container {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        margin-bottom: 15px;
    }
    
    .code-title {
        color: #667eea;
        font-weight: 700;
        font-size: 1.1em;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<div class='main-header'><h1>🔧 DocForge</h1></div>", unsafe_allow_html=True)
st.markdown("<div class='main-header'><p style='font-size: 18px; color: #666;'>AI-Powered Automatic Code Documentation Generation</p></div>", unsafe_allow_html=True)
st.markdown("---")

# Language options
LANGUAGES = {
    "Python": "python",
    "JavaScript": "javascript", 
    "TypeScript": "typescript",
    "Java": "java",
    "C++": "c++",
    "C#": "csharp"
}

# Input section
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### 📝 Enter Code Snippet")
    code_input = st.text_area(
        label="Code input",
        height=350,
        placeholder="""def add(a, b):
    \"\"\"Add two numbers.\"\"\"
    return a + b""",
        label_visibility="collapsed"
    )

with col2:
    st.markdown("### 🌐 Programming Language")
    selected_language = st.selectbox(
        label="Select language",
        options=list(LANGUAGES.keys()),
        index=0,
        label_visibility="collapsed"
    )

st.markdown("---")

# Generator function
def generate_documentation(code, language):
    prompt = f"Summarize {language}: {code}"
    
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512,
        padding=True
    )

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=256,
            num_beams=4,
            early_stopping=True
        )

    generated_text = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return generated_text

# Button and output
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    generate_btn = st.button("✨ Generate Documentation", use_container_width=True, type="primary")

if generate_btn:
    if code_input.strip() == "":
        st.warning("⚠️ Please enter a code snippet first.")
    else:
        with st.spinner("🔄 Generating documentation..."):
            documentation = generate_documentation(code_input, selected_language)

        st.markdown("---")
        
        # Output section
        st.markdown("<div class='success-section'><h3>📚 Generated Documentation</h3></div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1], gap="medium")
        
        with col1:
            st.markdown("<div class='code-container'><div class='code-title'>💻 Original Code</div>", unsafe_allow_html=True)
            st.code(code_input, language=LANGUAGES[selected_language])
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='code-container'><div class='code-title'>📄 Generated Documentation</div>", unsafe_allow_html=True)
            st.code(documentation, language="markdown")
            st.markdown("</div>", unsafe_allow_html=True)