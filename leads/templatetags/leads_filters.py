from django import template

register = template.Library()


@register.filter
def get_tup_val(_tuple, index):
    """Get tuple value by index"""
    return _tuple[index]


@register.filter
def replace(comment):
    return comment.replace('-', '').replace('\\n', ' ').replace('\\r', '')
