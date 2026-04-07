# app.py
"""
Streamlit UI for Notes Agent
Powered by Featherless AI (DeepSeek-V3)
"""

import streamlit as st
import os
from PIL import Image
from agent_core import process_notes
import tempfile

# Page config
st.set_page_config(
    page_title="📚 Notes Agent | AI Study Assistant",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 30px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 3em;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        font-size: 1.2em;
        margin: 10px 0 0 0;
    }
    
    .feature-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 10px 24px;
        background-color: #f0f2f6;
        border-radius: 10px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>📚 Notes Agent</h1>
    <p>Transform your study notes into professional PDFs with AI</p>
    <p style="font-size: 0.9em; opacity: 0.9;">🚀 Powered by Featherless AI (DeepSeek-V3, 32K Context)</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/3d-fluency/94/artificial-intelligence.png", width=80)
    
    st.markdown("### ✨ What You Get")
    st.markdown("""
    <div class="feature-card">
        ✅ <b>Clean, Structured Notes</b><br/>
        ✅ <b>Expanded Explanations</b><br/>
        ✅ <b>Simple Analogies</b><br/>
        ✅ <b>Exam Questions</b><br/>
        ✅ <b>Relevant Diagrams</b><br/>
        ✅ <b>Beautiful PDF</b>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### 🎯 How It Works")
    st.write("""
    1. **Paste/Type** your notes
    2. **AI processes** and enhances
    3. **Download** beautiful PDF
    4. **Share** with friends!
    """)
    
    st.divider()
    
    st.markdown("### 💡 Pro Tips")
    st.info("""
    • Notes can be messy - AI will clean them!
    • Add subject/topic for better results
    • Works with English & Hindi
    • Supports math equations (LaTeX)
    """)

# Main content with tabs
tab1, tab2 = st.tabs(["📝 Text Input (Recommended)", "📸 Image Upload (Experimental)"])

# ═══════════════════════════════════════════════════════════════
# TAB 1: TEXT INPUT (MAIN MODE)
# ═══════════════════════════════════════════════════════════════

with tab1:
    st.header("📝 Enter Your Notes")
    
    # Text area for notes
    notes_text = st.text_area(
        "Paste or type your notes here:",
        height=350,
        placeholder="""Example:

Photosynthesis - Process of making food in plants

Light Reaction:
- Occurs in thylakoid membrane
- Produces ATP and NADPH
- Splits water → releases O2
- Chlorophyll absorbs light energy

Dark Reaction (Calvin Cycle):
- Occurs in stroma
- Uses ATP and NADPH from light reaction
- CO2 + RuBP → 3-PGA → G3P → Glucose
- Does not require direct light

Overall Equation:
6CO2 + 6H2O + Light → C6H12O6 + 6O2

Factors Affecting:
- Light intensity
- CO2 concentration
- Temperature
- Chlorophyll amount
        """,
        key="notes_input"
    )
    
    # Optional metadata
    col1, col2 = st.columns(2)
    with col1:
        subject = st.text_input(
            "📚 Subject (optional)", 
            placeholder="e.g., Biology",
            key="subject_text"
        )
    with col2:
        topic = st.text_input(
            "📖 Topic (optional)", 
            placeholder="e.g., Photosynthesis",
            key="topic_text"
        )
    
    # Generate button
    if st.button("🚀 Generate Study PDF", type="primary", use_container_width=True, key="generate_text"):
        
        if not notes_text.strip():
            st.error("❌ Please enter some notes first!")
        
        else:
            # Progress container
            with st.spinner(""):
                progress_container = st.container()
                
                with progress_container:
                    progress_bar = st.progress(0)
                    status = st.empty()
                    
                    # Step 1
                    status.info("🧹 Cleaning and structuring notes...")
                    progress_bar.progress(15)
                    
                    # Step 2
                    status.info("📚 Expanding with detailed explanations...")
                    progress_bar.progress(30)
                    
                    # Step 3
                    status.info("💡 Generating simple analogies...")
                    progress_bar.progress(50)
                    
                    # Step 4
                    status.info("📊 Searching for relevant diagrams...")
                    progress_bar.progress(65)
                    
                    # Step 5
                    status.info("❓ Creating probable exam questions...")
                    progress_bar.progress(80)
                    
                    # Step 6
                    status.info("📄 Building beautiful PDF...")
                    progress_bar.progress(90)
                    
                    # Process
                    try:
                        pdf_path = process_notes(
                            text_input=notes_text,
                            subject=subject if subject else None,
                            topic=topic if topic else None,
                            verbose=False
                        )
                        
                        progress_bar.progress(100)
                        
                        if pdf_path and os.path.exists(pdf_path):
                            # Success!
                            status.empty()
                            progress_bar.empty()
                            
                            st.success("✅ PDF Generated Successfully!")
                            
                            # Stats
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                st.markdown("""
                                <div class="stat-box">
                                    <h3>📝</h3>
                                    <p>Structured Notes</p>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with col2:
                                st.markdown("""
                                <div class="stat-box">
                                    <h3>💡</h3>
                                    <p>Smart Analogies</p>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with col3:
                                st.markdown("""
                                <div class="stat-box">
                                    <h3>📊</h3>
                                    <p>Visual Diagrams</p>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            with col4:
                                st.markdown("""
                                <div class="stat-box">
                                    <h3>❓</h3>
                                    <p>Exam Questions</p>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            st.divider()
                            
                            # Download button
                            with open(pdf_path, "rb") as pdf_file:
                                pdf_bytes = pdf_file.read()
                            
                            st.download_button(
                                label="📥 Download Your Study PDF",
                                data=pdf_bytes,
                                file_name=os.path.basename(pdf_path),
                                mime="application/pdf",
                                use_container_width=True
                            )
                            
                            st.balloons()
                            
                        else:
                            status.error("❌ Failed to generate PDF")
                            
                    except Exception as e:
                        status.empty()
                        progress_bar.empty()
                        st.error(f"❌ Error: {str(e)}")
                        with st.expander("🔍 Debug Info"):
                            st.exception(e)

# ═══════════════════════════════════════════════════════════════
# TAB 2: IMAGE UPLOAD (EXPERIMENTAL)
# ═══════════════════════════════════════════════════════════════

with tab2:
    st.header("📸 Upload Image (Experimental)")
    
    st.warning("""
    ⚠️ **Note**: OCR for handwriting is experimental and may not work perfectly.
    
    **Recommended**: Use Tab 1 (Text Input) for best results!
    
    **For handwriting**: Take photo → Use Google Lens to copy text → Paste in Tab 1
    """)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image",
        type=['jpg', 'jpeg', 'png', 'webp'],
        help="For best results, use clear photos of PRINTED text",
        key="image_upload"
    )
    
    if uploaded_file:
        # Show image
        st.subheader("📷 Uploaded Image")
        image = Image.open(uploaded_file)
        st.image(image, use_column_width=True)
        
        # Metadata
        col1, col2 = st.columns(2)
        with col1:
            subject_img = st.text_input("📚 Subject", key="subject_img")
        with col2:
            topic_img = st.text_input("📖 Topic", key="topic_img")
        
        # Process button
        if st.button("🚀 Try OCR & Generate PDF", type="primary", use_container_width=True, key="generate_img"):
            st.info("🔧 OCR feature coming soon! Please use Tab 1 (Text Input) for now.")

# ═══════════════════════════════════════════════════════════════
# EXAMPLES SECTION
# ═══════════════════════════════════════════════════════════════

st.divider()

with st.expander("📖 See Example Input/Output"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Input (Messy Notes)")
        st.code("""
TCP/IP protocol

network layer - routing, IP addressing
transport layer - TCP, UDP

3-way handshake:
SYN -> SYN-ACK -> ACK

ports:
HTTP=80, HTTPS=443, SSH=22

reliable, error checking, flow control
        """, language="text")
    
    with col2:
        st.markdown("### 📄 Output (Beautiful PDF)")
        st.markdown("""
        **Includes:**
        
        ✅ **Structured Notes**
        - Clean headings & bullet points
        - Proper formatting
        - Complete explanations
        
        ✅ **Analogies**
        - "3-way handshake is like a phone call..."
        - Simple, memorable examples
        
        ✅ **Diagrams**
        - TCP handshake diagram
        - Network layer visualization
        
        ✅ **10 Exam Questions**
        - MCQs, Short, Long answers
        - With hints!
        """)

# Footer
st.divider()

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <p style="color: #666;">Built for <b>Hack4Good Lucknow</b> 🚀</p>
        <p style="color: #888; font-size: 0.9em;">
            Powered by <b>Featherless AI</b> | <b>DeepSeek-V3</b> | <b>32K Context</b>
        </p>
    </div>
    """, unsafe_allow_html=True)