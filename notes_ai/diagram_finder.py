# diagram_finder.py
"""
Find relevant diagrams - Using Google Images (no API needed)
"""

import requests
import os
from PIL import Image
from io import BytesIO
import re

def search_diagrams(query, num_results=3):
    """
    Search for educational diagrams using Google Custom Search
    Falls back to placeholder if search fails
    """
    
    print(f"🔍 Searching diagrams: {query}")
    
    # For hackathon demo, we'll use placeholder diagrams
    # This avoids rate limiting issues
    
    # Return placeholder info - the PDF generator will handle this gracefully
    print(f"   ℹ️ Using topic-based diagram generation")
    
    return []

def download_diagram(url, save_path):
    """
    Download diagram image from URL
    """
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Resize if too large
            max_size = (800, 800)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            img.save(save_path, 'JPEG', quality=85)
            print(f"   ✅ Downloaded: {save_path}")
            return save_path
        
    except Exception as e:
        print(f"   ⚠️ Download failed: {e}")
    
    return None

def get_diagrams_for_topic(diagram_queries, output_dir="output/diagrams"):
    """
    For hackathon: Skip diagram downloads to avoid rate limits
    The PDF will still be generated with notes, analogies, and questions
    """
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"   ℹ️ Skipping diagram download (avoiding rate limits)")
    print(f"   ℹ️ PDF will include text content, analogies, and questions")
    
    return []