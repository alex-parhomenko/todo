from logging import Logger
from definitions import initLogger
from packages.todo.action import Action
from packages.todo.task_service import TaskService


class Controller:

    def __init__(self) -> None:
        self.__service = TaskService()
        self.__log = initLogger('control')

    def start(self):
        ''' Start.
        '''
        self.__log.info('The beginning.')

        while True:
            try:
                self.__log.debug('Request action ...')
                action_id = self.__service.requet_action_id()
                self.__log.debug(f'... choosen action: {action_id}')

                if action_id == Action.SHOW:
                    self.__service.view()
                elif action_id == Action.ADD:
                    self.__service.add()
                elif action_id == Action.CHANGE:
                    self.__service.change()
                elif action_id == Action.DELETE:
                    self.__service.remove()
                elif action_id == Action.EXPORT_CSV:
                    self.__service.export()
                elif action_id == Action.EXPORT_JSON:
                    self.__service.export_json()
                elif action_id == Action.EXIT:
                    self.__log.info('The End!')
                    break
            except Exception as er:
                self.__log.critical(f'... action failed: {er}')
