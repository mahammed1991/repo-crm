from django import template

register = template.Library()


@register.filter
def get_tup_val(_tuple, index):
    """Get tuple value by index"""
    return _tuple[index]
