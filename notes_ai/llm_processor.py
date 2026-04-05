# llm_processor.py
"""
LLM Processing - Clean, enhance, and enrich the notes
"""

from langchain_groq import ChatGroq
import json
from config import GROQ_API_KEY, LLM_MODEL

llm = ChatGroq(
    model=LLM_MODEL,
    groq_api_key=GROQ_API_KEY,
    temperature=0.3
)

def clean_and_structure_notes(raw_text, subject=None, topic=None):
    """
    Clean up messy OCR text and structure it properly
    """
    
    prompt = f"""You are an expert note-taker and editor.

I have raw text extracted from handwritten notes (via OCR). 
The text may have:
- Spelling mistakes
- Grammar errors
- Missing words
- Jumbled sentences
- Abbreviations

Your job:
1. Fix all spelling and grammar errors
2. Expand abbreviations (e.g., "govt" → "government", "b/w" → "between")
3. Structure into proper headings and bullet points
4. Fill in obviously missing words
5. Keep the original meaning intact
6. Detect the topic if not provided

{"Subject: " + subject if subject else ""}
{"Topic: " + topic if topic else ""}

RAW OCR TEXT:
\"\"\"
{raw_text}
\"\"\"

OUTPUT FORMAT (JSON):
{{
    "detected_topic": "topic name",
    "detected_subject": "subject name",
    "cleaned_notes": "properly formatted notes with headings and bullets",
    "key_concepts": ["concept1", "concept2", "concept3"],
    "summary": "2-3 sentence summary of the notes"
}}

Output JSON only:
"""
    
    response = llm.invoke(prompt)
    
    try:
        content = response.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        return json.loads(content.strip())
    except:
        return {
            "detected_topic": topic or "Unknown Topic",
            "detected_subject": subject or "Unknown Subject",
            "cleaned_notes": raw_text,
            "key_concepts": [],
            "summary": ""
        }

def generate_analogies(concepts, topic):
    """
    Generate simple, relatable analogies for each concept
    """
    
    prompt = f"""You are a brilliant teacher who explains complex concepts using simple analogies.

Topic: {topic}
Key Concepts: {', '.join(concepts)}

For EACH concept, provide:
1. A simple analogy using everyday objects/situations
2. An example that a college student would relate to
3. Why this analogy works

OUTPUT FORMAT (JSON):
{{
    "analogies": [
        {{
            "concept": "concept name",
            "analogy": "simple analogy explanation",
            "example": "relatable example",
            "why_it_works": "brief explanation"
        }}
    ]
}}

Make analogies:
- Fun and memorable
- Using things students know (phones, games, food, social media)
- Easy to remember during exams

Output JSON only:
"""
    
    response = llm.invoke(prompt)
    
    try:
        content = response.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        return json.loads(content.strip())
    except:
        return {"analogies": []}

def generate_questions(notes, topic, num_questions=10):
    """
    Generate probable exam questions from the notes
    """
    
    prompt = f"""You are an experienced professor who sets exam papers.

Topic: {topic}

Notes:
\"\"\"
{notes[:3000]}
\"\"\"

Generate {num_questions} probable exam questions:
- 3 SHORT ANSWER questions (2-3 marks)
- 3 LONG ANSWER questions (5-10 marks)
- 2 MCQs with options
- 2 TRUE/FALSE with explanation

OUTPUT FORMAT (JSON):
{{
    "questions": [
        {{
            "type": "SHORT/LONG/MCQ/TRUE_FALSE",
            "question": "question text",
            "marks": 2,
            "hint": "brief hint for answering",
            "options": ["a", "b", "c", "d"]  // only for MCQ
        }}
    ]
}}

Make questions that are:
- Actually likely to come in exams
- Cover all key concepts from notes
- Varying difficulty levels

Output JSON only:
"""
    
    response = llm.invoke(prompt)
    
    try:
        content = response.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        return json.loads(content.strip())
    except:
        return {"questions": []}

def expand_notes(notes, topic):
    """
    Expand brief notes with more details and explanations
    """
    
    prompt = f"""You are a subject expert and textbook author.

Topic: {topic}

These are brief class notes:
\"\"\"
{notes[:2000]}
\"\"\"

Expand these notes by:
1. Adding more detailed explanations for each point
2. Including relevant formulas (if applicable)
3. Adding real-world applications
4. Including "Remember" tips for exams
5. Adding connecting statements between sections

Keep the same structure but make it more comprehensive.
Write as if explaining to a student who missed the class.

OUTPUT FORMAT:
Return the expanded notes as markdown with proper headings (##, ###), 
bullet points, and emphasis (**bold**, *italic*).
"""
    
    response = llm.invoke(prompt)
    return response.content

def generate_diagram_queries(topic, concepts):
    """
    Generate search queries to find relevant diagrams
    """
    
    prompt = f"""Topic: {topic}
Key Concepts: {', '.join(concepts)}

What diagrams/images would help understand this topic?

Generate 3-5 Google Image search queries to find relevant educational diagrams.

OUTPUT FORMAT (JSON):
{{
    "diagram_queries": [
        {{
            "query": "search query for google images",
            "description": "what this diagram shows",
            "relevance": "which concept it explains"
        }}
    ]
}}

Make queries specific enough to find educational diagrams, not random images.
Example: "TCP three way handshake diagram" not just "TCP"

Output JSON only:
"""
    
    response = llm.invoke(prompt)
    
    try:
        content = response.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        return json.loads(content.strip())
    except:
        return {"diagram_queries": []}