import logging
import faiss
import numpy as np
from typing import List, Dict, Any
from src.embedding_engine import VideoEmbeddingEngine
from src.fusion import FusionEngine

logger = logging.getLogger("MediaTrace.VectorSearch")

class VectorSearchEngine:
    """
    Handles semantic indexing and similarity search using Fused Multimodal Signatures.
    """
    def __init__(self, dimension: int = 1024):
        self.dimension = dimension 
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata_store = {}
        self.counter = 0
        self.embedding_engine = VideoEmbeddingEngine()
        self.fusion_engine = FusionEngine(target_dim=self.dimension)

    def add_video_analysis(self, video_id: str, frame_paths: List[str], 
                           yolo_stats: List[Dict[str, Any]], audio_data: Dict[str, Any], text_summary: str):
        """Generates fused signature and adds to index."""
        # 1. Get video-level CLIP embedding
        video_emb = self.embedding_engine.get_video_embedding(frame_paths)
        
        # 2. Fuse with other modalities
        master_vector = self.fusion_engine.fuse(video_emb, yolo_stats, audio_data)
        
        # 3. Index
        self.index.add(np.array([master_vector]))
        
        self.metadata_store[self.counter] = {"video_id": video_id, "summary": text_summary}
        self.counter += 1
        logger.info(f"Indexed video {video_id} with multimodal signature.")

    def search(self, query_vector: np.ndarray, k: int = 5) -> List[Dict[str, Any]]:
        distances, indices = self.index.search(query_vector, k)
        results = []
        for i in range(len(indices[0])):
            idx = indices[0][i]
            if idx != -1 and idx in self.metadata_store:
                results.append({
                    "metadata": self.metadata_store[idx],
                    "distance": float(distances[0][i])
                })
        return results
