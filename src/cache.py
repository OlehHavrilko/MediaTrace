import logging
import diskcache as dc
import os

logger = logging.getLogger("MediaTrace.Cache")

class PipelineCache:
    """
    Handles caching of analysis results based on video URL.
    """
    def __init__(self, cache_dir=".cache"):
        self.cache = dc.Cache(cache_dir)
        logger.info(f"Cache initialized at {cache_dir}")

    def get(self, url: str):
        return self.cache.get(url)

    def set(self, url: str, data: dict):
        self.cache.set(url, data)
        logger.info(f"Cached results for {url}")

    def clear(self):
        self.cache.clear()
        logger.info("Cache cleared.")
