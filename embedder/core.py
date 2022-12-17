import numpy as np
from typing import List


class Embedder:
    def compute_embeddings(self, sequences: List[str]) -> np.ndarray:
        raise NotImplementedError

    def compute_embedding(self, sequence: str) -> np.ndarray:
        raise NotImplementedError
