import os
import logging
import requests
import google.generativeai as genai

logger = logging.getLogger(__name__)

class SourceIdentifier:
    def __init__(self, api_key=None, tmdb_key=None):
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        self.tmdb_key = tmdb_key or os.environ.get("TMDB_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    def search_tmdb(self, query):
        """
        Searches TMDB for movies/TV shows.
        """
        if not self.tmdb_key:
            return []
        
        url = f"https://api.themoviedb.org/3/search/multi?api_key={self.tmdb_key}&query={query}"
        try:
            response = requests.get(url)
            return response.json().get('results', [])
        except Exception as e:
            logger.error(f"TMDB search failed: {e}")
            return []

    def identify(self, vision_results, audio_results):
        """
        Uses LLM to identify the source based on all gathered evidence.
        """
        # Combine evidence
        evidence = "VISION ANALYSIS:\n"
        for res in vision_results:
            evidence += f"- {res['analysis']}\n"
        
        evidence += "\nAUDIO TRANSCRIPTION:\n"
        evidence += audio_results['transcription'].get('text', 'No speech detected.')
        
        evidence += "\nMUSIC DETECTED:\n"
        for m in audio_results['music']:
            evidence += f"- {m['title']} by {m['artist']}\n"

        prompt = f"""
        Given the following evidence from a video analysis, identify the most likely source (Movie, TV Show, or Original Content).
        
        EVIDENCE:
        {evidence}
        
        Provide your reasoning and name the source if possible. 
        If it looks like original content (UGC), state so.
        Return in JSON format:
        {{
            "source_name": "...",
            "year": "...",
            "type": "movie/tv/ugc",
            "confidence": "high/medium/low",
            "reasoning": "..."
        }}
        """

        if not self.model:
            return {
                "source_name": "Unknown (MOCK)",
                "year": "N/A",
                "type": "unknown",
                "confidence": "low",
                "reasoning": "Running in mock mode."
            }

        try:
            response = self.model.generate_content(prompt)
            # Try to parse JSON from response (naive approach)
            import json
            text = response.text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            return json.loads(text)
        except Exception as e:
            logger.error(f"Identification failed: {e}")
            return { "error": str(e), "raw_response": response.text if 'response' in locals() else None }

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
