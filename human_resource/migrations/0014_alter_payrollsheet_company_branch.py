# Generated by Django 5.0.1 on 2024-02-09 09:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("human_resource", "0013_alter_deduction_deduction_module_and_more"),
        ("system_administration", "0010_companyprofile_company_super_hr_created"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payrollsheet",
            name="company_branch",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="branch_payroll_sheets",
                to="system_administration.companybranch",
            ),
        ),
    ]
