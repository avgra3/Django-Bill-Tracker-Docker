from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core import serializers
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Sum, Count, Avg, Q, Count, Case, When, F
from django.db.models.functions import TruncMonth
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Models created
from .models import BillPaid, Carrier, Bill, Product

# Forms created
from .forms import NewBillForm, NewCarrierForm, NewProductForm

# Homepage view.
def homepage(request):
    # Shows any unpaid bills:
    unpaid = BillPaid.objects.all().filter(paidBool=0).values('billID', 'totalPaid', 'notes')
    
    # Shows summed amount for total due
    unpaid_total = BillPaid.objects.all().filter(paidBool=0).aggregate(Sum('totalPaid'))
    
    # Show previous 5 bills
    paid = BillPaid.objects.all().select_related('billID').order_by('-paidDate')[:5]

    context = {"unpaid": unpaid, "paid":paid, "unpaid_total": unpaid_total}
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

""" Adding New Bills, Carriers, Products, etc. """
class BillCreateView(LoginRequiredMixin, CreateView):
    model = Bill
    fields = "__all__"
    template_name = 'pages/bill-form.html'

    def form_valid(self, form):
        return redirect('bills-paid')

class CarrierCreateView(LoginRequiredMixin, CreateView):
    model = Carrier
    fields = "__all__"
    template_name = 'pages/carrier-form.html'

    def form_valid(self, form):
        return redirect('pages/home.html')

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = "__all__"
    template_name = 'pages/product-form.html'

    def form_valid(self, form):
        return redirect('pages/home.html')

""" Listing all available bills in reverse order """
class BillListView(ListView):
    model = BillPaid
    # format: <app>/<model>_<viewtype>.html
    template_name = 'pages/BillPaid_listview.html'
    context_object_name = 'bills'
    ordering = ['-paidDate']

