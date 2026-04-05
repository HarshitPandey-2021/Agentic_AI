# 🔍 Fact-Check Agent 

An AI-powered fact-checking system that verifies claims using official government and trusted sources.

## 🎯 Problem Statement

Misinformation spreads rapidly on WhatsApp and social media in India, especially regarding:
- Government schemes (fake announcements)
- Health advice (dangerous medical misinformation)
- Viral messages (forward-this-or-bad-luck scams)

**83% of misinformation in India spreads via WhatsApp** (Reuters Digital News Report 2023).

## ✨ Our Solution

An **agentic AI system** that:
1. **Analyzes** the claim and categorizes it (government/health/general)
2. **Searches** official sources (PIB, WHO, fact-check sites)
3. **Compares** claim vs evidence using LLM reasoning
4. **Decides** verdict autonomously with confidence scoring
5. **Cites** exact sources for transparency

### Why "Agentic"?

The agent makes autonomous decisions:
- **Chooses** which sources to search based on claim type
- **Decides** confidence level based on source quality
- **Routes** to appropriate fact-checking pipeline
- **Escalates** with "Cannot Verify" when evidence is insufficient

## 🛠️ Tech Stack

- **LLM**: Groq (Llama 3.3 70B) - Free tier, blazing fast
- **Search**: SerpAPI - 100 free searches/month
- **Agent Framework**: LangChain
- **UI**: Streamlit
- **Caching**: JSON-based (saves API calls)

## 🚀 Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Add API keys to config.py
GROQ_API_KEY = "your_groq_key"
SERPAPI_KEY = "your_serpapi_key"

# Run the app
streamlit run app.py
