import dataclasses
from pathlib import Path

PG_EMBED_DIR = Path.home() / Path("pgembed")


@dataclasses.dataclass(unsafe_hash=True, frozen=True)
class InputFile:
    context: Path
    file: Path

    def rewrite_target(self, extension: str) -> 'InputFile':
        return InputFile(self.context, self.context / Path(extension))

    @classmethod
    def from_file(cls, file: Path):
        return cls(file.parents[0], file)

    def key(self):
        return f"{self.file.parents[0].name}"

    def __str__(self) -> str:
        return str(self.file)
