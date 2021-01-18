from django.urls import path
from .views import register, login_view


app_name = 'authenticate'
urlpatterns = [
    path('register/', register, name='register'),
    path('authentication/', login_view, name='login')
]
