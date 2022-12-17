import dataclasses
from typing import List

from proteinbert import load_pretrained_model, PretrainingModelGenerator, InputEncoder
from proteinbert.conv_and_global_attention_model import get_model_with_hidden_layers_as_outputs

from core import Embedder


@dataclasses.dataclass
class ProteinBertEmbedder(Embedder):
    model_generator: PretrainingModelGenerator
    input_encoder: InputEncoder

    @classmethod
    def load_model(cls):
        (generator, encoder) = load_pretrained_model()
        return cls(generator, encoder)

    def compute_embeddings(self, sequences: List[str]):
        length = max(map(len, sequences)) + 2
        model = self.model_generator.create_model(length)
        model = get_model_with_hidden_layers_as_outputs(model)

        local_representations, _ = model.predict(self.input_encoder.encode_X(sequences, length))
        return local_representations.mean(axis=1)

    def compute_embedding(self, sequence: str):
        return self.compute_embeddings([sequence])


if __name__ == '__main__':
    embedder = ProteinBertEmbedder.load_model()
    sequence = "MDDADPEERNYDNMLKMLSDLNKDLEKLLEEMEKISVQATWMAYDMVVMRTNPTLAESMRRLEDAFVNCKEEMEKNWQELLHETKQRL"
    embedding = embedder.compute_embeddings([sequence] * 5)
    print(type(embedding))
