import unittest
import os
import shutil
from downloader import VideoDownloader

class TestVideoDownloader(unittest.TestCase):
    def setUp(self):
        self.download_path = "test_downloads"
        self.downloader = VideoDownloader(download_path=self.download_path, quiet=True)

    def tearDown(self):
        if os.path.exists(self.download_path):
            shutil.rmtree(self.download_path)

    def test_downloader_init(self):
        self.assertTrue(os.path.exists(self.download_path))

    def test_invalid_url(self):
        # Using a clearly invalid URL that yt-dlp cannot handle
        with self.assertRaises(Exception):
            self.downloader.download("not_a_url")

    def test_metadata_structure(self):
        # This is more of a schema test, won't actually download unless we mock yt-dlp
        # For now, we'll just test that the class exists and handles options
        opts = self.downloader.get_opts()
        self.assertIn('outtmpl', opts)
        self.assertEqual(opts['merge_output_format'], 'mp4')

if __name__ == "__main__":
    unittest.main()
