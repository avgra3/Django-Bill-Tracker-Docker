from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core import serializers
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Sum, Count, Avg, Q, Count, Case, When, F, Func
from django.db.models.functions import TruncMonth
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
)
from django.urls import reverse_lazy

# Import users views
from users import views as user_views

# Models created
from .models import BillPaid, Carrier, Bill, Product

# Forms created
from .forms import NewBillForm, NewCarrierForm, NewProductForm

# Class to have output rounded, used for averages
class Round(Func):
    function = "ROUND"
    template = "%(function)s(%(expressions)s, 2)"


# Homepage view.
def homepage(request):
    # Shows any unpaid bills:
    unpaid = (
        BillPaid.objects.all().filter(paidBool=0).values("billID", "totalPaid", "notes")
    )

    # Shows summed amount for total due
    unpaid_total = BillPaid.objects.all().filter(paidBool=0).aggregate(Sum("totalPaid"))

    # Show previous 5 bills
    paid = BillPaid.objects.all().select_related("billID").order_by("-paidDate")[:5]

    # Group by, average each carrier type
    averages = (
        Bill.objects.select_related("carrierID")
        .values("carrierID")
        .annotate(avgCarrierAmount=Round(Avg(F("charge") + F("anc_fees") + F("taxes"))))
        .order_by("carrierID")
        .values("carrierID", "avgCarrierAmount")
    )

    carriers = (
        Carrier.objects.values("carrierId", "carrierName")
        .annotate(carrierID=F("carrierId"))
        .values("carrierID", "carrierName")
    )

    averages_dict = list(averages)
    carriers_dict = list(carriers)

    # Creates a list of dictionaries which combines the Averages and Carriers queries
    combined = []
    for i in range(len(averages_dict)):
        combined.append(averages_dict[i] | carriers_dict[i])
        print(combined)

    # Total average amount
    averages_total = (
        Bill.objects.values("carrierID")
        .annotate(avgCarrierAmount=Round(Avg(F("charge") + F("anc_fees") + F("taxes"))))
        .aggregate(Sum("avgCarrierAmount"))
    )

    context = {
        "unpaid": unpaid,
        "paid": paid,
        "unpaid_total": unpaid_total,
        "averages": averages,
        "averages_total": averages_total,
        "combinedAvg": combined,
    }
    return render(request, "bills/home.html", context=context)


# Average bill view
def AverageBillPaidView(request):
    # Get the running average billed amount for all bills
    runningAvg = BillPaid.objects.aggregate(Ravg=Avg("totalPaid"))

    # We want to get the average cost for each carrier/utility
    monthlyAvg = (
        BillPaid.objects.annotate(month=TruncMonth("paidDate"))
        .values("month")
        .annotate(a=Avg("totalPaid"))
        .values("month", "a")
        .order_by("month")
    )

    # Combines the two items we want to show in view
    context = {"runningAvg": runningAvg, "monthlyAvg": monthlyAvg}

    return render(
        request=request, template_name="bills/bills-avg.html", context=context
    )


# Monthly Breakdown view
# Create a view that summarizes the bills table
def MonthlyBreakdownListView(request):
    # Will return a grouped breakdown for each month
    context = (
        BillPaid.objects.annotate(month=TruncMonth("paidDate"))
        .values("month")
        .annotate(sums=Sum("totalPaid"))
        .values("month", "sums")
        .order_by("month")
    )

    return render(
        request=request, template_name="bills/bills-mb.html", context={"mb": context}
    )


""" Adding New Bills, Carriers, Products, etc. """


class BillCreateView(LoginRequiredMixin, CreateView):
    form_class = NewBillForm
    template_name = "bills/bill-form.html"

    login_url = "/login/"
    redirect_field_name = "redirect_to"

    success_url = reverse_lazy("bills/home.html")

    def form_valid(self, form):
        return super().form_valid(form)


class CarrierCreateView(LoginRequiredMixin, CreateView):
    form_class = NewCarrierForm
    template_name = "bills/carrier-form.html"

    login_url = "/login/"
    redirect_field_name = "redirect_to"

    success_url = reverse_lazy("bills/home.html")

    def form_valid(self, form):
        return super().form_valid(form)


class ProductCreateView(LoginRequiredMixin, CreateView):
    form_class = NewProductForm
    template_name = "bills/product-form.html"

    login_url = "/login/"
    redirect_field_name = "redirect_to"

    success_url = reverse_lazy("bills/home.html")

    def form_valid(self, form):
        return super().form_valid(form)


""" Listing all available bills in reverse order """


class BillListView(ListView):
    model = BillPaid
    # format: <app>/<model>_<viewtype>.html
    template_name = "bills/BillPaid_listview.html"
    context_object_name = "bills"
    ordering = ["paidDate"]


""" Paying unpaid bills """


class paidBillDetailView(LoginRequiredMixin, DetailView):
    model = BillPaid
    fields = "__all__"


class paidBillUpdateView(LoginRequiredMixin, UpdateView):
    model = BillPaid
    fields = "__all__"
    success_url = reverse_lazy("bills/home.html")

    login_url = "/login/"
    redirect_field_name = "redirect_to"

    def form_valid(self, form):
        return super().form_valid(form)
