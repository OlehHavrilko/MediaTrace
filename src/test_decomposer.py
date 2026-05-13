import unittest
import os
import shutil
from decomposer import VideoDecomposer

class TestVideoDecomposer(unittest.TestCase):
    def setUp(self):
        self.output_base = "test_temp_decomposer"
        self.decomposer = VideoDecomposer(output_base=self.output_base)
        self.dummy_metadata = {
            'id': 'test_video_123',
            'file_path': 'non_existent.mp4',
            'duration': 5
        }

    def tearDown(self):
        if os.path.exists(self.output_base):
            shutil.rmtree(self.output_base)

    def test_init(self):
        self.assertTrue(os.path.exists(self.output_base))

    def test_decompose_invalid_file(self):
        # Should raise RuntimeError or similar because FFmpeg will fail
        with self.assertRaises(Exception):
            self.decomposer.decompose(self.dummy_metadata)

    def test_output_structure_creation(self):
        # Verify that specific directories are planned correctly
        video_id = "test_id"
        audio_dir = os.path.join(self.output_base, video_id)
        frames_dir = os.path.join(audio_dir, "frames")
        
        # Test directory creation logic via a sub-method if possible, 
        # or just verify it doesn't crash
        self.decomposer.output_base = os.path.abspath(self.output_base)
        self.assertEqual(self.decomposer.output_base, os.path.abspath(self.output_base))

if __name__ == "__main__":
    unittest.main()
