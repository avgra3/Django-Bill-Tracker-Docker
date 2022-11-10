from django.contrib import admin, messages
from .models import Carrier, Product, Bill, BillPaid, AllBillDetail
from django.urls import path
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from import_export import resources
from import_export.admin import (
    ExportActionMixin,
    ImportExportActionModelAdmin,
    ImportExportModelAdmin,
)
from import_export.fields import Field

from import_export.widgets import ForeignKeyWidget

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


# Export class
class BillResource(resources.ModelResource):
    class Meta:
        model = Bill
        fields = (
            "billID",
            "carrierID",
            "billDate",
            "dueDate",
            "prodID",
            "charge",
            "anc_fees",
            "taxes",
            "credit",
        )

        # Order of columns on export
        export_order = fields

        # Uses Natural Foreign Keys
        use_natural_foreign_keys = True


class BillPaidResource(resources.ModelResource):
    class Meta:
        # Display Name
        name = "Import/Export Bills Paid"

        # Model we will refer to
        model = BillPaid
        # Fields we want to export
        fields = ("paidDate", "totalPaid", "notes", "billID_id")

        # Order of columns on export
        export_order = fields

        # Uses Natural Foreign Keys
        use_natural_foreign_keys = True


class AllBillDetailResource(resources.ModelResource):
    carrierName = Field(
        column_name="carrierName",
        attribute="carrier",
        widget=ForeignKeyWidget(Carrier, field="carrierName"),
    )

    productName = Field(
        column_name="product",
        attribute="product",
        widget=ForeignKeyWidget(Product, field="product"),
    )

    billDate = Field(
        column_name="billDate",
        attribute="bill",
        widget=ForeignKeyWidget(Bill, field="billDate"),
    )
    dueDate = Field(
        column_name="dueDate",
        attribute="bill",
        widget=ForeignKeyWidget(Bill, field="dueDate"),
    )
    charge = Field(
        column_name="charge", attribute="bill", widget=ForeignKeyWidget(Bill, "charge")
    )
    anc_fees = Field(
        column_name="anc_fees",
        attribute="bill",
        widget=ForeignKeyWidget(Bill, "anc_fees"),
    )
    taxes = Field(
        column_name="taxes", attribute="bill", widget=ForeignKeyWidget(Bill, "taxes")
    )
    credit = Field(
        column_name="credit", attribute="bill", widget=ForeignKeyWidget(Bill, "credit")
    )

    paidDate = Field(
        column_name="paidDate",
        attribute="paid",
        widget=ForeignKeyWidget(Bill, "paidDate"),
    )
    notes = Field(
        column_name="notes",
        attribute="paid",
        widget=ForeignKeyWidget(BillPaid, "notes"),
    )
    totalPaid = Field(
        column_name="totalPaid",
        attribute="paid",
        widget=ForeignKeyWidget(BillPaid, "totalPaid"),
    )

    class Meta:
        model = AllBillDetail
        import_id_fields = ["id"]
        fields = (
            "carrierName",
            "productName",
            "billDate",
            "dueDate",
            "paidDate",
            "notes",
            "charge",
            "anc_fees",
            "taxes",
            "credit",
            "totalPaid",
        )
        export_order = fields

    # def dehydrate_carrierName(self, AllBillDetail):
    #    pass  # return


# Custom Admin functionality
# ImportExportActionModelAdmin, ExportActionMixin,
class BillPaidAdmin(
    ImportExportModelAdmin, ImportExportActionModelAdmin, admin.ModelAdmin
):
    resource_classs = [BillPaidResource]


# ImportExportActionModelAdmin
class BillAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin, admin.ModelAdmin):
    resource_class = BillResource


class AllBillDetailAdmin(
    ImportExportModelAdmin, ImportExportActionModelAdmin, admin.ModelAdmin
):
    # list_display = ["carrierName", "paid", "product"]
    resource_class = AllBillDetailResource


# Registers models here so we can view them on the admin site.
admin.site.register(Carrier)
admin.site.register(Product)
admin.site.register(Bill, BillAdmin)
admin.site.register(BillPaid, BillPaidAdmin)
admin.site.register(AllBillDetail, AllBillDetailAdmin)
