from aliases import Task
from data import tasks
from helpers import get_new_id

# show_tasks()
# add_task()
# find_task()
# complete_task()
# delete_task()
# show_menu()

def show_tasks(tasks: list[Task]) -> None:
    if len(tasks) == 0:
        print("\nСписок задач пуст\n")
        return
    print("\nСписок задач:")
    for task in tasks:
        print(f"{task['id']} - {task['title']} - {task['completed']}")
    print()


def add_task(tasks: list[Task], title: str, priority: str = "low") -> Task:
    task = {
        "id": get_new_id(tasks),
        "title": title,
        "completed": False,
        "priority": priority,
    }
    tasks.append(task)
    return task

def find_task(tasks: list[Task], task_id : int) -> Task | None:
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

def complete_task(tasks: list[Task], id : int):
    task = find_task(tasks, id)
    if task is None:
        return None
    task['completed'] = True
    return task

def delete_task(tasks: list[Task], task_id: int) -> None:
    task = find_task(tasks, task_id)
    tasks.remove(task)

def search_tasks(tasks: list[Task], text: str) -> list[Task]:
    return [task for task in tasks if text.lower().strip() in task['title'].lower()]

def filter_tasks_by_status(tasks: list[Task], completed: bool) -> list[Task]:
    return [task for task in tasks if task['completed'] == completed]

def filter_tasks_by_priority(tasks: list[Task], priority: str) -> list[Task]:
    priority = priority.lower().strip()
    return [task for task in tasks if task['priority'].lower().strip() == priority]

def rename_task(tasks: list[Task], id: int, new_title: str) -> Task:
    task = find_task(tasks, id)
    task['title'] = new_title
    return task

def read_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("\nНекорректный ввод: нужно целое число\n")



def show_menu():
    stop = False
    while not stop:
        print("Меню - выберите пункт")
        print("1 - Показать задачи")
        print("2 - Добавить задачу")
        print("3 - Найти задачу")
        print("4 - Выполнить задачу")
        print("5 - Удалить задачу")
        print("6 - Найти задачу на части названия")
        print("7 - Фильтр по статусу")
        print("8 - Фильтр по приоритету")
        print("9 - Переименовать задачу")
        print("0 - Закрыть меню")

        choice: int = int(input())

        if (choice) == 1:
            print("")
            if len(tasks) > 0:
                show_tasks(tasks)
            else:
                print("Список пуст")
            print("")

        if (choice) == 2:
            titile = input("Введите title нового обращения: ")
            print("")
            add_task(tasks, titile, "medium")
            print("")

        if choice == 3:
            task_id = read_int("Введите id для поиска: ")

            task = find_task(tasks, task_id)

            if task is None:
                print("\nЗадача не найдена\n")
            else:
                print(f"\n{task['id']} - {task['title']} - {task['completed']} - {task['priority']}\n")

        if (choice) == 4:
            task_id = read_int("Введите id задачи для выполнения: ")
            task = complete_task(tasks, task_id)
            if task is None:
                print("\nЗадача не найдена\n")
            else:
                print(f"\n{task['id']} - {task['title']} - {task['completed']} - {task['priority']}\n")

        if (choice) == 5:
            task_id = read_int("Введите id задачи для удаления: ")
            task = find_task(tasks, task_id)
            if task is None:
                print("\nЗадача для удаления не найдена\n")
            else:
                delete_task(tasks, task_id)
                print(f"\nЗадача - {task['title']} - id - {task['id']} - удалена\n")

        if (choice) == 6:
            text = input("\nВведите часть названия задачи: ")
            result = search_tasks(tasks, text)
            show_tasks(result)

        if (choice) == 7:
            print("\n1 - Показать выполненные")
            print("2 - Показать невыполненные\n")

            choice = int(input("Выберите пункт: "))

            if choice not in (1,2):
                print("\nНекорректный пункт\n")

            if choice == 1:
                show_tasks(filter_tasks_by_status(tasks, completed=True))

            if choice == 2:
                show_tasks(filter_tasks_by_status(tasks, completed=False))

        if (choice) == 8:
            priority = input("\nВведите приоритет для поиска задач(low, medium, high): \n").strip().lower()

            if priority not in ("low", "medium", "high"):
                print("\nНекорректный приоритет\n")
            else:
                found = filter_tasks_by_priority(tasks, priority)
                if not found:
                    print(f"\nЗадач с приоритетом {priority} не найдено\n")
                else:
                    show_tasks(found)

        if (choice) == 9:
            task_id = read_int("\nВведите id для переименования: ")
            task = find_task(tasks, task_id)

            if task is None:
                print("\nЗадача с таким id отсутствует\n")
            else:
                new_title = input("\nВведите новое название: \n").strip()
                if not new_title:
                    print("\nНазвание не может быть пустым\n")
                else:
                    result = rename_task(tasks, task_id, new_title)
                    print(f"\nЗадача переименована: {result['title']}\n")

        if (choice) == 0:
            print("")
            print("Программа остановлена")
            print("")
            stop = True


def main() -> None:
    show_menu()

if __name__ == "__main__":
    main()


