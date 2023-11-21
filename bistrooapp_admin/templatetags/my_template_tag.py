from django import template

register = template.Library()

# siin failis on custom tag- saab kasutada html lehel muutuja väärtuse üleskorjamiseks ja kasutamiseks
# vt menuu_list.html
# https://pythoncircle.com/post/42/creating-custom-template-tags-in-django/
# https://pythoncircle.com/post/701/how-to-set-a-variable-in-django-template/
# https://docs.djangoproject.com/en/4.2/ref/templates/builtins/
# https://dev.to/anuragrana/for-loops-in-django-2jdi
# https://djangosnippets.org/snippets/2093/

@register.simple_tag
def setval(val=None):
    return val
