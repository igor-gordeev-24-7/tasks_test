import json
import os
import shutil
from pathlib import Path

from Task import Task


class TaskTracker:

    def __init__(self, path: str = "tasks.json"):
        self.path = Path(path)
        self.backup_path = self.path.with_suffix(self.path.suffix + ".bak")
        self.tasks: list[Task] = []
        self.load_from_file()

    #  Файл: загрузка / сохранение
    def _backup(self) -> None:
        """Копирует текущий файл в .bak перед перезаписью."""
        if not self.path.exists():
            return
        try:
            shutil.copy2(self.path, self.backup_path)
        except OSError as e:
            print(f"Не удалось создать резервную копию {self.backup_path}: {e}")

    def load_from_file(self) -> None:
        self.tasks = []

        if not self.path.exists():
            print(f"Файл {self.path} не найден — начинаем с пустого списка.")
            return

        try:
            with self.path.open("r", encoding="utf-8") as f:
                raw = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Файл {self.path} повреждён (неверный JSON): {e}")
            print("Работаем с пустым списком, файл не изменён.")
            return
        except OSError as e:
            print(f"Не удалось прочитать файл {self.path}: {e}")
            return

        if not isinstance(raw, list):
            print(f"Ожидался список задач в {self.path}, получено: {type(raw).__name__}")
            return

        if not raw:
            print(f"Файл {self.path} пуст.")
            return

        skipped = 0
        for index, item in enumerate(raw, start=1):
            try:
                self.tasks.append(Task.from_dict(item))
            except (KeyError, ValueError, TypeError) as e:
                skipped += 1
                print(f"Задача #{index} пропущена: {e}")

        if skipped:
            print(f"Загружено: {len(self.tasks)}, пропущено: {skipped}.")
        else:
            print(f"Загружено задач: {len(self.tasks)}.")

    def save_to_file(self) -> None:
        """Атомарная запись: сначала во временный файл, потом replace."""
        self._backup()
        data = [t.to_dict() for t in self.tasks]
        tmp_path = self.path.with_suffix(self.path.suffix + ".tmp")
        try:
            with tmp_path.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, self.path)   # атомарно заменяет старый файл
        except OSError as e:
            print(f"Не удалось сохранить файл {self.path}: {e}")
            tmp_path.unlink(missing_ok=True)

    #  CRUD
    def add_task(self, task: Task) -> None:
        if self.find_task(task.id) is not None:
            raise ValueError(f"Задача с id {task.id} уже существует")
        self.tasks.append(task)
        self.save_to_file()

    def find_task(self, task_id: int) -> Task | None:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def complete_task(self, task_id: int) -> Task | None:
        task = self.find_task(task_id)
        if task is None:
            return None                    # ✅ было False — несоответствие аннотации
        task.is_completed = True
        self.save_to_file()
        return task

    def delete_task(self, task_id: int) -> bool:
        task = self.find_task(task_id)
        if task is None:                   # ✅ было: remove(None) → ValueError
            return False
        self.tasks.remove(task)
        self.save_to_file()
        return True

    def rename_task(self, task_id: int, new_title: str) -> Task | None:
        task = self.find_task(task_id)
        if task is None:
            return None
        new_title = new_title.strip()
        if not new_title:
            raise ValueError("Название не может быть пустым")
        task.title = new_title             # вызовет сеттер Task.title (валидация)
        self.save_to_file()
        return task

    def delete_completed_tasks(self) -> int:
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if not t.is_completed]
        removed = before - len(self.tasks)
        if removed:
            self.save_to_file()
        return removed

    #  Фильтры и поиск
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
            result = [t for t in result if t.is_overdue == overdue]   # ✅ без скобок
        return result

    def search_tasks_by_text(self, text: str) -> list[Task]:
        needle = text.strip().lower()
        if not needle:
            return []
        return [task for task in self.tasks if needle in task.title.lower()]

    def sort_tasks_by_priority(self, reverse: bool = False) -> list[Task]:
        order = {"low": 0, "middle": 1, "high": 2}
        return sorted(
            self.tasks,
            key=lambda t: order.get(t.priority, -1),
            reverse=reverse,
        )

    #  Вывод
    def show_tasks(self, tasks: list[Task] | None = None) -> None:
        tasks = self.tasks if tasks is None else tasks
        if not tasks:
            print("Задач нет")
            return
        for task in tasks:
            print(task.get_details())      # полиморфизм: PersonalTask/WorkTask добавят своё
            print("-" * 40)




