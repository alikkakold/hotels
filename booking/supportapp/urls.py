from django.urls import path
from supportapp import views as supportapp

app_name = 'supportapp'

urlpatterns=[
    path('problem/', supportapp.new_problem, name="problem")
]