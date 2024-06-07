from django.urls import path
from control import views


urlpatterns = [
    path('', views.index, name='index'),
]