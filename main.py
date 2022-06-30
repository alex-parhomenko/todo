###############
# Author: Alex
# Date: 2022/06/30
# Task: 16 - TODO
###############

from sys import path
from definitions import initLogger


path.append("\\packages")


from packages.todo.controller import Controller


def main():

    log = initLogger('main')
    log.debug('main started')
    Controller().start()


# Run as the main only
if __name__ == "__main__":
    main()
