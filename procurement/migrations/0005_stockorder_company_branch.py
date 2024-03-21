# Generated by Django 5.0.1 on 2024-03-19 06:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("procurement", "0004_supplier_company_profile"),
        ("system_administration", "0011_alter_companyprofile_company_serial_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="stockorder",
            name="company_branch",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="branch_stock_orders",
                to="system_administration.companybranch",
            ),
        ),
    ]