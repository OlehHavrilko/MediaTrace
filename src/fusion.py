import numpy as np
import logging
from typing import Dict, Any, List

logger = logging.getLogger("MediaTrace.FusionEngine")

class FusionEngine:
    """
    Aggregates multimodal data into a unified semantic signature (master vector).
    """
    def __init__(self, target_dim: int = 1024):
        self.target_dim = target_dim

    def fuse(self, 
             video_embedding: List[float], 
             yolo_stats: List[Dict[str, Any]], 
             audio_metadata: Dict[str, Any]) -> np.ndarray:
        """
        Concatenates heterogeneous features into a normalized master vector.
        """
        logger.info("Fusing multimodal features...")
        
        # 1. Normalize video embedding (already from CLIP, usually 512d)
        v_emb = np.array(video_embedding)
        
        # 2. Extract and normalize object features (e.g., density and object count)
        obj_count = len(yolo_stats)
        # Simplify object labels to a small vector (frequency of top objects)
        obj_vec = np.zeros(64) # Reduced space for object stats
        obj_vec[0] = obj_count / 20.0 # Normalized count
        
        # 3. Audio feature summary
        audio_vec = np.zeros(64)
        if audio_metadata.get('music_matches'):
            audio_vec[0] = 1.0 # Flag for music presence
            
        # Concatenate and pad to target_dim
        master_vector = np.concatenate([v_emb, obj_vec, audio_vec])
        
        # Pad with zeros to reach target_dim
        if len(master_vector) < self.target_dim:
            padding = np.zeros(self.target_dim - len(master_vector))
            master_vector = np.concatenate([master_vector, padding])
        else:
            master_vector = master_vector[:self.target_dim]
            
        return master_vector.astype('float32')
