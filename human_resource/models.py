from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import re
#from sales_and_marketing.models import CommissionSheetInstance

from system_administration.models import CompanyBranch, CompanyDepartment, CompanyProfile


class staffPosition(models.Model):  #created by system admin
    company_profile = models.ForeignKey(
        CompanyProfile, null=True, on_delete=models.CASCADE, related_name="company_staff_positions")
    position_title = models.CharField(max_length=100, default="", blank=False)
    position_description = models.CharField(
        max_length=500, default="", blank=True)
    salary = models.CharField(
        max_length=12, default="0.00", blank=True)
    recycle_bin = models.BooleanField(default=False)
    # email_verification_code = models.CharField(max_length=6,null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        # ordering= ("first_name", "last_name",)
        verbose_name = "Staff Position"
        verbose_name_plural = "Staff Positions"

    

class StaffProfile(models.Model):
    # SET_NULL is the way to go forall
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL,related_name="user_staff_profile")
    staff_position = models.ForeignKey(
        staffPosition, null=True, on_delete=models.SET_NULL)
    company_branch = models.ForeignKey(
        CompanyBranch, null=True, on_delete=models.SET_NULL,related_name="company_branch_staffs")
    company_department = models.ForeignKey(
        CompanyDepartment, null=True, on_delete=models.SET_NULL, related_name="company_department_staffs")
    # remember these length limits
    staff_number = models.CharField(max_length=30,default="", unique=True)
    first_name = models.CharField(max_length=50, default="", blank=False)
    # remember these length limits
    last_name = models.CharField(max_length=50, default="", blank=False)
    email_address = models.EmailField(max_length=50, default="", blank=False)
    date_of_birth = models.DateField(null=True, blank=True)
    # remember these length limits
    country_name = models.CharField(
        max_length=20, default="Kenya (KE) [+254]", blank=False)
    identification_number = models.CharField(
        max_length=20, default="", blank=False)  # remember these length limits
    # remember these length limits
    phone_number = models.CharField(max_length=25, default="", blank=False)
    kra_pin = models.CharField(max_length=50, default="", blank=False)
    title_choices = [("mr", "Mr."), ("mrs", "Mrs."), ("miss", "Miss"),
                     ("other", "Other"), ("not_selected", "Not Selected")]
    staff_title = models.CharField(
        max_length=20, choices=title_choices, default="not_selected", blank=False)
    type_of_employment_choices = [("not_selected","Not Selected"),("contact","Contract"),("permanent","Permanent")]
    type_of_employment = models.CharField(
        max_length=20, choices=type_of_employment_choices, default="not_selected", blank=False)
    employment_start_date = models.DateField(null=True, blank=True)
    employment_end_date = models.DateField(null=True, blank=True)
    emergency_contact_phone = models.CharField(
        max_length=25, default="", blank=True)
    banking_institution_name = models.CharField(
        max_length=100, default="", blank=True)
    bank_account_name = models.CharField(
        max_length=100, default="", blank=True)
    bank_account_number = models.CharField(
        max_length=100, default="", blank=True)
    nhif_number = models.CharField(max_length=30, default="", blank=True)
    nhif_additional_info = models.CharField(max_length=500, default="", blank=True)
    nssf_number = models.CharField(max_length=30, default="", blank=True)
    nssf_additional_info = models.CharField(max_length=500, default="", blank=True)
    staff_additional_info = models.CharField(max_length=500, default="", blank=True)
    basic_salary = models.CharField(
        max_length=12, default="0.00", blank=True)
    # is_email_verified = models.BooleanField(default=False) #field for showing whether a user's email is verified
    # field for showing whether a user's profile is set
    is_profile_set = models.BooleanField(default=False)
    # marks a user to determine whether they have the priviledges for heading a department, can create payroll sheets for staff in that branch
    is_head_of_department = models.BooleanField(default=False)
    has_read_write_priviledges = models.BooleanField(default=False)
    is_super_admin = models.BooleanField(default=False) #belongs to the hr department. Has the priviledge to create bonuses, deductions, payroll sheets. Is only one and is created by the system admin
    is_on_leave = models.BooleanField(default=False)
    recycle_bin = models.BooleanField(default=False)
    # email_verification_code = models.CharField(max_length=6,null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(default=timezone.now) #must be included for all models requiring numbers generation

    class Meta:
        # ordering= ("first_name", "last_name",)
        verbose_name = "Staff Profile"
        verbose_name_plural = "Staff Profiles"

    # def save(self, *args, **kwargs):   #marked for change
    #     if not self.pk:
    #         numberReg = re.sub(
    #             r'[^0-9]', '', self.timestamp.strftime('%M'))
    #         self.staff_number = "MEL"+f'{self.user.id}'+numberReg
    #     super().save(*args, **kwargs)

