from typing import List
from packages.todo.action import Action
from packages.todo.task import Task
from packages.todo.storage.task_bo import TaskBo


class TaskView:

    SEPARATOR_ROW = "-"
    SEPARATOR_COLUMN = "|"
    COLUMN_MAX_LEN = 17

    def requet_action_id(self, sub_title: str = "") -> str:
        """Request action ID.
        Returns:
            {str}: an action number
        """
        res = input(
            f"""Choose an action for task processing ({sub_title}):
            {Action.SHOW} - view
            {Action.ADD} - add
            {Action.CHANGE} - change
            {Action.DELETE} - delete
            {Action.EXPORT_CSV} - export csv
            {Action.EXIT} - exit
            """
        )
        return res

    def requet_storage_id(self, id_names: tuple, exit_condition="") -> int:
        """Request storage ID.
        Returns:
            {str}: an storage number
        """
        lst = [f"{id} - {id_names[id]}" for id in id_names]
        res = input(
            # fmt: off
            "Choose a storage to be used "
            f"('{exit_condition}' for exit) {lst}: "
            # fmt: on
        )
        if exit_condition == res:
            return res
        elif res.isdecimal():
            return int(res)
        else:
            return None

    def show_msg(self, msg) -> None:
        print(msg)

    def showTaskTable(self, tasks: List[TaskBo]) -> None:
        """Show tasks in table."""
        header = []
        body = []
        # Output - tasks - body.
        for task in tasks:
            body.append(
                # TODO ...
                self.__strTask(
                    task.id,
                    task.name,
                    task.priority,
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
            )
        )
        header.append(TaskView.SEPARATOR_ROW * maxRecLen)

        for rec in header + body:
            print(rec)

    def add(self, exit_condition="") -> object:
        """Get details for a new task."""
        name = self.__inputTaskName(
            f"Enter a name of the new task ('{exit_condition}' for exit): ",
            exit_condition,
        )
        if name is None:
            return None
        priority = self.__inputPriority("Enter task priority (1-100): ")
        return Task(name=name, priority=priority)

    def __strTask(self, *columns):
        """Format output item."""
        output = TaskView.SEPARATOR_COLUMN
        for col in columns:
            output += " {0: <{2}}{1}".format(
                col, TaskView.SEPARATOR_COLUMN, TaskView.COLUMN_MAX_LEN
            )

        return output

    def input_task_name(self, exitCondition):
        # fmt: off
        return input(
            "Enter a name of the new task " f"('{exitCondition}' for exit): "
        )
        # fmt: on

    def input_task_id(self, exitCondition):
        return input(f"Enter a task ID('{exitCondition}' for exit): ")

    def input_priority(self):
        return input("Enter task priority (1-100): ")
