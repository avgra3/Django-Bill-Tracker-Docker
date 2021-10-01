from django import forms
# Models created
from .models import BillPaid, Carrier, Bill, Product

# create a ModelForm
class NewBillForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Bill
        fields = "__all__"

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


