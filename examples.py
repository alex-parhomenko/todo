from sys import path

path.append("\\packages")


from packages.todo.controller import Controller


Controller().start()
