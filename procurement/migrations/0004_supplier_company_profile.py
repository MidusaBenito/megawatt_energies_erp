# Generated by Django 5.0.1 on 2024-01-28 21:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("procurement", "0003_supplier_user"),
        ("system_administration", "0006_companydepartment_company_profile_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="supplier",
            name="company_profile",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="company_suppliers",
                to="system_administration.companyprofile",
            ),
        ),
    ]
