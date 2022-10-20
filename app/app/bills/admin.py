from django.contrib import admin
from .models import Carrier, Product, Bill, BillPaid

# Create a filter for paid bills
class ProfileBillPaid(admin.ModelAdmin):
    list_filter = ("paidBool", "paidDate")

# Creates a filter for bills
class ProfileBill(admin.ModelAdmin):
    list_filter = ("dueDate", "prodID", "carrierID")

# Registers models here so we can view them on the admin site.
admin.site.register(Carrier)
admin.site.register(Product)
admin.site.register(Bill, ProfileBill)
admin.site.register(BillPaid, ProfileBillPaid)
