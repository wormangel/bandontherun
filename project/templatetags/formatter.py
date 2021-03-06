from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter
def currency(number):
    number = float(number)
    return "$ %s%s" % (intcomma(int(number)), ("%0.2f" % number)[-3:])
        
@register.filter
def yes_no(boolean):
    return 'Yes' if boolean == True else 'No'

