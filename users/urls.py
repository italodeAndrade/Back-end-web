from django.urls import path
from . import views
from .views import home
from filmes.views import user_logout

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/',views.login, name='login'),
    path('', home, name='home'),
    path('logout/', user_logout, name='logout'), 
]
