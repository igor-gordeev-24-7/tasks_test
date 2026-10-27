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

    def save(self) -> None:
        data = [
            {
                "id": t.id,
                "title": t.title,
                "add_date": t.add_date.isoformat(),
                "deadline": t.deadline.isoformat() if t.deadline else None,
                "is_completed": t.is_completed,
                "priority": t.priority,
            }
            for t in self.tasks
        ]
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)
        self.save()

    def find_task(self, task_id: int) -> Task | None:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None









