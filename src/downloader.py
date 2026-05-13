import os
import yt_dlp
import logging
from datetime import datetime

logger = logging.getLogger("MediaTrace.Downloader")

class VideoDownloader:
    """
    Advanced downloader for video content using yt-dlp.
    Optimized for TikTok but supports multiple platforms.
    """
    def __init__(self, download_path="temp", quiet=True):
        self.download_path = download_path
        self.quiet = quiet
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)
            logger.info(f"Created download directory: {self.download_path}")

    def get_opts(self):
        """Returns standard yt-dlp options."""
        return {
            'outtmpl': f'{self.download_path}/%(id)s.%(ext)s',
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'quiet': self.quiet,
            'no_warnings': True,
            'noprogress': self.quiet,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            }
        }

    def download(self, url):
        """
        Downloads a video and returns comprehensive metadata.
        
        Args:
            url (str): The video URL.
            
        Returns:
            dict: Metadata including file path, duration, resolution, and source info.
        """
        logger.info(f"Initiating download for URL: {url}")
        opts = self.get_opts()

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                # First extract info to check metadata
                info = ydl.extract_info(url, download=True)
                
                # Handle cases where extension might change after merge
                base_path = ydl.prepare_filename(info)
                file_path = base_path
                if not os.path.exists(file_path):
                    # Try with .mp4 if the default extension doesn't exist (due to merging)
                    potential_mp4 = os.path.splitext(base_path)[0] + '.mp4'
                    if os.path.exists(potential_mp4):
                        file_path = potential_mp4

                metadata = {
                    'id': info.get('id'),
                    'title': info.get('title', 'Unknown Title'),
                    'uploader': info.get('uploader', 'Unknown Uploader'),
                    'duration': info.get('duration'),
                    'width': info.get('width'),
                    'height': info.get('height'),
                    'fps': info.get('fps'),
                    'ext': info.get('ext'),
                    'file_path': os.path.abspath(file_path),
                    'original_url': url,
                    'timestamp': datetime.now().isoformat(),
                    'filesize': os.path.getsize(file_path) if os.path.exists(file_path) else 0
                }
                
                logger.info(f"Download complete: {metadata['id']} ({metadata['filesize']} bytes)")
                return metadata

        except yt_dlp.utils.DownloadError as e:
            logger.error(f"yt-dlp download error: {e}")
            raise Exception(f"Failed to download video: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in downloader: {e}")
            raise

if __name__ == "__main__":
    # Basic CLI test
    import sys
    logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
    
    if len(sys.argv) > 1:
        test_url = sys.argv[1]
        dl = VideoDownloader(quiet=False)
        try:
            result = dl.download(test_url)
            print("\nDownload Successful!")
            for k, v in result.items():
                print(f"{k}: {v}")
        except Exception as err:
            print(f"\nDownload Failed: {err}")
    else:
        print("Usage: python downloader.py <URL>")
