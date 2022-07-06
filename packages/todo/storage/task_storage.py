from abc import ABC, abstractmethod
from packages.todo.storage.task_bo import TaskBo


class TaskStorageException(Exception):
    pass


class TaskStorage(ABC):
    """Todo list - Task storage."""

    @abstractmethod
    def add(self, task: TaskBo) -> None:
        """Add a new task."""
        pass

    @abstractmethod
    def update_by_id(self, task: TaskBo) -> None:
        """Update a task by its ID."""
        pass

    @abstractmethod
    def fetch_all(self) -> list[TaskBo]:
        """Get all rows."""
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> TaskBo:
        """Get a row by ID."""

    @abstractmethod
    def delete_by_id(self, id: int) -> None:
        """Delete a row by ID."""
        pass
