from django.urls import path
from . import views
from .views import home

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/',views.login, name='login'),
    path('', home, name='home'),
]
