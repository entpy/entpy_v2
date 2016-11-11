from django import template

register = template.Library()

@register.filter
def str_cat(arg1, arg2):
    """Custom filter to concatenate arg1 with arg2"""
    return str(arg1) + str(arg2)

@register.filter
def get_item(dictionary, key):
    """Custom filter to retrieve a value from a dictionary"""
    return dictionary.get(key)
