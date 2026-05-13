import logging
from transformers import AutoModelForVision2Seq, AutoProcessor
from PIL import Image
import torch
from typing import Dict, Any

logger = logging.getLogger("MediaTrace.VisionAnalyzer")

class LocalVisionModel:
    """
    Local Vision-to-Text model implementation (Moondream2).
    """
    def __init__(self, model_id: str = "vikhyatk/moondream2"):
        logger.info(f"Loading local model: {model_id}...")
        self.model = AutoModelForVision2Seq.from_pretrained(
            model_id, trust_remote_code=True, torch_dtype=torch.float32
        )
        self.processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
        logger.info("Local model loaded successfully.")

    def caption(self, image_path: str) -> str:
        image = Image.open(image_path)
        enc_image = self.model.encode_image(image)
        return self.model.answer_question(enc_image, "Describe this scene in detail, including characters, setting, objects, and visual style.", self.processor)

class VisionAnalyzer:
    """
    Analyzes video frames using local Moondream2 model and YOLOv8.
    """
    def __init__(self):
        self.model = LocalVisionModel()
        from object_detector import ObjectDetector
        self.detector = ObjectDetector()
        logger.info("VisionAnalyzer initialized with local models.")

    def analyze_frame(self, frame_path: str) -> Dict[str, Any]:
        """
        Analyzes a single frame with local Vision model and YOLO.
        """
        # 1. Run YOLO detection
        yolo_results = self.detector.detect(frame_path)

        # 2. Run Local Vision Description
        analysis_text = self.model.caption(frame_path)
        
        return {
            "analysis": analysis_text, 
            "yolo_detections": yolo_results,
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
