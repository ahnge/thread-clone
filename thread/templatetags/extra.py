from django import template

register = template.Library()


@register.filter(name="cut")
def cut(value):
    """Get the first 2 characters of the value"""
    if len(value) <= 2:
        return value
    return value[:2]
