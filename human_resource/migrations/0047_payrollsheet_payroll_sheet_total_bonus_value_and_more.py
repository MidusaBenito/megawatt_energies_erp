# Generated by Django 5.0.1 on 2024-02-26 09:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("human_resource", "0046_alter_staffbonusscheme_bonus_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="payrollsheet",
            name="payroll_sheet_total_bonus_value",
            field=models.CharField(default="0.00", max_length=15),
        ),
        migrations.AddField(
            model_name="payrollsheet",
            name="payroll_sheet_total_commission_value",
            field=models.CharField(default="0.00", max_length=15),
        ),
        migrations.AddField(
            model_name="payrollsheet",
            name="payroll_sheet_total_deduction_value",
            field=models.CharField(default="0.00", max_length=15),
        ),
        migrations.AddField(
            model_name="payrollsheet",
            name="payroll_sheet_total_net_pay_value",
            field=models.CharField(default="0.00", max_length=15),
        ),
    ]
