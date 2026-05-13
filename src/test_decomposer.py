import unittest
import os
import shutil
from decomposer import VideoDecomposer

class TestDecomposer(unittest.TestCase):
    def setUp(self):
        self.output_base = "test_temp"
        self.decomposer = VideoDecomposer(output_base=self.output_base)
        # Create a dummy video file if we had one, but for this test,
        # we will test with a path that doesn't exist and expect error handling
        self.dummy_metadata = {
            'file_path': 'non_existent.mp4',
            'duration': 5
        }

    def tearDown(self):
        if os.path.exists(self.output_base):
            shutil.rmtree(self.output_base)

    def test_init(self):
        self.assertTrue(os.path.exists(self.output_base))

    def test_decompose_invalid_file(self):
        with self.assertRaises(Exception):
            self.decomposer.decompose(self.dummy_metadata)

if __name__ == "__main__":
    unittest.main()
