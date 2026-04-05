# app.py
"""
Streamlit web interface for the fact-checking agent.
"""

import streamlit as st
from agent_core import fact_check
from cache_manager import cache
from rate_limiter import limiter
import time

# Page config
st.set_page_config(
    page_title="Fact-Check Agent | Hack4Good",
    page_icon="🔍",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .verdict-true {
        background-color: #d4edda;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #28a745;
    }
    .verdict-false {
        background-color: #f8d7da;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #dc3545;
    }
    .verdict-misleading {
        background-color: #fff3cd;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
    }
    .verdict-unknown {
        background-color: #e2e3e5;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #6c757d;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🔍 Fact-Check Agent")
st.caption("Verify claims using official government and trusted sources | Built for Hack4Good Lucknow")

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    This AI agent verifies claims by:
    1. Analyzing the claim
    2. Searching official sources (PIB, WHO, etc.)
    3. Comparing evidence with the claim
    4. Providing a verdict with sources
    """)
    
    st.divider()
    
    st.header("📊 Stats")
    cache_stats = cache.get_stats()
    st.metric("Cached Claims", cache_stats['total_cached'])
    st.metric("Cache Hit Rate", cache_stats['hit_rate'])
    
    rate_stats = limiter.get_stats()
    st.metric("API Calls (Today)", rate_stats['total_calls_today'])
    
    if st.button("🗑️ Clear Cache"):
        cache.clear()
        st.success("Cache cleared!")
        st.rebalance()

# Main area
st.divider()

# Example claims
with st.expander("📝 Example Claims to Test"):
    st.write("""
    - Government is giving ₹5000 to all students
    - PM announced free laptop scheme for college students
    - WHO said garlic cures dengue fever
    - Eating 5 bananas daily prevents heart disease
    - Modi govt giving ₹15000 to women, forward this message
    """)

# Input
claim = st.text_area(
    "Enter claim to verify:",
    placeholder="E.g., Government giving free laptops to all students",
    height=100,
    help="Enter any claim you want to fact-check"
)

col1, col2 = st.columns([3, 1])

with col1:
    check_button = st.button("🔍 Check Fact", type="primary", use_container_width=True)

with col2:
    if st.button("🔄 Reset"):
        st.rerun()

# Process
if check_button:
    if not claim.strip():
        st.warning("⚠️ Please enter a claim to verify")
    else:
        with st.spinner("🤖 Agent is working..."):
            # Add progress bar for UX
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("📋 Analyzing claim...")
            progress_bar.progress(33)
            time.sleep(0.5)
            
            status_text.text("🔍 Searching sources...")
            progress_bar.progress(66)
            time.sleep(0.5)
            
            # Run fact-check
            result = fact_check(claim, verbose=False)
            
            status_text.text("⚖️ Verifying...")
            progress_bar.progress(100)
            time.sleep(0.3)
            
            # Clear progress
            progress_bar.empty()
            status_text.empty()
        
        # Display result
        st.divider()
        
        # Verdict card
        verdict = result['verdict']
        
        verdict_config = {
            "TRUE": {
                "emoji": "✅",
                "color": "green",
                "css_class": "verdict-true"
            },
            "FALSE": {
                "emoji": "❌",
                "color": "red",
                "css_class": "verdict-false"
            },
            "MISLEADING": {
                "emoji": "⚠️",
                "color": "orange",
                "css_class": "verdict-misleading"
            },
            "CANNOT_VERIFY": {
                "emoji": "❓",
                "color": "gray",
                "css_class": "verdict-unknown"
            }
        }
        
        config = verdict_config.get(verdict, verdict_config["CANNOT_VERIFY"])
        
        # Verdict display
        st.markdown(f"""
        <div class="{config['css_class']}">
            <h2>{config['emoji']} {verdict}</h2>
            <p style="font-size: 16px; margin-top: 10px;">{result['reasoning']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Details
        st.subheader("📍 Key Facts")
        if result.get('key_facts'):
            for fact in result['key_facts']:
                st.write(f"• {fact}")
        else:
            st.write("_No specific facts extracted_")
        
        # Sources
        st.subheader("📚 Sources Checked")
        for source in result['sources']:
            st.write(f"• {source}")
        
        # Confidence
        confidence_color = {
            "HIGH": "🟢",
            "MEDIUM": "🟡",
            "LOW": "🔴"
        }
        st.metric(
            "Confidence Level",
            result['confidence'],
            delta=None,
            delta_color="off"
        )
        
        # Show evidence (collapsible)
        with st.expander("🔍 View Raw Evidence"):
            for i, evidence in enumerate(result['evidence'], 1):
                st.write(f"**Evidence {i}:**")
                st.write(evidence)
                st.divider()

# Footer
st.divider()
st.caption("Built with ❤️ for Hack4Good Lucknow | Powered by Groq + SerpAPI")