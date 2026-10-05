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
        print(f"Список задач пуст")
        return
    print(f"Список задач:")
    for task in tasks:
        print(f"{task['id']} - {task['title']} - {task['completed']}")


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
    if task is None:
        print("Задача не найдена")
        return
    tasks.remove(task)
    print("Задача удалена")

def search_tasks(tasks: list[Task], text: str) -> list[Task]:
    result = []
    find = False
    for task in tasks:
        if text.lower() in task['title'].lower():
            result.append(task)
            find = True
        else:
            find = False
    return result

def filter_tasks_by_status(tasks: list[Task], completed: bool) -> list[Task]:
    return [task for task in tasks if task['completed'] == completed]

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
            try:
                task_id = int(input("Введите id для поиска: "))
            except ValueError:
                print("Некорректный id: нужно целое число")
            else:
                task = find_task(tasks, task_id)
                if task is None:
                    print()
                    print("Задача не найдена")
                    print()
                else:
                    print()
                    print(f"{task['id']} - {task['title']} - {task['completed']} - {task['priority']}")
                    print()

        if (choice) == 4:
            try:
                print("")
                id = int(input("Введите id для смены статуса: "))
                print("")
            except ValueError:
                print("")
                print("Некорректный id: нужно целое число")
                print("")
            else:
                task = complete_task(tasks, id)
                if task is None:
                    print("")
                    print("Задача не найдена")
                    print("")
                else:
                    print("")
                    print(f"\nID - {task['id']}, статус - {task['completed']}\n")
                    print("")



        if (choice) == 5:
            try:
                print("")
                id = int(input("Введите id для смены статуса: "))
                print("")
            except ValueError:
                print("")
                print("Некорректный id: нужно целое число")
                print("")
            else:
                print("")
                delete_task(tasks, id)
                print("")

        if (choice) == 6:
            text = input("Введите часть названия задачи: ")
            result = search_tasks(tasks, text)
            print("")
            if len(result) > 0:
                for task in result:
                    print(f"{task['id']} - {task['title']} - {task['completed']}")
            else:
                print("Задачи не найдены")
            print("")

        if (choice) == 7:
            print("")
            print("1 - Показать выполненные")
            print("2 - Показать невыполненные")
            print("")

            choice = int(input("Выберите пункт: "))

            print("")
            if choice not in (1,2):
                print("Некорректный пункт")
            print("")

            if choice == 1:
                print("")
                show_tasks(filter_tasks_by_status(tasks, completed=True))
                print("")

            if choice == 2:
                print("")
                show_tasks(filter_tasks_by_status(tasks, completed=False))
                print("")

        if (choice) == 0:
            print("")
            print("Программа остановлена")
            print("")
            stop = True


def main() -> None:
    # show_tasks(tasks)
    #
    # add_task(tasks, "новое название", "medium")
    # print(tasks)
    #
    # complete_task(tasks, 1)
    # print(tasks)
    #
    # delete_task(tasks, 1)
    # print(tasks)

    show_menu()


    # show_tasks(filter_tasks_by_status(tasks, completed=True))
    #
    # show_tasks(filter_tasks_by_status(tasks, completed=False))

if __name__ == "__main__":
    main()


