import os


def resolve_data(file_name):
    r = os.path.dirname(os.path.abspath(__file__))
    return f"{r}/../../data/{file_name}"


def resolve_app_config(file_name):
    r = os.path.dirname(os.path.abspath(__file__))
    return f"{r}/../appconfig/{file_name}"


def resolve_config(file_name):
    r = os.path.dirname(os.path.abspath(__file__))
    return f"{r}/../../config/{file_name}"
