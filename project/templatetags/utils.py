from django import template

register = template.Library()

# Takes one object, insert it into a list, returns the list
@register.filter
def listify(obj):
    list = []
    list.append(obj)
    return list