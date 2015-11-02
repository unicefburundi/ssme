from django import template

register = template.Library()

@register.filter(name='getit')
def getit(value, arg):
    return value[arg]
