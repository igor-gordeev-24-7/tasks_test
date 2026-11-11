from datetime import date, datetime

from TaskTracker import TaskTracker
from data.exporters import JsonTaskExporter, TextTaskExporter
from menu_text import MENU_TEXT
from Task import Task


tracker = TaskTracker("data/tasks.json")

def read_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("\nНекорректный ввод: нужно целое число\n")
#
def get_task_statistics(tasks: list[Task]) -> dict[str, int | float]:
    len_of_tasks = len(tasks)
    len_completed_of_tasks = len(tracker.filter_tasks(completed=True))
    len_not_completed_of_tasks = len(tracker.filter_tasks(completed=False))
    len_low_priority_tasks = len(tracker.filter_tasks(priority="low"))
    len_middle_priority_tasks = len(tracker.filter_tasks(priority="middle"))
    len_high_priority_tasks = len(tracker.filter_tasks(priority="high"))

    percentage_of_completed_tasks = (
        len_completed_of_tasks / len_of_tasks * 100
        if len_of_tasks > 0
        else 0.0
    )

    task_statistics = {
        "total": len_of_tasks,
        "completed": len_completed_of_tasks,
        "not_completed": len_not_completed_of_tasks,
        "low_priority": len_low_priority_tasks,
        "middle_priority": len_middle_priority_tasks,
        "high_priority": len_high_priority_tasks,
        "percentage_completed": percentage_of_completed_tasks,
    }
    return task_statistics


def show_statistics(stats: dict) -> None:
    print()
    print("Статистика Task Tracker")
    print(f"Всего задач: {stats['total']}")
    print(f"Выполнено: {stats['completed']}")
    print(f"Осталось: {stats['not_completed']}")
    print(f"Прогресс: {stats['percentage_completed']:.1f}%")
    print()
    print("Приоритеты:")
    print(f"low: {stats['low_priority']}")
    print(f"middle: {stats['middle_priority']}")
    print(f"high: {stats['high_priority']}")
    print()

def show_menu():
    stop = False
    while not stop:
        print(MENU_TEXT)
        choice = read_int("Введите пункт меню: ")

        if (choice) == 1:
            print("")
            if len(tracker.tasks) > 0:
                tracker.show_tasks()
            else:
                print("Список пуст")
            print("")

        if choice == 2:
            title = input("Введите title нового обращения: ").strip()
            if not title:
                print("Название не может быть пустым")
                continue

            new_id = tracker.next_id()
            add_date = date.today()

            deadline_raw = input("Дедлайн (ГГГГ-ММ-ДД, Enter — без дедлайна): ").strip()
            if deadline_raw:
                try:
                    deadline = datetime.strptime(deadline_raw, "%Y-%m-%d").date()
                except ValueError:
                    print("Неверный формат даты, задача не добавлена")
                    continue
            else:
                deadline = None

            priority = input("Приоритет (low/middle/high) [low]: ").strip().lower() or "low"

            try:
                task = Task(
                    id=new_id,
                    title=title,
                    add_date=add_date,
                    deadline=deadline,
                    priority=priority,
                )
            except ValueError as e:
                print(f"Ошибка: {e}")
                continue

            tracker.add_task(task)
            print(f"Задача #{new_id} добавлена")


        if choice == 3:
            task_id = read_int("Введите id для поиска: ")

            task = tracker.find_task(task_id)

            if not task:
                print("\nЗадача не найдена\n")
                continue
            print(task)

        if (choice) == 4:
            task_id = read_int("Введите id задачи для выполнения: ")
            task = tracker.find_task(task_id)
            if not task:
                print("\nЗадача не найдена\n")
                continue

            tracker.complete_task(task_id)
            print(task)

        if (choice) == 5:
            task_id = read_int("Введите id задачи для удаления: ")
            task = tracker.find_task(task_id)
            if not task:
                print("\nЗадача для удаления не найдена\n")
                continue

            tracker.delete_task(task_id)
            print(f"\nЗадача - {task.title} - id - {task.id} - удалена\n")

        if (choice) == 6:
            text = input("\nВведите часть названия задачи: ")
            result = tracker.search_tasks_by_text(text)
            tracker.show_tasks(result)

        if (choice) == 7:
            print("\n1 - Показать выполненные")
            print("2 - Показать невыполненные\n")

            choice = read_int("Выберите пункт: ")

            if choice not in (1,2):
                print("\nНекорректный пункт\n")

            if choice == 1:
                 tracker.show_tasks(tracker.filter_tasks(completed=True))

            if choice == 2:
                tracker.show_tasks(tracker.filter_tasks(completed=False))

        if (choice) == 8:
            value = input("\nВведите приоритет для поиска задач(low, middle, high): \n").strip().lower()

            if value not in ("low", "middle", "high"):
                print("\nНекорректный приоритет\n")
                continue

            found = tracker.filter_tasks(priority=value)
            if not found:
                print(f"\nЗадач с приоритетом {value} не найдено\n")
                continue
            tracker.show_tasks(found)

        if choice == 9:
            task_id = read_int("\nВведите id для переименования: ")
            new_title = input("\nВведите новое название: \n").strip()

            if not new_title:
                print("\nНазвание не может быть пустым\n")
                continue

            try:
                task = tracker.rename_task(task_id, new_title)
            except ValueError as e:
                print(f"\nОшибка: {e}\n")
                continue

            if task is None:
                print("\nЗадача с таким id отсутствует\n")
                continue

            print(f"\nЗадача переименована: {task.title}\n")
        #
        if choice == 10:
            task_id = read_int("\nВведите id для смены приоритета: ")
            task = tracker.find_task(task_id)

            if not task:
                print("\nЗадача с таким id отсутствует\n")
                continue

            new_priority = input("\nВведите приоритет(low, middle, high): ").strip()
            if new_priority not in ("low", "middle", "high"):
                print("\nНекорректный приоритет\n")
                continue

            task.priority = new_priority
            tracker.save_to_file()
            print("\nПриоритет изменен")
            print(f"Задача - {task.title} - приоритет {task.priority}\n")

        if choice == 11:
            show_statistics(get_task_statistics(tracker.tasks))

        if choice == 12:
            print()
            count = tracker.delete_completed_tasks()
            if count == 0:
                print("Выполненных задач нет")
            else:
                print(f"Удалено выполненных задач: {count}")
            print()

        if choice == 13:
            print("Отсортированный список задач по приоритету:")
            tracker.show_tasks(tracker.sort_tasks_by_priority(reverse=True))

        if choice == 14:
            print("\n--- ЭКСПОРТ ЗАДАЧ ---")
            print("Создаём список экспортёров...")

            # 1. Создаём список объектов.
            # Мы не проверяем их тип, они просто лежат в списке.
            exporters = [
                JsonTaskExporter(),
                TextTaskExporter(),
            ]

            # 2. ОДИН И ТОТ ЖЕ КОД для всех экспортёров
            for exporter in exporters:
                try:
                    # Полиморфный вызов.
                    # TaskTracker не знает, какой формат сейчас в exporter.
                    tracker.export(exporter)
                except Exception as e:
                    print(f"Ошибка экспорта через {type(exporter).__name__}: {e}")

            print("\nГотово! Проверьте папку 'exports'.")
            print("")


        if choice == 0:
            print("")
            print("Программа остановлена")
            print("")
            stop = True


def main() -> None:
    show_menu()

if __name__ == "__main__":
    main()


