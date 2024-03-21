# Generated by Django 5.0.1 on 2024-03-07 05:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("system_administration", "0011_alter_companyprofile_company_serial_number"),
        ("warehouse_management", "0007_alter_warehouse_company_branch"),
    ]

    operations = [
        migrations.AlterField(
            model_name="warehouse",
            name="company_branch",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="branch_warehouses",
                to="system_administration.companybranch",
            ),
        ),
    ]