class Deduction(models.Model):
    company_profile = models.ForeignKey(
        CompanyProfile, null=True, on_delete=models.CASCADE, related_name="company_deductions")
    deduction_title = models.CharField(max_length=100, default="", blank=False)
    deduction_description = models.CharField(
        max_length=500, default="", blank=True)
    deduction_choices = [("tax", "Tax"), ("insurance", "Insurance"), ("pension", "Pension"), ("loan_repayment", "Loan Repayment"),
                         ("other", "Other"), ("not_selected", "Not Selected")]
    deduction_type = models.CharField(
        max_length=20, choices=deduction_choices, default="not_selected", blank=False)
    deduction_module_choices = [
        ("percentage", "Percentage"), ("fixed", "Fixed"), ("other", "Other"),("not_selected", "Not Selected")]
    deduction_module = models.CharField(
        max_length=20, choices=deduction_module_choices, default="not_selected", blank=False)
    deduction_value = models.CharField(max_length=20, default="0.00", blank=False)
    date_effective_from = models.DateField(null=True, blank=True)
    date_effective_to = models.DateField(null=True, blank=True)
    recycle_bin = models.BooleanField(default=False)
    #deducted_from_gross_salary = models.BooleanField(defau)
    # email_verification_code = models.CharField(max_length=6,null=True,blank=True)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL,related_name="deductions_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="deductions_last_updated_by")
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

class Bonus(models.Model):
    company_profile = models.ForeignKey(
        CompanyProfile, null=True, on_delete=models.CASCADE, related_name="company_bonuses")
    bonus_title = models.CharField(
        max_length=100, default="", blank=False)
    bonus_description = models.CharField(
        max_length=500, default="", blank=True)
    bonus_type_choices = [
        ("performance_bonus", "Performance Bonus"), ("annual_bonus", "Annual Bonus"), ("retention_bonus", "Retention Bonus"), ("sales_commision", "Sales Commision"), ("attendance_bonus", "Attendance Bonus"), ("other", "Other"), ("not_selected", "Not Selected")]
    bonus_type = models.CharField(
        max_length=20, choices=bonus_type_choices, default="not_selected", blank=False)
    bonus_amount = models.CharField(max_length=12, default="0.00", blank=False)
    date_effective_from = models.DateField(null=True,blank=True)
    date_effective_to = models.DateField(null=True, blank=True)
    recycle_bin = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="bonuses_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="bonuses_last_updated_by")
    # email_verification_code = models.CharField(max_length=6,null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        # ordering= ("first_name", "last_name",)
        verbose_name = "Bonus"
        verbose_name_plural = "Bonuses"


class WorkShift(models.Model):
    company_profile = models.ForeignKey(
        CompanyProfile, null=True, on_delete=models.CASCADE, related_name="company_work_shifts")
    shift_name = models.CharField(
        max_length=50, default="", blank=False)
    #working_day = models.OneToOneField(WorkingDays, null=True, on_delete=models.SET_NULL)
    shift_hours_start = models.TimeField(null=True, blank=True)
    shift_hours_end = models.TimeField(null=True, blank=True)
    shift_description = models.CharField(
        max_length=500, default="", blank=True)
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)


class WorkingDays(models.Model):
    day_of_week_identifier = models.CharField(
        max_length=1, default="0",)
    work_shift = models.ForeignKey(
        WorkShift, on_delete=models.CASCADE, blank=True, related_name="workday_shifts",null=True)
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)


class TimeSheet(models.Model):
    staff_profile = models.ForeignKey(StaffProfile, null=True, on_delete=models.SET_NULL,related_name="staff_time_sheets")
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField(null=True,blank=True)
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

