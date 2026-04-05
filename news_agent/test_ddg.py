# test_ddg.py
from ddgs import DDGS
ddgs = DDGS()
results = ddgs.text("site:pib.gov.in laptop scheme students", region='in-en', max_results=3)

for r in results:
    print(f"Title: {r['title']}")
    print(f"Snippet: {r['body'][:150]}")
    print(f"Link: {r['href']}")
    print("-" * 50)