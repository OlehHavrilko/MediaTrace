import os
import cv2
import numpy as np
import logging
from typing import List, Dict, Any
from object_detector import ObjectDetector
import easyocr

logger = logging.getLogger("MediaTrace.VisionAnalyzer")

class VisionAnalyzer:
    """
    Lightweight analysis of video frames using YOLOv8, OCR, and color statistics.
    """
    def __init__(self):
        self.detector = ObjectDetector()
        self.reader = easyocr.Reader(['en'], gpu=False) # Keep CPU for portability
        logger.info("VisionAnalyzer initialized (Lightweight Mode).")

    def analyze_frame(self, frame_path: str) -> Dict[str, Any]:
        """
        Extracts visual metadata: objects, text, and color palette.
        """
        # 1. YOLO Objects
        yolo_results = self.detector.detect(frame_path)
        
        # 2. OCR Text
        text_results = self.reader.readtext(frame_path, detail=0)
        
        # 3. Color Stats (OpenCV)
        img = cv2.imread(frame_path)
        if img is not None:
            avg_color = np.mean(img, axis=(0, 1)).tolist()
        else:
            avg_color = [0, 0, 0]
            
        return {
            "objects_found": yolo_results,
            "text_found": text_results,
            "avg_color_bgr": avg_color,
            "status": "success"
        }

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
