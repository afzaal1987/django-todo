from django.urls import path
from . import views

app_name = 'todos'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:vm_id>/control/', views.control_vm, name='control_vm'),
]