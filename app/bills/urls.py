from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='pages/home.html'),
    path('avg/', views.AverageBillPaidView, name='bills-avg'),
    path('mb/', views.MonthlyBreakdownListView, name='bills-mb'),
    path('new-bill/', views.NewBillView, name='bills-bill-form'),
    path('new-carrier/', views.NewCarrierView, name='bills-carrier-form'),
    path('new-product/', views.NewProductView, name='bills-product-form'),
]