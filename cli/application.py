#!/usr/bin/env python
from embed_command import EmbedCommand

from cleo.application import Application

application = Application()
application.add(EmbedCommand())

if __name__ == "__main__":
    application.run()
