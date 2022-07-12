import unittest
from unittest.mock import patch

import requests
from packages.todo.storage.task_bo import TaskBo, TaskEncoder
from packages.todo.storage.task_json import TaskJson
import json
from packages.logger.logger import Logger


class TestTaskJson(unittest.TestCase):
    """Test web storage in json."""

    @classmethod
    def setUpClass(cls):
        print("setUpClass")

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        with patch("packages.todo.storage.task_json.requests.get") as mocked:
            mocked.return_value.status_code = 200
            mocked.return_value.text = "ok"

            self.__taskJson = TaskJson(Logger("test"), "url", "root")

    def tearDown(self):
        del self.__taskJson

    def test_fetch_all(self):

        ID = 123
        NAME = "abc"
        PRIORITY = 0

        with patch("packages.todo.storage.task_json.requests.get") as mocked:
            mocked.return_value.status_code = requests.codes.ok
            mocked.return_value.text = json.dumps(
                [TaskBo(ID, NAME, PRIORITY)], cls=TaskEncoder
            )

            res = self.__taskJson.fetch_all()

            self.assertIsNotNone(res)
            self.assertEqual(len(res), 1)

            res_task: TaskBo = res[0]
            self.assertIsNotNone(res_task)
            self.assertEqual(res_task.id, ID)
            self.assertEqual(res_task.name, NAME)
            self.assertEqual(res_task.priority, PRIORITY)

    def test_fetch_all_failed(self):

        with patch("packages.todo.storage.task_json.requests.get") as mck:
            mck.return_value.status_code = requests.codes.not_found
            mck.return_value.text = json.dumps([], cls=TaskEncoder)

            res = self.__taskJson.fetch_all()
            self.assertIsNotNone(res)
            self.assertEqual(len(res), 0)

    def test_update_by_id_ok(self):
        with patch("packages.todo.storage.task_json.requests.put") as mck:
            mck.return_value.status_code = requests.codes.ok
            mck.return_value.text = "ok"

            res = self.__taskJson.update_by_id(TaskBo(123, "abc", 0))
            self.assertEquals(res, True)

    def test_update_by_id_failed(self):
        with patch("packages.todo.storage.task_json.requests.put") as mck:
            mck.return_value.status_code = requests.codes.not_found
            mck.return_value.text = "not_found"

            res = self.__taskJson.update_by_id(TaskBo(123, "abc", 0))
            self.assertEquals(res, False)

    def test_add_ok(self):
        with patch("packages.todo.storage.task_json.requests.post") as mck:
            mck.return_value.status_code = requests.codes.created
            mck.return_value.text = "created"

            res = self.__taskJson.add(TaskBo(name="abc", priority=0))
            self.assertEquals(res, True)

    def test_add_failed(self):
        with patch("packages.todo.storage.task_json.requests.post") as mck:
            mck.return_value.status_code = requests.codes.not_found
            mck.return_value.text = "not_found"

            res = self.__taskJson.add(TaskBo(name="abc", priority=0))
            self.assertEquals(res, False)

    def test_delete_by_id_ok(self):
        with patch("packages.todo.storage.task_json.requests.delete") as mck:
            mck.return_value.status_code = requests.codes.ok
            mck.return_value.text = "ok"

            res = self.__taskJson.delete_by_id(TaskBo(name="abc", priority=0))
            self.assertEquals(res, True)

    def test_delete_by_id_failed(self):
        with patch("packages.todo.storage.task_json.requests.delete") as mck:
            mck.return_value.status_code = requests.codes.not_found
            mck.return_value.text = "not_found"

            res = self.__taskJson.delete_by_id(TaskBo(name="abc", priority=0))
            self.assertEquals(res, False)
