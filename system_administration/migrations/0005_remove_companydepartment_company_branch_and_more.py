# Generated by Django 5.0.1 on 2024-01-20 22:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("system_administration", "0004_systemadmincreationstatus"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="companydepartment",
            name="company_branch",
        ),
        migrations.AlterField(
            model_name="companyprofile",
            name="company_profile_set",
            field=models.BooleanField(default=False),
        ),
    ]
