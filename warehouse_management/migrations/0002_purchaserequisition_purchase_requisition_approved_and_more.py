# Generated by Django 5.0.1 on 2024-01-14 21:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("warehouse_management", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="purchaserequisition",
            name="purchase_requisition_approved",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="purchaserequisitioninstance",
            name="purchase_requisition_items_purchased",
            field=models.BooleanField(default=False),
        ),
    ]
