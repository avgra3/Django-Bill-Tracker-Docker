from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='pages/home.html'),
    path('avg/', views.AverageBillPaidView, name='bills-avg'),
]