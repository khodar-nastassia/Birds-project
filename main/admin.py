from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class BirdsAdmin(admin.ModelAdmin):
    '''Отображение нужных полей из модели Birds в админке, настройка'''
    list_display = ('id', 'name', 'description', 'get_html_photo') #список отображаемых полей
    list_display_links = ('id', 'name') #поля для прехода по ссылке для редактирования
    search_fields = ('name', 'description') #поля для поиска
    list_filter = ('cat',) #поля для фильтра
    prepopulated_fields = {"slug": ("name",)} #автоматическое заполнение слага по названию птицы в админке

    def get_html_photo(self,object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = "Фото"

class CategoryOfBirdsAdmin(admin.ModelAdmin):
    '''Отображение нужных полей из модели CategoryOfBirds в админке, настройка'''
    list_display = ('id', 'category')
    list_display_links = ('id', 'category')
    search_fields = ('category',)
    prepopulated_fields = {"slug": ("category",)}

admin.site.register(Birds, BirdsAdmin) #регистрация модели Birds в админ-панели
admin.site.register(CategoryOfBirds, CategoryOfBirdsAdmin) #регистрация модели CategoryOfBirds в админ-панели
