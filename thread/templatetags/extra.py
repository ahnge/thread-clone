from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()


@register.filter(name="ecut")
def ecut(value):
    """Get the first 2 characters of the value"""
    if len(value) <= 2:
        return value
    return value[:2]


@register.filter(name="time_ago")
def time_ago_filter(value):
    now = timezone.now()
    delta = now - value

    if delta < timedelta(minutes=1):
        return "now"
    elif delta < timedelta(hours=1):
        return f"{delta.seconds // 60}m"
    elif delta < timedelta(days=1):
        return f"{delta.seconds // 3600}h"
    elif delta < timedelta(weeks=1):
        return f"{delta.days}d"
    elif delta < timedelta(weeks=52):
        return f"{delta.days // 7}w"
    else:
        return f"{delta.days // 365}y"


@register.filter
def format_kay(value):
    if value >= 1000000:
        return f"{value / 1000000:.1f}m"
    elif value >= 1000:
        return f"{value / 1000:.1f}k"
    else:
        return str(value)
