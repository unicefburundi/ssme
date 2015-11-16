from django import template

register = template.Library()

@register.filter(name='getit')
def getit(value, arg):
    return value[arg]

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)
