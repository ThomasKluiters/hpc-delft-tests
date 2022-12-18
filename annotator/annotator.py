import dataclasses
from pathlib import Path
from typing import Optional

from common import PG_EMBED_DIR, InputFile

ANNOTATORS_DIR = PG_EMBED_DIR / Path("annotators")


@dataclasses.dataclass
class Annotator:
    def name(self):
        raise NotImplementedError

    def version(self) -> Optional[str]:
        raise NotImplementedError

    def configure(self, force: bool = False):
        raise NotImplementedError

    def output_file_for_file(self, file: Path, target_directory: Path) -> InputFile:
        return InputFile(target_directory, target_directory / Path(f"{self.name()}.{file.name}.proteins"))

    def annotate_input_file(self, file: InputFile) -> InputFile:
        return self.annotate_fasta_file(file.file, file.context)

    def annotate_fasta_file(self, file: Path, target_directory: Path) -> InputFile:
        raise NotImplementedError
