# agent_core.py
"""
Main fact-checking agent with caching, rate limiting, and real search.
"""

from langchain_groq import ChatGroq
import json
from notes_agent.config import GROQ_API_KEY, LLM_MODEL, LLM_TEMPERATURE
from notes_agent.rate_limiter import limiter
from notes_agent.cache_manager import cache
from notes_agent.search_tools import search_evidence

# ══════════════════════════════════════════════════════
# LLM Setup
# ══════════════════════════════════════════════════════

llm = ChatGroq(
    model=LLM_MODEL,
    groq_api_key=GROQ_API_KEY,
    temperature=LLM_TEMPERATURE
)

# ══════════════════════════════════════════════════════
# STEP 1: Claim Classification
# ══════════════════════════════════════════════════════

def classify_claim(claim_text):
    """Extract and categorize claim"""
    
    # Wait for rate limit if needed
    limiter.wait_if_needed()
    
    prompt = f"""You are a claim analysis expert for Indian misinformation.

INPUT CLAIM: "{claim_text}"

Analyze this claim and extract:
1. The MAIN factual claim (one clear sentence)
2. Category: GOVERNMENT_SCHEME / HEALTH / NEWS / SCAM / OTHER
3. 3-5 search keywords (focus on verifiable facts)

OUTPUT FORMAT (JSON only, no explanation):
{{
  "claim": "exact factual claim here",
  "category": "GOVERNMENT_SCHEME",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "needs_verification": true
}}

EXAMPLES:

Input: "Modi ji giving 5000 rupees to all students, forward this to get money"
Output: {{"claim": "Government giving ₹5000 to all students", "category": "GOVERNMENT_SCHEME", "keywords": ["5000 rupees", "students", "government scheme"], "needs_verification": true}}

Input: "Eating garlic cures dengue fever"
Output: {{"claim": "Garlic cures dengue fever", "category": "HEALTH", "keywords": ["garlic", "dengue", "cure"], "needs_verification": true}}

Now process:
"""
    
    response = llm.invoke(prompt)
    
    # Parse JSON
    try:
        content = response.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        result = json.loads(content.strip())
        return result
    except Exception as e:
        print(f"⚠️  Classification error: {str(e)}")
        return {
            "claim": claim_text,
            "category": "OTHER",
            "keywords": claim_text.split()[:5],
            "needs_verification": True
        }

# ══════════════════════════════════════════════════════
# STEP 2: Verification
# ══════════════════════════════════════════════════════

def verify_claim(claim_data, evidence_data):
    """Compare claim against evidence"""
    
    # Wait for rate limit
    limiter.wait_if_needed()
    
    claim = claim_data['claim']
    evidence = "\n\n".join(evidence_data['evidence'])
    sources = ", ".join(evidence_data['sources'])
    
    prompt = f"""You are a fact-checking agent for Indian claims.

CLAIM TO VERIFY:
"{claim}"

EVIDENCE FOUND FROM TRUSTED SOURCES:
{evidence}

SOURCES CHECKED:
{sources}

Your task:
1. Carefully compare the claim against the evidence
2. Determine verdict:
   - TRUE: Claim is accurate and matches evidence
   - FALSE: Claim is incorrect and contradicts evidence  
   - MISLEADING: Claim is partially true but missing context/conditions
   - CANNOT_VERIFY: Insufficient or no evidence found

3. Explain reasoning in 2-3 clear sentences
4. Rate confidence: HIGH (official sources) / MEDIUM (indirect evidence) / LOW (no clear evidence)

IMPORTANT:
- If evidence says "No announcement found" → verdict is likely FALSE
- If claim says "all students" but evidence says "SC/ST students only" → MISLEADING
- Always cite specific facts from evidence

OUTPUT FORMAT (JSON only):
{{
  "verdict": "TRUE/FALSE/MISLEADING/CANNOT_VERIFY",
  "reasoning": "Clear explanation with specific facts from evidence",
  "confidence": "HIGH/MEDIUM/LOW",
  "key_facts": ["fact 1 from evidence", "fact 2"]
}}

Now verify:
"""
    
    response = llm.invoke(prompt)
    
    try:
        content = response.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        result = json.loads(content.strip())
        return result
    except Exception as e:
        print(f"⚠️  Verification error: {str(e)}")
        return {
            "verdict": "CANNOT_VERIFY",
            "reasoning": "Error in verification process",
            "confidence": "LOW",
            "key_facts": []
        }

