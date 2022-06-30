import csv
import json
import os
from definitions import SOURCE_DIR, initConfig, initLogger
from packages.logger.logger import Logger
from packages.todo.action import Action
from packages.todo.task import Task
from packages.todo.task_view import TaskView
from packages.todo.task_db import TaskDb


class TaskService:

    EXIT_CONDITION = 'e'

    ACTIONS = (
        Action.SHOW,
        Action.ADD,
        Action.CHANGE,
        Action.DELETE,
        Action.EXPORT_CSV,
        Action.EXPORT_JSON,
        Action.EXIT,
    )

    def __init__(self) -> None:
        self.__log = initLogger('service')
        # self.__log = Logger('service')

        self.__view = TaskView()
        self.__db = TaskDb()
        self._config = initConfig()

    def requet_action_id(self) -> int:
        '''Run action 'init' - initialization.
        Returns:
            {int}: an action number
        '''
        res = None
        while res is None:

            res = self.__view.requet_action_id()

            if not res.isdecimal() or int(res) not in TaskService.ACTIONS:
                self.__view.show_msg(f'incorrect action number {res}')
                print()
                res = None

        self.__log.debug(f'action: {res}')
        return int(res)

    def view(self) -> None:
        '''Run action 'view' tasks.
        '''
        todoList = self.__db.fetchall()

        if (len(todoList) == 0):
            self.__view.show_msg('No task is found')
        else:
            self.__view.showTaskTable(todoList)

    def add(self) -> None:
        '''Run action 'add' - add tasks to DB.
        '''
        self.__log.debug('add task')

        while True:
            name = self.__input_task_name(TaskService.EXIT_CONDITION)
            if name is None:
                break
            prior = self.__input_priority()
            self.__db.add(Task(name=name, priority=prior))
        self.view()

    def change(self):
        '''Update a task list.
        '''
        self.__log.debug('change task')

        while True:
            id = self.__input_task_id(TaskService.EXIT_CONDITION)
            if id is None:
                break
            row = self.__db.find_by_id(int(id))
            if row is None:
                self.__view.show_msg('Task is not found')
            else:
                prior = self.__input_priority()
                self.__db.update_prior_by_id(Task(id=id, priority=prior))
        self.view()

    def remove(self):
        '''Run action 'remove' a task.
        '''
        self.__log.debug('remove task')

        while True:
            id = self.__input_task_id(TaskService.EXIT_CONDITION)
            if id is None:
                break
            try:
                row = self.__db.find_by_id(int(id))
                if row is None:
                    self.__view.show_msg('Task is not found')
                else:
                    self.__db.delete_by_id(id)
            except ValueError:
                self.__log.critical('Wrong input')
        self.view()

    def export(self):
        '''Run action 'export' tasks to CSV.
        '''

        todoList = self.__db.fetchall()

        full_fname = os.path.join(
            SOURCE_DIR, self._config['export']['csv_file_name'])

        with open(full_fname, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow([Task.ID, Task.NAME, Task.PRIORITY])
            for row in todoList:
                spamwriter.writerow(row)
        self.__log.info(f'{len(list(todoList))} tasks are exported')

    def export_json(self):
        '''Run action 'export' tasks to json.
        '''

        todoList = self.__db.fetchall()

        def decode(t):
            if isinstance(t, Task):
                return t.__dict__
            else:
                raise Exception('wrong type')

        str_jasks = json.dumps(
            [Task(row[0], row[1], row[2],) for row in todoList],
            default=decode
        )

        full_fname = os.path.join(
            SOURCE_DIR, self._config['export']['json_file_name']
        )

        with open(full_fname, 'w') as outfile:
            outfile.write(str_jasks)

        self.__log.info(f'{len(list(todoList))} tasks are exported to json')

    def __input_task_name(self, exitCondition):
        '''Requests task name.
        Task name length should be in the range ({NAME_MIN_LEN}-{NAME_MAX_LEN})
        Parameters:
            exitCondition{str}: exit condition
        Returns:
            {str}: a task name. None if there is an exit condition
        '''
        while True:
            res = self.__view.input_task_name(exitCondition)
            if res == exitCondition:
                return None
            if len(res) >= Task.NAME_MIN_LEN and len(res) < Task.NAME_MAX_LEN:
                return res
            else:
                self.__view.show_msg(
                    f'Task name length should be in the range ({Task.NAME_MIN_LEN}-{Task.NAME_MAX_LEN})'
                )

    def __input_task_id(self, exitCondition):
        '''Requests task name.
        Task id  should be a number
        Parameters:
            exitCondition{str}: exit condition
        Returns:
            {str}: a task name. None if there is an exit condition
        '''
        while True:
            res = self.__view.input_task_id(exitCondition)
            if res == exitCondition:
                return None
            if res.isnumeric():
                return res
            else:
                self.__view.show_msg(
                    'Task ID should be a number'
                )

    def __input_priority(self):
        '''Requests task priority.
        Task priority should have in the expected range
        Returns:
            {int}: a priority number
        '''
        res = None
        while res is None:
            res = self.__view.input_priority()
            if not res.isdecimal():
                self.__view.show_msg(
                    'Task priority should be a number'
                )
                res = None
            else:
                num = int(res)
                if num < Task.PRIORITY_RANGE_MIN_BORDER \
                        or num > Task.PRIORITY_RANGE_MAX_BORDER:
                    self.__view.show_msg(
                        'Task priority should be in the range({}, {})'.format(
                            Task.PRIORITY_RANGE_MIN_BORDER,
                            Task.PRIORITY_RANGE_MAX_BORDER
                        )
                    )
                    res = None
        return num
