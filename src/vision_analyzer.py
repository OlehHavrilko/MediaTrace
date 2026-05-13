import os
import logging
import time
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
from object_detector import ObjectDetector

load_dotenv()
logger = logging.getLogger("MediaTrace.VisionAnalyzer")

class VisionAnalyzer:
    """
    Analyzes video frames using Google Gemini Vision capabilities 
    and YOLOv8 object detection.
    """
    def __init__(self, model_name: str = 'gemini-1.5-flash'):
        self.api_key = os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            logger.error("GOOGLE_API_KEY environment variable is not set.")
            raise ValueError("API key missing")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)
        self.detector = ObjectDetector()
        self.prompt = """
        Analyze this video frame. Provide a structured JSON output with the following keys:
        - 'characters': list of descriptions or names
        - 'setting': detailed description of environment
        - 'objects_found': list of objects found in the scene
        - 'visual_style': description of lighting, color, camera angle
        - 'source_hint': movie/series guess if recognizable
        - 'confidence': 0.0 to 1.0
        """

    def analyze_frame(self, frame_path: str, retries: int = 3) -> Dict[str, Any]:
        """
        Analyzes a single frame with Gemini and YOLO.
        """
        if not os.path.exists(frame_path):
            return {"error": "File not found"}

        # 1. Run YOLO detection
        yolo_results = self.detector.detect(frame_path)

        # 2. Run Gemini Vision
        for attempt in range(retries):
            try:
                img = Image.open(frame_path)
                response = self.model.generate_content([self.prompt, img])
                
                return {
                    "analysis": response.text, 
                    "yolo_detections": yolo_results,
                    "status": "success"
                }
            
            except Exception as e:
                logger.warning(f"Attempt {attempt+1} failed for {frame_path}: {e}")
                time.sleep(2 ** attempt)
                
        return {"error": "Analysis failed after retries"}

    def analyze_frames(self, frame_paths: List[str], timestamps: List[float]) -> List[Dict[str, Any]]:
        results = []
        for i, path in enumerate(frame_paths):
            logger.info(f"Analyzing frame {i+1}/{len(frame_paths)}: {os.path.basename(path)}")
            analysis = self.analyze_frame(path)
            results.append({
                'frame_path': path,
                'timestamp': timestamps[i] if i < len(timestamps) else None,
                **analysis
            })
        return results

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Simple CLI test
    import sys
    if len(sys.argv) > 1:
        analyzer = VisionAnalyzer()
        result = analyzer.analyze_frame(sys.argv[1])
        print(result)
