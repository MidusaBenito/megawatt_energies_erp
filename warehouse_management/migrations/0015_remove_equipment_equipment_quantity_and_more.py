# Generated by Django 5.0.1 on 2024-03-17 10:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("warehouse_management", "0014_equipment_equipment_quantity"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="equipment",
            name="equipment_quantity",
        ),
        migrations.AddField(
            model_name="equipment",
            name="equipment_serial_number",
            field=models.CharField(default="", max_length=50),
        ),
        migrations.AlterField(
            model_name="equipment",
            name="equipment_name",
            field=models.CharField(default="", max_length=100),
        ),
    ]