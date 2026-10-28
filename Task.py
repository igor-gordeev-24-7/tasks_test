from datetime import date, datetime

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
        if self.is_completed:
            return False
        return self.deadline < date.today()

    def show_info(self) -> None:
        status = "выполнена" if self.is_completed else "не выполнена"
        deadline = self.deadline.isoformat() if self.deadline else "без срока"
        overdue = " Просрочена" if self.is_overdue() else ""

        print(
            f"\nID: {self.id}\n"
            f"Название: {self.title}\n"
            f"Приоритет: {self.priority}\n"
            f"Добавлена: {self.add_date.isoformat()}\n"
            f"Дедлайн: {deadline}{overdue}\n"
            f"Статус: {status}\n"
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

    @classmethod
    def from_dict(cls, d: dict) -> Task:
        deadline = (
            datetime.strptime(d.get("deadline"), cls.DATE_FORMAT).date()
            if d.get("deadline") else None
        )
        return cls(
            id=d["id"],
            title=d["title"],
            add_date=datetime.strptime(d["add_date"], cls.DATE_FORMAT).date(),
            deadline=deadline,
            is_completed=d.get("is_completed", False),
            priority=d.get("priority", "low"),
        )

    @classmethod
    def from_string(cls, s: str) -> "Task":
        """Создаёт Task из строки: id;title;priority;add_date;deadline;is_completed."""
        parts = [p.strip() for p in s.split(";")]
        if len(parts) != 6:
            raise ValueError(
                f"Ожидалось 6 полей через ';', получено {len(parts)}: {s!r}"
            )

        raw_id, title, priority, add_date_s, deadline_s, completed_s = parts

        try:
            task_id = int(raw_id)
        except ValueError:
            raise ValueError(f"id должен быть целым, получено: {raw_id!r}")

        try:
            add_date = datetime.strptime(add_date_s, cls.DATE_FORMAT).date()
        except ValueError:
            raise ValueError(f"add_date в формате {cls.DATE_FORMAT}, получено: {add_date_s!r}")

        if deadline_s in (cls.NO_DEADLINE, ""):
            deadline = None
        else:
            try:
                deadline = datetime.strptime(deadline_s, cls.DATE_FORMAT).date()
            except ValueError:
                raise ValueError(
                    f"deadline в формате {cls.DATE_FORMAT} или '{cls.NO_DEADLINE}', получено: {deadline_s!r}")

        is_completed = completed_s.lower() in ("1", "true", "yes", "да")

        return cls(
            id=task_id,
            title=title,
            add_date=add_date,
            deadline=deadline,
            is_completed=is_completed,
            priority=priority,
        )

    def to_dict(self) -> dict:
        """Возвращает словарь, безопасный для json.dump()."""
        return {
            "id": self.id,
            "title": self.title,
            "add_date": self.add_date.isoformat(),  # date → "2026-10-27"
            "deadline": self.deadline.isoformat() if self.deadline else None,  # None → null
            "is_completed": self.is_completed,  # bool остаётся bool
            "priority": self.priority,
        }




