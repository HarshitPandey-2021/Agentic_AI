# search_tools.py (BEST OPTION - NO API KEY NEEDED)

from duckduckgo_search import DDGS

def search_with_duckduckgo(query, site=None, num_results=3):
    """
    FREE DuckDuckGo search - NO API KEY NEEDED!
    Unlimited searches
    """
    
    # Add site filter
    if site:
        search_query = f"site:{site} {query}"
    else:
        search_query = query
    
    try:
        ddgs = DDGS()
        results = ddgs.text(search_query, region='in-en', max_results=num_results)
        
        snippets = []
        for r in results:
            snippets.append({
                "text": f"{r.get('title', '')}. {r.get('body', '')}",
                "source": r.get('href', '')
            })
        
        return snippets if snippets else []
    
    except Exception as e:
        print(f"⚠️  Search error: {str(e)}")
        return []

# UPDATE all search functions to use this:

def search_government_sources(keywords):
    query = " ".join(keywords)
    all_evidence = []
    sources_checked = []
    
    # Search PIB
    results = search_with_duckduckgo(query, site="pib.gov.in", num_results=3)
    
    if results:
        sources_checked.append("Press Information Bureau (pib.gov.in)")
        all_evidence.extend([r["text"] for r in results])
    
    # Search MyScheme
    results2 = search_with_duckduckgo(query, site="myscheme.gov.in", num_results=2)
    
    if results2:
        sources_checked.append("MyScheme.gov.in (Official)")
        all_evidence.extend([r["text"] for r in results2])
    
    return {
        "sources": sources_checked if sources_checked else ["Government websites"],
        "evidence": all_evidence if all_evidence else ["No official announcements found"]
    }

def search_health_sources(keywords):
    query = " ".join(keywords)
    all_evidence = []
    sources_checked = []
    
    # Search WHO
    results = search_with_duckduckgo(query, site="who.int", num_results=3)
    
    if results:
        sources_checked.append("World Health Organization (who.int)")
        all_evidence.extend([r["text"] for r in results])
    
    return {
        "sources": sources_checked if sources_checked else ["WHO"],
        "evidence": all_evidence if all_evidence else ["No health guidance found"]
    }

def search_factcheck_sources(keywords):
    query = " ".join(keywords)
    
    # Search fact-check sites
    fc_sites = ["altnews.in", "boomlive.in", "factchecker.in"]
    all_evidence = []
    sources_checked = []
    
    for site in fc_sites:
        results = search_with_duckduckgo(query, site=site, num_results=2)
        if results:
            sources_checked.append(f"{site} (Fact-check)")
            all_evidence.extend([r["text"] for r in results])
    
    return {
        "sources": sources_checked if sources_checked else ["Fact-check sites"],
        "evidence": all_evidence if all_evidence else ["No fact-checks found"]
    }