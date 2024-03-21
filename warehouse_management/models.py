from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import re
from human_resource.models import StaffProfile

from system_administration.models import CompanyBranch, CompanyProfile

class Warehouse(models.Model):
    company_branch = models.ForeignKey(
        CompanyBranch, null=True, on_delete=models.SET_NULL,related_name="branch_warehouses")
    warehouse_name = models.CharField(max_length=50, default="", unique=True)
    warehouse_location = models.CharField(
        max_length=50, default="",)
    warehouse_capacity = models.CharField(
        max_length=12, default="0",)#capacity in square feet
    warehouse_contact_phone = models.CharField(
        max_length=25, default="", blank=False)
    warehouse_description = models.CharField(
        max_length=500, default="",blank=True)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="warehouse_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="warehouse_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

# created by warehouse staff at the main branch
class Category(models.Model):
    category_name = models.CharField(max_length=50, default="", unique=True)
    category_description = models.CharField(
        max_length=500, default="", blank=True)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="category_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="category_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        # ordering= ("first_name", "last_name",)
        verbose_name = "Category"
        verbose_name_plural = "Categories"


#created by warehouse staff at the main branch
class Product(models.Model):
    category=models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL, related_name="category_products")
    product_name = models.CharField(max_length=50, default="", unique=True)
    stock_keeping_unit = models.CharField(
        max_length=20, default="", unique=True)
    measurement_choices = [
        ("kilowatts", "Kilowatts"), ("piece", "Piece"), ("box", "Box"), ("pallet", "Pallet"), ("metre", "Metre"), ("kg", "Kg"), ("litre", "Litre"), ("other", "Other"), ("not_selected", "Not Selected")]
    unit_of_measurement = models.CharField(
        max_length=20, choices=measurement_choices,default="not_selected",)
    product_description = models.CharField(
        max_length=500, default="", blank=True)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="product_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="product_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.pk:
            # numberReg = re.sub(
            #     r'[^0-9]', '', self.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
            numberReg = re.sub(
                r'[^0-9]', '', self.timestamp.strftime('%Y-%d %H:%M:%S'))
            self.stock_keeping_unit = 'SKU'+ numberReg
        super().save(*args, **kwargs)

class Inventory(models.Model):  #inventory is unique for every branch
    product = models.ForeignKey(
        Product, null=True, on_delete=models.SET_NULL, related_name="product_inventories")
    warehouse = models.ForeignKey(
        Warehouse, null=True, on_delete=models.SET_NULL, related_name="warehouse_inventories")
    quantity = models.CharField(max_length=15, default="0",)
    minimum_stock_level = models.CharField(max_length=15, default="0",)
    inventory_description = models.CharField(
        max_length=500, default="", blank=True)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="inventory_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="inventory_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    class Meta:
        # ordering= ("first_name", "last_name",)
        verbose_name = "Inventory"
        verbose_name_plural = "Inventories"

