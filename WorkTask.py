from datetime import date

from Task import Task


class WorkTask(Task):
    TYPE = "work"
    def __init__(
            self,
            id: int,
            title: str,
            add_date: date,
            deadline: date | None = None,
            is_completed: bool = False,
            priority: str = "low",
            project:str = "",
            assignee:str = "",
    ):
        super().__init__(
            id=id,
            title=title,
            add_date=add_date,
            deadline=deadline,
            is_completed=is_completed,
            priority=priority
        )
        self._project = None
        self._assignee = None
        self.project = project
        self.assignee = assignee

    @property
    def project(self) -> str:
        return self._project

    @project.setter
    def project(self, value: str):
        if not isinstance(value, str):
            raise ValueError("project должен быть строкой")
        self._project = value

    @property
    def assignee(self) -> str:
        return self._assignee

    @assignee.setter
    def assignee(self, value: str):
        if not isinstance(value, str):
            raise ValueError("assignee должен быть строкой")
        self._assignee = value

    @property
    def status_text(self) -> str:
        base = super().status_text
        extras =[]
        if self._project:
            extras.append(f"проект: {self._project}")
        if self._assignee:
            extras.append(f"ответсьвенн: {self._assignee}")
        return f"{base} ({', '.join(extras)})" if extras else base

    def get_details(self) -> str:
        return (
            f"{super().get_details()} | "
            f"проект: {self.project or '—'} | "
            f"ответственный: {self.assignee or '—'}"
        )