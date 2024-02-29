from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import re
from human_resource.models import StaffPayrollInstance, StaffProfile

from system_administration.models import CompanyBranch, CompanyProfile
from warehouse_management.models import Inventory, Product, Warehouse
#kindly note to access model instances from the top using related names
#products
class ProductImageCatalogue(models.Model):
    product = models.ForeignKey(
        Product, null=True, on_delete=models.CASCADE,related_name="product_images")
    product_image = models.ImageField(blank=True) #
    image_attribute = models.CharField(max_length=50, default="", blank=True)
    use_as_main_image = models.BooleanField(default=False)

    class Meta:
        # ordering= ("first_name", "last_name",)
        verbose_name = "Product Image Catalogue"
        verbose_name_plural = "Product Image Catalogues"
    
class ProductFeaturesCatalogue(models.Model):
    product = models.ForeignKey(
        Product, null=True, on_delete=models.CASCADE, related_name="product_features")
    product_feature_title = models.CharField(
        max_length=50, default="", blank=True)
    
class ProductFeaturesAttributes(models.Model):
    product_feature_catalogue = models.ForeignKey(
        ProductFeaturesCatalogue, null=True, on_delete=models.CASCADE, related_name="product_feature_attributes")
    feature_attribute_title = models.CharField(
        max_length=50, default="", blank=True)
    feature_attribute_description = models.CharField(
        max_length=500, default="", blank=True)
    
class ProductComponent(models.Model):
    product = models.ForeignKey(
        Product, null=True, on_delete=models.CASCADE, related_name="product_components")
    component_name = models.CharField(
        max_length=50, default="", blank=True)
    component_quantity = models.CharField(
        max_length=12, default="1", blank=True)

#brands will be stored and the sales team will be able to select from brands or add new    
class ProductBrand(models.Model):
    product = models.ForeignKey(
        Product, null=True, on_delete=models.SET_NULL, related_name="product_brands")
    product_brand_name = models.CharField(
        max_length=50, default="", blank=True)
    product_brand_description = models.CharField(
        max_length=500, default="", blank=True)
    
class ProductPricing(models.Model):
    product = models.OneToOneField(
        Product, null=True, on_delete=models.CASCADE, related_name="product_pricing")
    product_net_price = models.CharField(
        max_length=50, default="0.00",)
    
class ProductDiscount(models.Model):
    product = models.OneToOneField(
        Product, null=True, on_delete=models.CASCADE,related_name="product_discount")
    discount_type_choices = [
        ("percentage_discount", "Percentage Discount"), ("fixed_discount", "Fixed Discount"), ("not_selected", "Not Selected")]
    discount_type = models.CharField(
        max_length=20, choices=discount_type_choices, default="not_selected",)
    discount_value = models.CharField(
        max_length=5, default="0.00",)
    
#sales
class SaleOutlet(models.Model):
    company_branch = models.ForeignKey(
        CompanyProfile, null=True, on_delete=models.SET_NULL)
    sale_outlet_name = models.CharField(max_length=50, default="", unique=True)
    sale_outlet_location = models.CharField(
        max_length=50, default="",)
    sale_outlet_contact_phone = models.CharField(
        max_length=25, default="", blank=False)
    sale_outlet_description = models.CharField(
        max_length=500, default="",)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="sale_outlet_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="sale_outlet_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

class SalesOrder(models.Model):
    sales_order_number = models.CharField(max_length=50, unique=True)
    sale_outlet = models.ForeignKey(
        SaleOutlet, null=True, on_delete=models.CASCADE, related_name="sale_outlet_sales_order")
    warehouse = models.OneToOneField(
        Warehouse, null=True, on_delete=models.SET_NULL, related_name="sales_order_warehouse")
    sales_order_description = models.CharField(
        max_length=500, default="",)
    sales_order_approved = models.BooleanField(default=False)
    sales_order_fulfilled = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="sales_order_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="sales_order_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            numberReg = re.sub(
                r'[^0-9]', '', self.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
            self.sales_order_number = "SO"+numberReg
        super().save(*args, **kwargs)

#if you delete a sales order items, the quantity must be returned to the respective inventory
class SalesOrderItems(models.Model):
    sales_order = models.ForeignKey(
        SalesOrder, null=True, on_delete=models.CASCADE, related_name="sales_order_sales_items")
    inventory = models.ForeignKey(
        Inventory, null=True, on_delete=models.CASCADE, related_name="inventory_sales_order_items")
    quantity = models.CharField(max_length=15, default="0",)
    sales_item_order_fulfilled = models.BooleanField(default=False)

class SalesInventory(models.Model):
    product = models.OneToOneField(
        Product, null=True, on_delete=models.SET_NULL, related_name="product_sales_inventories")
    sale_outlet = models.ForeignKey(
        SaleOutlet, null=True, on_delete=models.CASCADE, related_name="sale_outlet_sales_inventory")
    quantity = models.CharField(max_length=15, default="0",)
    minimum_stock_level = models.CharField(max_length=15, default="0",)
    sales_inventory_description = models.CharField(
        max_length=500, default="",)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="sales_inventory_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="sales_inventory_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        # ordering= ("first_name", "last_name",)
        verbose_name = "Sales Inventory"
        verbose_name_plural = "Sales Inventories"

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL,related_name="user_customer_profile")
    company_profile = models.ForeignKey(
        CompanyProfile, null=True, on_delete=models.CASCADE, related_name="company_customers")
    customer_first_name = models.CharField(
        max_length=20, default="", blank=False)
    customer_last_name = models.CharField(
        max_length=20, default="", blank=False)
    email_address = models.EmailField(max_length=50, default="", blank=False)
    phone_number = models.CharField(max_length=25, default="", blank=False)
    title_choices = [("mr", "Mr."), ("mrs", "Mrs."), ("miss", "Miss"),
                     ("other", "Other"), ("not_selected", "Not Selected")]
    customer_title = models.CharField(
        max_length=20, choices=title_choices, default="not_selected", blank=False)
    is_profile_set = models.BooleanField(default=False)
    recycle_bin = models.BooleanField(default=False)
    # email_verification_code = models.CharField(max_length=6,null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        # ordering= ("first_name", "last_name",)
        verbose_name = "Customer Profile"
        verbose_name_plural = "Customer Profiles"

