from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'account'

urlpatterns = [
    path('', TemplateView.as_view(template_name='landing.html'), name='landing'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='logout'),
    path('check_code/', views.code, name='code'),
    path('profile/', views.profile, name='profile'),
    path('create_image/', views.create_image, name='create_image'),
    path('file/', views.get_file, name='get_file'),
    path('all_results/', views.get_all_results, name='all_results'),
]
