from aliases import Task
from helpers import get_new_id
from data import load_tasks, save_tasks
from menu_text import MENU_TEXT

tasks = load_tasks()

def show_task(task: Task):
    print(f"\n{task['id']} - {task['title']} - {task['completed']} - {task['priority']}\n")


def show_tasks(tasks: list[Task]) -> None:
    if len(tasks) == 0:
        print("\nСписок задач пуст\n")
        return
    print("\nСписок задач:")
    for task in tasks:
        print(f"{task['id']} - {task['title']} - {task['completed']} - {task['priority']}")
    print()

def add_task(tasks: list[Task], title: str, priority: str = "low") -> Task:
    task = {
        "id": get_new_id(tasks),
        "title": title,
        "completed": False,
        "priority": priority,
    }
    tasks.append(task)
    save_tasks(tasks)
    return task

def find_task(tasks: list[Task], task_id : int) -> Task | None:
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

def complete_task(tasks: list[Task], id : int):
    task = find_task(tasks, id)
    task['completed'] = True
    save_tasks(tasks)
    return task

def delete_task(tasks: list[Task], task_id: int) -> None:
    task = find_task(tasks, task_id)
    tasks.remove(task)
    save_tasks(tasks)

def search_tasks(tasks: list[Task], text: str) -> list[Task]:
    return [task for task in tasks if text.strip().lower() in task['title'].lower()]

def filter_tasks_by_status(tasks: list[Task], completed: bool) -> list[Task]:
    return [task for task in tasks if task['completed'] == completed]

def filter_tasks_by_priority(tasks: list[Task], priority: str) -> list[Task]:
    priority = priority.strip().lower()
    return [task for task in tasks if task['priority'].lower().strip() == priority]

def rename_task(tasks: list[Task], id: int, new_title: str) -> Task:
    task = find_task(tasks, id)
    task['title'] = new_title
    save_tasks(tasks)
    return task

def get_task_statistics(tasks: list[Task], id: int, priority: str) -> Task:
    task = find_task(tasks, id)
    task['priority'] = priority.strip().lower()

def read_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("\nНекорректный ввод: нужно целое число\n")

def get_task_statistics(tasks: list[Task]) -> dict[str, int | float]:
    len_of_tasks = len(tasks)
    len_completed_of_tasks = len(filter_tasks_by_status(tasks, True))
    len_not_completed_of_tasks = len(filter_tasks_by_status(tasks, False))
    len_low_priority_tasks = len(filter_tasks_by_priority(tasks, "low"))
    len_medium_priority_tasks = len(filter_tasks_by_priority(tasks, "medium"))
    len_high_priority_tasks = len(filter_tasks_by_priority(tasks, "high"))

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
        "medium_priority": len_medium_priority_tasks,
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
    print(f"medium: {stats['medium_priority']}")
    print(f"high: {stats['high_priority']}")
    print()

def delete_completed_tasks(tasks: list[Task]) -> int:
    completed = [task for task in tasks if task['completed']]
    if not completed:
        return 0
    tasks[:] = [task for task in tasks if not task['completed']]
    return len(completed)

PRIORITY_WEIGHT = {
    "high": 0,
    "medium": 1,
    "low": 2,
}

def sort_tasks_by_priority(tasks: list[Task]) -> list[Task]:
    return sorted(tasks, key=lambda task: PRIORITY_WEIGHT[task['priority']])


def show_menu():
    stop = False
    while not stop:
        print(MENU_TEXT)
        choice = read_int("Введите пункт меню: ")

        if (choice) == 1:
            print("")
            if len(tasks) > 0:
                show_tasks(tasks)
            else:
                print("Список пуст")
            print("")

        if choice == 2:
            title = input("Введите title нового обращения: ").strip()
            if not title:
                print("Название не может быть пустым")
                continue

            new_id = get_new_id(tracker.tasks)
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

        if choice == 0:
            print("")
            print("Программа остановлена")
            print("")
            stop = True


def main() -> None:
    show_menu()

if __name__ == "__main__":
    main()


