"""
Configuration management for QA Portfolio tests.
"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

@dataclass
class TestConfig:
    """Test configuration with environment variable support."""
    base_url: str
    timeout: int = 30
    retry_count: int = 3
    retry_backoff_factor: float = 1.0
    parallel_workers: int = 4
    log_level: str = "INFO"
    enable_html_report: bool = True
    enable_allure_report: bool = True
    
    @classmethod
    def from_env(cls) -> 'TestConfig':
        """Create configuration from environment variables."""
        return cls(
            base_url=os.getenv("BASE_URL", "https://reqres.in"),
            timeout=int(os.getenv("TIMEOUT", "30")),
            retry_count=int(os.getenv("RETRY_COUNT", "3")),
            retry_backoff_factor=float(os.getenv("RETRY_BACKOFF_FACTOR", "1.0")),
            parallel_workers=int(os.getenv("PARALLEL_WORKERS", "4")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            enable_html_report=os.getenv("ENABLE_HTML_REPORT", "true").lower() == "true",
            enable_allure_report=os.getenv("ENABLE_ALLURE_REPORT", "true").lower() == "true"
        )

# Global configuration instance
config = TestConfig.from_env()
