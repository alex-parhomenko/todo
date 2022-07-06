from packages.todo.storage.task_storage import TaskStorage
from packages.todo.storage.task_bo import TaskBo
import sqlite3
from definitions import getFullFileName, SOURCE_DIR
from packages.logger.logger import Logger


class TaskDb(TaskStorage):
    """Todo list - DB part processing."""

    def __init__(self, log: Logger, db_name: str, db_table_name: str) -> None:
        """Initialization."""
        self.__log: Logger = log

        self.__conn = sqlite3.connect(getFullFileName(SOURCE_DIR, db_name))
        self.c = self.__conn.cursor()
        self.__db_table_name = self.__create_table(db_table_name)

        self.__log.info("connection is opened")

    def __create_table(self, db_table_name: str) -> str:
        """Create a new table if it does exists"""
        sql = (
            f"CREATE TABLE IF NOT EXISTS {db_table_name}"
            """(
            id INTEGER PRIMARY KEY,
            name TEXT NULL,
            priority INTEGER NOT NULL
        )"""
        )
        self.c.execute(sql)
        return db_table_name

    def add(self, task: TaskBo) -> None:
        """Add a new task"""
        self.c.executemany(
            # fmt: off
            f"INSERT INTO {self.__db_table_name} "
            "(name, priority) VALUES (?, ?)",
            [(task.name, task.priority)],
            # fmt: on
        )
        self.__conn.commit()
        # fmt: off
        self.__log.info(
            f"new task '{task.name}' with priority {task.priority}"
        )
        # fmt: on

    def update_by_id(self, task: TaskBo) -> None:
        """Update a task priority by its ID"""
        self.c.execute(
            # fmt: off
            f"UPDATE {self.__db_table_name} "
            "SET name = ?, priority = ? WHERE id =?",
            # fmt: off
            (task.name, task.priority, task.id),
        )
        self.__conn.commit()
        self.__log.info(f"task {task.id} has got priority {task.priority}")

    def fetch_all(self) -> list[TaskBo]:
        """Get all rows"""
        self.c.execute(f"SELECT * FROM  {self.__db_table_name}")
        rows = self.c.fetchall()
        return list(map(lambda row: TaskBo(*row), rows))

    def find_by_id(self, id: int) -> TaskBo:
        """Get a row by ID"""
        # fmt: off
        self.c.execute(
            f'SELECT * FROM  {self.__db_table_name} where id="{id}"'
        )
        # fmt: on
        row = self.c.fetchone()
        return row if row is None else TaskBo(*row)

    def delete_by_id(self, id: int) -> None:
        """Delete a row by ID."""
        self.c.execute(f'DELETE FROM  {self.__db_table_name} where id="{id}"')
        self.__conn.commit()
        self.__log.info(f"task {id} is removed")

    def __del__(self) -> None:
        """Destroy - close connection."""
        self.__conn.close()

        self.__log.info("connection is closed")
