import json


def open_file(path) -> dict:
    """
    Позволяет открыть json-файл. Возвращает содержимое файла
    """
    try:
        with open(f'app/data/{path}', 'r') as f:
            file = json.load(f)
    except Exception:
        with open(f'./data/{path}', 'r') as f:
            file = json.load(f)
    return file


def set_value(path: str, key, data) -> None:
    """
    Позволяет установить определенное значение по ключю в json-файле
    """
    try:
        file = open_file(path)
        file[key] = data
        with open(f'app/data/{path}', 'w') as f:
            json.dump(file, f)
    except Exception:
        file = open_file(path)
        file[key] = data
        with open(f'./data/{path}', 'w') as f:
            json.dump(file, f)


def get_value(path: str, key) -> any:
    """
    Возвращает значение по ключю в json-файле
    """
    file = open_file(path)
    try:
        return file.get(key)
    except Exception:
        return None
