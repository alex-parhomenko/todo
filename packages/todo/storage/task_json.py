# fmt: off
from packages.todo.storage.task_storage \
    import TaskStorage, TaskStorageException
from packages.todo.task_bo \
    import TaskBo, TaskDecoder, TaskEncoder
# fmt: on
import json
from packages.logger.logger import Logger
import requests


class TaskJson(TaskStorage):
    """Todo list - web storage in json"""

    __HEADER_CONTENT = {"Content-Type": "application/json"}

    def __init__(self, log, url, json_root) -> None:
        """Initialization."""
        self.__log: Logger = log

        self.__resource_url = self.__defineResourceUrl(url, json_root)

    def add(self, task: TaskBo) -> None:
        """Add a new task."""

        msg = "new task "
        response = None
        try:
            task.id = None
            response = requests.post(
                self.__resource_url,
                headers=TaskJson.__HEADER_CONTENT,
                data=json.dumps(task, cls=TaskEncoder),
            )
        except requests.RequestException as er:
            self.__log.error(msg + str(er))
        else:
            msg = self.__getReponseMsg(msg, response)
            if response.status_code == requests.codes.created:
                self.__log.debug(msg)
            else:
                self.__log.error(msg)

    def update_by_id(self, task: TaskBo) -> None:
        """Update a task by its ID"""

        msg = f"Update task by id {task.id} "
        response = None
        try:
            response = requests.put(
                f"{self.__resource_url}/{task.id}",
                headers=TaskJson.__HEADER_CONTENT,
                data=json.dumps(task, cls=TaskEncoder),
            )
        except requests.RequestException as er:
            self.__log.error(msg + str(er))
        else:
            msg = self.__getReponseMsg(msg, response)
            if response.status_code == requests.codes.ok:
                self.__log.info(msg)
            else:
                self.__log.error(msg)

        self.__log.info(f"task {task.id} has got priority {task.priority}")

    def fetch_all(self) -> list[TaskBo]:
        """Get all rows"""

        msg = "all tasks "
        res: list[TaskBo] = []
        response = None
        try:
            response = requests.get(
                self.__resource_url, headers=TaskJson.__HEADER_CONTENT
            )
        except requests.RequestException as er:
            self.__log.error(msg + str(er))
        else:
            msg = self.__getReponseMsg(msg, response)
            if response.status_code == requests.codes.ok:
                res = json.loads(response.text, cls=TaskDecoder)
            else:
                res = []
                self.__log.error(msg)
        return res

    def find_by_id(self, id: int) -> TaskBo:
        """Get a row by ID"""

        res: TaskBo = None
        msg = f"find task {id}"
        response = None
        try:
            # fmt: off
            response = requests.get(
                f"{self.__resource_url}/{id}",
                headers=TaskJson.__HEADER_CONTENT
            )
            # fmt: on
        except requests.RequestException as er:
            self.__log.error(msg + str(er))
        else:
            msg = self.__getReponseMsg(msg, response)
            if response.status_code == requests.codes.ok:
                self.__log.debug(msg)
                res = json.loads(response.text, cls=TaskDecoder)
            else:
                self.__log.error(msg)
        return res

    def delete_by_id(self, id: int) -> None:
        """Delete a task by ID"""
        msg = f"delete task {id}"
        try:
            response = requests.delete(
                f"{self.__resource_url}/{id}",
                headers=TaskJson.__HEADER_CONTENT,
            )
        except requests.RequestException as er:
            self.__log.error(msg + str(er))
        else:
            if response.status_code == requests.codes.ok:
                self.__log.info(msg + " - DONE")
            else:
                msg = self.__getReponseMsg(msg, response)
                self.__log.error(msg)

    def __getReponseMsg(self, subj: str, resp):
        # fmt: off
        return f"{subj} - response - code: " \
            f"{resp.status_code} - text: {resp.text}"
        # fmt: on

    def __defineResourceUrl(self, url, json_root) -> str:
        """Generate and validated a resource URL."""
        # Resource URL
        resource_url = f"{url}/{json_root}"

        # Check by a simple request
        msg = "Check resource_url: " + resource_url
        try:
            response = requests.get(resource_url)
        except requests.exceptions.InvalidURL as er:
            raise TaskStorageException(msg + " InvalidURL: " + str(er))
        except requests.exceptions.ConnectionError as er:
            raise TaskStorageException(msg + " ConnectionError: " + str(er))
        except requests.exceptions.RequestException as er:
            raise TaskStorageException(msg + " RequestException: " + str(er))
        else:
            msg = f'JSON web-server resource "{resource_url}"'
            if response.status_code == requests.codes.not_found:
                msg += " is NOT found"
                raise TaskStorageException(msg)
            elif response.status_code == requests.codes.ok:
                self.__log.debug(msg + " is found")
            else:
                msg += f" - wrong response code: {response.status_code}"
                raise TaskStorageException(msg)

        return resource_url
