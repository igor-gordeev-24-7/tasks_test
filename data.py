import json
from aliases import Task

def load_tasks(filename: str = 'tasks.json') -> list[Task]:
    try:
        with open(filename, 'r', encoding='utf-8') as data_json_file:
           return json.load(data_json_file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Файл поврежден")
        return []


def save_tasks(tasks: list[Task], filename: str = 'tasks.json'):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(tasks, json_file, ensure_ascii=False, indent=4)
