import unittest
import os
import shutil
from downloader import TikTokDownloader

class TestDownloader(unittest.TestCase):
    def setUp(self):
        self.download_path = "test_downloads"
        self.downloader = TikTokDownloader(download_path=self.download_path)

    def tearDown(self):
        if os.path.exists(self.download_path):
            shutil.rmtree(self.download_path)

    def test_downloader_init(self):
        self.assertTrue(os.path.exists(self.download_path))

    def test_invalid_url(self):
        # We expect a download error for an invalid URL
        with self.assertRaises(Exception):
            self.downloader.download("https://www.tiktok.com/invalid")

if __name__ == "__main__":
    unittest.main()
