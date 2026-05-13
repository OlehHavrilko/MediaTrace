import os
import logging
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

load_dotenv()
logger = logging.getLogger(__name__)

class VisionAnalyzer:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            logger.warning("GOOGLE_API_KEY not found. VisionAnalyzer will run in MOCK mode.")
            self.model = None

    def analyze_frame(self, frame_path):
        """
        Analyzes a single frame using Gemini Vision.
        """
        if not self.model:
            return self._mock_analysis(frame_path)

        try:
            img = Image.open(frame_path)
            prompt = """
            Analyze this frame from a TikTok video. 
            Identify:
            1. Characters (if any)
            2. Setting/Environment
            3. Objects/Props
            4. Visual style (color, lighting)
            5. Potential source (movie/TV show name if recognizable)
            
            Return the analysis in a structured format.
            """
            response = self.model.generate_content([prompt, img])
            return response.text
        except Exception as e:
            logger.error(f"Error analyzing frame {frame_path}: {e}")
            return f"Error: {e}"

    def analyze_scenes(self, frame_paths, scene_timestamps):
        """
        Analyzes representative frames for each scene.
        """
        results = []
        
        for i, frame_path in enumerate(frame_paths):
            logger.info(f"Analyzing scene frame: {frame_path}")
            analysis = self.analyze_frame(frame_path)
            results.append({
                'frame_path': frame_path,
                'timestamp': scene_timestamps[i] if i < len(scene_timestamps) else None,
                'analysis': analysis
            })
        
        return results

    def _mock_analysis(self, frame_path):
        return f"MOCK ANALYSIS for {os.path.basename(frame_path)}: A scene with characters and objects."

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
