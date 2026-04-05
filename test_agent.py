# test_agent.py
"""
Test suite for the fact-checking agent.
"""

from agent_core import fact_check
from cache_manager import cache

# Test claims
TEST_CLAIMS = [
    "Government is giving ₹5000 to all students",
    "Eating garlic cures COVID-19",
    "PM announced laptop scheme for SC/ST students",
    "WHO said vaccines are dangerous",
    "Modi giving ₹15000 to women, forward this message"
]

def run_tests():
    """Run all test claims"""
    print("\n" + "="*60)
    print("🧪 TESTING FACT-CHECK AGENT")
    print("="*60)
    
    results = []
    
    for i, claim in enumerate(TEST_CLAIMS, 1):
        print(f"\n\n{'='*60}")
        print(f"TEST {i}/{len(TEST_CLAIMS)}")
        print(f"{'='*60}")
        
        result = fact_check(claim, verbose=True)
        results.append(result)
        
        input("\n⏸️  Press Enter to continue to next test...")
    
    # Summary
    print("\n\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    for i, (claim, result) in enumerate(zip(TEST_CLAIMS, results), 1):
        print(f"\n{i}. {claim[:50]}...")
        print(f"   → {result['verdict']} ({result['confidence']} confidence)")
    
    # Stats
    print("\n")
    cache.print_stats()

if __name__ == "__main__":
    # Optional: Clear cache before testing
    # cache.clear()
    
    run_tests()