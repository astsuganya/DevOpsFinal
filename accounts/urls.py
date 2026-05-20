from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('password/change/', views.change_password, name='change_password'),
    path('delete/', views.delete_account, name='delete_account'),
    path('register/', views.register, name='register'),
]
