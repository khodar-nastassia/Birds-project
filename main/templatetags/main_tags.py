from django import template
from main.models import *

'''Создание пользовательского тэга'''

register = template.Library()

@register.simple_tag(name='getcats')
def get_categories():
    '''Возвращает все категории птиц'''
    return CategoryOfBirds.objects.all()