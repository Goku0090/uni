from django import template

register = template.Library()

@register.filter(name='split')
def split(value, arg):
    """Split a string by the given separator"""
    if value:
        return value.split(arg)
    return []

@register.filter(name='get_item')
def get_item(dictionary, key):
    """Get an item from a dictionary"""
    if dictionary and key:
        return dictionary.get(key)
    return None

@register.filter(name='strip')
def strip(value):
    """Strip whitespace from a string"""
    if value:
        return value.strip()
    return value
