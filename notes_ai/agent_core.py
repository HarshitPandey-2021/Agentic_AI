# agent_core.py
"""
Main Notes Agent - Powered by Featherless AI
Orchestrates the entire pipeline: Text → Structure → Enhance → PDF
"""

import os
from datetime import datetime

from llm_processor import (
    clean_and_structure_notes,
    generate_analogies,
    generate_questions,
    expand_notes,
    generate_diagram_queries
)
from diagram_finder import get_diagrams_for_topic
from pdf_generator import generate_pdf
from config import OUTPUT_DIR

def process_notes(text_input, subject=None, topic=None, image_path=None, verbose=True):
    """
    Process notes from TEXT INPUT (recommended) or OCR from image (experimental)
    
    Args:
        text_input: The actual notes text (typed/pasted) - PREFERRED
        subject: Optional subject name
        topic: Optional topic name
        image_path: Optional image for reference (not used for OCR in this version)
        verbose: Print progress
    
    Returns:
        Path to generated PDF
    """
    
    if verbose:
        print("\n" + "=" * 60)
        print("🚀 NOTES AGENT STARTED")
        print("   Powered by Featherless AI (DeepSeek-V3)")
        print("=" * 60)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Validate input
    if not text_input or not text_input.strip():
        print("❌ No text provided!")
        return None
    
    raw_text = text_input.strip()
    
    if verbose:
        print(f"\n📝 Processing {len(raw_text)} characters...")
        print(f"   Words: {len(raw_text.split())}")
        print(f"   Preview: {raw_text[:150]}...")
    
    # ═══════════════════════════════════════
    # STEP 1: CLEAN AND STRUCTURE
    # ═══════════════════════════════════════
    
    if verbose:
        print("\n🧹 Step 1/6: Cleaning and structuring notes...")
    
    structured = clean_and_structure_notes(raw_text, subject, topic)
    
    detected_topic = structured.get("detected_topic", topic or "Study Notes")
    detected_subject = structured.get("detected_subject", subject or "General")
    cleaned_notes = structured.get("cleaned_notes", raw_text)
    key_concepts = structured.get("key_concepts", [])
    summary = structured.get("summary", "")
    
    if verbose:
        print(f"   ✅ Topic: {detected_topic}")
        print(f"   ✅ Subject: {detected_subject}")
        print(f"   ✅ Key concepts: {len(key_concepts)}")
    
    # ═══════════════════════════════════════
    # STEP 2: EXPAND NOTES
    # ═══════════════════════════════════════
    
    if verbose:
        print("\n📚 Step 2/6: Expanding notes with details...")
    
    expanded = expand_notes(cleaned_notes, detected_topic)
    
    if verbose:
        print(f"   ✅ Expanded to {len(expanded)} characters")
    
    # ═══════════════════════════════════════
    # STEP 3: GENERATE ANALOGIES
    # ═══════════════════════════════════════
    
    if verbose:
        print("\n💡 Step 3/6: Creating analogies...")
    
    analogies = generate_analogies(key_concepts[:5], detected_topic)
    
    if verbose:
        print(f"   ✅ Generated {len(analogies.get('analogies', []))} analogies")
    
    # ═══════════════════════════════════════
    # STEP 4: FIND DIAGRAMS
    # ═══════════════════════════════════════
    
    if verbose:
        print("\n📊 Step 4/6: Finding relevant diagrams...")
    
    try:
        diagram_queries = generate_diagram_queries(detected_topic, key_concepts[:3])
        diagrams = get_diagrams_for_topic(diagram_queries)
        
        if verbose:
            print(f"   ✅ Downloaded {len(diagrams)} diagrams")
    except Exception as e:
        diagrams = []
        if verbose:
            print(f"   ⚠️ Diagram search skipped ({str(e)[:50]})")
    
    # ═══════════════════════════════════════
    # STEP 5: GENERATE QUESTIONS
    # ═══════════════════════════════════════
    
    if verbose:
        print("\n❓ Step 5/6: Generating exam questions...")
    
    questions = generate_questions(cleaned_notes, detected_topic)
    
    if verbose:
        print(f"   ✅ Generated {len(questions.get('questions', []))} questions")
    
    # ═══════════════════════════════════════
    # STEP 6: CREATE PDF
    # ═══════════════════════════════════════
    
    if verbose:
        print("\n📄 Step 6/6: Generating PDF...")
    
    # Prepare data for PDF
    pdf_data = {
        "topic": detected_topic,
        "subject": detected_subject,
        "cleaned_notes": cleaned_notes,
        "expanded_notes": expanded,
        "summary": summary,
        "key_concepts": key_concepts,
        "analogies": analogies,
        "questions": questions,
        "diagrams": diagrams
    }
    
    # Generate output filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = "".join(c for c in detected_topic if c.isalnum() or c in ' -_')[:40]
    safe_topic = safe_topic.strip().replace(' ', '_')
    output_path = os.path.join(OUTPUT_DIR, f"{safe_topic}_{timestamp}.pdf")
    
    pdf_path = generate_pdf(pdf_data, output_path)
    
    # ═══════════════════════════════════════
    # DONE!
    # ═══════════════════════════════════════
    
    if verbose:
        print("\n" + "=" * 60)
        print("✅ NOTES AGENT COMPLETED!")
        print("=" * 60)
        print(f"\n📄 PDF saved: {pdf_path}")
        print(f"\n📊 Statistics:")
        print(f"   • Topic: {detected_topic}")
        print(f"   • Subject: {detected_subject}")
        print(f"   • Key concepts: {len(key_concepts)}")
        print(f"   • Analogies: {len(analogies.get('analogies', []))}")
        print(f"   • Diagrams: {len(diagrams)}")
        print(f"   • Questions: {len(questions.get('questions', []))}")
        print(f"   • Total pages: ~{(len(expanded) // 2000) + 5}")
    
    return pdf_path

# ═══════════════════════════════════════
# SIMPLE TEST
# ═══════════════════════════════════════

if __name__ == "__main__":
    # Test with sample text
    sample_notes = """
    Machine Learning Basics
    
    Supervised Learning:
    - Uses labeled data
    - Example: Classification, Regression
    - Common algorithms: Linear Regression, SVM, Decision Trees
    
    Unsupervised Learning:
    - No labeled data
    - Finds patterns automatically
    - Examples: Clustering (K-means), Dimensionality Reduction (PCA)
    
    Key Concepts:
    - Training data vs Test data (80-20 split)
    - Overfitting: Model memorizes instead of learning
    - Underfitting: Model too simple
    - Cross-validation: K-fold technique
    
    Neural Networks:
    - Inspired by human brain
    - Layers: Input → Hidden → Output
    - Activation functions: ReLU, Sigmoid, Tanh
    - Backpropagation for training
    
    Applications:
    - Image recognition
    - Natural language processing
    - Recommendation systems
    - Autonomous vehicles
    """
    
    print("\n🧪 TESTING NOTES AGENT WITH SAMPLE DATA...\n")
    
    result = process_notes(
        sample_notes, 
        subject="Artificial Intelligence", 
        topic="Machine Learning Fundamentals"
    )
    
    if result:
        print(f"\n🎉 SUCCESS! Check the PDF: {result}")
    else:
        print("\n❌ Test failed!")