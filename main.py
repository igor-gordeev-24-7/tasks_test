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

def find_task(tasks: list[Task], id : int) -> Task | None:
    for task in tasks:
        if task["id"] == id:
            return task
    return None


def complete_task(tasks: list[Task], id : int):
    task = find_task(tasks, id)
    task["completed"] = True


def main() -> None:
    show_tasks(tasks)

    add_task(tasks, "новое название", "medium")
    print(tasks)

    complete_task(tasks, 1)
    print(tasks)



if __name__ == "__main__":
    main()


