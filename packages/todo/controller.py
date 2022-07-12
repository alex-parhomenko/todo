from logging import Logger
from definitions import initLogger
from packages.todo.action import Action
from packages.todo.task_service import TaskService


class Controller:
    def __init__(self, log: Logger = initLogger("control")) -> None:
        self.__log = log

    def start(self):
        """Start."""
        self.__log.info("The beginning.")

        service = TaskService(initLogger("service"))

        while True:
            try:
                self.__log.debug("Request action ...")
                action_id = service.requet_action_id()
                self.__log.debug(f"... choosen action: {action_id}")

                if action_id == Action.SHOW:
                    service.view()
                elif action_id == Action.ADD:
                    service.add()
                elif action_id == Action.CHANGE:
                    service.change()
                elif action_id == Action.DELETE:
                    service.remove()
                elif action_id == Action.EXPORT_CSV:
                    service.export()
                elif action_id == Action.EXIT or action_id is None:
                    break
            except Exception as er:
                self.__log.critical(f"... action failed: {er}")
                break
        self.__log.info("The End!")
