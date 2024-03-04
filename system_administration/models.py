from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import re

class CompanyProfile(models.Model):
    company_name = models.CharField(max_length=100, default="", blank=True)
    company_serial_number = models.CharField(
        max_length=100, default="", blank=True,unique=True, editable=True)
    company_description = models.CharField(
        max_length=500, default="", blank=True)
    company_postal_address = models.CharField(
        max_length=50, default="", blank=True)
    company_country_location = models.CharField(max_length=50, default="", blank=True)
    company_phone = models.CharField(max_length=30, default="", blank=True)
    currency_choices = [("usd", "USD"), ("gbp", "GBP"), ("eur", "EUR"),
                        ("kes", "KES"), ("not_selected", "Not Selected")]
    company_preferred_currency = models.CharField(
        max_length=30, choices=currency_choices, default="kes")
    company_profile_set = models.BooleanField(default=False)
    company_departments_set = models.BooleanField(default=False)
    company_super_hr_created = models.BooleanField(default=False)
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        # ordering= ("first_name", "last_name",)
        verbose_name = "Company Profile"
        verbose_name_plural = "Company Profiles"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.company_serial_number = re.sub(
                r'[^0-9]', '', self.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
        super().save(*args, **kwargs)

class CompanyBranch(models.Model): #it's this company branch that i will be using to link to other models
    company_profile = models.ForeignKey(
        CompanyProfile, null=True, on_delete=models.CASCADE, related_name="company_branches")
    branch_name = models.CharField(
        max_length=100, default="", blank=True)
    branch_description = models.CharField(
        max_length=500, default="", blank=True)
    branch_county_location = models.CharField(max_length=30, default="", blank=True)
    branch_phone = models.CharField(max_length=30, default="", blank=True)
    branch_active = models.BooleanField(default=True)
    main_branch = models.BooleanField(default=False)
    # mpesa payment details
    branch_mpesa_consumer_key = models.CharField(
        max_length=150, null=True, default="", blank=True)
    branch_mpesa_consumer_secret = models.CharField(
        max_length=150, null=True, default="", blank=True)
    branch_mpesa_business_short_code = models.CharField(
        max_length=50, null=True, default="", blank=True)
    branch_mpesa_password = models.CharField(
        max_length=150, null=True, default="", blank=True)
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        # ordering= ("first_name", "last_name",)
        verbose_name = "Company Branch"
        verbose_name_plural = "Company Branches"

class CompanyDepartment(models.Model):
    company_profile = models.ForeignKey(
        CompanyProfile, null=True, on_delete=models.CASCADE,related_name="company_departments")
    department_choices = [("system_and_administration", "System and Administration"), ("procurement", "Procurement"), ("human_resource_management", "Human Resource Management"),
                          ("warehouse_management", "Warehouse Management"), ("sales_and_marketing", "Sales and Marketing"), ("finance_and_accounting", "Finance and Accounting"), ("support_services", "Support Services"), ("management", "Management"), ("not_selected", "Not Selected")]
    department_name = models.CharField(max_length=100,choices=department_choices, default="not_selected", unique=True)
    department_description = models.CharField(
        max_length=500, default="", blank=True)
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        # ordering= ("first_name", "last_name",)
        verbose_name = "Company Department"
        verbose_name_plural = "Company Departments"

# model to store whether a system administrator account has been created or not


class SystemAdminCreationStatus(models.Model):#there is to be only one system admin for the whole system
    # when admin account is deleted, the record is deleted
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_profile = models.OneToOneField(
        CompanyProfile, null=True, on_delete=models.CASCADE)
    systemAdminCreated = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)




    
