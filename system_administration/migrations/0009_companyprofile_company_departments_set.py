# Generated by Django 5.0.1 on 2024-02-06 14:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "system_administration",
            "0008_alter_companyprofile_company_country_location_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="companyprofile",
            name="company_departments_set",
            field=models.BooleanField(default=False),
        ),
    ]
