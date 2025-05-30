import re


def snake2Pascal(string: str) -> str:
    return "".join(word.capitalize() for word in string.split("_"))


def pascal2Snake(string):
    return "_".join([word.lower() for word in re.findall(r"[A-Z][a-z]*|[0-9]", string)])
