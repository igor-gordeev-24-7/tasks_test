from Task import Task
from datetime import date, datetime


class PersonalTask(Task):
    ALLOWED_CATEGORIES = ("здоровье", "покупки", "дом", "обучение", "другое")
    DEFAULT_CATEGORY = "другое"

    def __init__(
        self,
        id: int,
        title: str,
        add_date: date,
        deadline: date | None = None,
        is_completed: bool = False,
        priority: str = "low",
        category: str = DEFAULT_CATEGORY,
    ):
        super().__init__(
            id = id,
            title=title,
            add_date=add_date,
            deadline=deadline,
            is_completed=is_completed,
            priority=priority
        )
        self._category = category
        self.category = category

    @property
    def category(self) -> str:
        return self._category

    @category.setter
    def category(self, value: str):
        if not isinstance(value, str):
            raise ValueError("category не может быть пустой или строкой из пробелов")
        value = value.strip().lower()
        if value in self.ALLOWED_CATEGORIES:
            raise ValueError(
                f"category должна быть одной из {self.ALLOWED_CATEGORIES}, "
                f"получено: {value!r}"
            )
        self._category = value

    @property
    def status(self) -> str:
        return f"{super().status_text} [{self.priority}]"

    def get_details(self) -> str:
        return f"{super().get_details()} | категория: {self.category}"
