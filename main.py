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

def show_tasks(tasks: list[dict[str, int | str | bool]]) -> None:
    if len(tasks) == 0:
        print(f"Список задач пуст")
        return
    print(f"Список задач:")
    for task in tasks:
        print(f"{task['id']} - {task['title']} - {task['completed']}")

show_tasks(tasks)