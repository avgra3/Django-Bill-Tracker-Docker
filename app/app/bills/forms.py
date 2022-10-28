from django import forms
from django.forms.widgets import DateInput
from django.forms import ValidationError

# Models created
from .models import BillPaid, Carrier, Bill, Product

# create a ModelForm
# , forms.Form
class NewBillForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Bill
        fields = "__all__"
        widgets = {
            "dueDate": forms.DateInput(
                format=("%d/%m/%Y"),
                attrs={
                    "class": "form-control",
                    "placeholder": "Please select a date",
                    "type": "date",
                },
            ),
            "billDate": forms.DateInput(
                format=("%d/%m/%Y"),
                attrs={
                    "class": "form-control",
                    "placeholder": "Please select a date",
                    "type": "date",
                },
            ),
        }


class NewCarrierForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Carrier
        fields = "__all__"


class NewProductForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Product
        fields = "__all__"


class UpdateBillForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = BillPaid
        fields = "__all__"
        widgets = {
            "paidDate": forms.DateInput(
                format=("%d/%m/%Y"),
                attrs={
                    "class": "form-control",
                    "placeholder": "Please select a date",
                    "type": "date",
                },
            ),
        }
