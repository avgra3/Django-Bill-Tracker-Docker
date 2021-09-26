# Generated by Django 3.2.7 on 2021-09-26 19:29

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('billID', models.IntegerField(editable=False, primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10000)])),
                ('billDate', models.DateField(verbose_name='Billed Date')),
                ('dueDate', models.DateField(verbose_name='Due Date')),
                ('charge', models.DecimalField(decimal_places=2, max_digits=65)),
                ('anc_fees', models.DecimalField(decimal_places=2, max_digits=65, verbose_name='Ancilliary Fees')),
                ('taxes', models.DecimalField(decimal_places=2, max_digits=65)),
                ('credit', models.DecimalField(decimal_places=2, max_digits=65)),
            ],
            options={
                'ordering': ['billDate'],
            },
        ),
        migrations.CreateModel(
            name='Carrier',
            fields=[
                ('carrierId', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('carrierName', models.CharField(max_length=40)),
                ('carrierAcctNum', models.CharField(max_length=80)),
            ],
            options={
                'ordering': ['carrierName', 'carrierAcctNum'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('prodID', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('product', models.CharField(max_length=80)),
            ],
            options={
                'ordering': ['product'],
            },
        ),
        migrations.CreateModel(
            name='BillPaid',
            fields=[
                ('paidID', models.IntegerField(editable=False, primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10000)], verbose_name='Paid ID')),
                ('paidDate', models.DateField(blank=True, null=True, verbose_name='Date Paid')),
                ('notes', models.CharField(default='N/A', max_length=100, verbose_name='Notes')),
                ('paidBool', models.BooleanField(verbose_name='Paid (True or False)')),
                ('totalPaid', models.DecimalField(decimal_places=2, max_digits=65, verbose_name='Total Paid')),
                ('billID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bills.bill', verbose_name='related bill')),
            ],
            options={
                'ordering': ['paidDate', 'billID'],
            },
        ),
        migrations.AddField(
            model_name='bill',
            name='carrierID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bills.carrier', verbose_name='Related Carrier'),
        ),
        migrations.AddField(
            model_name='bill',
            name='prodID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bills.product', verbose_name='related product'),
        ),
    ]
