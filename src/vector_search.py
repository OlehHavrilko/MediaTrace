import logging
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any

logger = logging.getLogger("MediaTrace.VectorSearch")

class VectorSearchEngine:
    """
    Handles semantic indexing and similarity search for video analyses.
    """
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata_store = {} # Maps index ID to metadata
        self.counter = 0

    def add_analysis(self, video_id: str, text: str):
        """Generates embedding and adds to index."""
        embedding = self.model.encode([text]).astype('float32')
        self.index.add(embedding)
        self.metadata_store[self.counter] = {"video_id": video_id, "text": text}
        self.counter += 1
        logger.info(f"Added analysis for video {video_id} to index.")

    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Finds k most similar analysis entries."""
        query_embedding = self.model.encode([query]).astype('float32')
        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for i in range(len(indices[0])):
            idx = indices[0][i]
            if idx != -1 and idx in self.metadata_store:
                results.append({
                    "metadata": self.metadata_store[idx],
                    "distance": float(distances[0][i])
                })
        return results
