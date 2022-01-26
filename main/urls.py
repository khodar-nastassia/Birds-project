from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'), #name для редиректа
    path('birds', views.BirdsList.as_view(), name='birds'),
    path('add_bird', views.AddBird.as_view(), name='add_bird'),
    path('contacts', views.ContactFormView.as_view(), name='contacts'),
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.RegisterUser.as_view(), name='register'),
    path('birds/<slug:bird_slug>', views.ShowBird.as_view(), name='bird'),
    path('category/<slug:cat_slug>', views.CategoryList.as_view(), name='category'),
    path('social-auth/', include('social_django.urls', namespace="social"))
]
