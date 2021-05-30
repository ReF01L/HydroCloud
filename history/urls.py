from django.urls import path
from . import views

app_name = 'history'

urlpatterns = [
    path('', views.history, name='history'),
    path('all/', views.all_history, name='all_history'),
]
