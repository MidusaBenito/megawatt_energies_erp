# Generated by Django 5.0.1 on 2024-01-21 17:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("human_resource", "0004_staffprofile_has_read_write_priviledges_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="payrollsheet",
            old_name="payroll_sheet_for_the_month_off",
            new_name="payroll_sheet_for_the_month_of",
        ),
        migrations.AddField(
            model_name="payrollsheet",
            name="payroll_sheet_for_the_year",
            field=models.CharField(default="2024", max_length=15),
        ),
    ]
