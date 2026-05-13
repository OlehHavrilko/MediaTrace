import unittest
import os
from vision_analyzer import VisionAnalyzer

class TestVisionAnalyzer(unittest.TestCase):
    def setUp(self):
        # We don't have a real API key for testing, so it should fall back to MOCK mode.
        # Ensure GOOGLE_API_KEY is not in env for this test
        if "GOOGLE_API_KEY" in os.environ:
            del os.environ["GOOGLE_API_KEY"]
        self.analyzer = VisionAnalyzer()

    def test_mock_mode(self):
        result = self.analyzer.analyze_frame("test.jpg")
        self.assertIn("MOCK ANALYSIS", result)

if __name__ == "__main__":
    unittest.main()
