import os
import logging
import tmdbsimple as tmdb
from typing import Dict, Any, List, Optional

logger = logging.getLogger("MediaTrace.SourceIdentifier")

class SourceIdentifier:
    """
    Identifies video sources using TMDB API based on multimodal insights.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("TMDB_API_KEY")
        if not self.api_key:
            logger.error("TMDB_API_KEY is missing.")
            raise ValueError("TMDB_API_KEY must be provided.")
        
        tmdb.API_KEY = self.api_key
        logger.info("SourceIdentifier initialized with TMDB.")

    def search_media(self, query: str, media_type: str = 'movie') -> List[Dict[str, Any]]:
        """
        Searches TMDB for movies or TV shows.
        """
        try:
            if media_type == 'movie':
                search = tmdb.Search()
                response = search.movie(query=query)
            else:
                search = tmdb.Search()
                response = search.tv(query=query)
                
            return response.get('results', [])
        except Exception as e:
            logger.error(f"TMDB search failed: {e}")
            return []

    def identify(self, analysis_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Attempts to identify the source based on gathered multimodal insights.
        """
        potential_sources = []
        
        # 1. Use source_hint from vision analysis
        vision_analysis = analysis_data.get('vision', {})
        hint = vision_analysis.get('source_hint')
        if hint and hint != "Unknown":
            results = self.search_media(hint)
            potential_sources.extend(results)
            
        # 2. Add transcription entities if available
        # (This would be expanded with NER in a full implementation)
        
        return potential_sources

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # CLI test (needs API key)
    if os.environ.get("TMDB_API_KEY"):
        si = SourceIdentifier()
        results = si.search_media("Inception")
        print(f"Found {len(results)} matches.")
