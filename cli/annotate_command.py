from cleo.commands.command import Command
from cleo.helpers import option


class AnnotateCommand(Command):
    name = "annotate"
    description = "Annotate nucleotide sequences"
    arguments = [
    ]
    options = [
        option(
            "file",
            "f",
            description="""
            The location of the nucleotide sequences stored in FASTA format.
            
            If the location is a directory, fasta files will be recursively searched in the
            directory and annotated.
            """,
            flag=False,
        ),
        option(
            "algorithm",
            "a",
            description="""
            The algorithm to use for gene annotation.
            
            Available algorithms:
            - 'prodigal'
            
            If the algorithm is not installed, it will be installed,
            
            Defaults to 'prodigal'
            """,
            default='prodigal'
        )
    ]

    def handle(self) -> int:
        pass
