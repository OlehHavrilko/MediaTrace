import os
import yt_dlp
import logging

logger = logging.getLogger(__name__)

class TikTokDownloader:
    def __init__(self, download_path="temp"):
        self.download_path = download_path
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

    def download(self, url):
        """
        Downloads a TikTok video and returns metadata.
        """
        ydl_opts = {
            'outtmpl': f'{self.download_path}/%(id)s.%(ext)s',
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                # Ensure filename extension matches the merge_output_format if merged
                if not os.path.exists(file_path) and os.path.exists(file_path.rsplit('.', 1)[0] + '.mp4'):
                    file_path = file_path.rsplit('.', 1)[0] + '.mp4'
                
                metadata = {
                    'id': info.get('id'),
                    'title': info.get('title'),
                    'duration': info.get('duration'),
                    'width': info.get('width'),
                    'height': info.get('height'),
                    'fps': info.get('fps'),
                    'ext': info.get('ext'),
                    'file_path': file_path
                }
                logger.info(f"Successfully downloaded: {file_path}")
                return metadata
        except Exception as e:
            logger.error(f"Error downloading video: {e}")
            raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Example usage (commented out to avoid execution without URL)
    # dl = TikTokDownloader()
    # meta = dl.download("https://www.tiktok.com/@user/video/1234567890")
    # print(meta)
