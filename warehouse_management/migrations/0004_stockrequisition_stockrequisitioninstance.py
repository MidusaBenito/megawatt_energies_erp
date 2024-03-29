# Generated by Django 5.0.1 on 2024-01-21 17:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "human_resource",
            "0005_rename_payroll_sheet_for_the_month_off_payrollsheet_payroll_sheet_for_the_month_of_and_more",
        ),
        ("warehouse_management", "0003_inventory_minimum_stock_level_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="StockRequisition",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "stock_requisition_number",
                    models.CharField(max_length=50, unique=True),
                ),
                (
                    "stock_requisition_description",
                    models.CharField(default="", max_length=500),
                ),
                ("stock_requisition_approved", models.BooleanField(default=False)),
                ("recycle_bin", models.BooleanField(default=False)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("last_updated_on", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="stock_requisitions_created_by",
                        to="human_resource.staffprofile",
                    ),
                ),
                (
                    "last_updated_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="stock_requisitions_last_updated_by",
                        to="human_resource.staffprofile",
                    ),
                ),
                (
                    "warehouse",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="warehouse_stock_requisitions",
                        to="warehouse_management.warehouse",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StockRequisitionInstance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.CharField(default="0", max_length=15)),
                (
                    "stock_requisition_items_delivered",
                    models.BooleanField(default=False),
                ),
                ("recycle_bin", models.BooleanField(default=False)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("last_updated_on", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="stock_requisition_instances_created_by",
                        to="human_resource.staffprofile",
                    ),
                ),
                (
                    "last_updated_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="stock_requisition_instances_last_updated_by",
                        to="human_resource.staffprofile",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="product_stock_requisitions",
                        to="warehouse_management.product",
                    ),
                ),
                (
                    "stock_requisition",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="stock_requisition_instances",
                        to="warehouse_management.stockrequisition",
                    ),
                ),
            ],
        ),
    ]
