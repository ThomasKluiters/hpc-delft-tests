import numpy as np
from typing import List

from common import InputFile


class Embedder:
    def configure(self):
        raise NotImplementedError

    def compute_embeddings(self, sequences: List[str]) -> np.ndarray:
        raise NotImplementedError

    def compute_embedding(self, sequence: str) -> np.ndarray:
        raise NotImplementedError

    def compute_embeddings_from_fasta_file(self, input_file: InputFile) -> InputFile:
        pass
