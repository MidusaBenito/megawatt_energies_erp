# Generated by Django 5.0.1 on 2024-02-17 17:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("human_resource", "0022_bonus_bonus_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bonus",
            name="bonus_title",
            field=models.CharField(default="", max_length=100),
        ),
        migrations.AlterField(
            model_name="deduction",
            name="deduction_title",
            field=models.CharField(default="", max_length=100),
        ),
    ]
