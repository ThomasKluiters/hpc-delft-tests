from annotator.annotator import Annotator
from annotator.prodigal import ProdigalAnnotator


def annotator_for_algorithm(algorithm: str, **kwargs) -> Annotator:
    if algorithm == 'prodigal':
        return ProdigalAnnotator(**kwargs)
