# ocr_engine.py
"""
OCR Engine - SIMPLIFIED VERSION
For now, we recommend using manual text input instead of OCR
"""

def extract_text(image_path=None, manual_text=None):
    """
    Extract text - manual input recommended
    
    Args:
        image_path: Path to image (not implemented yet)
        manual_text: Text provided by user
    
    Returns:
        Text string
    """
    
    if manual_text:
        return manual_text.strip()
    
    # OCR not implemented yet
    print("⚠️ OCR not available. Please use manual text input.")
    return ""

# For future: Integrate Google Vision API or similar
# For now: Users can use Google Lens → copy text → paste