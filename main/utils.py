from django.core.cache import cache

from .models import *


menu = [{'title': 'Главная страница', 'url_name': 'index'},
        {'title': 'Птицы', 'url_name': 'birds'},       
        {'title': 'Добавить птицу', 'url_name': 'add_bird'},
        {'title': 'Контакты', 'url_name': 'contacts'},
]


class DataMixin:
    paginate_by = 3 # пагинация по 3 птицы на странице
    def get_user_context(self, **kwargs):
        '''Формирует контекст по умолчанию'''
        context = kwargs
        cats = cache.get('cats')
        if not cats:
            cats = CategoryOfBirds.objects.all()
            cache.set('cats', cats, 60)     
        context['menu'] = menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
