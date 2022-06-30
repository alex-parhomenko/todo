class Task:

    # Task record keys.
    ID = 'Id'
    NAME = 'Name'
    PRIORITY = 'Priority'

    NAME_MAX_LEN = 17
    NAME_MIN_LEN = 2

    PRIORITY_RANGE_MIN_BORDER = 1
    PRIORITY_RANGE_MAX_BORDER = 100

    def __init__(self, id=None, name=None, priority=None) -> None:
        self.id = id
        self.name = name
        self.priority = priority
