from django import template

register = template.Library()


@register.filter
def in_list(var, list_obj):
    """Check if var in list"""
    return var in list_obj


@register.filter
def concatenate(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def get_dict_val(dictionary, key):
    """Get dictionary value by key"""
    return dictionary.get(key)


@register.filter
def get_range(value, start=0):
    return range(start, value)


@register.filter
def either(value1, value2):
    return value1 or value2


@register.filter
def get_range_specific(value, end_val):
    return range(value, int(end_val))
