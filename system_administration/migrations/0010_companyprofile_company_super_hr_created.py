# Generated by Django 5.0.1 on 2024-02-07 05:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("system_administration", "0009_companyprofile_company_departments_set"),
    ]

    operations = [
        migrations.AddField(
            model_name="companyprofile",
            name="company_super_hr_created",
            field=models.BooleanField(default=False),
        ),
    ]
