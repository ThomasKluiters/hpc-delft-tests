import dataclasses
from pathlib import Path
from typing import List

from Bio import SeqIO
from proteinbert import load_pretrained_model, PretrainingModelGenerator, InputEncoder
from proteinbert.conv_and_global_attention_model import get_model_with_hidden_layers_as_outputs

from common import PG_EMBED_DIR, InputFile
from embedder.core import Embedder


@dataclasses.dataclass
class ProteinBertEmbedder(Embedder):
    model_generator: PretrainingModelGenerator
    input_encoder: InputEncoder

    @classmethod
    def load_model(cls):
        model_directory = PG_EMBED_DIR / Path("models") / Path("protein-bert")
        model_directory.mkdir(parents=True, exist_ok=True)
        (generator, encoder) = load_pretrained_model(model_directory)
        return cls(generator, encoder)

    def configure(self):
        pass

    def compute_embeddings(self, sequences: List[str]):
        length = max(map(len, sequences)) + 2
        model = self.model_generator.create_model(length)
        model = get_model_with_hidden_layers_as_outputs(model)

        local_representations, _ = model.predict(self.input_encoder.encode_X(sequences, length))
        return local_representations.mean(axis=1)

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


if __name__ == '__main__':
    embedder = ProteinBertEmbedder.load_model()
    sequence = "MDDADPEERNYDNMLKMLSDLNKDLEKLLEEMEKISVQATWMAYDMVVMRTNPTLAESMRRLEDAFVNCKEEMEKNWQELLHETKQRL"
    embedding = embedder.compute_embeddings([sequence] * 512)
    print(embedding)
