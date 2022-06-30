from packages.todo.action import Action
from packages.todo.task import Task


class TaskView:

    COLUMN_MAX_LEN = 17

    SEPARATOR_ROW = '-'
    SEPARATOR_COLUMN = '|'
    COLUMN_MAX_LEN = 17

    def requet_action_id(self) -> str:
        '''Request action ID.
        Returns:
            {str}: an action number
        '''
        res = input(f'''Choose an action for task processing:
            {Action.SHOW} - view
            {Action.ADD} - add
            {Action.CHANGE} - change
            {Action.DELETE} - delete
            {Action.EXPORT_CSV} - export csv
            {Action.EXPORT_JSON} - export json
            {Action.EXIT} - exit
            ''')
        return res

    def show_msg(self, msg) -> None:
        print(msg)

    def showTaskTable(self, tasks) -> None:
        '''Show tasks in table.
        '''
        header = []
        body = []
        # Output - tasks - body.
        for task in tasks:
            body.append(
                self.__strTask(
                    task[0],
                    task[1],
                    task[2],
                )
            )

        # Output - tasks - header.
        maxRecLen = max([len(x) for x in body])
        body.append(TaskView.SEPARATOR_ROW * maxRecLen)
        header.append(TaskView.SEPARATOR_ROW * maxRecLen)
        header.append(
            self.__strTask(
                Task.ID,
                Task.NAME,
                Task.PRIORITY,
            ))
        header.append(TaskView.SEPARATOR_ROW * maxRecLen)

        for rec in header + body:
            print(rec)

    def add(self) -> object:
        '''Get details for a new task
        '''
        name = self.__inputTaskName(
            f'Enter a name of the new task (\'{Action.EXIT_CONDITION}\' for exit): ',
            Action.EXIT_CONDITION
        )
        if name is None:
            return None
        prior = self.__inputPriority('Enter task priority (1-100): ')
        return Task(name=name, priority=prior)

    def __strTask(self, *columns):
        '''Format output item.
        '''
        output = TaskView.SEPARATOR_COLUMN
        for col in columns:
            output += ' {0: <{2}}{1}'.format(
                col,
                TaskView.SEPARATOR_COLUMN,
                TaskView.COLUMN_MAX_LEN
            )

        return output

    def input_task_name(self, exitCondition):
        return input(f'Enter a name of the new task (\'{exitCondition}\' for exit): ')

    def input_task_id(self, exitCondition):
        return input(f'Enter a task ID(\'{exitCondition}\' for exit): ')

    def input_priority(self):
        return input('Enter task priority (1-100): ')
