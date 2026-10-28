import json
from datetime import datetime
from pathlib import Path

from Task import Task
from helpers import get_new_id

class TaskTracker:
    def __init__(self, path: str = "tasks.json"):
        self.path = Path(path)
        self.tasks: list[Task] = self._load()

    def _load(self) -> list[Task]:
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return [self._task_from_dict(item) for item in data]

    @staticmethod
    def _task_from_dict(d: dict) -> Task:
        return Task(
            id=d["id"],
            title=d["title"],
            add_date=datetime.strptime(d["add_date"], "%Y-%m-%d").date(),
            deadline=(
                datetime.strptime(d["deadline"], "%Y-%m-%d").date()
                if d.get("deadline") else None
            ),
            is_completed=d.get("is_completed", False),
            priority=d.get("priority", "low"),
        )

    def save_to_file(self) -> None:
        data = [t.to_dict() for t in self.tasks]
        try:
            with self.path.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print(f"Не удалось сохранить файл {self.path}: {e}")

    def add_task(self, task: Task) -> None:
        if self.find_task(task.id) is not None:
            raise ValueError(f"Задача с id {task.id} уже существует")
        self.tasks.append(task)
        self.save()

    def find_task(self, task_id: int) -> Task | None:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def complete_task(self, task_id : int) -> Task | None:
        task = self.find_task(task_id)
        if task is None:
            return False
        task.is_completed = True
        self.save()
        return task

    def delete_task(self, task_id: int) -> None:
        task = self.find_task(task_id)
        self.tasks.remove(task)
        self.save()

    def filter_tasks(
            self,
            *,
            priority: str | None = None,
            completed: bool | None = None,
            overdue: bool | None = None,
    ) -> list[Task]:
        result = self.tasks
        if priority is not None:
            result = [t for t in result if t.priority == priority]
        if completed is not None:
            result = [t for t in result if t.is_completed == completed]
        if overdue is not None:
            result = [t for t in result if t.is_overdue() == overdue]
        return result

    def show_tasks(self, tasks: list[Task] | None = None) -> None:
        tasks = self.tasks if tasks is None else tasks
        if not tasks:
            print("Задач нет")
            return
        for task in tasks:
            task.show_info()
            print("-" * 40)











