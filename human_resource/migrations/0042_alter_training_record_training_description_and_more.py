# Generated by Django 5.0.1 on 2024-02-23 09:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("human_resource", "0041_alter_staffprofile_bank_account_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="training_record",
            name="training_description",
            field=models.CharField(blank=True, default="", max_length=500),
        ),
        migrations.AlterField(
            model_name="training_record",
            name="training_title",
            field=models.CharField(blank=True, default="", max_length=100),
        ),
    ]