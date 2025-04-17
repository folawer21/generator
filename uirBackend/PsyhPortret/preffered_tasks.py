def get_tasks_by_traits(traits, data):
    preferred_tasks = []
    unwanted_tasks = []

    for trait in traits:
        if trait in data:
            preferred_tasks.extend(data[trait].get("предпочтительные_задания", []))
            unwanted_tasks.extend(data[trait].get("нежелательные_задания", []))

    preferred_tasks = list(set(preferred_tasks))
    unwanted_tasks = list(set(unwanted_tasks))

    return preferred_tasks