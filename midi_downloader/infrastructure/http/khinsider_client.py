"""HTTP client for khinsider.com using cloudscraper to bypass Cloudflare."""

import time
import cloudscraper
from typing import Optional
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException


class KhinsiderClient:
    """HTTP client with automatic retries and rate limiting."""
    
    def __init__(
        self,
        rate_limit_delay: float = 1.0,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
        user_agent: Optional[str] = None
    ):
        """
        Initialize the HTTP client.
        
        Args:
            rate_limit_delay: Seconds to wait between requests
            max_retries: Maximum number of retry attempts
            backoff_factor: Exponential backoff multiplier
            user_agent: Custom user agent string
        """
        self.rate_limit_delay = rate_limit_delay
        self.last_request_time = 0.0
        
        # Create cloudscraper session (bypasses Cloudflare)
        self.session = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            }
        )
        
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=['GET', 'HEAD']
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        
        # Set headers
        self.session.headers.update({
            'User-Agent': user_agent or 'Mozilla/5.0 (compatible; MIDIDownloader/1.0)'
        })
    
    def get(self, url: str) -> Optional[bytes]:
        """
        Make a GET request with rate limiting.
        
        Args:
            url: URL to request
            
        Returns:
            Response content as bytes, or None on failure
        """
        self._rate_limit()
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.content
        except RequestException as e:
            print(f"Request failed for {url}: {e}")
            return None
    
    def get_text(self, url: str) -> Optional[str]:
        """
        Make a GET request and return text content.
        
        Args:
            url: URL to request
            
        Returns:
            Response content as string, or None on failure
        """
        content = self.get(url)
        if content:
            return content.decode('utf-8', errors='ignore')
        return None
    
    def _rate_limit(self) -> None:
        """Enforce rate limiting between requests."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        
        self.last_request_time = time.time()
    
    def close(self) -> None:
        """Close the session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager support."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup."""
        self.close()
