# cache_manager.py
"""
Caching system to avoid re-checking the same claims.
Saves money and API calls.
"""

import json
import os
import hashlib
from datetime import datetime
from config import CACHE_FILE, ENABLE_CACHE

class CacheManager:
    def __init__(self, cache_file=CACHE_FILE):
        self.cache_file = cache_file
        self.cache = self._load_cache()
        self.hits = 0
        self.misses = 0
    
    def _load_cache(self):
        """Load cache from file"""
        if not ENABLE_CACHE:
            return {}
        
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_cache(self):
        """Save cache to file"""
        if not ENABLE_CACHE:
            return
        
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, indent=2, ensure_ascii=False)
    
    def _get_cache_key(self, claim):
        """Generate unique key for claim"""
        # Normalize claim (lowercase, strip whitespace)
        normalized = claim.lower().strip()
        # Create hash
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def get(self, claim):
        """Get cached result for claim"""
        if not ENABLE_CACHE:
            return None
        
        key = self._get_cache_key(claim)
        
        if key in self.cache:
            self.hits += 1
            cached_data = self.cache[key]
            print(f"\n📦 Cache HIT! (Last checked: {cached_data['timestamp']})")
            return cached_data['result']
        
        self.misses += 1
        return None
    
    def set(self, claim, result):
        """Cache result for claim"""
        if not ENABLE_CACHE:
            return
        
        key = self._get_cache_key(claim)
        
        self.cache[key] = {
            'claim': claim,
            'result': result,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self._save_cache()
    
    def clear(self):
        """Clear all cache"""
        self.cache = {}
        self._save_cache()
        print("🗑️  Cache cleared")
    
    def get_stats(self):
        """Get cache statistics"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            'total_cached': len(self.cache),
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': f"{hit_rate:.1f}%"
        }
    
    def print_stats(self):
        """Print cache stats"""
        stats = self.get_stats()
        print(f"\n💾 Cache Stats:")
        print(f"   Cached claims: {stats['total_cached']}")
        print(f"   Hits: {stats['hits']} | Misses: {stats['misses']}")
        print(f"   Hit rate: {stats['hit_rate']}")

# Global cache instance
cache = CacheManager()