# Generated by Django 5.0.1 on 2024-02-19 09:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("human_resource", "0027_staffprofile_nhif_additional_info_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="staffprofile",
            name="basic_salary",
            field=models.CharField(blank=True, default="0.00", max_length=12),
        ),
    ]
