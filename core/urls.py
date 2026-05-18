from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('item/new/', views.item_create, name='item_create'),
]
