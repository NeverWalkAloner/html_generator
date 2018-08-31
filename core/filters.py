import markdown2
from slugify import slugify


def slugify_category(value: str):
    """
    slugify category and return as html file name
    :param value: category name
    :return: html file name
    """
    return f"{slugify(value)}.html"


def parse_markdown(value: str):
    """
    parse markdonw content return HTML
    :param value: markdown string
    :return: html string
    """
    return markdown2.markdown(value, extras=['break-on-newline'])
