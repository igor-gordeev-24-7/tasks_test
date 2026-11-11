# exporters.py
from abc import ABC, abstractmethod
import json
from pathlib import Path

from Task import Task


class TaskExporter(ABC):
    """Базовый экспортёр. Наследники обязаны реализовать export() и extension."""

    @property
    @abstractmethod
    def extension(self) -> str:
        """Расширение файла без точки: 'json', 'txt', ..."""
        ...

    @abstractmethod
    def export(self, tasks: list[Task], path: str | Path) -> None:
        """Сохранить задачи в файл path."""
        ...


class JsonTaskExporter(TaskExporter):
    @property
    def extension(self) -> str:
        return "json"

    def export(self, tasks: list[Task], path: str | Path) -> None:
        data = [t.to_dict() for t in tasks]
        with Path(path).open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


class TextTaskExporter(TaskExporter):
    HEADER = "=" * 60

    @property
    def extension(self) -> str:
        return "txt"

    def export(self, tasks: list[Task], path: str | Path) -> None:
        lines = [self.HEADER, "ОТЧЁТ ПО ЗАДАЧАМ", self.HEADER, ""]

        if not tasks:
            lines.append("Задач нет.")
        else:
            for task in tasks:
                lines.append(task.get_details())
                lines.append("-" * 40)

            total = len(tasks)
            done = sum(1 for t in tasks if t.is_completed)
            overdue = sum(1 for t in tasks if t.is_overdue)
            lines.append("")
            lines.append(self.HEADER)
            lines.append(f"Всего: {total} | выполнено: {done} | просрочено: {overdue}")
            lines.append(self.HEADER)

        Path(path).write_text("\n".join(lines), encoding="utf-8")