class StaffLeave(models.Model):
    staff_profile = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="staff_leave_instances")
    leave_type_choices = [
        ("sick_leave", "Sick Leave"), ("vacation_leave", "Vacation Leave"), ("maternity_leave", "Maternity Leave"), ("paternity_leave", "Paternity Leave"), ("medical_leave", "Medical Leave"), ("bereavement_leave", "Bereavement Leave"), ("other", "Other"), ("not_selected", "Not Selected")]
    leave_type = models.CharField(
        max_length=20, choices=leave_type_choices, default="not_selected", blank=False)
    leave_description = models.CharField(
        max_length=500, default="", blank=True)
    leave_start_date = models.DateField()
    leave_end_date = models.DateField()
    number_of_leave_days = models.CharField(
        max_length=5, default="1", blank=False)
    leave_approval_choices = [
        ("pending", "Pending"), ("denied", "Denied"), ("approved", "Approved")]
    leave_department_approval = models.CharField(
        max_length=20, choices=leave_approval_choices, default="pending", blank=False)
    leave_hr_approval = models.CharField(
        max_length=20, choices=leave_approval_choices, default="pending", blank=False)
    #leave_active_status = models.BooleanField(default=False)
    leave_status_type = [("active", "Active"),
                         ("pending", "Pending"), ("cancelled", "Cancelled"), ("expired", "Expired"), ("denied", "Denied"), ("completed", "Completed")]
    leave_status = models.CharField(
        max_length=20, choices=leave_status_type, default="pending", blank=False)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="staff_leaves_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="staff_leaves_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

class PayrollSheet(models.Model):
    company_branch = models.ForeignKey(#to be looked at later
        CompanyBranch, null=True, on_delete=models.SET_NULL,related_name="branch_payroll_sheets")
    payroll_sheet_title = models.CharField(max_length=100, default="", blank=False)
    payroll_sheet_number = models.CharField(max_length=50,default="",unique=True)
    payroll_sheet_description = models.CharField(max_length=500, default="", blank=True)
    month_titles_choices = [
        ("january", "January"), ("february", "February"), ("march", "March"), ("april", "April"), ("may", "May"),("june", "June"),("july", "July"),("august", "August"),("september", "September"),("october", "October"),("november", "November"),("december", "December"), ("not_selected", "Not Selected")]
    payroll_sheet_for_the_month_of = models.CharField(max_length=100,choices=month_titles_choices, default="not_selected", blank=False)
    payroll_sheet_for_the_year = models.CharField(
        max_length=15, default="2024", blank=False)
    payroll_sheet_value = models.CharField(max_length=15,default="0.00",blank=False)
    #added
    payroll_sheet_total_net_pay_value = models.CharField(
        max_length=15, default="0.00", blank=False)
    payroll_sheet_total_bonus_value = models.CharField(
        max_length=15, default="0.00", blank=False)
    payroll_sheet_total_deduction_value = models.CharField(
        max_length=15, default="0.00", blank=False)
    payroll_sheet_total_commission_value = models.CharField(
        max_length=15, default="0.00", blank=False)
    payroll_sheet_approved_by_finance = models.BooleanField(default=False)
    payroll_sheet_payment_settled = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="payroll_sheets_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="payroll_sheets_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    # must be included for all models requiring numbers generation
    timestamp = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.pk:
            numberReg = re.sub(
                r'[^0-9]', '', self.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
            self.payroll_sheet_number = "PS"+numberReg
        super().save(*args, **kwargs)

class DeductionInstance(models.Model):
    deduction = models.ForeignKey(Deduction, null=True, on_delete=models.SET_NULL,related_name="deduction_items")
    deduction_instance_value = models.CharField(max_length=12,default="0.00",blank=False)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="deductions_instances_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="deductions_instances_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

class BonusInstance(models.Model):
    bonus = models.ForeignKey(Bonus, null=True, on_delete=models.SET_NULL,related_name="bonus_items")
    bonus_instance_value = models.CharField(max_length=12,default="0.00",blank=False)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="bonus_instances_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="bonus_instances_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

class StaffPayrollInstance(models.Model):
    staff_profile = models.ForeignKey(StaffProfile, null=True, on_delete=models.SET_NULL)
    payroll_sheet = models.ForeignKey(PayrollSheet, null=True, on_delete=models.SET_NULL,related_name="staff_payroll_items")
    deduction_instance = models.ManyToManyField(
        DeductionInstance, related_name="staff_deductions")
    gross_salary=models.CharField(max_length=12,default="0.00",blank=False)
    bonus_instance = models.ManyToManyField(
        BonusInstance, blank=True, related_name="staff_bonuses")
    commissions_total = models.CharField(
        max_length=12, default="0.00", blank=False)
    net_salary = models.CharField(max_length=12,default="0.00",blank=False)
    created_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="payroll_instances_created_by")
    last_updated_by = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.SET_NULL, related_name="payroll_instances_last_updated_by")
    recycle_bin = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)
    is_prorated = models.BooleanField(default=False)
    pro_rate_factor = models.CharField(
        max_length=12, default="1.00", blank=False)

