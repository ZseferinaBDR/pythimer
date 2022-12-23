import os


def get_relative_path(file_name: str) -> str:
    return os.path.join(os.path.abspath(os.curdir), file_name)
