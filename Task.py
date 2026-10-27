from datetime import date

from data import save_tasks


class Task:
    ALLOWED_PRIORITIES = ("low", "middle", "high")
    DATE_FORMAT = "%Y-%m-%d"
    created_count = 0

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

        Task.created_count += 1

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

    def is_overdue(self) -> bool:
        if self.deadline is None:
            return False
        if self.is_complited:
            return False
        return self.deadline < date.today()

    def show_info(self) -> None:
        status = "выполнена" if self.is_completed else "не выполнена"
        deadline = self.deadline.isoformat() if self.deadline else "без срока"
        overdue = " Просрочена" if self.is_overdue() else ""

        print(
            f"ID: {self.id}\n"
            f"Название: {self.title}\n"
            f"Приоритет: {self.priority}\n"
            f"Добавлена: {self.add_date.isoformat()}\n"
            f"Дедлайн: {deadline}{overdue}\n"
            f"Статус: {status}"
        )

    @staticmethod
    def is_valid_title(title: str) -> bool:
        return isinstance(title, str) and title.strip() != ""

    @staticmethod
    def is_valid_priority(priority: str) -> bool:
        return priority in Task.ALLOWED_PRIORITIES

    @staticmethod
    def is_valid_id(task_id: int) -> bool:
        return isinstance(task_id, int) and not isinstance(task_id, bool) and task_id > 0
