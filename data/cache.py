from pathlib import Path
from typing import List, Optional, Tuple, Callable

import dask
from Bio import Entrez, SeqIO
import os

import json

from dask.delayed import Delayed

from common import InputFile, PG_EMBED_DIR
from data.entry import Kind

Entrez.email = "tmkluiters@tudelft.nl"


def search_assemblies(term: str) -> List[str]:
    with Entrez.esearch(term=term, db="nucleotide", retmax=90) as probe:
        query = Entrez.read(probe)
        count = query['Count']

    with Entrez.esearch(term=term, db="nucleotide", retmax=count) as result:
        entries = Entrez.read(result)

    return entries['IdList']


def download_assembly_for_query_as_tasks(
        term: str,
        target_directory: Path = None,
) -> List[Tuple[Tuple[str, str], Tuple[Callable, str, str]]]:
    if target_directory is None:
        target_directory = PG_EMBED_DIR / Path(term)
    indices = search_assemblies(term)
    os.makedirs(target_directory, exist_ok=True)

    return [(('nucleotide', index), (download_assembly_with_id, index, target_directory)) for index in indices]


def download_assembly_with_id(index: str, target_directory: Path) -> Optional[InputFile]:
    base = target_directory / Path(index)
    os.makedirs(base, exist_ok=True)
    location = base / Path(f"nucleotide.fasta")

    if location.exists() and location.stat().st_size > 0:
        return InputFile.from_file(location)

    with Entrez.efetch(
            db="nucleotide",
            rettype="fasta",
            retmode="text",
            id=index
    ) as read_handle:
        location.touch()
        location.write_text(read_handle.read())
        return InputFile.from_file(location)
