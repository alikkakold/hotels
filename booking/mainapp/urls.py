from django.urls import path
from mainapp import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.main_page, name='main'),
    path('404/', mainapp.error_404, name='404'),
]
