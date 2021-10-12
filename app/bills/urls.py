from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', views.homepage, name='pages/home.html'),
    path('avg/', views.AverageBillPaidView, name='bills-avg'),
    path('mb/', views.MonthlyBreakdownListView, name='bills-mb'),
    path('bills/bills/', BillListView.as_view(), name='bills-paid'),
    path('bills/create/bill/', BillCreateView.as_view(), name='bills-create-bill'),
    path('bills/create/product/', ProductCreateView.as_view(), name='bills-create-product'),
    path('bills/create/carrier/', CarrierCreateView.as_view(), name='bills-create-carrier'),
]