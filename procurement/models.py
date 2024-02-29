from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import re
from human_resource.models import StaffProfile

from system_administration.models import CompanyProfile
from warehouse_management.models import Product, PurchaseRequisition, PurchaseRequisitionInstance, StockRequisitionInstance

class Supplier(models.Model):
    user = models.OneToOneField(
        User, null=True, on_delete=models.SET_NULL, related_name="user_supplier_profile")
    company_profile = models.ForeignKey(
        CompanyProfile, null=True, on_delete=models.CASCADE, related_name="company_suppliers")
    supplier_name = models.CharField(max_length=100, default="", unique=True)
    supplier_phone = models.CharField(max_length=15,)
    supplier_email = models.EmailField(max_length=50, default="", blank=False)
    supplier_address = models.CharField(max_length=100,default="")
    supplied_products = models.ManyToManyField(
        Product, blank=True, related_name="supplier_products")
    supplier_description = models.CharField(
        max_length=500, default="",)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="supplier_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="supplier_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

class PurchaseOrder(models.Model):
    purchase_order_number = models.CharField(
        max_length=50, unique=True, default="")
    purchase_value_overall = models.CharField(max_length=15, default="0.00",)
    purchase_order_approved = models.BooleanField(default=False) #approved by the head of finance
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="purchase_order_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="purchase_order_last_updated_by")
    purchase_order_approved_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="purchase_order_approved_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

    
    class Meta:
        # ordering= ("first_name", "last_name",)
        verbose_name = "Purchase Order"
        verbose_name_plural = "Purchase Orders"

    def save(self, *args, **kwargs):
        if not self.pk:
            numberReg = re.sub(
                r'[^0-9]', '', self.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
            self.purchase_order_number = "PO"+numberReg
        super().save(*args, **kwargs)

class ProductPurchaseInstance(models.Model):
    purchase_order = models.ForeignKey(
        PurchaseOrder, null=True, on_delete=models.SET_NULL, related_name="purchase_order_product_instances")
    purchase_requisition_instance = models.OneToOneField(
        PurchaseRequisitionInstance, null=True, on_delete=models.SET_NULL, related_name="purchase_requisition_product_instances")
    supplier = models.ForeignKey(
        Supplier, null=True, on_delete=models.SET_NULL, related_name="supplier_product_purchase_instances")
    purchase_value_per_unit = models.CharField(max_length=15, default="0.00",)
    purchase_value_overall = models.CharField(max_length=15, default="0.00",)
    purchase_amount_paid_to_supplier = models.CharField(max_length=15, default="0.00",)
    supplier_payment_settled = models.BooleanField(default=False)
    product_purchase_delivered = models.BooleanField(default=False)
    quantity_delivered = models.CharField(max_length=15, default="0",)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="product_purchase_instance_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="product_purchase_instance_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        # ordering= ("first_name", "last_name",)
        verbose_name = "Product Purchase Instance"
        verbose_name_plural = "Product Purchase Instances"


class StockOrder(models.Model): #only applicable to subsidiary procurement departments
    stock_order_number = models.CharField(max_length=50, unique=True,default="")
    stock_order_approved = models.BooleanField(default=False) #approved by head of procurement of the main branch
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="stock_order_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="stock_order_last_updated_by")
    stock_order_approved_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="stock_order_approved_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        # ordering= ("first_name", "last_name",)
        verbose_name = "Stock Order"
        verbose_name_plural = "Stock Orders"

    def save(self, *args, **kwargs):
        if not self.pk:
            numberReg = re.sub(
                r'[^0-9]', '', self.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
            self.stock_order_number = "SO"+numberReg
        super().save(*args, **kwargs)


# only applicable to subsidiary procurement departments
class StockOrderInstance(models.Model):
    stock_order = models.ForeignKey(
        PurchaseOrder, null=True, on_delete=models.SET_NULL, related_name="stock_order_product_instances")
    stock_requisition_instance = models.OneToOneField(
        StockRequisitionInstance, null=True, on_delete=models.SET_NULL, related_name="stock_requisition_product_instances")
    # supplier = models.ForeignKey(
    #     Supplier, null=True, on_delete=models.SET_NULL, related_name="supplier_product_purchase_instances")
    # purchase_value_per_unit = models.CharField(max_length=15, default="0.00",)
    # purchase_value_overall = models.CharField(max_length=15, default="0.00",)
    # purchase_amount_paid_to_supplier = models.CharField(
    #     max_length=15, default="0.00",)
    # supplier_payment_settled = models.BooleanField(default=False)
    stock_order_item_delivered = models.BooleanField(default=False)
    quantity_delivered = models.CharField(max_length=15, default="0",)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="stock_order_instance_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="stock_order_instance_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        # ordering= ("first_name", "last_name",)
        verbose_name = "Stock Order Instance"
        verbose_name_plural = "Stock Order Instances"

    
    
