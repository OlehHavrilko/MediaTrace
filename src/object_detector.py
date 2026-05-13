import logging
from ultralytics import YOLO
from typing import List, Dict, Any

logger = logging.getLogger("MediaTrace.ObjectDetector")

class ObjectDetector:
    """
    Detects objects in video frames using YOLOv8.
    """
    def __init__(self, model_name: str = 'yolov8n.pt'):
        logger.info(f"Loading YOLO model: {model_name}")
        self.model = YOLO(model_name)

    def detect(self, frame_path: str) -> List[Dict[str, Any]]:
        """
        Runs detection on a single image.
        """
        try:
            results = self.model(frame_path, verbose=False)
            detections = []
            for r in results:
                for box in r.boxes:
                    cls = int(box.cls[0])
                    detections.append({
                        "label": self.model.names[cls],
                        "confidence": float(box.conf[0]),
                        "bbox": box.xyxy[0].tolist()
                    })
            return detections
        except Exception as e:
            logger.error(f"Detection failed: {e}")
            return []
