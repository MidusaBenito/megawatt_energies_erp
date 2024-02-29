from django.db import models

# Create your models here.
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import re

from human_resource.models import PayrollSheet, StaffProfile
from procurement.models import PurchaseOrder
from sales_and_marketing.models import Refund

class ChartOfAccount(models.Model):
    account_name = models.CharField(max_length=100, unique=True)
    account_number = models.CharField(max_length=50, unique=True)
    account_descriptions = models.CharField(max_length=500, default="",)
    running_balance = models.CharField(
        max_length=50, default="0.00",)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="financial_account_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="financial_account_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)


class Expense(models.Model):
    expense_number = models.CharField(max_length=50, unique=True)
    expense_title = models.CharField(max_length=100, default="",)
    expense_description = models.CharField(max_length=500, default="",)
    expense_type_choices = [("purchase_expense", "Purchase Expense"),
                            ("salary_expense", "Salary Expense"), ("utility_expense", "Utility Expense"), ("rent_expense", "Rent Expense"), ("operations_expense", "Operations Expense"), ("refund_expense", "Refund Expense"),("tax_and_license_expense", "Tax and License Expense"), ("other", "Other"),("not_selected", "Not Selected")]
    expense_type = models.CharField(
        max_length=25, choices=expense_type_choices, default="not_selected", blank=False)
    # expense_account = models.ForeignKey(
    #     ChartOfAccount, null=True, on_delete=models.SET_NULL, related_name="account_expenses")
    payroll_sheet = models.OneToOneField(
        PayrollSheet, null=True, on_delete=models.SET_NULL, related_name="payroll_sheet_expense")#not null for expense of type salary, otherwise null
    purchase_order = models.OneToOneField(
        PurchaseOrder, null=True, on_delete=models.SET_NULL, related_name="purchase_order_expense")#same as above
    refund = models.ForeignKey(
        Refund, null=True, on_delete=models.SET_NULL, related_name="refund_expense")#same as above
    expense_amount = models.CharField(
        max_length=50, default="0.00",)
    expense_approved = models.BooleanField(default=False)
    expense_approved_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="expense_approved_by")
    expense_settled = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="expense_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="expense_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            numberReg = re.sub(
                r'[^0-9]', '', self.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
            self.expense_number = "EP"+numberReg
        super().save(*args, **kwargs)

class Deposit(models.Model):  #if deposit is deleted, the balance must be subtracted from the account
    deposit_number = models.CharField(max_length=50, unique=True)
    # deposit_account = models.ForeignKey(
    #     ChartOfAccount, null=True, on_delete=models.SET_NULL, related_name="account_deposits")
    source_choices = [("sales_revenue", "Sales Revenue"), ("loans", "Loans"),
                      ("other", "Other"), ("not_selected", "Not Selected")]
    deposit_source = models.CharField(
        max_length=20, choices=source_choices, default="not_selected", blank=False)
    deposit_amount = models.CharField(
        max_length=50, default="0.00",)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="deposit_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="deposit_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            numberReg = re.sub(
                r'[^0-9]', '', self.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
            self.deposit_number = "DN"+numberReg
        super().save(*args, **kwargs)

class Transaction(models.Model):
    transaction_number = models.CharField(max_length=50, unique=True)
    transaction_mode_choices = [
        ("inflow", "Inflow"), ("outflow", "Outflow"), ("not_selected", "Not Selected")]
    transaction_mode = models.CharField(
        max_length=20, choices=transaction_mode_choices, default="not_selected", blank=False)
    transaction_amount = models.CharField(
        max_length=50, default="0.00",)
    expense = models.OneToOneField(
        Expense, null=True, on_delete=models.SET_NULL, related_name="expense_transaction")
    deposit = models.OneToOneField(
        Deposit, null=True, on_delete=models.SET_NULL, related_name="deposit_transaction")
    account = models.ForeignKey(
        ChartOfAccount, null=True, on_delete=models.SET_NULL, related_name="account_transactions")
    transaction_reference = models.CharField(
        max_length=50, default="",) #used to store mpesa code or bank transaction code for identification of the transaction
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="transaction_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="transaction_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            numberReg = re.sub(
                r'[^0-9]', '', self.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
            self.transaction_number = "TN"+numberReg
        super().save(*args, **kwargs)


