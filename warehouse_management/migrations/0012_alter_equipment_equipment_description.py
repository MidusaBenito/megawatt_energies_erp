# Generated by Django 5.0.1 on 2024-03-15 21:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "warehouse_management",
            "0011_alter_stocktransactioninstance_stock_transaction",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="equipment",
            name="equipment_description",
            field=models.CharField(blank=True, default="", max_length=500),
        ),
    ]
