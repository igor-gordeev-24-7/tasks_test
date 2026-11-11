from datetime import date, datetime


class Task:
    TYPE = "task"
    ALLOWED_PRIORITIES = ("low", "middle", "high")
    DATE_FORMAT = "%Y-%m-%d"
    NO_DEADLINE = "none"
    created_count = 0

    #  Создание
    def __init__(
        self,
        id: int,
        title: str,
        add_date: date,
        deadline: date | None = None,
        is_completed: bool = False,
        priority: str = "low",
    ):
        self.__id = id

        # объявляем поля до сеттеров, чтобы @property нашли атрибуты
        self._title = None
        self._priority = None
        self._deadline = None
        self._is_completed = None
        self._add_date = add_date

        # начальные значения проходят через сеттеры (валидация)
        self.title = title
        self.priority = priority
        self.deadline = deadline
        self.is_completed = is_completed

        Task.created_count += 1

    #  Свойства (id — только чтение)
    @property
    def id(self) -> int:
        return self.__id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("title не может быть пустым или строкой из пробелов")
        self._title = value.strip()

    @property
    def priority(self) -> str:
        return self._priority

    @priority.setter
    def priority(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("priority не может быть пустым или строкой из пробелов")
        if value not in self.ALLOWED_PRIORITIES:
            raise ValueError(
                f"priority должен быть одним из {self.ALLOWED_PRIORITIES}, "
                f"получено: {value!r}"
            )
        self._priority = value

    @property
    def deadline(self) -> date | None:
        return self._deadline

    @deadline.setter
    def deadline(self, value):
        if value is None or value == self.NO_DEADLINE:
            self._deadline = None
            return

        if isinstance(value, str):
            try:
                value = datetime.strptime(value, self.DATE_FORMAT).date()
            except ValueError as exc:
                raise ValueError(
                    f"deadline должен быть датой в формате {self.DATE_FORMAT} "
                    f"или None, получено: {value!r}"
                ) from exc

        if not isinstance(value, date):
            raise ValueError(
                f"deadline должен быть date или None, получено: {type(value).__name__}"
            )
        self._deadline = value

    @property
    def is_completed(self) -> bool:
        return self._is_completed

    @is_completed.setter
    def is_completed(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_completed должен быть bool")
        self._is_completed = value

    @property
    def add_date(self) -> date:
        return self._add_date

    #  Вычисляемые свойства (только чтение)
    @property
    def is_overdue(self) -> bool:
        if self._is_completed or self._deadline is None:
            return False
        return date.today() > self._deadline

    @property
    def status_text(self) -> str:
        if self._is_completed:
            return "выполнена"
        if self.is_overdue:
            return "просрочена"
        return "активна"

    #  Представление
    def get_details(self) -> str:
        """Строка для пользователя. Наследники дополняют через super()."""
        deadline = self.deadline.isoformat() if self.deadline else "без срока"
        overdue = " (просрочена)" if self.is_overdue else ""
        return (
            f"[{self.id}] {self.title} | "
            f"приоритет: {self.priority} | "
            f"добавлена: {self.add_date.isoformat()} | "
            f"дедлайн: {deadline}{overdue} | "
            f"статус: {self.status_text}"
        )

    def __str__(self) -> str:
        return self.get_details()

    #  Сериализация
    def to_dict(self) -> dict:
        """Объект → словарь, безопасный для json.dump()."""
        return {
            "type": self.TYPE,
            "id": self.id,
            "title": self.title,
            "add_date": self.add_date.isoformat(),
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "is_completed": self.is_completed,
            "priority": self.priority,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Task":
        """Фабрика: по полю 'type' создаёт объект нужного класса."""
        common = {
            "id": d["id"],
            "title": d["title"],
            "add_date": datetime.strptime(d["add_date"], cls.DATE_FORMAT).date(),
            "deadline": (
                datetime.strptime(d["deadline"], cls.DATE_FORMAT).date()
                if d.get("deadline") else None
            ),
            "is_completed": d.get("is_completed", False),
            "priority": d.get("priority", "low"),
        }

        task_type = d.get("type", "task")

        # импорт внутри метода — чтобы не было циклического импорта
        # (Task ← PersonalTask/WorkTask, но они наследуются от Task)
        if task_type == "personal":
            from PersonalTask import PersonalTask
            return PersonalTask(
                **common,
                category=d.get("category", PersonalTask.DEFAULT_CATEGORY),
            )
        if task_type == "work":
            from WorkTask import WorkTask
            return WorkTask(
                **common,
                project=d.get("project", ""),
                assignee=d.get("assignee", ""),
            )
        if task_type == "task":
            return Task(**common)

        raise ValueError(f"Неизвестный тип задачи: {task_type!r}")

    #  Статические проверки (для UI)
    @staticmethod
    def is_valid_title(title: str) -> bool:
        return isinstance(title, str) and title.strip() != ""

    @staticmethod
    def is_valid_priority(priority: str) -> bool:
        return priority in Task.ALLOWED_PRIORITIES

    @staticmethod
    def is_valid_id(task_id: int) -> bool:
        return (
            isinstance(task_id, int)
            and not isinstance(task_id, bool)
            and task_id > 0
        )