class CustomerShippingAddress(models.Model):
    customer_profile = models.ForeignKey(
        CustomerProfile, null=True, on_delete=models.CASCADE)
    shipping_address = models.CharField(
        max_length=100, default="", blank=False)
    shipping_town = models.CharField(
        max_length=50, default="", blank=False)
    
class CustomerOrder(models.Model):
    customer_order_number = models.CharField(max_length=50, unique=True)
    customer_profile = models.ForeignKey(
        CustomerProfile, null=True, on_delete=models.SET_NULL)
    order_type_choices = [("order_online", "Order Online"), ("order_offline", "Order Offline"),("not_selected", "Not Selected")]
    customer_order_type = models.CharField(
        max_length=20, choices=order_type_choices, default="not_selected", blank=False)
    customer_order_description = models.CharField(
        max_length=500, default="",) #edited by the sales team
    customer_order_total_gross_value = models.CharField(
        max_length=50, default="0.00",)
    customer_order_total_discount = models.CharField(
        max_length=50, default="0.00",)
    customer_order_total_net_value = models.CharField(
        max_length=50, default="0.00",)
    customer_order_approved = models.BooleanField(default=False)
    customer_order_fulfilled_for_transit = models.BooleanField(default=False)
    customer_ordered_delivered_to_destination = models.BooleanField(
        default=False)
    customer_order_picked_by_customer = models.BooleanField(default=False)
    customer_order_cancelled_by_customer = models.BooleanField(default=False) #customer must first cancel the order to return the items
    customer_order_cancelled_by_sales_team = models.BooleanField(default=False) #in the event that the order is unable to be fullfilled
    sales_person = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="customer_offline_sales_representative") #represents the sles person that made the sales possible for commissions purposes
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="customer_offline_order_created_by") #used for offline orders to capture the sales team that serves the order
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="customer_offline_order_last_updated_by")  # used for offline orders to capture the sales team that serves the order
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    expected_delivery_date = models.DateField()
    
    def save(self, *args, **kwargs):
        if not self.pk:
            numberReg = re.sub(
                r'[^0-9]', '', self.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
            self.customer_order_number = "CO"+numberReg
        super().save(*args, **kwargs)

class CustomerOrderItem(models.Model):
    customer_order = models.ForeignKey(
        CustomerOrder, null=True, on_delete=models.CASCADE, related_name="customer_order_items")
    inventory = models.ForeignKey(
        SalesInventory, null=True, on_delete=models.CASCADE, related_name="customer_order_products")
    quantity = models.CharField(max_length=15, default="0",)
    price_per_item = models.CharField(
        max_length=50, default="0.00",)
    discount_per_item = models.CharField(
        max_length=50, default="0.00",)
    gross_subtotal = models.CharField(
        max_length=50, default="0.00",)
    total_discount = models.CharField(
        max_length=50, default="0.00",)
    net_subtotal = models.CharField(
        max_length=50, default="0.00",)
    sales_item_order_fulfilled = models.BooleanField(default=False)

class SalesCommission(models.Model):
    product = models.ManyToManyField(
        Product, related_name="product_sales_commissions")
    commission_title = models.CharField(
        max_length=50, default="", blank=False)
    commission_description = models.CharField(
        max_length=500, default="",)
    commission_value = models.CharField(max_length=15, default="0",)
    sales_person = models.ManyToManyField(
        StaffProfile, related_name="sales_commission_sales_persons")
    commission_period_start_date = models.DateField()
    commission_period_end_date = models.DateField()
    commission_module_choices = [
        ("percentage", "Percentage"), ("fixed", "Fixed"), ("not_selected", "Not Selected")]
    commission_module = models.CharField(
        max_length=20, choices=commission_module_choices, default="not_selected", blank=False)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="sales_commission_created_by")  # used for offline orders to capture the sales team that serves the order
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="sales_commission_last_updated_by")  # used for offline orders to capture the sales team that serves the order
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

