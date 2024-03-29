# Generated by Django 5.0.1 on 2024-02-08 12:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("human_resource", "0010_alter_staffprofile_company_branch_and_more"),
        ("system_administration", "0010_companyprofile_company_super_hr_created"),
    ]

    operations = [
        migrations.AddField(
            model_name="staffposition",
            name="company_profile",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="company_staff_positions",
                to="system_administration.companyprofile",
            ),
        ),
    ]
