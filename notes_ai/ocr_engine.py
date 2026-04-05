# ocr_engine.py
"""
OCR Engine using Google Cloud Vision API
This is the BEST option for handwriting recognition
FREE: 1000 images/month
"""

import requests
import base64
import os
from config import GOOGLE_CLOUD_API_KEY

def extract_text(image_path):
    """
    Extract text from handwritten notes using Google Vision API
    
    Args:
        image_path: Path to the image file
    
    Returns:
        Extracted text as string
    """
    
    print(f"\n📝 Extracting text with Google Vision API...")
    print(f"   Image: {image_path}")
    
    # Check if file exists
    if not os.path.exists(image_path):
        print(f"❌ File not found: {image_path}")
        return ""
    
    # Check if API key is set
    if not GOOGLE_CLOUD_API_KEY or GOOGLE_CLOUD_API_KEY == "YOUR_GOOGLE_VISION_API_KEY_HERE":
        print("❌ Google Vision API key not set in config.py!")
        print("   Get your free key from: https://console.cloud.google.com/apis/credentials")
        print("   Make sure 'Cloud Vision API' is enabled!")
        return ""
    
    # Read and encode image as base64
    try:
        with open(image_path, "rb") as image_file:
            image_content = base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        print(f"❌ Failed to read image: {e}")
        return ""
    
    # Prepare API request
    url = f"https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_CLOUD_API_KEY}"
    
    payload = {
        "requests": [
            {
                "image": {
                    "content": image_content
                },
                "features": [
                    {
                        "type": "DOCUMENT_TEXT_DETECTION",
                        "maxResults": 1
                    }
                ],
                "imageContext": {
                    "languageHints": ["en", "hi"]  # English and Hindi
                }
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # Make API request
    try:
        print("   Sending to Google Vision API...")
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        # Check for HTTP errors
        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code}")
            print(f"   Response: {response.text[:500]}")
            return ""
        
        result = response.json()
        
        # Check for API-level errors
        if "error" in result:
            error_msg = result["error"].get("message", "Unknown error")
            print(f"❌ Google Vision Error: {error_msg}")
            return ""
        
        # Extract text from response
        responses = result.get("responses", [])
        
        if not responses:
            print("⚠️ No response from API")
            return ""
        
        first_response = responses[0]
        
        # Check for errors in response
        if "error" in first_response:
            print(f"❌ Error: {first_response['error'].get('message', 'Unknown')}")
            return ""
        
        # Get full text annotation
        full_text_annotation = first_response.get("fullTextAnnotation", {})
        extracted_text = full_text_annotation.get("text", "")
        
        if not extracted_text:
            # Try textAnnotations as fallback
            text_annotations = first_response.get("textAnnotations", [])
            if text_annotations:
                extracted_text = text_annotations[0].get("description", "")
        
        # Report results
        if extracted_text:
            char_count = len(extracted_text)
            word_count = len(extracted_text.split())
            print(f"✅ Success! Extracted {char_count} characters ({word_count} words)")
            print(f"\n📄 Preview (first 500 chars):")
            print("-" * 50)
            print(extracted_text[:500])
            print("-" * 50)
        else:
            print("⚠️ No text found in image. Is the image clear?")
        
        return extracted_text
    
    except requests.exceptions.Timeout:
        print("❌ Request timed out. Check your internet connection.")
        return ""
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return ""
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return ""


# ═══════════════════════════════════════════════════════════════
# TEST FUNCTION
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Test with sample image
    test_image = "uploads/note.jpg"
    
    if os.path.exists(test_image):
        text = extract_text(test_image)
        if text:
            print("\n\n✅ OCR TEST PASSED!")
            print(f"Extracted {len(text)} characters")
        else:
            print("\n\n❌ OCR TEST FAILED!")
            print("Check your API key and image")
    else:
        print(f"⚠️ Test image not found: {test_image}")
        print("Please add a test image and try again")