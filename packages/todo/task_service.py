import csv
import os
from definitions import SOURCE_DIR, initConfig, initLogger
from packages.logger.logger import Logger
from packages.todo.action import Action
from config import Config

# fmt: off
from packages.todo.storage.task_storage \
    import TaskStorage, TaskStorageException
# fmt: on
from packages.todo.task import Task
from packages.todo.storage.task_bo import TaskBo
from packages.todo.task_view import TaskView
from packages.todo.storage.task_db import TaskDb
from packages.todo.storage.task_json import TaskJson


class TaskService:

    EXIT_CONDITION = "e"

    ACTIONS = (
        Action.SHOW,
        Action.ADD,
        Action.CHANGE,
        Action.DELETE,
        Action.EXPORT_CSV,
        Action.EXIT,
    )

    def __init__(self, log: Logger) -> None:

        # Logger object for services.
        self.__log = log

        self.__view = TaskView()

        config = initConfig()
        self.__csv_full_fname = self.__define_csv_full_fname(config)
        try:
            self.__db: TaskStorage = self.__define_storage(config)
        except TaskStorageException as er:
            self.__log.error("Storage init: " + str(er))
            print("Exit with an error. Look at logging for details")
            exit(1)

    def requet_action_id(self) -> int:
        """Run action 'init' - initialization.
        Returns:
            {int}: an action number
        """
        res = None
        while res is None:

            res = self.__view.requet_action_id(self.__get_storage_label())
            if not res.isdecimal() or int(res) not in TaskService.ACTIONS:
                self.__view.show_msg(f"incorrect action number {res}")
                print()
                res = None

        self.__log.debug(f"action: {res}")
        return int(res)

    def view(self) -> None:
        """Run action 'view' tasks."""
        todoList = self.__db.fetch_all()

        if len(todoList) == 0:
            self.__view.show_msg("No task is found")
        else:
            self.__view.showTaskTable(todoList)

    def add(self) -> None:
        """Run action 'add' - add tasks to storage."""
        self.__log.debug("add task")

        while True:
            name: str = self.__input_task_name(TaskService.EXIT_CONDITION)
            if name is None:
                break
            priority = self.__input_priority()
            self.__db.add(TaskBo(name=name, priority=priority))
            self.__view.show_msg("new task is added")
        self.view()

    def change(self) -> None:
        """Change task's priorities."""
        self.__log.debug("change task's priorities")

        while True:
            id: int = self.__input_task_id(TaskService.EXIT_CONDITION)
            if id is None:
                break
            task = self.__db.find_by_id(id)
            if task is None:
                self.__view.show_msg(f"task {id} is not found")
            else:
                task.priority = self.__input_priority()
                self.__db.update_by_id(task)
                self.__view.show_msg(f"task {id} is changed")
        self.view()

    def remove(self) -> None:
        """Run action 'remove' tasks."""
        self.__log.debug("remove tasks")

        while True:
            id: int = self.__input_task_id(TaskService.EXIT_CONDITION)
            if id is None:
                break
            try:
                task = self.__db.find_by_id(id)
                if task is None:
                    self.__view.show_msg("Task is not found")
                else:
                    self.__db.delete_by_id(id)
                    self.__view.show_msg(f"task {id} is removed")
            except ValueError as er:
                self.__log.error("Wrong input " + str(er))
        self.view()

    def export(self) -> None:
        """Run action 'export' tasks to CSV."""
        # Get tasks.
        t_list: list[TaskBo] = self.__db.fetch_all()

        # Write to CSV file
        with open(self.__csv_full_fname, "w", newline="") as csvfile:
            spamwriter = csv.writer(csvfile)
            # CSV - header.
            spamwriter.writerow([Task.ID, Task.NAME, Task.PRIORITY])
            # CSV - body
            for row in t_list:
                spamwriter.writerow([row.id, row.name, row.priority])

        # Display result.
        msg = f"{len(t_list)} tasks are exported"
        self.__view.show_msg(msg)
        self.__log.info(msg)

    def __input_task_name(self, exitCondition: str) -> str:
        """Requests task name.
        Task name length should be in the range ({NAME_MIN_LEN}-{NAME_MAX_LEN})
        Parameters:
            exitCondition{str}: exit condition
        Returns:
            {str}: a task name. None if there is an exit condition
        """
        while True:
            res = self.__view.input_task_name(exitCondition)
            if res == exitCondition:
                return None
            if len(res) >= Task.NAME_MIN_LEN and len(res) < Task.NAME_MAX_LEN:
                return res
            else:
                self.__view.show_msg(
                    "Task name length should be in the range "
                    f"({Task.NAME_MIN_LEN}-{Task.NAME_MAX_LEN})"
                )

    def __input_task_id(self, exitCondition) -> int:
        """Requests task name.
        Task id  should be a number
        Parameters:
            exitCondition{str}: exit condition
        Returns:
            {str}: a task name. None if there is an exit condition
        """
        while True:
            res = self.__view.input_task_id(exitCondition)
            if res == exitCondition:
                return None
            if res.isnumeric():
                return int(res)
            else:
                self.__view.show_msg("Task ID should be a number")

    def __input_priority(self) -> int:
        """Requests task priority.
        Task priority should have in the expected range
        Returns:
            {int}: a priority number
        """
        res = None
        while res is None:
            res = self.__view.input_priority()
            if not res.isdecimal():
                self.__view.show_msg("Task priority should be a number")
                res = None
            else:
                num = int(res)
                if (
                    num < Task.PRIORITY_RANGE_MIN_BORDER
                    or num > Task.PRIORITY_RANGE_MAX_BORDER
                ):
                    self.__view.show_msg(
                        "Task priority should be in the range({}, {})".format(
                            Task.PRIORITY_RANGE_MIN_BORDER,
                            Task.PRIORITY_RANGE_MAX_BORDER,
                        )
                    )
                    res = None
        return num

    def __define_csv_full_fname(self, config) -> str:

        return os.path.join(
            SOURCE_DIR, config[Config.SEC_EXPORT][Config.ATTR_CSV_FILE_NAME]
        )

    def __define_storage(self, config) -> TaskStorage:
        """Storage initialization."""
        id_names = {1: "DB", 2: "JSON"}

        storage_type = config[Config.SEC_DEFAULT][Config.ATTR_STORAGE_TYPE]
        res: int = None
        while True:
            if storage_type == Config.VAL_CUSTOM:
                res = self.__view.requet_storage_id(
                    id_names, TaskService.EXIT_CONDITION
                )
            elif storage_type == Config.SEC_WEB_STORAGE:
                res = 2
            elif storage_type == Config.SEC_DB_STORAGE:
                res = 1
            else:
                raise Exception("wrong config: storage_type=" + storage_type)

            if res == 1:
                db_config = config[Config.SEC_DB_STORAGE]
                return TaskDb(
                    initLogger("_____db"),
                    db_config[Config.ATTR_DB_FILE_NAME],
                    db_config[Config.ATTR_DB_NAME],
                )
            elif res == 2:
                web_config = config[Config.SEC_WEB_STORAGE]
                return TaskJson(
                    initLogger("___json"),
                    web_config[Config.ATTR_URL],
                    web_config[Config.ATTR_ROOT_NAME],
                )
            elif res == TaskService.EXIT_CONDITION:
                exit()
            else:
                self.__view.show_msg("incorrect number entered\n")

    def __get_storage_label(self) -> str:
        return "DB" if isinstance(self.__db, TaskDb) else "JSON"
