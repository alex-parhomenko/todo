import sqlite3
from definitions import getFullFileName, SOURCE_DIR, initLogger
from packages.logger.logger import Logger


class TaskDb:
    '''Todo list - DB part processing    
    '''
    DB_NAME = 'todo.db'
    DB_TABLE_NAME = 'tasks'

    def __init__(self) -> None:
        '''Initialization.
            Create a table by default if it does exist
        '''
        self.__log = initLogger('task_db')

        database = getFullFileName(SOURCE_DIR, TaskDb.DB_NAME)
        self.conn = sqlite3.connect(database)

        self.__log.info('connection is opened')

        self.c = self.conn.cursor()
        self.__create_table()

    def __create_table(self):
        '''Create a new table if it does exists
        '''
        sql = f'CREATE TABLE IF NOT EXISTS {TaskDb.DB_TABLE_NAME}' \
            """(
            id INTEGER PRIMARY KEY,
            name TEXT NULL,
            prior INTEGER NOT NULL
        )"""
        self.c.execute(sql)

    def add(self, task):
        '''Add a new task
        '''
        self.c.executemany(
            f'INSERT INTO {TaskDb.DB_TABLE_NAME} (name, prior) VALUES (?, ?)',
            [(task.name, task.priority)]
        )
        self.conn.commit()
        self.__log.info(
            f'new task \'{task.name}\' with prioruty {task.priority}')

    def update_prior_by_id(self, task):
        '''Update a task priority by its ID
        '''
        self.c.execute(
            f'UPDATE {TaskDb.DB_TABLE_NAME} SET prior = ? WHERE id =?',
            (task.priority, task.id)
        )
        self.conn.commit()
        self.__log.info(f'task {task.id} has got priority {task.priority}')

    def fetchall(self):
        '''Get all rows
        '''
        self.c.execute(f'SELECT * FROM  {TaskDb.DB_TABLE_NAME}')
        rows = self.c.fetchall()
        return rows

    def find_by_id(self, id):
        '''Get a row by ID
        '''
        self.c.execute(
            f'SELECT * FROM  {TaskDb.DB_TABLE_NAME} where id="{id}"')
        row = self.c.fetchone()
        return row

    def find_by_name(self, name):
        '''Get a row by name
        '''
        self.c.execute(
            f'SELECT * FROM  {TaskDb.DB_TABLE_NAME} where name="{name}"')
        row = self.c.fetchone()
        return row

    def delete_by_id(self, id):
        '''Delete a row by ID
        '''
        self.c.execute(f'DELETE FROM  {TaskDb.DB_TABLE_NAME} where id="{id}"')
        self.conn.commit()
        self.__log.info(f'task {id} is removed')

    def __del__(self):
        '''Destroy - close connection
        '''
        self.conn.close()

        self.__log.info('connection is closed')
