from django import template

register = template.Library()

@register.filter(name='getit')
def getit(value, arg):
    # import ipdb; ipdb.set_trace()
    return value[arg]
