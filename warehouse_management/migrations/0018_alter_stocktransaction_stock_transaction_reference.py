# Generated by Django 5.0.1 on 2024-03-21 10:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("warehouse_management", "0017_alter_product_unit_of_measurement"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stocktransaction",
            name="stock_transaction_reference",
            field=models.CharField(blank=True, default="", max_length=50),
        ),
    ]