# Generated by Django 5.0.1 on 2024-01-20 22:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("human_resource", "0003_payrollsheet_company_branch"),
    ]

    operations = [
        migrations.AddField(
            model_name="staffprofile",
            name="has_read_write_priviledges",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="staffprofile",
            name="is_super_admin",
            field=models.BooleanField(default=False),
        ),
    ]