import uuid


class Task:
    """Holds all information needed for a task."""

    def __init__(
        self,
        data: dict,
        app_id: str,
        task_type: str,
        task_id: str = "",
        message: str = "",
        message_detailed: str = "",
        progress: int = 0,
        status: str = "created",
        result: dict = {},
    ):
        if task_id == "":
            task_id = str(uuid.uuid4())

        self.data = data
        self.task_id = task_id
        self.app_id = app_id  # TODO: implement solution for report to "all" Blenders
        self.task_type = task_type

        self.message = message
        self.message_detailed = message_detailed
        self.progress = progress
        self.status = status  # created / finished / error
        if result != None:
            self.result = result.copy()
        else:  # to be extra safe
            print("result is None", self.task_type)
            self.result = {}

    def __str__(self):
        return f"ID={self.task_id}, APP_ID={self.app_id}"
