# Generated by Django 5.0.1 on 2024-03-20 07:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("procurement", "0005_stockorder_company_branch"),
    ]

    operations = [
        migrations.AddField(
            model_name="productpurchaseinstance",
            name="quantity_purchased",
            field=models.CharField(default="0", max_length=15),
        ),
    ]
