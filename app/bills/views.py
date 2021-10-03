from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core import serializers
from django.views.generic import ListView, DetailView
from django.db.models import Sum, Count, Avg, Q, Count, Case, When, F
from django.db.models.functions import TruncMonth
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Models created
from .models import BillPaid, Carrier, Bill

# Forms created
from .forms import NewBillForm, NewCarrierForm, NewProductForm

# Homepage view.
def homepage(request):
    # Shows any unpaid bills:
    unpaid = BillPaid.objects.all().filter(paidBool=0).values('billID', 'totalPaid', 'notes')
    
    # Show previous 5 bills
    paid = BillPaid.objects.all().select_related('billID').order_by('-paidDate')[:5]

    context = {"unpaid": unpaid, "paid":paid}
    return render(request, 'pages/home.html', context=context)

# Average bill view
def AverageBillPaidView(request):
    # Get the running average billed amount for all bills
    runningAvg = BillPaid.objects.aggregate(Ravg=Avg('totalPaid'))

    # We want to get the average cost for each carrier/utility
    monthlyAvg = BillPaid.objects.annotate(month=TruncMonth('paidDate')).values('month').annotate(a = Avg('totalPaid')).values('month', 'a').order_by('month')

    # Combines the two items we want to show in view
    context = {"runningAvg": runningAvg,  "monthlyAvg": monthlyAvg}

    return render(request = request, template_name='pages/bills-avg.html', context=context)

# Monthly Breakdown view
# Create a view that summarizes the bills table
def MonthlyBreakdownListView(request):
    # Will return a grouped breakdown for each month
    context = BillPaid.objects.annotate(month=TruncMonth('paidDate')).values('month').annotate(sums=Sum('totalPaid')).values('month','sums').order_by('month')
    
    return render(request = request, template_name='pages/bills-mb.html', context={"mb": context})

# New Bill Form view
def NewBillView(request):
    context = NewBillForm()
    return render(request = request, template_name='pages/bills-bill-form.html', context={"form":context})

# New Carrier Form view
def NewCarrierView(request):
    context = NewCarrierForm()
    return render(request = request, template_name='pages/bills-carrier-form.html', context={"form":context})

# New Product Form view
def NewProductView(request):
    context = NewProductForm()
    return render(request = request, template_name='pages/bills-product-form.html', context={"form":context})

"""
Detail view to see more details of the bill...
"""
class BillListView(ListView):
    model = BillPaid
    # format: <app>/<model>_<viewtype>.html
    template_name = 'pages/BillPaid_listview.html'
    context_object_name = 'bills'
    ordering = ['-paidDate']