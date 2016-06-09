from django import template

register = template.Library()

@register.filter(name='getit')
def getit(value, arg):
    if arg not in value:
        return 0
    return value[arg.strip()]

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)
