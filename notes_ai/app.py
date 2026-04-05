# app.py
"""
Streamlit UI for Notes Agent
"""

import streamlit as st
import os
from PIL import Image
from agent_core import process_notes
import tempfile

# Page config
st.set_page_config(
    page_title="📚 Notes Agent | Handwriting to PDF",
    page_icon="📚",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 30px;
    }
    
    .feature-box {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
    }
    
    .stDownloadButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>📚 Notes Agent</h1>
    <p>Transform messy handwritten notes into beautiful study PDFs</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("ℹ️ How it works")
    st.write("""
    1. 📸 Upload photo of handwritten notes
    2. 🤖 AI extracts and cleans text
    3. 📚 Generates study material
    4. 📄 Download beautiful PDF
    """)
    
    st.divider()
    
    st.header("✨ What you get")
    st.write("""
    - ✅ Clean, typed notes
    - ✅ Relevant diagrams
    - ✅ Simple analogies
    - ✅ Probable exam questions
    - ✅ Key concepts summary
    """)

# Main content
st.header("📸 Upload Your Notes")

# File uploader
uploaded_file = st.file_uploader(
    "Choose an image of handwritten notes",
    type=['jpg', 'jpeg', 'png', 'webp'],
    help="Take a clear photo of your handwritten notes"
)

# Optional inputs
col1, col2 = st.columns(2)
with col1:
    subject = st.text_input("Subject (optional)", placeholder="e.g., Computer Networks")
with col2:
    topic = st.text_input("Topic (optional)", placeholder="e.g., TCP/IP Protocol")

if uploaded_file:
    # Show uploaded image
    st.subheader("📷 Uploaded Image")
    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True)
    
    # Process button
    if st.button("🚀 Generate Study PDF", type="primary", use_container_width=True):
        
        with st.spinner("🤖 Processing your notes... This may take 30-60 seconds"):
            
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                image.save(tmp_file.name, 'JPEG')
                temp_path = tmp_file.name
            
            # Progress updates
            progress_bar = st.progress(0)
            status = st.empty()
            
            status.text("📸 Step 1/8: Enhancing image...")
            progress_bar.progress(10)
            
            status.text("📝 Step 2/8: Extracting text (OCR)...")
            progress_bar.progress(25)
            
            status.text("🧹 Step 3/8: Cleaning notes...")
            progress_bar.progress(35)
            
            status.text("📚 Step 4/8: Expanding content...")
            progress_bar.progress(50)
            
            status.text("💡 Step 5/8: Creating analogies...")
            progress_bar.progress(60)
            
            status.text("📊 Step 6/8: Finding diagrams...")
            progress_bar.progress(75)
            
            status.text("❓ Step 7/8: Generating questions...")
            progress_bar.progress(85)
            
            # Actually process
            try:
                pdf_path = process_notes(
                    temp_path,
                    subject=subject if subject else None,
                    topic=topic if topic else None,
                    verbose=False
                )
                
                status.text("📄 Step 8/8: Creating PDF...")
                progress_bar.progress(100)
                
                if pdf_path and os.path.exists(pdf_path):
                    # Success!
                    st.success("✅ PDF Generated Successfully!")
                    
                    # Read PDF for download
                    with open(pdf_path, "rb") as pdf_file:
                        pdf_bytes = pdf_file.read()
                    
                    # Download button
                    st.download_button(
                        label="📥 Download PDF",
                        data=pdf_bytes,
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf",
                        use_container_width=True
                    )
                    
                    st.info(f"📊 Your PDF includes:\n"
                            f"- Cleaned & structured notes\n"
                            f"- Relevant diagrams\n"
                            f"- Simple analogies\n"
                            f"- {10} probable exam questions")
                else:
                    st.error("❌ Failed to generate PDF. Please try again.")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
            
            finally:
                # Cleanup
                progress_bar.empty()
                status.empty()
                
                # Remove temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)

else:
    # Show example
    st.info("👆 Upload a photo of handwritten notes to get started!")
    
    st.subheader("📝 Example Input & Output")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Input:** Messy handwritten notes")
        st.image("https://via.placeholder.com/300x400?text=Handwritten+Notes", 
                 caption="Your messy notes")
    
    with col2:
        st.write("**Output:** Beautiful study PDF")
        st.markdown("""
        ```
        📄 PDF Contents:
        
        ✅ Clean typed notes
        ✅ Key concepts highlighted
        ✅ Diagrams added
        ✅ Simple analogies
        ✅ 10 exam questions
        ```
        """)

# Footer
st.divider()
st.caption("Built with ❤️ for Students | Powered by Groq + Google Vision")
# pip install torch torchvision