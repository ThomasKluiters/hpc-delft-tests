from pathlib import Path

from Bio import Entrez, SeqIO
import os

import json
from data.entry import Kind

Entrez.email = "tmkluiters@tudelft.nl"


def download_assembly_for_query(
        term: str,
        target_directory: Path,
        batch_size=10,
):
    os.makedirs(target_directory, exist_ok=True)
    with Entrez.esearch(term=term, db="nucleotide", retmax=90) as probe:
        query = Entrez.read(probe)
        count = query['Count']

    with Entrez.esearch(term=term, db="nucleotide", retmax=count) as result:
        entries = Entrez.read(result)

    indices = entries['IdList']
    cache = target_directory / Path("info.json")

    info = {"CachedNucleotide": []}
    if cache.exists():
        with open(cache) as info_file:
            info = json.load(info_file)
            indices = [
                acc
                for acc
                in entries['IdList']
                if acc not in info.get('CachedNucleotide', [])
            ]

    for start_index in range(len(indices) // batch_size):
        offset = start_index * batch_size
        indices_to_fetch = indices[offset:min(int(count), offset + batch_size)]
        with Entrez.efetch(
                db="nucleotide",
                rettype="fasta",
                retmode="text",
                id=",".join(indices_to_fetch)
        ) as read_handle:
            for record in SeqIO.parse(read_handle, 'fasta'):
                base = target_directory / Path(record.id)
                os.makedirs(base, exist_ok=True)
                location = base / Path(f"nucleotide.fasta")
                with open(location, "w+") as write_handle:
                    SeqIO.write(record, write_handle, 'fasta')
            info['CachedNucleotide'] += indices_to_fetch
            with open(cache, "w+") as info_file:
                json.dump(info, info_file)


download_assembly_for_query('PRJNA555636', Path.home() / Path('.pgembed/PRJNA555636'))
