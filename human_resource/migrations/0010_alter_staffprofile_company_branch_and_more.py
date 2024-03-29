# Generated by Django 5.0.1 on 2024-01-28 19:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("human_resource", "0009_alter_staffprofile_user"),
        ("system_administration", "0006_companydepartment_company_profile_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="staffprofile",
            name="company_branch",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="company_branch_staffs",
                to="system_administration.companybranch",
            ),
        ),
        migrations.AlterField(
            model_name="staffprofile",
            name="company_department",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="company_department_staffs",
                to="system_administration.companydepartment",
            ),
        ),
    ]
