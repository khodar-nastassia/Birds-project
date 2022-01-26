from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *


class AddBirdForm(forms.ModelForm):
    '''Форма связана с моделью'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) #конструктор базового класса для доступа к свойствам
        self.fields['cat'].empty_label = "Категория не выбрана" #прописываем категория не выбрана вместо -----

    class Meta:
        model = Birds #форма связана с моделью Birds 
        fields = '__all__' #отобразить все поля
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        } #стили для указанных полей

    def clean_name(self): #пользовательский валидатор на количество символов в названии птицы
        name = self.cleaned_data['name']
        if len(name) > 40:
            raise ValidationError('Длина превышает 40 символов')
        return name


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'cols':60, 'rows': 10}))
