###############
# Author: Alex
# Date: 2022/06/30
# Task: TODO
###############

from packages.todo.controller import Controller
from sys import path
from definitions import initLogger


path.append("\\packages")


def main(log):

    log.debug("main started")
    Controller(initLogger("control")).start()


# Run as the main only
if __name__ == "__main__":
    main(initLogger("main"))
