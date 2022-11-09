from django.contrib import admin, messages
from .models import Carrier, Product, Bill, BillPaid
from django.urls import path
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Creates the CSV uploader
class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()


# Create a filter for paid bills
class ProfileBillPaid(admin.ModelAdmin):
    list_filter = ("paidBool", "paidDate")


# Creates a filter for bills and a csv uploader
class ProfileBill(admin.ModelAdmin):
    list_filter = ("dueDate", "prodID", "carrierID")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path("upload-csv/", self.upload_csv),
        ]
        return new_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            # gets the csv file uploaded from upload-csv
            csv_file = request.FILES["csv_upload"]

            if not csv_file.name.endswith(".csv"):
                messages.warning(
                    request, "Incorrect file type was uploaded. Please use a CSV file."
                )
                return HttpResponseRedirect(request.path_info)

            # Formats the file to UTF-8 just incase
            file_data = csv_file.read().decode("utf-8")

            # Split the data into rows
            csv_data = file_data.split("\n")

            # Iterate line by line
            for data in csv_data:
                fields = data.split(",")

                # Relating foreign keys
                if data == "":
                    continue

                created = Bill.objects.create(
                    carrierID=Carrier.objects.get(carrierId=fields[0]),
                    billDate=fields[1],
                    dueDate=fields[2],
                    prodID=Product.objects.get(prodID=fields[3]),
                    charge=fields[4],
                    anc_fees=fields[5],
                    taxes=fields[6],
                    credit=fields[7],
                )
            url = reverse("admin:index")
            return HttpResponseRedirect(url)

        # department_id = Department.objects.get(password = password, department_name = department_name)
        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)


# Registers models here so we can view them on the admin site.
admin.site.register(Carrier)
admin.site.register(Product)
admin.site.register(Bill, ProfileBill)
admin.site.register(BillPaid, ProfileBillPaid)