# ══════════════════════════════════════════════════════
# MAIN AGENT
# ══════════════════════════════════════════════════════

def fact_check(user_claim, verbose=True):
    """
    Main fact-checking function.
    
    Args:
        user_claim: Claim to verify
        verbose: Print step-by-step progress
    
    Returns:
        {claim, verdict, reasoning, sources, evidence, confidence}
    """
    
    # Check cache first
    cached_result = cache.get(user_claim)
    if cached_result:
        return cached_result
    
    if verbose:
        print("\n🔍 FACT-CHECK AGENT STARTED")
        print("=" * 60)
    
    # STEP 1: Classify claim
    if verbose:
        print("\n📋 Step 1: Analyzing claim...")
    
    claim_data = classify_claim(user_claim)
    
    if verbose:
        print(f"   ✓ Claim: {claim_data['claim']}")
        print(f"   ✓ Category: {claim_data['category']}")
        print(f"   ✓ Keywords: {', '.join(claim_data['keywords'])}")
    
    # STEP 2: Search for evidence
    if verbose:
        print("\n🔍 Step 2: Searching for evidence...")
    
    evidence_data = search_evidence(claim_data['category'], claim_data['keywords'])
    
    if verbose:
        print(f"   ✓ Sources checked: {len(evidence_data['sources'])}")
        for source in evidence_data['sources']:
            print(f"      • {source}")
        print(f"   ✓ Evidence found: {len(evidence_data['evidence'])} items")
    
    # STEP 3: Verify
    if verbose:
        print("\n⚖️  Step 3: Verifying claim...")
    
    verdict_data = verify_claim(claim_data, evidence_data)
    
    # Build result
    result = {
        "claim": claim_data['claim'],
        "verdict": verdict_data['verdict'],
        "reasoning": verdict_data['reasoning'],
        "sources": evidence_data['sources'],
        "evidence": evidence_data['evidence'],
        "confidence": verdict_data['confidence'],
        "key_facts": verdict_data.get('key_facts', [])
    }
    
    # Cache the result
    cache.set(user_claim, result)
    
    # Print formatted output
    if verbose:
        print("\n" + "=" * 60)
        print("📊 FACT-CHECK RESULT")
        print("=" * 60)
        print(f"\n📌 CLAIM: {result['claim']}")
        
        verdict_emoji = {
            "TRUE": "✅",
            "FALSE": "❌",
            "MISLEADING": "⚠️",
            "CANNOT_VERIFY": "❓"
        }
        print(f"\n{verdict_emoji.get(result['verdict'], '🔵')} VERDICT: {result['verdict']}")
        print(f"\n💭 REASONING:\n   {result['reasoning']}")
        
        if result.get('key_facts'):
            print(f"\n📍 KEY FACTS:")
            for fact in result['key_facts']:
                print(f"   • {fact}")
        
        print(f"\n📚 SOURCES CHECKED:")
        for source in result['sources']:
            print(f"   • {source}")
        
        print(f"\n🎚️  CONFIDENCE: {result['confidence']}")
        print("=" * 60)
        
        # Show stats
        limiter.print_stats()
        cache.print_stats()
    
    return result

# ══════════════════════════════════════════════════════
# Test
# ══════════════════════════════════════════════════════

if __name__ == "__main__":
    test_claim = "Government is giving free laptops to all students"
    result = fact_check(test_claim)