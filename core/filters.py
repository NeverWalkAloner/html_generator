# tools imports
import markdown2


def parse_markdown(value: str):
    """
    parse markdonw content return HTML
    :param value: markdown string
    :return: html string
    """
    return markdown2.markdown(value, extras=['break-on-newline'])


def urlify_category(value: str):
    """
    urlify category and return as html file name
    :param value: category name
    :return: html file name
    """
    return f"{value}1.html"
