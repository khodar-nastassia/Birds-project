from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView

from .forms import *
from .models import *
from .utils import *


def index(request): #Функция-представления главной страницы
    '''Представление главной страницы'''
    cats = CategoryOfBirds.objects.all()    
    context = {        
        'menu': menu,
        'cats': cats,
        'title': 'Главная страница',
        'cat_selected': 0,
    } #определение переменных для шаблона
    return render(request, 'main/index.html', context=context)


class BirdsList(DataMixin,ListView):
    '''Класс-представление для отображения всех птиц'''

    model = Birds #используемая модель
    template_name = 'main/birds.html' #имя шаблона
    context_object_name = 'birds' #имя переменной для отображения птиц в шаблоне

    def get_context_data(self, *,object_list=None, **kwargs):
        '''Формирование динамического и статического контекста'''
        context = super().get_context_data(**kwargs) #обращение к базовому классу ListView для получени уже существующего контекста
        c_def = self.get_user_context(title="Птицы") #контекст из DataMixin
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Birds.objects.all().select_related('cat') #select_related сжатый запрос для оптимизации


class AddBird(LoginRequiredMixin,DataMixin,CreateView): 
    '''Класс-представление для формы добавления птицы'''

    form_class = AddBirdForm #используемая форма
    template_name = 'main/add_bird.html' #имя шаблона
    login_url = reverse_lazy('birds') #адрес перенаправления для незарегистрированного пользователя
    raise_exception = True

    def get_context_data(self, *,object_list=None, **kwargs):
        '''Формирование динамического и статического контекста'''
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление птицы")
        return dict(list(context.items()) + list(c_def.items()))


class ContactFormView(DataMixin,FormView):
    '''Класс-представление для формы с контактами'''
    form_class = ContactForm
    template_name = 'main/contacts.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, *,object_list=None, **kwargs):
        '''Формирование динамического и статического контекста'''
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Контакты")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        '''При успешном заполнении пользователь переходит на главную страницу'''
        print(form.cleaned_data)
        return redirect('index')


class ShowBird(DataMixin,DetailView):
    '''Класс-представление для  отбражения подробной информации о птице'''

    model = Birds
    template_name = 'main/show_bird.html'
    slug_url_kwarg = 'bird_slug' #переменная для слага в url
    context_object_name = 'bird' #имя переменной для отображения птиц в шаблоне

    def get_context_data(self, *,object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['bird'])
        return dict(list(context.items()) + list(c_def.items()))


class CategoryList(DataMixin,ListView):
    '''Класс-представление для категорий птиц'''

    model = Birds
    template_name = 'main/birds.html'
    context_object_name = 'birds'
    allow_empty = False #если слага нет, то исключение 404

    def get_queryset(self):
        '''Выбрать только категории по указанному слагу'''
        return Birds.objects.filter(cat__slug = self.kwargs['cat_slug']).select_related('cat') #select_related сжатый запрос для оптимизации

    def get_context_data(self, *,object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = CategoryOfBirds.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - '+ str(c.category),
                                      cat_selected=c.pk) 
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin,CreateView):
    '''Класс-представление для регистрации пользователя'''

    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *,object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        '''При успешной регистрации пользователь сразу авторизуется'''
        user = form.save()
        login(self.request, user)
        return redirect('birds')


class LoginUser(DataMixin,LoginView):
    '''Класс-представление для входа пользователя'''
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_context_data(self, *,object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self): 
        '''Переход на главную страницу после успешного входа'''
        return reverse_lazy('index')


def logout_user(request):
    logout(request)
    return redirect('login')


def pageNotFound(request, exception):
    '''Страница не найдена'''
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