#additional models
class Task(models.Model):
    company_profile = models.ForeignKey(
        CompanyProfile, null=True, on_delete=models.CASCADE, related_name="company_tasks")
    task_title = models.CharField(max_length=100, default="", blank=False)
    staff = models.ManyToManyField(
        StaffProfile, blank=True, related_name="staff_tasks")
    task_description = models.CharField(
        max_length=500, default="", blank=False)
    task_effective_from = models.DateTimeField(null=True, blank=True)
    task_effective_to = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)


class Engagement(models.Model):
    company_profile = models.ForeignKey(
        CompanyProfile, null=True, on_delete=models.CASCADE, related_name="company_engagements")
    engagement_title = models.CharField(max_length=100, default="", blank=False)
    staff = models.ManyToManyField(
        StaffProfile, blank=True, related_name="staff_engagements")
    engagement_description = models.CharField(
        max_length=500, default="", blank=False)
    engagement_effective_from = models.DateTimeField(null=True, blank=True)
    engagement_effective_to = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

class Educational_Qualification(models.Model):
    staff = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.CASCADE,related_name="staff_education_qualifications")
    qualification_title = models.CharField(
        max_length=100, default="", blank=False)
    accredition_category_choices = [("not_selected","Not Selected"),("phd","PhD"),("masters","Masters"),("bachelors","Bachelors"),("diploma","Diploma"),("certificate","Certificate"),("other","Other")] 
    accredition_category = models.CharField(
        max_length=20, choices=accredition_category_choices, default="not_selected", blank=False)
    accrediting_institution = models.CharField(
        max_length=100, default="", blank=False)
    year_of_accredition = models.CharField(
        max_length=10, default="", blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

class Training_Record(models.Model):
    staff = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.CASCADE, related_name="staff_training_records")
    training_title = models.CharField(
        max_length=100, default="", blank=True)
    training_description = models.CharField(
        max_length=500, default="", blank=True)
    training_effective_from = models.DateTimeField(null=True, blank=True)
    training_effective_to = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

class Disciplinary_Record(models.Model):
    staff = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.CASCADE, related_name="staff_disciplinary_records")
    disciplinary_incidence_title = models.CharField(
        max_length=100, default="", blank=True)
    disciplinary_incidence_description = models.CharField(
        max_length=500, default="", blank=True)
    disciplinary_verdict = models.CharField(
        max_length=100, default="", blank=True)
    disciplinary_verdict_description = models.CharField(
        max_length=500, default="", blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

class VacancyRecord(models.Model):
    vacant_position = models.ForeignKey(
        staffPosition, null=True, on_delete=models.CASCADE, related_name="position_vacancies")
    vacancy_title = models.CharField(
        max_length=100, default="", blank=False)
    vacancy_description = models.CharField(
        max_length=500, default="", blank=False)
    vacancy_count = models.CharField(
        max_length=10, default="1", blank=False)
    vacancy_deadline = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

class VacantPositionRequirement(models.Model):
    vacancy_record = models.ForeignKey(
        VacancyRecord, null=True, on_delete=models.CASCADE, related_name="vacancy_requirements")
    requirement_title = models.CharField(
        max_length=100, default="", blank=False)
    requirement_description = models.CharField(
        max_length=500, default="", blank=False)
    
class JobApplication(models.Model): #to be continued
    vacancy_record = models.ForeignKey(
        VacancyRecord, null=True, on_delete=models.CASCADE, related_name="vacancy_applications")
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)

class StaffDeductionScheme(models.Model):
    staff_profile = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.CASCADE, related_name="staff_deduction_schemes")
    deduction = models.ForeignKey(Deduction, null=True,
                                  on_delete=models.CASCADE, related_name="deduction_schemes")
    

class StaffBonusScheme(models.Model):
    staff_profile = models.ForeignKey(
        StaffProfile, null=True, on_delete=models.CASCADE, related_name="staff_bonus_schemes")
    bonus = models.ForeignKey(Bonus, null=True,
                              on_delete=models.CASCADE, related_name="bonus_schemes")
    

