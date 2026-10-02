from aliases import Task

def get_new_id(tasks: list[Task]) -> int:
    max_id = 0
    for task in tasks:
        if (task["id"] > max_id):
            max_id = task["id"]
    return max_id + 1