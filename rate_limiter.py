# rate_limiter.py
"""
Rate limiter to prevent hitting API limits.
Groq free tier: 30 requests/minute
"""

import time
from datetime import datetime, timedelta
from config import MAX_CALLS_PER_MINUTE

class RateLimiter:
    def __init__(self, max_calls_per_minute=MAX_CALLS_PER_MINUTE):
        self.max_calls = max_calls_per_minute
        self.calls = []
        self.total_calls = 0
    
    def can_call(self):
        """Check if we can make another API call"""
        now = datetime.now()
        # Remove calls older than 1 minute
        self.calls = [t for t in self.calls if now - t < timedelta(minutes=1)]
        
        return len(self.calls) < self.max_calls
    
    def wait_if_needed(self):
        """Wait if we've hit rate limit"""
        if not self.can_call():
            wait_time = 60 - (datetime.now() - self.calls[0]).seconds
            print(f"⏳ Rate limit reached. Waiting {wait_time} seconds...")
            time.sleep(wait_time + 1)
        
        self.calls.append(datetime.now())
        self.total_calls += 1
        return True
    
    def get_stats(self):
        """Show current usage"""
        now = datetime.now()
        recent = [t for t in self.calls if now - t < timedelta(minutes=1)]
        return {
            "calls_last_minute": len(recent),
            "remaining_this_minute": self.max_calls - len(recent),
            "total_calls_today": self.total_calls
        }
    
    def print_stats(self):
        """Print usage stats"""
        stats = self.get_stats()
        print(f"\n📊 API Usage: {stats['calls_last_minute']}/{self.max_calls} calls this minute")
        print(f"   Total today: {stats['total_calls_today']}")

# Global rate limiter instance
limiter = RateLimiter()