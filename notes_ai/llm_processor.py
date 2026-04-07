# llm_processor.py
"""
LLM Processing - Direct API calls (No OpenAI SDK issues!)
"""

import json
import requests
from config import FEATHERLESS_API_KEY

# Featherless API endpoint
FEATHERLESS_URL = "https://api.featherless.ai/v1/chat/completions"
MODEL = "deepseek-ai/DeepSeek-V3.2"

def call_llm(prompt, temperature=0.3, max_tokens=4000):
    """
    Call Featherless AI directly (no OpenAI SDK needed!)
    """
    try:
        headers = {
            "Authorization": f"Bearer {FEATHERLESS_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "You are an expert educational AI assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        response = requests.post(FEATHERLESS_URL, json=payload, headers=headers, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            print(f"❌ Featherless API Error: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return None
    
    except Exception as e:
        print(f"❌ Error calling Featherless: {e}")
        return None

def clean_and_structure_notes(raw_text, subject=None, topic=None):
    """Clean and structure notes"""
    
    prompt = f"""You are an expert note-taker and editor.

I have raw text from class notes. Clean and structure them properly.

{"Subject: " + subject if subject else ""}
{"Topic: " + topic if topic else ""}

RAW TEXT:
\"\"\"
{raw_text[:3000]}
\"\"\"

OUTPUT FORMAT (JSON):
{{
    "detected_topic": "topic name",
    "detected_subject": "subject name",
    "cleaned_notes": "properly formatted notes",
    "key_concepts": ["concept1", "concept2", "concept3", "concept4", "concept5"],
    "summary": "2-3 sentence summary"
}}

Return ONLY valid JSON:
"""
    
    response = call_llm(prompt, max_tokens=3000)
    
    if not response:
        return {
            "detected_topic": topic or "Study Notes",
            "detected_subject": subject or "General",
            "cleaned_notes": raw_text,
            "key_concepts": [],
            "summary": ""
        }
    
    try:
        content = response.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        return json.loads(content.strip())
    except:
        return {
            "detected_topic": topic or "Study Notes",
            "detected_subject": subject or "General",
            "cleaned_notes": raw_text,
            "key_concepts": [],
            "summary": ""
        }

def generate_analogies(concepts, topic):
    """Generate analogies"""
    
    if not concepts:
        return {"analogies": []}
    
    prompt = f"""Generate simple analogies for these concepts:
Topic: {topic}
Concepts: {', '.join(concepts[:5])}

OUTPUT FORMAT (JSON):
{{
    "analogies": [
        {{
            "concept": "concept name",
            "analogy": "simple explanation",
            "example": "relatable example",
            "why_it_works": "explanation"
        }}
    ]
}}

Return ONLY valid JSON:
"""
    
    response = call_llm(prompt, max_tokens=2000)
    
    if not response:
        return {"analogies": []}
    
    try:
        content = response.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        return json.loads(content.strip())
    except:
        return {"analogies": []}

def generate_questions(notes, topic):
    """Generate exam questions"""
    
    prompt = f"""Generate 10 exam questions from these notes about {topic}:

{notes[:3000]}

OUTPUT FORMAT (JSON):
{{
    "questions": [
        {{
            "type": "SHORT/LONG/MCQ/TRUE_FALSE",
            "question": "question text",
            "marks": 5,
            "hint": "brief hint",
            "options": ["a", "b", "c", "d"]
        }}
    ]
}}

Return ONLY valid JSON:
"""
    
    response = call_llm(prompt, max_tokens=3000)
    
    if not response:
        return {"questions": []}
    
    try:
        content = response.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        return json.loads(content.strip())
    except:
        return {"questions": []}

def expand_notes(notes, topic):
    """Expand notes"""
    
    prompt = f"""Expand these notes about {topic} with detailed explanations:

{notes[:2500]}

Return expanded text with headings and bullet points.
"""
    
    response = call_llm(prompt, max_tokens=4000)
    return response if response else notes

def generate_diagram_queries(topic, concepts):
    """Generate diagram queries"""
    
    if not concepts:
        return {"diagram_queries": []}
    
    prompt = f"""Generate 3-5 search queries for diagrams about {topic}.
Concepts: {', '.join(concepts[:5])}

OUTPUT FORMAT (JSON):
{{
    "diagram_queries": [
        {{
            "query": "search query",
            "description": "what this shows",
            "relevance": "which concept"
        }}
    ]
}}

Return ONLY valid JSON:
"""
    
    response = call_llm(prompt, max_tokens=1000)
    
    if not response:
        return {"diagram_queries": []}
    
    try:
        content = response.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        return json.loads(content.strip())
    except:
        return {"diagram_queries": []}

# ═══════════════════════════════════════════════════════════════
# Test
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n✅ LLM Processor loaded!")
    print(f"📊 Using: Featherless AI ({MODEL})")
    print(f"\n🧪 Testing connection...\n")
    
    test = call_llm("Say 'Hello from Featherless!' in a friendly way.")
    
    if test:
        print(f"✅ SUCCESS!\n{test}\n")
    else:
        print("❌ Test failed! Check your API key.")