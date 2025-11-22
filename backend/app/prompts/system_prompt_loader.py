import os


def get_system_prompt() -> str:
    base_dir = os.path.dirname(__file__)
    path = os.path.join(base_dir, "system_prompt.txt")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
