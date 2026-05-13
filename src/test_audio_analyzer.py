import unittest
import os
from audio_analyzer import AudioAnalyzer

class TestAudioAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = AudioAnalyzer()

    def test_transcribe_nonexistent(self):
        result = self.analyzer.transcribe("non_existent.wav")
        self.assertEqual(result['status'], 'failed')
        self.assertIn('error', result)

    def test_music_identification_no_key(self):
        # Should not raise exception, just warn and return empty
        result = self.analyzer.identify_music("test.wav")
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()
