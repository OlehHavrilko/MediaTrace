import os
import cv2
import numpy as np
import pytesseract
import logging

logger = logging.getLogger(__name__)

class EditingAnalyzer:
    def __init__(self):
        pass

    def analyze_color_grading(self, frame_paths):
        """
        Analyzes dominant colors and contrast in frames.
        """
        results = []
        for path in frame_paths:
            img = cv2.imread(path)
            if img is None:
                continue
            
            # Dominant color (simple average)
            avg_color_per_row = np.average(img, axis=0)
            avg_color = np.average(avg_color_per_row, axis=0)
            
            # Contrast (std dev of grayscale)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            contrast = np.std(gray)
            
            results.append({
                'frame': os.path.basename(path),
                'avg_color_bgr': avg_color.tolist(),
                'contrast': float(contrast)
            })
        return results

    def detect_text(self, frame_paths):
        """
        Runs OCR on frames to find text overlays.
        """
        text_results = []
        for path in frame_paths:
            try:
                img = Image.open(path)
                text = pytesseract.image_to_string(img)
                if text.strip():
                    text_results.append({
                        'frame': os.path.basename(path),
                        'text': text.strip()
                    })
            except Exception as e:
                logger.warning(f"OCR failed for {path}: {e}")
        return text_results

    def analyze_motion(self, video_path):
        """
        Analyzes motion to detect slow-mo or fast-mo.
        (Conceptual implementation using optical flow)
        """
        cap = cv2.VideoCapture(video_path)
        ret, frame1 = cap.read()
        if not ret:
            return {}
        
        prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        motion_magnitudes = []
        
        frame_count = 0
        while cap.isOpened() and frame_count < 100: # Limit analysis to first 100 frames
            ret, frame2 = cap.read()
            if not ret:
                break
            next_img = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            flow = cv2.calcOpticalFlowFarneback(prvs, next_img, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            motion_magnitudes.append(np.mean(mag))
            prvs = next_img
            frame_count += 1
        
        cap.release()
        
        avg_motion = np.mean(motion_magnitudes) if motion_magnitudes else 0
        return {
            'avg_motion_magnitude': float(avg_motion),
            'motion_variability': float(np.std(motion_magnitudes)) if motion_magnitudes else 0
        }

    def analyze(self, video_path, frame_paths):
        """
        Full editing analysis.
        """
        color_data = self.analyze_color_grading(frame_paths[:5]) # Sample first 5
        text_data = self.detect_text(frame_paths[:5])
        motion_data = self.analyze_motion(video_path)
        
        return {
            'color_grading': color_data,
            'text_overlays': text_data,
            'motion_analysis': motion_data
        }

from PIL import Image
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
