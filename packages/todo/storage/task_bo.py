import json


class TaskEncoder(json.JSONEncoder):
    def default(self, t):
        if isinstance(t, TaskBo):
            return t.__dict__
        else:
            return super.default(self, t)


class TaskDecoder(json.JSONDecoder):
    def __init__(
        self,
    ) -> None:
        json.JSONDecoder.__init__(self, object_hook=self.__decode)

    def __decode(self, t):
        return TaskBo(**t)


class TaskBo:
    # fmt: off
    def __init__(
        self,
        id: int = None,
        name: str = None,
        priority: int = None
    ) -> None:
        self.id = id
        self.name = name
        self.priority = priority
    # fmt: on