#commision sheet, will be prepared by the head of sales
class CommissionSheet(models.Model):
    company_branch = models.ForeignKey(
        CompanyBranch, null=True, on_delete=models.SET_NULL, related_name="branch_commission_sheets")
    commission_sheet_title = models.CharField(
        max_length=100, default="", blank=False)
    commission_sheet_number = models.CharField(max_length=50, unique=True)
    commission_sheet_description = models.CharField(
        max_length=500, default="", blank=False)
    month_titles_choices = [
        ("january", "January"), ("february", "February"), ("march", "March"), ("april", "April"), ("may", "May"), ("june", "June"), ("july", "July"), ("august", "August"), ("september", "September"), ("october", "October"), ("november", "November"), ("december", "December"), ("not_selected", "Not Selected")]
    commission_sheet_for_the_month_of = models.CharField(
        max_length=100, choices=month_titles_choices, default="not_selected", blank=False)
    commission_sheet_for_the_year = models.CharField(
        max_length=15, default="2024", blank=False)
    commission_sheet_value = models.CharField(
        max_length=15, default="0.00", blank=False)
    commission_sheet_approved_by_finance = models.BooleanField(default=False)
    commission_sheet_payment_settled = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="commission_sheets_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="commission_sheets_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            numberReg = re.sub(
                r'[^0-9]', '', self.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
            self.commission_sheet_number = "COM"+numberReg
        super().save(*args, **kwargs)

class CommissionSheetInstance(models.Model):
    # staff_profile = models.ForeignKey(
    #     StaffProfile, null=True, on_delete=models.SET_NULL,related_name="staff_commission_sheets")
    staff_payroll_instance = models.ForeignKey(StaffPayrollInstance, null=True,
                      on_delete=models.SET_NULL, related_name="staff_payroll_instance_commissions")
    customer_order = models.OneToOneField(
        CustomerOrder, null=True, on_delete=models.CASCADE, related_name="customer_order_commissions")
    commission_sheet = models.ForeignKey(
        CommissionSheet, null=True, on_delete=models.SET_NULL, related_name="commission_items")
    commission_value = models.CharField(
        max_length=12, default="0.00", blank=False)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="commission_items_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="commission_items_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)


class OrderItemReturn(models.Model):
    customer_order = models.ForeignKey(
        CustomerOrder, null=True, on_delete=models.CASCADE, related_name="customer_order_items_return")
    recycle_bin = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    date_of_return = models.DateField()

class ReturnItem(models.Model):
    order_item_return = models.ForeignKey(
        OrderItemReturn, null=True, on_delete=models.CASCADE, related_name="order_items_return")
    ordered_item_returned = models.OneToOneField(
        CustomerOrderItem, null=True, on_delete=models.CASCADE, related_name="ordered_items_returned")
    reason_for_return = models.CharField(
        max_length=500, default="", blank=False)
    
#sales payments
class CustomerOrderPayment(models.Model):
    payment_number = models.CharField(max_length=50, unique=True)
    customer_order = models.ForeignKey(
        CustomerOrder, null=True, on_delete=models.SET_NULL, related_name="customer_order_payments")
    payment_amount = models.CharField(
        max_length=50, default="0.00",)
    payment_type_choices = [("m_pesa", "M-Pesa"),
                            ("cash", "Cash"), ("credit_card", "Credit Card"), ("not_selected", "Not Selected")]
    payment_method = models.CharField(
        max_length=20, choices=payment_type_choices, default="not_selected", blank=False)
    payer_account_number = models.CharField(max_length=30, default="",) #will store the mobile number that has made the payment
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="payment_created_by") #used for payment of offline orders to capture the sales team that serves the order payment
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="payment_last_updated_by")  # used for payment of offline orders to capture the sales team that serves the order payment
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            numberReg = re.sub(
                r'[^0-9]', '', self.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
            self.payment_number = "PN"+numberReg
        super().save(*args, **kwargs)

class Refund(models.Model): #refund will be created by sales team and not customer
    payment = models.ForeignKey(
        CustomerOrderPayment, null=True, on_delete=models.SET_NULL, related_name="payment_refunds")
    order_item_return = models.OneToOneField(
        OrderItemReturn, null=True, on_delete=models.CASCADE, related_name="order_items_requesting_refunds")
    refund_amount = models.CharField(
        max_length=50, default="0.00",)
    refund_approved = models.BooleanField(default=False)
    refund_fullfilled = models.BooleanField(default=False)
    recycle_bin = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="refund_created_by") 
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="refund_last_updated_by")  
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)


