import torch
import clip
from PIL import Image
import logging
from typing import List, Dict, Any

logger = logging.getLogger("MediaTrace.EmbeddingEngine")

class VideoEmbeddingEngine:
    """
    Generates semantic embeddings for frames using CLIP.
    """
    def __init__(self, device: str = "cuda" if torch.cuda.is_available() else "cpu"):
        self.device = device
        logger.info(f"Loading CLIP model on {self.device}...")
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)

    def get_frame_embedding(self, frame_path: str) -> List[float]:
        """Generates embedding for a single frame."""
        image = self.preprocess(Image.open(frame_path)).unsqueeze(0).to(self.device)
        with torch.no_grad():
            embedding = self.model.encode_image(image)
            return embedding.cpu().numpy().flatten().tolist()

    def get_video_embedding(self, frame_paths: List[str]) -> List[float]:
        """Averages embeddings across frames for a video-level representation."""
        embeddings = [self.get_frame_embedding(p) for p in frame_paths]
        if not embeddings:
            return []
        return np.mean(embeddings, axis=0).tolist()
import numpy as np
