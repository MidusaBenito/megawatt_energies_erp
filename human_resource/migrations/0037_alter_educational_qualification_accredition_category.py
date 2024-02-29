# Generated by Django 5.0.1 on 2024-02-22 08:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("human_resource", "0036_staffprofile_banking_institution_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="educational_qualification",
            name="accredition_category",
            field=models.CharField(
                choices=[
                    ("not_selected", "Not Selected"),
                    ("phd", "PhD"),
                    ("masters", "Masters"),
                    ("bachelors", "Bachelors"),
                    ("diploma", "Diploma"),
                    ("certificate", "Certificate"),
                    ("other", "Other"),
                ],
                default="not_selected",
                max_length=20,
            ),
        ),
    ]
