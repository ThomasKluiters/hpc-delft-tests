from pathlib import Path
from typing import List
import numpy as np
from Bio import SeqIO

from common import PG_EMBED_DIR, InputFile
from embedder.core import Embedder


class ProteinBertEmbedder(Embedder):
    def configure(self):
        pass

    def compute_embeddings(self, sequences: List[str]):
        from proteinbert.conv_and_global_attention_model import get_model_with_hidden_layers_as_outputs

        from proteinbert import load_pretrained_model
        model_directory = PG_EMBED_DIR / Path("models") / Path("protein-bert")
        model_directory.mkdir(parents=True, exist_ok=True)
        (generator, encoder) = load_pretrained_model(model_directory)

        tensors = []
        for i in range(len(sequences) // 10):
            batch = sequences[i * 10:min(len(sequences), (i + 1) * 10)]
            length = max(map(len, batch)) + 2
            model = generator.create_model(length)
            model = get_model_with_hidden_layers_as_outputs(model)

            local_representations, _ = model.predict(encoder.encode_X(batch, length))
            tensors.append(local_representations.mean(axis=1))
        return np.concatenate(tensors)

    def compute_embeddings_from_fasta_file(self, input_file: InputFile):
        output_file = input_file.context / Path("embeddings.data")
        if output_file.exists():
            return output_file
        with open(input_file.file) as handle:
            sequences = [str(seq.seq).replace('*', '') for seq in SeqIO.parse(handle, 'fasta')]
            embeddings = self.compute_embeddings(sequences)
            embeddings.tofile(output_file)
        return output_file

    def compute_embedding(self, sequence: str):
        return self.compute_embeddings([sequence])


