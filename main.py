type Task = dict[str, int | str | bool]

tasks = [
    {
        "id": 1,
        "title": "Подготовить презентацию",
        "completed": False,
        "priority": "high",
    },
    {
        "id": 2,
        "title": "Изучить словари",
        "completed": True,
        "priority": "medium",
    },
    {
        "id": 3,
        "title": "Создать репозиторий",
        "completed": False,
        "priority": "low",
    },
]

# for task in tasks:
#     print(f"{task['id']} - {task['title']} - {task['completed']} ")
# print(f"Количество тасков {len(tasks)}")

# show_tasks()
# add_task()
# find_task()
# complete_task()
# delete_task()
# show_menu()

# def get_count_price(price: float | int, quantity : int) -> float | int:
#     return price * quantity
#
# get_count_price()

def show_tasks(tasks: list[Task]) -> None:
    if len(tasks) == 0:
        print(f"Список задач пуст")
        return
    print(f"Список задач:")
    for task in tasks:
        print(f"{task['id']} - {task['title']} - {task['completed']}")

show_tasks(tasks)


def get_new_id(tasks: list[Task]) -> int:
    max_id = 0
    for task in tasks:
        if (task["id"] > max_id):
            max_id = task["id"]
    return max_id + 1


def add_task(tasks: list[Task], title: str, priority: str = "low") -> Task:
    task = {
        "id": get_new_id(tasks),
        "title": title,
        "completed": False,
        "priority": priority,
    }
    tasks.append(task)
    return task

add_task(tasks, "новое название", "medium")
print(tasks)


