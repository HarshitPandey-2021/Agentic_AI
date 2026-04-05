# agent_core.py
"""
Main Notes Agent - Orchestrates the entire pipeline
"""

import os
from datetime import datetime

from image_processor import enhance_image, detect_regions
from ocr_engine import extract_text
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

def process_notes(image_path, subject=None, topic=None, verbose=True):
    """
    Main function that processes handwritten notes image
    and generates a complete study PDF.
    
    Args:
        image_path: Path to handwritten notes image
        subject: Optional subject name
        topic: Optional topic name
        verbose: Print progress
    
    Returns:
        Path to generated PDF
    """
    
    if verbose:
        print("\n" + "=" * 60)
        print("🚀 NOTES AGENT STARTED")
        print("=" * 60)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # ═══════════════════════════════════════
    # STEP 1: ENHANCE IMAGE
    # ═══════════════════════════════════════
    
    if verbose:
        print("\n📸 Step 1: Enhancing image...")
    
    try:
        enhanced_path = enhance_image(image_path)
    except:
        enhanced_path = image_path  # Use original if enhancement fails
    
    # ═══════════════════════════════════════
    # STEP 2: EXTRACT TEXT (OCR)
    # ═══════════════════════════════════════
    
    if verbose:
        print("\n📝 Step 2: Extracting text from handwriting...")
    
    raw_text = extract_text(enhanced_path)
    
    if not raw_text.strip():
        print("❌ Could not extract text from image!")
        return None
    
    if verbose:
        print(f"   Extracted {len(raw_text)} characters")
        print(f"   Preview: {raw_text[:200]}...")
    
    # ═══════════════════════════════════════
    # STEP 3: CLEAN AND STRUCTURE
    # ═══════════════════════════════════════
    
    if verbose:
        print("\n🧹 Step 3: Cleaning and structuring notes...")
    
    structured = clean_and_structure_notes(raw_text, subject, topic)
    
    detected_topic = structured.get("detected_topic", topic or "Study Notes")
    detected_subject = structured.get("detected_subject", subject or "General")
    cleaned_notes = structured.get("cleaned_notes", raw_text)
    key_concepts = structured.get("key_concepts", [])
    summary = structured.get("summary", "")
    
    if verbose:
        print(f"   Topic detected: {detected_topic}")
        print(f"   Subject: {detected_subject}")
        print(f"   Key concepts: {', '.join(key_concepts[:5])}")
    
    # ═══════════════════════════════════════
    # STEP 4: EXPAND NOTES
    # ═══════════════════════════════════════
    
    if verbose:
        print("\n📚 Step 4: Expanding notes with details...")
    
    expanded = expand_notes(cleaned_notes, detected_topic)
    
    # ═══════════════════════════════════════
    # STEP 5: GENERATE ANALOGIES
    # ═══════════════════════════════════════
    
    if verbose:
        print("\n💡 Step 5: Creating analogies...")
    
    analogies = generate_analogies(key_concepts, detected_topic)
    
    if verbose:
        print(f"   Generated {len(analogies.get('analogies', []))} analogies")
    
    # ═══════════════════════════════════════
    # STEP 6: FIND DIAGRAMS
    # ═══════════════════════════════════════
    
    if verbose:
        print("\n📊 Step 6: Finding relevant diagrams...")
    
    diagram_queries = generate_diagram_queries(detected_topic, key_concepts)
    diagrams = get_diagrams_for_topic(diagram_queries)
    
    if verbose:
        print(f"   Downloaded {len(diagrams)} diagrams")
    
    # ═══════════════════════════════════════
    # STEP 7: GENERATE QUESTIONS
    # ═══════════════════════════════════════
    
    if verbose:
        print("\n❓ Step 7: Generating exam questions...")
    
    questions = generate_questions(cleaned_notes, detected_topic)
    
    if verbose:
        print(f"   Generated {len(questions.get('questions', []))} questions")
    
    # ═══════════════════════════════════════
    # STEP 8: CREATE PDF
    # ═══════════════════════════════════════
    
    if verbose:
        print("\n📄 Step 8: Generating PDF...")
    
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
    safe_topic = "".join(c for c in detected_topic if c.isalnum() or c == ' ')[:30]
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
        print(f"\n📊 Summary:")
        print(f"   • Topic: {detected_topic}")
        print(f"   • Key concepts: {len(key_concepts)}")
        print(f"   • Analogies: {len(analogies.get('analogies', []))}")
        print(f"   • Diagrams: {len(diagrams)}")
        print(f"   • Questions: {len(questions.get('questions', []))}")
    
    return pdf_path

# ═══════════════════════════════════════
# TEST
# ═══════════════════════════════════════

if __name__ == "__main__":
    # Test with a sample image
    test_image = "uploads/note.jpg"
    
    if os.path.exists(test_image):
        result = process_notes(test_image)
        print(f"\n🎉 Done! Check: {result}")
    else:
        print(f"⚠️ Please add a test image: {test_image}")