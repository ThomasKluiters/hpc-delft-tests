import os
import requests
from cleo.commands.command import Command
from cleo.helpers import argument, option


class EmbedCommand(Command):
    name = "embed"
    description = "Computes embeddings of a protein sequence"
    arguments = [
    ]
    options = [
        option(
            "file",
            "f",
            description="The location of the protein sequences stored in FASTA format",
            flag=False,
        )
    ]

    def handle(self) -> int:
        file_location = self.option("file")

        if not os.path.exists(file_location):
            self.line_error(f"The file '{file_location}' foes not exist!")
            return 2

