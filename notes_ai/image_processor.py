# image_processor.py
"""
Image preprocessing to improve OCR accuracy
"""

import cv2
import numpy as np
from PIL import Image
import os

def enhance_image(image_path):
    """
    Enhance image for better OCR results
    - Increase contrast
    - Remove noise
    - Deskew (straighten)
    """
    
    # Read image
    img = cv2.imread(image_path)
    
    if img is None:
        raise ValueError(f"Cannot read image: {image_path}")
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Increase contrast using CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast = clahe.apply(gray)
    
    # Denoise
    denoised = cv2.fastNlMeansDenoising(contrast, None, 10, 7, 21)
    
    # Threshold to make text clearer
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Save enhanced image
    enhanced_path = image_path.replace('.', '_enhanced.')
    cv2.imwrite(enhanced_path, thresh)
    
    print(f"✅ Image enhanced: {enhanced_path}")
    
    return enhanced_path

def detect_regions(image_path):
    """
    Detect text regions vs diagram regions in the image
    Returns bounding boxes for each region
    """
    
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Find contours
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    text_regions = []
    diagram_regions = []
    
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h
        aspect_ratio = w / h if h > 0 else 0
        
        # Heuristic: diagrams are usually more square, text is wide
        if area > 5000:  # Ignore tiny regions
            if 0.3 < aspect_ratio < 3:  # Could be diagram
                diagram_regions.append((x, y, w, h))
            else:  # Likely text
                text_regions.append((x, y, w, h))
    
    return {
        "text_regions": text_regions,
        "diagram_regions": diagram_regions
    }

def extract_diagrams(image_path, regions):
    """
    Extract diagram portions from image
    """
    
    img = cv2.imread(image_path)
    diagrams = []
    
    for i, (x, y, w, h) in enumerate(regions.get("diagram_regions", [])):
        diagram = img[y:y+h, x:x+w]
        diagram_path = f"uploads/diagram_{i}.png"
        cv2.imwrite(diagram_path, diagram)
        diagrams.append(diagram_path)
    
    return diagrams