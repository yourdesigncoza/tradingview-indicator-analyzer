import pytest
import time
from scraper.rate_limiter import RateLimiter, rate_limit

def test_rate_limiter():
    limiter = RateLimiter(calls_per_minute=60)
    
    start_time = time.time()
    for _ in range(3):
        limiter.wait()
    elapsed = time.time() - start_time
    
    assert elapsed >= 2/60  # Should take at least 2 seconds for 3 calls at 60 calls/minute

@rate_limit(calls_per_minute=60)
def dummy_function():
    return True

def test_rate_limit_decorator():
    start_time = time.time()
    for _ in range(3):
        dummy_function()
    elapsed = time.time() - start_time
    
    assert elapsed >= 2/60