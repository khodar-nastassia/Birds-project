from django.db import models
from django.urls import reverse


class Birds(models.Model): #Модель с информацией о птицах
    name = models.CharField(max_length=50, verbose_name='Название птицы')# тип поля Charfield,verbose_name - для отображения в админке 
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name= "URL")
    photo = models.ImageField(upload_to="photos", default='', verbose_name='Фото') #поле хранит ссылку на фото, upload_tо указывает, в какие катологи загружать фото
    description = models.TextField(verbose_name='Описание')
    audio = models.FileField(upload_to="audio", default='', verbose_name='Аудио') #поле хранит ссылку на аудио, upload_tо указывает, в какие катологи загружать аудио 
    cat = models.ForeignKey('CategoryOfBirds', on_delete=models.PROTECT, verbose_name='Категория') #(первичная модель, on_deletе-ограничени при удалении: запрещает удаление записи ))

    def __str__(self):
        '''Выводит название птицы'''
        return self.name

    class Meta:
        '''Класс для отображения названий в админ-панели'''
        verbose_name = 'Птицы'
        verbose_name_plural = 'Птицы'
        ordering = ['name'] #Сортировка по названию птицы

    def get_absolute_url(self):
        '''Формирование маршрута к конкретной записи в таблице Birds'''
        return reverse('bird', kwargs={'bird_slug': self.slug})

class CategoryOfBirds(models.Model): #Таблица с категориями птиц, первичная модель
    category = models.CharField(verbose_name='Категория', max_length=50)
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name= "URL")

    def __str__(self):
        '''Выводит название категории птиц'''
        return self.category

    class Meta:
        '''Класс для отображения названий в админ-панели'''
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['category'] 

    def get_absolute_url(self):
        '''Формирование маршрута к конкретной записи в таблице CategoryOfBirds'''
        return reverse('category', kwargs={'cat_slug': self.slug})
