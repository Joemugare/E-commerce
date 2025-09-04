# compare/templatetags/compare_filters.py
from django import template

register = template.Library()

@register.filter
def div(value, arg):
    try:
        # Ensure value and arg are numbers
        val = int(value)
        # Handle case where arg might be a QuerySet length
        if isinstance(arg, (list, tuple, set)) or hasattr(arg, '__len__'):
            arg = len(arg)
        arg = int(arg)
        if arg == 0:
            return 0  # Avoid ZeroDivisionError
        return val // arg  # Integer division
    except (ValueError, TypeError, ZeroDivisionError) as e:
        print(f"div filter error: value={value}, arg={arg}, error={str(e)}")  # Debugging
        return 0