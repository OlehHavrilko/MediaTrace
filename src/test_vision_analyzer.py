import unittest
import os
from unittest.mock import patch
from vision_analyzer import VisionAnalyzer

class TestVisionAnalyzer(unittest.TestCase):
    @patch.dict(os.environ, {"GOOGLE_API_KEY": "fake-key"})
    def test_init_success(self):
        with patch('google.generativeai.GenerativeModel'):
            analyzer = VisionAnalyzer()
            self.assertIsNotNone(analyzer.model)

    def test_init_missing_key(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                VisionAnalyzer()

if __name__ == "__main__":
    unittest.main()
