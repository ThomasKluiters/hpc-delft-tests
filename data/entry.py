import dataclasses
import os
from enum import Enum
from pathlib import Path
from typing import List, Iterable

from Bio import SeqIO

CACHE_ROOT = "~/.pgembed"


class Kind(Enum):
    NUCLEOTIDE = "NUCLEOTIDE"
    PROTEIN = "PROTEIN"
    EMBEDDINGS = "EMBEDDING"

    def lower(self):
        return self.name.lower()


class Source(Enum):
    SEQ_IO = "SEQ_IO"

    def lower(self):
        return self.name.lower()


@dataclasses.dataclass
class Entry:
    name: str
    kind: Kind
    source: Source

    def path(self) -> Path:
        return Path(CACHE_ROOT) / Path(self.source.lower()) / Path(self.kind.lower())


@dataclasses.dataclass
class BioSeqEntry(Entry):
    source = Source.SEQ_IO

    def store(self, seq: List[SeqIO.SeqRecord]) -> None:
        path = self.path()
        path.mkdir(parents=True, exist_ok=True)
        with open(path) as handle:
            SeqIO.write(seq, handle, 'fasta')

    def load(self) -> Iterable[SeqIO.SeqRecord]:
        with open(self.path()) as handle:
            return SeqIO.read(handle, 'fasta')
