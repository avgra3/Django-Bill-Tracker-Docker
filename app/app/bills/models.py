from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
# Creates the carriers table
class Carrier(models.Model):
    carrierId = models.AutoField(primary_key=True, editable=False)
    carrierName = models.CharField(max_length=40)
    carrierAcctNum = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.carrierName} - {self.carrierAcctNum}"

    class Meta:
        ordering = ["carrierName", "carrierAcctNum"]


# Creates the Products table
class Product(models.Model):
    prodID = models.AutoField(primary_key=True, editable=False)
    product = models.CharField(max_length=80)

    def __str__(self):
        return self.product

    class Meta:
        ordering = ["product"]


# Creates the bills table
class Bill(models.Model):
    billID = models.IntegerField(
        primary_key=True,
        validators=[MinValueValidator(1), MaxValueValidator(10000)],
        editable=False,
    )
    carrierID = models.ForeignKey(
        Carrier, on_delete=models.CASCADE, verbose_name="Related Carrier"
    )
    billDate = models.DateField(verbose_name="Billed Date")
    dueDate = models.DateField(verbose_name="Due Date")
    prodID = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="related product"
    )
    charge = models.DecimalField(max_digits=65, decimal_places=2)
    anc_fees = models.DecimalField(
        max_digits=65, decimal_places=2, verbose_name="Ancilliary Fees"
    )
    taxes = models.DecimalField(max_digits=65, decimal_places=2)
    credit = models.DecimalField(max_digits=65, decimal_places=2)

    def dates(self):
        date = self.dueDate.strftime("%b %y")
        return date

    def __str__(self):
        date = self.dueDate.strftime("%b %y")
        return f"{self.carrierID} - {date}"

    class Meta:
        ordering = ["billDate"]


# Creates the Bills Paid table
class BillPaid(models.Model):
    def id_default():
        id = self.paidID.max()
        return id

    paidID = models.IntegerField(
        primary_key=True,
        validators=[MinValueValidator(1), MaxValueValidator(10000)],
        verbose_name="Paid ID",
        editable=False,
    )
    paidDate = models.DateField(verbose_name="Date Paid", null=True, blank=True)
    billID = models.ForeignKey(
        Bill, on_delete=models.CASCADE, verbose_name="related bill"
    )
    notes = models.CharField(max_length=100, default="N/A", verbose_name="Notes")
    paidBool = models.BooleanField(verbose_name="Paid (True or False)")
    totalPaid = models.DecimalField(
        max_digits=65, decimal_places=2, verbose_name="Total Paid"
    )

    def __str__(self):
        return f"{self.paidID}"

    def dates(self):
        date = self.dueDate.strftime("%b %y")
        return date

    class Meta:
        ordering = ["paidDate", "billID"]


# Combined All Tables
class AllBillDetail(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, verbose_name="bill")
    paid = models.ForeignKey(BillPaid, on_delete=models.CASCADE, verbose_name="paid")
    carrier = models.ForeignKey(
        Carrier, on_delete=models.CASCADE, verbose_name="carrier"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="product"
    )

    def __str__(self):
        return f"{self.paid} - {self.carrier}"

    class Meta:
        ordering = ["bill", "carrier", "product", "paid"]
