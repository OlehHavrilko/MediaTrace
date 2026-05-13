import os
import logging
import tmdbsimple as tmdb
from omdbapi.movie_search import GetMovie
from typing import Dict, Any, List, Optional

logger = logging.getLogger("MediaTrace.SourceIdentifier")

class SourceIdentifier:
    """
    Identifies video sources using multiple databases (TMDB, OMDb) 
    with a weighted scoring engine.
    """
    def __init__(self, tmdb_key: str = None, omdb_key: str = None):
        self.tmdb_key = tmdb_key or os.environ.get("TMDB_API_KEY")
        self.omdb_key = omdb_key or os.environ.get("OMDB_API_KEY")
        
        if not self.tmdb_key:
            logger.warning("TMDB_API_KEY missing.")
        else:
            tmdb.API_KEY = self.tmdb_key
            
        self.omdb = None
        if self.omdb_key:
            self.omdb = GetMovie(api_key=self.omdb_key)
        else:
            logger.warning("OMDB_API_KEY missing.")

    def search_tmdb(self, query: str) -> List[Dict[str, Any]]:
        if not self.tmdb_key: return []
        search = tmdb.Search()
        response = search.movie(query=query)
        return response.get('results', [])

    def search_omdb(self, query: str) -> List[Dict[str, Any]]:
        if not self.omdb: return []
        try:
            results = self.omdb.get_search(title=query)
            return results if isinstance(results, list) else []
        except Exception:
            return []

    def identify(self, analysis_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Aggregates results from multiple sources and applies weighted scoring.
        """
        vision_hint = analysis_data.get('vision', {}).get('source_hint')
        if not vision_hint or vision_hint == "Unknown":
            return []
            
        # Perform searches
        tmdb_res = self.search_tmdb(vision_hint)
        omdb_res = self.search_omdb(vision_hint)
        
        # Merge logic (simplified weighted score: TMDB match = 0.6, OMDb match = 0.4)
        scores = {}
        for item in tmdb_res:
            title = item['title'].lower()
            scores[title] = scores.get(title, 0) + 0.6
            
        for item in omdb_res:
            title = item['title'].lower()
            scores[title] = scores.get(title, 0) + 0.4
            
        # Convert to list and sort by score
        final_list = [{"title": k, "confidence": v} for k, v in scores.items()]
        return sorted(final_list, key=lambda x: x['confidence'], reverse=True)
