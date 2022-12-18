#!/usr/bin/env python
from cli.annotate_command import AnnotateCommand
from embed_command import EmbedCommand

from cleo.application import Application

application = Application()
application.add(EmbedCommand())
application.add(AnnotateCommand())

if __name__ == "__main__":
    application.run()
