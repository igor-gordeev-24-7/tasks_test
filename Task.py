from datetime import date

from data import save_tasks


class Task:
    ALLOWED_PRIORITIES = ("low", "middle", "high")

    def __init__(
        self,
        id: int,
        title: str,
        add_date: date,
        deadline: date | None = None,
        is_completed: bool = False,
        priority: str = "low",

    ):
        if priority not in self.ALLOWED_PRIORITIES:
            raise ValueError(
                f"priority должен быть одним из {self.ALLOWED_PRIORITIES}, получено: {priority!r}"
            )
        self.id = id
        self.title = title
        self.add_date = add_date
        self.deadline = deadline
        self.is_completed = is_completed
        self.priority = priority

    def __str__(self) -> str:
        status = "выполнена" if self.is_completed else "не выполнена"
        return (
            f"[{self.id}] {self.title} | "
            f"приоритет: {self.priority} | "
            f"добавлена: {self.add_date} | "
            f"дедлайн: {self.deadline} | "
            f"статус: {status}"
        )

    def find_task(self, tasks: list[Task], task_id: int) -> Task | None:
        for task in tasks:
            if task["id"] == task_id:
                return task
        return None

    def complete(self, tasks: list[Task], task_id: int) -> bool:
        task = self.find_task(tasks, task_id)
        task['is_completed'] = True
        save_tasks(tasks)



