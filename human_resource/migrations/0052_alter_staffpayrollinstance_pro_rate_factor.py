# Generated by Django 5.0.1 on 2024-03-03 17:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("human_resource", "0051_staffpayrollinstance_pro_rate_factor"),
    ]

    operations = [
        migrations.AlterField(
            model_name="staffpayrollinstance",
            name="pro_rate_factor",
            field=models.CharField(default="1.00", max_length=12),
        ),
    ]
