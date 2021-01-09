from django.urls import path
from . views import home, about, contact_us

app_name = 'dashboard'
urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact_us/', contact_us, name='contact_us'),
]