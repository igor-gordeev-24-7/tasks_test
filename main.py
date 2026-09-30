print("Hello World")

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

for task in tasks:
    print(f"{task['id']} - {task['title']} - {task['completed']} ")
print(f"Количество тасков {len(tasks)}")