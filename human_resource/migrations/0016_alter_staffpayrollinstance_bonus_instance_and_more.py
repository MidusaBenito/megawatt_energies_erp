# Generated by Django 5.0.1 on 2024-02-10 05:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("human_resource", "0015_staffpayrollinstance_commissions_total"),
    ]

    operations = [
        migrations.AlterField(
            model_name="staffpayrollinstance",
            name="bonus_instance",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="staff_bonuses",
                to="human_resource.bonusinstance",
            ),
        ),
        migrations.AlterField(
            model_name="staffpayrollinstance",
            name="deduction_instance",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="staff_deductions",
                to="human_resource.deductioninstance",
            ),
        ),
    ]
