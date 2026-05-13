import os
import logging
from typing import List, Dict, Any, Optional
import whisper
import acoustid

logger = logging.getLogger("MediaTrace.AudioAnalyzer")

class AudioAnalyzer:
    """
    Handles speech transcription (Whisper) and music recognition (AcoustID).
    """
    def __init__(self, model_size: str = "base"):
        self.model_size = model_size
        self.acoustid_key = os.environ.get("ACOUSTID_API_KEY")
        self._model = None

    def _get_model(self):
        """Lazy load the Whisper model."""
        if self._model is None:
            logger.info(f"Loading Whisper model: {self.model_size}...")
            self._model = whisper.load_model(self.model_size)
        return self._model

    def transcribe(self, audio_path: str) -> Dict[str, Any]:
        """Transcribes audio using Whisper."""
        if not os.path.exists(audio_path):
            return {"status": "failed", "error": "File not found"}
            
        try:
            logger.info("Starting transcription...")
            model = self._get_model()
            result = model.transcribe(audio_path)
            return {
                'text': result['text'].strip(),
                'language': result.get('language', 'unknown'),
                'status': 'success'
            }
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            return {'text': "", 'error': str(e), 'status': 'failed'}

    def identify_music(self, audio_path: str) -> List[Dict[str, Any]]:
        """Identifies music using AcoustID API."""
        if not self.acoustid_key:
            logger.warning("ACOUSTID_API_KEY missing, skipping music identification.")
            return []

        try:
            # Note: acoustid.match expects file_path
            matches = acoustid.match(self.acoustid_key, audio_path)
            results = []
            for score, recording_id, title, artist in matches:
                results.append({
                    'score': float(score),
                    'recording_id': recording_id,
                    'title': title,
                    'artist': artist
                })
            # Return top 3 matches
            return sorted(results, key=lambda x: x['score'], reverse=True)[:3]
        except Exception as e:
            logger.error(f"Music identification failed: {e}")
            return []

    def analyze(self, audio_path: str) -> Dict[str, Any]:
        """Full audio analysis pipeline."""
        return {
            'transcription': self.transcribe(audio_path),
            'music_matches': self.identify_music(audio_path)
        }

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import sys
    if len(sys.argv) > 1:
        analyzer = AudioAnalyzer()
        print(analyzer.analyze(sys.argv[1]))