class StockTransaction(models.Model):
    stock_transaction_number = models.CharField(max_length=50, unique=True,default="")
    source_warehouse = models.ForeignKey(
        Warehouse, null=True, on_delete=models.SET_NULL, related_name="source_warehouse_stock_transactions")
    recipient_warehouse = models.ForeignKey(
        Warehouse, null=True, on_delete=models.SET_NULL, related_name="recipient_warehouse_stock_transactions")
    transaction_type_choices = [
        ("in_bound", "Inbound"), ("outbound", "Outbound"), ("not_selected", "Not Selected")]
    transaction_type = models.CharField(
        max_length=20, choices=transaction_type_choices, default="not_selected",)
    transaction_description = models.CharField(
        max_length=500, default="", blank=True)
    stock_transaction_reference = models.CharField(
        max_length=50, default="",blank=True) #will store the stock order number or sales order number that the stock transaction is fullfilling
    stock_transaction_added_to_inventory = models.BooleanField(default=False) #turned True only for inbound after they are received
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="stock_transaction_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="stock_transaction_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(default=timezone.now)
    class Meta:
        # ordering= ("first_name", "last_name",)
        verbose_name = "Stock Transaction"
        verbose_name_plural = "Stock Transactions"

    def save(self, *args, **kwargs):
        if not self.pk:
            numberReg = re.sub(
                r'[^0-9]', '', self.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
            self.stock_transaction_number = "ST"+numberReg
        super().save(*args, **kwargs)

class StockTransactionInstance(models.Model):
    product = models.ForeignKey(
        Product, null=True, on_delete=models.SET_NULL, related_name="product_stock_transactions")
    quantity = models.CharField(max_length=15, default="0",)
    stock_transaction = models.ForeignKey(
        StockTransaction, null=True, on_delete=models.SET_NULL, related_name="stock_transaction_instances")
    #purchase_requisition_items_purchased = models.BooleanField(default=False)

class Equipment(models.Model):
    warehouse = models.ForeignKey(
        Warehouse, null=True, on_delete=models.SET_NULL, related_name="warehouse_equipment")
    equipment_name = models.CharField(max_length=100, default="",)
    equipment_serial_number = models.CharField(max_length=50, default="",)
    equipment_description = models.CharField(
        max_length=500, default="", blank=True)
    status_choices = [
        ("operational", "Operational"), ("under_maintenance", "Under Maintenance"), ("decommisioned", "Decommisioned"), ("not_selected", "Not Selected")]
    status = models.CharField(
        max_length=20, choices=status_choices, default="not_selected",)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="equipment_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="equipment_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

class PurchaseRequisition(models.Model): #only applicable to the main warehouse
    warehouse = models.ForeignKey(
        Warehouse, null=True, on_delete=models.SET_NULL, related_name="warehouse_purchase_requisitions")
    purchase_requisition_number = models.CharField(max_length=50, unique=True)
    purchase_requisition_description = models.CharField(
        max_length=500, default="", blank=True)
    purchase_requisition_approved = models.BooleanField(default=False) #approved by head of procurement
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="purchase_requisitions_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="purchase_requisitions_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)


    class Meta:
        # ordering= ("first_name", "last_name",)
        verbose_name = "Purchase Requisition"
        verbose_name_plural = "Purchase Requisitions"

    def save(self, *args, **kwargs):
        if not self.pk:
            numberReg = re.sub(
                r'[^0-9]', '', self.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
            self.purchase_requisition_number = "PR"+numberReg
        super().save(*args, **kwargs)


# only applicable to the main warehouse
class PurchaseRequisitionInstance(models.Model):
    product = models.ForeignKey(
        Product, null=True, on_delete=models.SET_NULL, related_name="product_purchase_requisitions")
    purchase_requisition = models.ForeignKey(
        PurchaseRequisition, null=True, on_delete=models.SET_NULL, related_name="purchase_requisition_instances")
    quantity = models.CharField(max_length=15, default="0",)
    purchase_requisition_items_purchased = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="purchase_requisition_instances_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="purchase_requisition_instances_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

class StockRequisition(models.Model): #only made by subsidiary warehouses to their respective procurement department
    warehouse = models.ForeignKey(
        Warehouse, null=True, on_delete=models.SET_NULL, related_name="warehouse_stock_requisitions")
    stock_requisition_number = models.CharField(max_length=50, unique=True)
    stock_requisition_description = models.CharField(
        max_length=500, default="", blank=True)
    stock_requisition_approved = models.BooleanField(default=False) #approved by the h.o.d of the respective procurement department
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="stock_requisitions_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="stock_requisitions_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

class StockRequisitionInstance(models.Model):
    product = models.ForeignKey(
        Product, null=True, on_delete=models.SET_NULL, related_name="product_stock_requisitions")
    stock_requisition = models.ForeignKey(
        StockRequisition, null=True, on_delete=models.SET_NULL, related_name="stock_requisition_instances")
    quantity = models.CharField(max_length=15, default="0",)
    stock_requisition_items_delivered = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="stock_requisition_instances_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="stock_requisition_instances_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)




    
