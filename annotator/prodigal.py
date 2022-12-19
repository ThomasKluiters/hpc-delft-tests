import dataclasses
import os
import re
import subprocess
import tempfile
from pathlib import Path
import shutil
from typing import Optional, List

from annotator.annotator import Annotator, ANNOTATORS_DIR
from common import InputFile

PRODIGAL_REPO = "git@github.com:hyattpd/Prodigal.git"
PRODIGAL_VERSION_REGEX = r"Prodigal V([0-9.]+): ([a-zA-Z]+), ([0-9]+)"
PRODIGAL_DIR = ANNOTATORS_DIR / Path("prodigal")
PRODIGAL_EXECUTABLES = [
    "prodigal",
    PRODIGAL_DIR / Path("prodigal")
]


def check_prodigal_version(executable: str) -> Optional[str]:
    try:
        version_string = subprocess.check_output(
            [executable, "-v"],
            stderr=subprocess.STDOUT
        ).decode('utf-8').strip()
        match = re.search(PRODIGAL_VERSION_REGEX, version_string)
        if match:
            return match.group(0)
    except subprocess.CalledProcessError as e:
        return None
    except FileNotFoundError as e:
        return None


@dataclasses.dataclass
class ProdigalAnnotator(Annotator):
    prodigal_executables: List[str] = dataclasses.field(default_factory=lambda: PRODIGAL_EXECUTABLES)
    prodigal_extra_args: List[str] = dataclasses.field(default_factory=list)
    prodigal_training_file: Optional[str] = None

    def name(self):
        return "prodigal"

    def find_executable(self):
        for executable in self.prodigal_executables:
            if shutil.which(executable) and check_prodigal_version(executable):
                return executable
        return None

    def version(self):
        return check_prodigal_version(self.find_executable())

    def configure(self, force: bool = False):
        if not force and self.version() is not None:
            return
        install_directory = PRODIGAL_DIR
        install_directory.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory() as tmp:
            if os.system(f"git clone {PRODIGAL_REPO} {tmp}") != 0:
                return None
            if os.system(f"make install INSTALLDIR={PRODIGAL_DIR} -C {tmp}") != 0:
                return None

    def annotate_fasta_file(self, input_file: Path, target_directory: Path) -> InputFile:
        output_file = self.output_file_for_file(target_directory)
        if output_file.file.exists():
            return output_file
        command = [
            self.find_executable(),
            "-i", input_file,
            "-a", output_file.file
        ]
        if self.prodigal_training_file:
            command += ["-t", self.prodigal_training_file]
        command += self.prodigal_extra_args
        if subprocess.call(command) != 0:
            raise Exception("")
        return output_file
