import os
import logging
import whisper
import acoustid

logger = logging.getLogger(__name__)

class AudioAnalyzer:
    def __init__(self, model_size="base", acoustid_key=None):
        self.model_size = model_size
        self.acoustid_key = acoustid_key or os.environ.get("ACOUSTID_API_KEY")
        self._model = None

    @property
    def model(self):
        if self._model is None:
            logger.info(f"Loading Whisper model: {self.model_size}")
            self._model = whisper.load_model(self.model_size)
        return self._model

    def transcribe(self, audio_path):
        """
        Transcribes audio using Whisper.
        """
        try:
            logger.info(f"Transcribing: {audio_path}")
            result = self.model.transcribe(audio_path)
            return {
                'text': result['text'],
                'segments': result['segments'],
                'language': result.get('language')
            }
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            return {'text': "", 'segments': [], 'error': str(e)}

    def identify_music(self, audio_path):
        """
        Identifies music using AcoustID.
        """
        if not self.acoustid_key:
            logger.warning("ACOUSTID_API_KEY not found. Skipping music identification.")
            return []

        try:
            results = acoustid.match(self.acoustid_key, audio_path)
            matches = []
            for score, recording_id, title, artist in results:
                matches.append({
                    'score': score,
                    'recording_id': recording_id,
                    'title': title,
                    'artist': artist
                })
            return matches
        except Exception as e:
            logger.error(f"Error identifying music: {e}")
            return []

    def analyze(self, audio_path):
        """
        Full audio analysis.
        """
        transcription = self.transcribe(audio_path)
        music = self.identify_music(audio_path)
        
        return {
            'transcription': transcription,
            'music': music
        }

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
