# Generated by Django 5.0.1 on 2024-02-16 16:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "human_resource",
            "0018_rename_bonuses_value_bonusinstance_bonus_instance_value_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="staffleave",
            name="leave_active_status",
        ),
        migrations.AddField(
            model_name="staffleave",
            name="leave_status",
            field=models.CharField(
                choices=[
                    ("sick_leave", "Sick Leave"),
                    ("vacation_leave", "Vacation Leave"),
                    ("maternity_leave", "Maternity Leave"),
                    ("paternity_leave", "Paternity Leave"),
                    ("medical_leave", "Medical Leave"),
                    ("bereavement_leave", "Bereavement Leave"),
                    ("other", "Other"),
                    ("not_selected", "Not Selected"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="staffprofile",
            name="first_name",
            field=models.CharField(default="", max_length=50),
        ),
        migrations.AlterField(
            model_name="staffprofile",
            name="last_name",
            field=models.CharField(default="", max_length=50),
        ),
    ]
