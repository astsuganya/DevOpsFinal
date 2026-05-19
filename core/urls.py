from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('lost/', views.item_list_lost, name='item_list_lost'),
    path('found/', views.item_list_found, name='item_list_found'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('item/new/', views.item_create, name='item_create'),
    path('item/<int:pk>/edit/', views.item_update, name='item_update'),
    path('item/<int:pk>/delete/', views.item_delete, name='item_delete'),
    path('comment/<int:pk>/edit/', views.comment_edit, name='comment_edit'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
    path('comment/<int:pk>/reply/', views.comment_reply, name='comment_reply'),
]
