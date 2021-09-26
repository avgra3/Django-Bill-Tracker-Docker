from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core import serializers
from django.views.generic import ListView
from django.db.models import Sum, Count, Avg, Q, Count, Case, When, F
from django.db.models.functions import TruncMonth

# Models created
from .models import BillPaid, Carrier, Bill

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


