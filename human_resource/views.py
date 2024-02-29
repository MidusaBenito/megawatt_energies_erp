from django.shortcuts import render

from system_administration.utils import checkIfStaffCanEdit, convertTo24HRFormat, get_staff_profile_data
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from datetime import datetime
import json
from django.http import JsonResponse
from system_administration.models import *

# Create your views here.
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def human_resource_dashboard(request):
    date_format = '%d/%m/%Y, %H:%M'
    company_serial_number = request.data["serial_number"]
    active_user = request.user
    payload = {}
    staff_positions_list = []
    #staff_profiles = []
    deductions_list = []
    bonuses_list = []
    work_shifts_list = []
    company_departments_list = []
    company_branches_list = []
    current_date = datetime.now().date()
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        #
        staff_profile = StaffProfile.objects.get(user=request.user)
        if staff_profile.company_department.department_name == "human_resource_management" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
        #
            active_staff_profile_data = get_staff_profile_data(active_user)
            company_departments = company_profile.company_departments.all()
            for department in company_departments:
                if department.recycle_bin == False:
                    department_map = {}
                    department_map["department_id"] = str(department.id)
                    department_map["department_name"] = department.department_name
                    department_map["department_description"] = department.department_description
                    department_map["created_on"] = datetime.strftime(
                        department.created_on, date_format)
                    department_map["last_updated_on"] = datetime.strftime(
                        department.last_updated_on, date_format)
                    company_departments_list.append(department_map)
            company_branches = company_profile.company_branches.all()
            #criteria = {"company_profile": company_profile}
            if staff_profile.is_super_admin != True:
                #criteria = {"main_branch": False}
                company_branches = staff_profile.company_branch
            for branch in company_branches:
                if branch.recycle_bin == False and branch.branch_active == True:
                    branch_map = {}
                    branch_map["branch_id"] = str(branch.id)
                    branch_map["branch_name"] = branch.branch_name
                    branch_map["branch_description"] = branch.branch_description
                    branch_map["branch_county_location"] = branch.branch_county_location
                    branch_map["branch_phone"] = branch.branch_phone
                    branch_map["main_branch"] = "true" if branch.main_branch == True else "false"
                    branch_map["created_on"] = datetime.strftime(
                        branch.created_on, date_format)
                    branch_map["last_updated_on"] = datetime.strftime(
                        branch.last_updated_on, date_format)
                    #company_branches_list.append(branch_map)
                    #branch users
                    company_branch_staffs_list = []
                    branch_staffs = branch.company_branch_staffs.all()
                    for staff in branch_staffs:
                        if staff.recycle_bin == False:
                            time_sheets_list = []
                            staff_leaves_list = []
                            education_qualifications_list = []
                            staff_training_records_list = []
                            staff_disciplinary_records_list = []
                            staff_deduction_schemes_list = []
                            staff_bonus_schemes_list = []
                            staff_map = {}
                            staff_map["staff_id"] = str(staff.id)
                            staff_map["email_address"] = staff.user.username
                            staff_map["staff_position"] = staff.staff_position.position_title if staff.staff_position is not None else ""
                            staff_map["staff_number"] = staff.staff_number
                            staff_map["first_name"] = staff.first_name
                            staff_map["last_name"] = staff.last_name
                            staff_map["date_of_birth"] = staff.date_of_birth if staff.date_of_birth is not None else ''
                            staff_map["country_name"] = staff.country_name
                            staff_map["identification_number"] = staff.identification_number
                            staff_map["phone_number"] = staff.phone_number
                            staff_map["staff_title"] = staff.staff_title
                            staff_map["employment_start_date"] = staff.employment_start_date if staff.employment_start_date is not None else ''
                            staff_map["employment_end_date"] = staff.employment_end_date if staff.employment_end_date is not None else ''
                            staff_map["emergency_contact_phone"] = staff.emergency_contact_phone
                            staff_map["company_branch_name"] = branch.branch_name
                            staff_map["company_department"] = staff.company_department.department_name if staff.company_branch is not None else ""
                            staff_map["is_profile_set"] = "true" if staff.is_profile_set else "false"
                            staff_map["is_head_of_department"] = "true" if staff.is_head_of_department else "false"
                            staff_map["has_read_write_priviledges"] = "true" if staff.has_read_write_priviledges else "false"
                            staff_map["is_super_admin"] = "true" if staff.is_super_admin else "false"
                            staff_map["is_on_leave"] = "true" if staff.is_on_leave else "false"
                            #additional
                            staff_map["kra_pin"] = staff.kra_pin
                            staff_map["type_of_employment"] = staff.type_of_employment
                            staff_map["banking_institution_name"] = staff.banking_institution_name
                            staff_map["bank_account_name"] = staff.bank_account_name
                            staff_map["bank_account_number"] = staff.bank_account_number
                            staff_map["nhif_number"] = staff.nhif_number
                            staff_map["nhif_additional_info"] = staff.nhif_additional_info
                            staff_map["nssf_number"] = staff.nssf_number
                            staff_map["nssf_additional_info"] = staff.nssf_additional_info
                            staff_map["staff_additional_info"] = staff.staff_additional_info
                            staff_map["basic_salary"] = staff.basic_salary
                            staff_map["currency"] = company_profile.company_preferred_currency
                            #end
                            time_sheets = staff.staff_time_sheets.all()
                            for time_sheet in time_sheets:
                                if time_sheet.recycle_bin == False:
                                    time_sheet_map = {}
                                    time_sheet_map["time_sheet_id"] = str(time_sheet.id)
                                    time_sheet_map["check_in_time"] = datetime.strftime(
                                        time_sheet.check_in_time, date_format) if time_sheet.check_in_time is not None else ""
                                    time_sheet_map["check_out_time"] = datetime.strftime(
                                        time_sheet.check_out_time, date_format) if time_sheet.check_out_time is not None else ""
                                    time_sheet_map["created_on"] = datetime.strftime(
                                        time_sheet.created_on, date_format) if time_sheet.created_on is not None else ""
                                    time_sheet_map["last_updated_on"] = datetime.strftime(
                                        time_sheet.last_updated_on, date_format) if time_sheet.last_updated_on is not None else ""
                                    time_sheets_list.append(time_sheet_map)
                            staff_map["time_sheets_list"] = time_sheets_list
                            #adding extra data points
                            education_qualifications = staff.staff_education_qualifications.all()
                            for education_qualification in education_qualifications:
                                education_qualification_map = {}
                                education_qualification_map["education_qualification_id"] = str(
                                    education_qualification.id)
                                education_qualification_map["qualification_title"] = education_qualification.qualification_title
                                education_qualification_map["accredition_category"] = education_qualification.accredition_category
                                education_qualification_map["accrediting_institution"] = education_qualification.accrediting_institution
                                education_qualification_map["year_of_accredition"] = education_qualification.year_of_accredition
                                education_qualification_map["created_on"] = datetime.strftime(
                                        education_qualification.created_on, date_format) if education_qualification.created_on is not None else "" 
                                education_qualification_map["last_updated_on"] = datetime.strftime(
                                    education_qualification.last_updated_on, date_format) if education_qualification.last_updated_on is not None else ""
                                education_qualifications_list.append(
                                    education_qualification_map)
                            staff_map["education_qualifications_list"] = education_qualifications_list
                            staff_training_records = staff.staff_training_records.all()
                            for staff_training_record in staff_training_records:
                                staff_training_record_map = {}
                                staff_training_record_map["training_record_id"] = str(
                                    staff_training_record.id)
                                staff_training_record_map["training_title"] = staff_training_record.training_title
                                staff_training_record_map["training_description"] = staff_training_record.training_description
                                staff_training_record_map["training_effective_from"] = datetime.strftime(
                                    staff_training_record.training_effective_from, date_format) if staff_training_record.training_effective_from is not None else ""
                                staff_training_record_map["training_effective_to"] = datetime.strftime(
                                    staff_training_record.training_effective_to, date_format) if staff_training_record.training_effective_to is not None else ""
                                staff_training_record_map["created_on"] = datetime.strftime(
                                    staff_training_record.created_on, date_format) if staff_training_record.created_on is not None else ""
                                staff_training_record_map["last_updated_on"] = datetime.strftime(
                                    staff_training_record.last_updated_on, date_format) if staff_training_record.last_updated_on is not None else ""
                                staff_training_records_list.append(
                                    staff_training_record_map)
                            staff_map["staff_training_records_list"] = staff_training_records_list
                            staff_disciplinary_records = staff.staff_disciplinary_records.all()
                            for staff_disciplinary_record in staff_disciplinary_records:
                                staff_disciplinary_record_map = {}
                                staff_disciplinary_record_map["staff_disciplinary_record_id"] = str(
                                    staff_disciplinary_record.id)
                                staff_disciplinary_record_map[
                                    "disciplinary_incidence_title"] = staff_disciplinary_record.disciplinary_incidence_title
                                staff_disciplinary_record_map[
                                    "disciplinary_incidence_description"] = staff_disciplinary_record.disciplinary_incidence_description
                                staff_disciplinary_record_map[
                                    "disciplinary_verdict"] = staff_disciplinary_record.disciplinary_verdict
                                staff_disciplinary_record_map[
                                    "disciplinary_verdict_description"] = staff_disciplinary_record.disciplinary_verdict_description
                                staff_disciplinary_record_map[
                                    "created_on"] = datetime.strftime(
                                    staff_disciplinary_record.created_on, date_format) if staff_disciplinary_record.created_on is not None else ""
                                staff_disciplinary_record_map[
                                    "last_updated_on"] = datetime.strftime(
                                    staff_disciplinary_record.last_updated_on, date_format) if staff_disciplinary_record.last_updated_on is not None else ""
                                staff_disciplinary_records_list.append(staff_disciplinary_record_map)
                            staff_map["staff_disciplinary_records_list"] = staff_disciplinary_records_list
                            #end of extra data points
                            staff_leaves = staff.staff_leave_instances.all()
                            for staff_leave in staff_leaves:
                                if staff_leave.recycle_bin == False:
                                    staff_leave_map = {}
                                    staff_leave_map["leave_id"] = str(staff_leave.id)
                                    staff_leave_map["leave_type"] = staff_leave.leave_type
                                    staff_leave_map["leave_description"] = staff_leave.leave_description
                                    staff_leave_map["leave_start_date"] = datetime.strftime(
                                        staff_leave.leave_start_date, '%d/%m/%Y') if staff_leave.leave_start_date is not None else ""
                                    staff_leave_map["leave_end_date"] = datetime.strftime(
                                        staff_leave.leave_end_date, '%d/%m/%Y') if staff_leave.leave_end_date is not None else ""
                                    staff_leave_map["number_of_leave_days"] = staff_leave.number_of_leave_days #only count working days
                                    staff_leave_map["leave_department_approval"] = staff_leave.leave_department_approval
                                    staff_leave_map["leave_hr_approval"] = staff_leave.leave_hr_approval
                                    staff_leave_map["leave_status"] = staff_leave.leave_status
                                    creator_map = {}
                                    creator_map["staff_id"] = str(
                                        staff_leave.created_by.id) if staff_leave.created_by is not None else ""
                                    creator_map["staff_name"] = f'{staff_leave.created_by.first_name} {staff_leave.created_by.last_name}' if staff_leave.created_by is not None else ""
                                    creator_map["staff_position"] = staff_leave.created_by.staff_position.position_title if staff_leave.created_by.staff_position is not None else ""
                                    staff_leave_map["created_by"] = creator_map
                                    creator_map = {}
                                    creator_map["staff_id"] = str(
                                        staff_leave.last_updated_by.id) if staff_leave.last_updated_by is not None else ""
                                    creator_map["staff_name"] = f'{staff_leave.last_updated_by.first_name} {staff_leave.last_updated_by.last_name}' if staff_leave.last_updated_by is not None else ""
                                    creator_map["staff_position"] = staff_leave.last_updated_by.staff_position.position_title if staff_leave.last_updated_by.staff_position is not None else ""
                                    staff_leave_map["last_updated_by"] = creator_map
                                    staff_leave_map["created_on"] = datetime.strftime(
                                        staff_leave.created_on, date_format) if staff_leave.created_on is not None else ""
                                    staff_leave_map["last_updated_on"] = datetime.strftime(
                                        staff_leave.last_updated_on, date_format) if staff_leave.last_updated_on is not None else ""
                                    #print(staff_leave_map)
                                    staff_leaves_list.append(staff_leave_map)
                            staff_map["staff_leaves_list"] = staff_leaves_list
                            staff_deduction_schemes = staff.staff_deduction_schemes.all()
                            for staff_deduction_scheme in staff_deduction_schemes:
                                staff_deduction_scheme_map = {}
                                staff_deduction_scheme_map["staff_deduction_scheme_id"] = str(staff_deduction_scheme.id)
                                staff_deduction_scheme_map["deduction_id"] = str(
                                    staff_deduction_scheme.deduction.id)
                                staff_deduction_scheme_map["deduction_title"] = staff_deduction_scheme.deduction.deduction_title
                                staff_deduction_scheme_map["deduction_description"] = staff_deduction_scheme.deduction.deduction_description
                                staff_deduction_scheme_map["deduction_type"] = staff_deduction_scheme.deduction.deduction_type
                                staff_deduction_scheme_map["deduction_module"] = staff_deduction_scheme.deduction.deduction_module
                                staff_deduction_scheme_map["deduction_value"] = staff_deduction_scheme.deduction.deduction_value
                                if staff_deduction_scheme.deduction.date_effective_to >= current_date:
                                    staff_deduction_schemes_list.append(
                                        staff_deduction_scheme_map)  # 
                            staff_map["staff_deduction_schemes_list"] = staff_deduction_schemes_list
                            staff_bonus_schemes = staff.staff_bonus_schemes.all()
                            for staff_bonus_scheme in staff_bonus_schemes:
                                staff_bonus_scheme_map = {}
                                staff_bonus_scheme_map["staff_bonus_scheme_id"] = str(staff_bonus_scheme.id)
                                staff_bonus_scheme_map["bonus_id"] = str(
                                    staff_bonus_scheme.bonus.id)
                                staff_bonus_scheme_map["bonus_title"] = staff_bonus_scheme.bonus.bonus_title
                                staff_bonus_scheme_map["bonus_description"] = staff_bonus_scheme.bonus.bonus_description
                                staff_bonus_scheme_map["bonus_type"] = staff_bonus_scheme.bonus.bonus_type
                                staff_bonus_scheme_map["bonus_amount"] = staff_bonus_scheme.bonus.bonus_amount
                                if staff_bonus_scheme.bonus.date_effective_to >= current_date:
                                    staff_bonus_schemes_list.append(
                                        staff_bonus_scheme_map)
                            staff_map["staff_bonus_schemes_list"] = staff_bonus_schemes_list
                            staff_map["created_on"] = datetime.strftime(
                                staff.created_on, date_format) if staff.created_on is not None else ""
                            staff_map["last_updated_on"] = datetime.strftime(
                                staff.last_updated_on, date_format) if staff.last_updated_on is not None else ""
                            company_branch_staffs_list.append(staff_map)
                    branch_map["branch_staff_profiles"] = company_branch_staffs_list
                    payroll_sheets_list = []
                    payroll_sheets = branch.branch_payroll_sheets.all()
                    for payroll_sheet in payroll_sheets:
                        if payroll_sheet.recycle_bin == False:
                            payroll_sheet_map = {}
                            payroll_sheet_map["payroll_sheet_id"] =  str(payroll_sheet.id)
                            payroll_sheet_map["payroll_sheet_title"] = payroll_sheet.payroll_sheet_title
                            payroll_sheet_map["payroll_sheet_number"] = payroll_sheet.payroll_sheet_number
                            payroll_sheet_map["payroll_sheet_description"] = payroll_sheet.payroll_sheet_description
                            payroll_sheet_map["payroll_sheet_for_the_month_of"] = payroll_sheet.payroll_sheet_for_the_month_of
                            payroll_sheet_map["payroll_sheet_for_the_year"] = payroll_sheet.payroll_sheet_for_the_year
                            payroll_sheet_map["payroll_sheet_value"] = payroll_sheet.payroll_sheet_value
                            #added
                            payroll_sheet_map["payroll_sheet_total_net_pay_value"] = payroll_sheet.payroll_sheet_total_net_pay_value
                            payroll_sheet_map["payroll_sheet_total_bonus_value"] = payroll_sheet.payroll_sheet_total_bonus_value
                            payroll_sheet_map["payroll_sheet_total_deduction_value"] = payroll_sheet.payroll_sheet_total_deduction_value
                            payroll_sheet_map["payroll_sheet_total_commission_value"] = payroll_sheet.payroll_sheet_total_commission_value
                            payroll_sheet_map["currency"] = company_profile.company_preferred_currency
                            #end added
                            payroll_sheet_map["payroll_sheet_approved_by_finance"] = "true" if payroll_sheet.payroll_sheet_approved_by_finance == True else "false"
                            payroll_sheet_map["payroll_sheet_payment_settled"] = "true" if payroll_sheet.payroll_sheet_payment_settled == True else "false"
                            staff_map = {}
                            staff_map["staff_id"] = str(
                                payroll_sheet.created_by.id) if payroll_sheet.created_by is not None else ""
                            staff_map["staff_name"] = f'{payroll_sheet.created_by.first_name} {payroll_sheet.created_by.last_name}' if payroll_sheet.created_by is not None else ""
                            staff_map["staff_position"] = payroll_sheet.created_by.staff_position.position_title if payroll_sheet.created_by.staff_position is not None else ""
                            payroll_sheet_map["created_by"] = staff_map
                            staff_map = {}
                            staff_map["staff_id"] = str(
                                payroll_sheet.last_updated_by.id) if payroll_sheet.last_updated_by is not None else ""
                            staff_map["staff_name"] = f'{payroll_sheet.last_updated_by.first_name} {payroll_sheet.last_updated_by.last_name}' if payroll_sheet.last_updated_by is not None else ""
                            staff_map["staff_position"] = payroll_sheet.last_updated_by.staff_position.position_title if payroll_sheet.last_updated_by.staff_position is not None else ""
                            payroll_sheet_map["last_updated_by"] = staff_map
                            payroll_sheet_map["created_on"] = datetime.strftime(
                                payroll_sheet.created_on, date_format) if payroll_sheet.created_on is not None else ""
                            payroll_sheet_map["last_updated_on"] = datetime.strftime(
                                payroll_sheet.last_updated_on, date_format) if payroll_sheet.last_updated_on is not None else ""
                            payroll_instances_list = []
                            payroll_instances = payroll_sheet.staff_payroll_items.all()
                            for payroll_instance in payroll_instances:
                                if payroll_instance.recycle_bin == False:
                                    payroll_instance_map = {}
                                    payroll_instance_map["staff_id"] = str(
                                        payroll_instance.staff_profile.id)
                                    deduction_instances = payroll_instance.deduction_instance.all()
                                    deduction_instances_list = []
                                    for deduction_instance in deduction_instances:
                                        if deduction_instance.recycle_bin == False:
                                            deduction_instance_map ={}
                                            deduction_instance_map["deduction_instance_id"] = str(deduction_instance.id)
                                            deduction_instance_map["deduction_id"] = str(
                                                deduction_instance.deduction.id) if deduction_instance.deduction is not None else ""
                                            deduction_instance_map["deduction_title"] = deduction_instance.deduction.deduction_title
                                            deduction_instance_map["deduction_instance_value"] = deduction_instance.deduction_instance_value
                                            staff_map = {}
                                            staff_map["staff_id"] = str(
                                                deduction_instance.created_by.id) if deduction_instance.created_by is not None else ""
                                            staff_map["staff_name"] = f'{deduction_instance.created_by.first_name} {deduction_instance.created_by.last_name}' if deduction_instance.created_by is not None else ""
                                            staff_map["staff_position"] = deduction_instance.created_by.staff_position.position_title if deduction_instance.created_by.staff_position is not None else ""
                                            deduction_instance_map["created_by"] = staff_map
                                            staff_map = {}
                                            staff_map["staff_id"] = str(
                                                deduction_instance.last_updated_by.id) if deduction_instance.last_updated_by is not None else ""
                                            staff_map["staff_name"] = f'{deduction_instance.last_updated_by.first_name} {deduction_instance.last_updated_by.last_name}' if deduction_instance.last_updated_by is not None else ""
                                            staff_map["staff_position"] = deduction_instance.last_updated_by.staff_position.position_title if deduction_instance.last_updated_by.staff_position is not None else ""
                                            deduction_instance_map["last_updated_by"] = staff_map
                                            deduction_instance_map["created_on"] = datetime.strftime(
                                                deduction_instance.created_on, date_format) if deduction_instance.created_on is not None else ""
                                            deduction_instance_map["last_updated_on"] = datetime.strftime(
                                                deduction_instance.last_updated_on, date_format) if deduction_instance.last_updated_on is not None else ""
                                            deduction_instances_list.append(deduction_instance_map)
                                    payroll_instance_map["deduction_instances_list"] = deduction_instances_list
                                    payroll_instance_map["gross_salary"] = payroll_instance.gross_salary
                                    bonus_instances = payroll_instance.bonus_instance.all()
                                    bonus_instances_list = []
                                    for bonus_instance in bonus_instances:
                                        if bonus_instance.recycle_bin == False:
                                            bonus_instance_map = {}
                                            bonus_instance_map["bonus_instance_id"] = str(
                                                bonus_instance.id)
                                            bonus_instance_map["bonus_id"] = str(
                                                bonus_instance.bonus.id) if bonus_instance.bonus is not None else ""
                                            bonus_instance_map["bonus_instance_value"] = bonus_instance.bonus_instance_value
                                            bonus_instance_map["bonus_title"] = bonus_instance.bonus.bonus_title
                                            staff_map = {}
                                            staff_map["staff_id"] = str(
                                                bonus_instance.created_by.id) if bonus_instance.created_by is not None else ""
                                            staff_map["staff_name"] = f'{bonus_instance.created_by.first_name} {bonus_instance.created_by.last_name}' if bonus_instance.created_by is not None else ""
                                            staff_map["staff_position"] = bonus_instance.created_by.staff_position.position_title if bonus_instance.created_by.staff_position is not None else ""
                                            bonus_instance_map["created_by"] = staff_map
                                            staff_map = {}
                                            staff_map["staff_id"] = str(
                                                bonus_instance.last_updated_by.id) if bonus_instance.last_updated_by is not None else ""
                                            staff_map["staff_name"] = f'{bonus_instance.last_updated_by.first_name} {bonus_instance.last_updated_by.last_name}' if bonus_instance.last_updated_by is not None else ""
                                            staff_map["staff_position"] = bonus_instance.last_updated_by.staff_position.position_title if bonus_instance.last_updated_by.staff_position is not None else ""
                                            bonus_instance_map["last_updated_by"] = staff_map
                                            bonus_instance_map["created_on"] = datetime.strftime(
                                                bonus_instance.created_on, date_format) if deduction_instance.created_on is not None else ""
                                            bonus_instance_map["last_updated_on"] = datetime.strftime(
                                                bonus_instance.last_updated_on, date_format) if bonus_instance.last_updated_on is not None else ""
                                            bonus_instances_list.append(
                                                bonus_instance_map)
                                    payroll_instance_map["bonus_instances_list"] = bonus_instances_list
                                    payroll_instance_map["net_salary"] = payroll_instance.net_salary
                                    #
                                    payroll_instance_commissions = payroll_instance.staff_payroll_instance_commissions.all()
                                    payroll_instance_commissions_list = []
                                    for commission_sheet_instance in payroll_instance_commissions:
                                        if commission_sheet_instance.recycle_bin == False:
                                            commission_sheet_instance_map = {}
                                            commission_sheet_instance_map["commission_sheet_instance_id"] = str(
                                                commission_sheet_instance.id)
                                            commission_sheet_instance_map["customer_order_id"] = str(
                                                commission_sheet_instance.customer_order.id) if commission_sheet_instance.customer_order is not None else ""
                                            commission_sheet_instance_map[
                                                "commission_value"] = commission_sheet_instance.commission_value
                                            commission_sheet_instance_map[
                                                "commission_sheet_id"] = str(commission_sheet_instance.commission_sheet.id) if commission_sheet_instance.commission_sheet is not None else ""
                                            commission_sheet_instance_map[
                                                "commission_sheet_number"] = commission_sheet_instance.commission_sheet.commission_sheet_number if commission_sheet_instance.commission_sheet is not None else ""
                                            commission_sheet_instance_map[
                                                "commission_sheet_title"] = commission_sheet_instance.commission_sheet.commission_sheet_title if commission_sheet_instance.commission_sheet is not None else ""
                                            payroll_instance_commissions_list.append(
                                                commission_sheet_instance_map)
                                    payroll_instance_map["payroll_instance_commissions_list"] = payroll_instance_commissions_list
                                    payroll_instance_map["commissions_total"] = payroll_instance.commissions_total
                                    #
                                    staff_map = {}
                                    staff_map["staff_id"] = str(
                                        payroll_instance.created_by.id) if payroll_instance.created_by is not None else ""
                                    staff_map["staff_name"] = f'{payroll_instance.created_by.first_name} {payroll_instance.created_by.last_name}' if payroll_instance.created_by is not None else ""
                                    staff_map["staff_position"] = payroll_instance.created_by.staff_position.position_title if payroll_instance.created_by.staff_position is not None else ""
                                    payroll_instance_map["created_by"] = staff_map
                                    staff_map = {}
                                    staff_map["staff_id"] = str(
                                        payroll_instance.last_updated_by.id) if payroll_instance.last_updated_by is not None else ""
                                    staff_map["staff_name"] = f'{payroll_instance.last_updated_by.first_name} {payroll_instance.last_updated_by.last_name}' if payroll_instance.last_updated_by is not None else ""
                                    staff_map["staff_position"] = payroll_instance.last_updated_by.staff_position.position_title if payroll_instance.last_updated_by.staff_position is not None else ""
                                    payroll_instance_map["last_updated_by"] = staff_map
                                    payroll_instance_map["created_on"] = datetime.strftime(
                                        payroll_instance.created_on, date_format) if payroll_instance.created_on is not None else ""
                                    payroll_instance_map["last_updated_on"] = datetime.strftime(
                                        payroll_instance.last_updated_on, date_format) if payroll_instance.last_updated_on is not None else ""
                                    payroll_instances_list.append(
                                        payroll_instance_map)
                            #print(payroll_instances_list)
                            payroll_sheet_map["payroll_instances_list"] = payroll_instances_list
                            payroll_sheets_list.append(payroll_sheet_map)
                    branch_map["payroll_sheets_list"] = payroll_sheets_list
                    company_branches_list.append(branch_map)
            staff_positions = company_profile.company_staff_positions.all()
            for position in staff_positions:
                if position.recycle_bin == False:
                    staff_position_map ={}
                    staff_position_map["staff_position_id"] = str(position.id)
                    staff_position_map["position_title"] = position.position_title
                    staff_position_map["position_description"] = position.position_description
                    staff_position_map["salary"] = position.salary
                    staff_position_map["created_on"] = datetime.strftime(
                        position.created_on, date_format) if position.created_on is not None else ""
                    staff_position_map["last_updated_on"] = datetime.strftime(
                        position.last_updated_on, date_format) if position.last_updated_on is not None else ""
                    staff_positions_list.append(staff_position_map)
            deductions = company_profile.company_deductions.all()
            for deduction in deductions:
                if deduction.recycle_bin == False:
                    deduction_map = {}
                    deduction_map["deduction_id"] = str(deduction.id)
                    deduction_map["deduction_title"] = deduction.deduction_title
                    deduction_map["deduction_description"] = deduction.deduction_description
                    deduction_map["deduction_type"] = deduction.deduction_type
                    deduction_map["deduction_module"] = deduction.deduction_module
                    deduction_map["deduction_value"] = deduction.deduction_value
                    deduction_map["date_effective_from"] = deduction.date_effective_from
                    deduction_map["date_effective_to"] = deduction.date_effective_to
                    staff_map = {}
                    staff_map["staff_id"] = str(deduction.created_by.id) if deduction.created_by is not None else ""
                    staff_map["staff_name"] = f'{deduction.created_by.first_name} {deduction.created_by.last_name}' if deduction.created_by is not None else ""
                    staff_map["staff_position"] = deduction.created_by.staff_position.position_title if deduction.created_by.staff_position is not None else ""
                    deduction_map["created_by"] = staff_map
                    staff_map = {}
                    staff_map["staff_id"] = str(
                        deduction.last_updated_by.id) if deduction.last_updated_by is not None else ""
                    staff_map["staff_name"] = f'{deduction.last_updated_by.first_name} {deduction.last_updated_by.last_name}' if deduction.last_updated_by is not None else ""
                    staff_map["staff_position"] = deduction.last_updated_by.staff_position.position_title if deduction.last_updated_by.staff_position is not None else ""
                    deduction_map["last_updated_by"] = staff_map
                    deduction_map["created_on"] = datetime.strftime(
                        deduction.created_on, date_format) if deduction.created_on is not None else ""
                    deduction_map["last_updated_on"] = datetime.strftime(
                        deduction.last_updated_on, date_format) if deduction.last_updated_on is not None else ""
                    deductions_list.append(deduction_map)
            #bonuses
            bonuses = company_profile.company_bonuses.all()
            for bonus in bonuses:
                if bonus.recycle_bin == False:
                    bonus_map = {}
                    bonus_map["bonus_id"] = str(bonus.id)
                    bonus_map["bonus_title"] = bonus.bonus_title
                    bonus_map["bonus_description"] = bonus.bonus_description
                    bonus_map["bonus_type"] = bonus.bonus_type
                    bonus_map["bonus_amount"] = bonus.bonus_amount
                    bonus_map["date_effective_from"] = datetime.strftime(
                        bonus.date_effective_from, '%d/%m/%Y')
                    bonus_map["date_effective_to"] = datetime.strftime(
                        bonus.date_effective_to, '%d/%m/%Y')
                    staff_map = {}
                    staff_map["staff_id"] = str(
                        bonus.created_by.id) if bonus.created_by is not None else ""
                    staff_map["staff_name"] = f'{bonus.created_by.first_name} {bonus.created_by.last_name}' if bonus.created_by is not None else ""
                    staff_map["staff_position"] = bonus.created_by.staff_position.position_title if bonus.created_by.staff_position is not None else ""
                    bonus_map["created_by"] = staff_map
                    staff_map = {}
                    staff_map["staff_id"] = str(
                        bonus.last_updated_by.id) if bonus.last_updated_by is not None else ""
                    staff_map["staff_name"] = f'{bonus.last_updated_by.first_name} {bonus.last_updated_by.last_name}' if bonus.last_updated_by is not None else ""
                    staff_map["staff_position"] = bonus.last_updated_by.staff_position.position_title if bonus.last_updated_by.staff_position is not None else ""
                    bonus_map["last_updated_by"] = staff_map
                    bonus_map["created_on"] = datetime.strftime(
                        bonus.created_on, date_format) if bonus.created_on is not None else ""
                    bonus_map["last_updated_on"] = datetime.strftime(
                        bonus.last_updated_on, date_format) if bonus.last_updated_on is not None else ""
                    bonuses_list.append(bonus_map)
            work_shifts = company_profile.company_work_shifts.all()
            for work_shift in work_shifts:
                if work_shift.recycle_bin == False:
                    work_shift_map = {}
                    work_shift_map["work_shift_id"] = str(work_shift.id)
                    work_shift_map["shift_name"] = work_shift.shift_name
                    work_shift_map["shift_hours_start"] = work_shift.shift_hours_start
                    work_shift_map["shift_hours_end"] = work_shift.shift_hours_end
                    work_shift_map["shift_description"] = work_shift.shift_description
                    working_days = work_shift.workday_shifts.all()
                    working_days_list = []
                    for working_day in working_days:
                        if working_day.recycle_bin == False:
                            working_day_map = {}
                            working_day_map["working_day_id"] = str(working_day.id)
                            working_day_map["day_of_week_identifier"] = working_day.day_of_week_identifier
                            #working_day_map["working_day_description"] = working_day.working_day_description
                            working_day_map["created_on"] = datetime.strftime(
                                working_day.created_on, date_format) if working_day.created_on is not None else ""
                            working_day_map["last_updated_on"] = datetime.strftime(
                                working_day.last_updated_on, date_format) if working_day.last_updated_on is not None else ""
                            working_days_list.append(working_day_map)
                    work_shift_map["working_days"] = working_days_list

                    work_shift_map["created_on"] = datetime.strftime(
                        work_shift.created_on, date_format) if work_shift.created_on is not None else ""
                    work_shift_map["last_updated_on"] = datetime.strftime(
                        work_shift.last_updated_on, date_format) if work_shift.last_updated_on is not None else ""
                    work_shifts_list.append(work_shift_map)
            
            payload["active_staff_profile_data"] = active_staff_profile_data
            payload["staff_positions_list"] = staff_positions_list
            payload["deductions_list"] = deductions_list
            payload["bonuses_list"] = bonuses_list
            payload["work_shifts_list"] = work_shifts_list
            payload["company_departments_list"] = company_departments_list
            payload["company_branches_list"] = company_branches_list
            #print(staff_positions_list)
            return Response({"message": "true", "payload": payload}, status=200)
        else:
            return Response({"message": "false", "payload": payload}, status=401)
    except Exception as e:
        print(e)
        return Response({"message": "false", "payload": payload}, status=500)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_staff_profile(request):  
    date_format = '%d/%m/%Y'
    try:
        company_serial_number = request.data["serial_number"]
        staff_id_to_edit = request.data["staff_id_to_edit"]
        #print(staff_id_to_edit)
        is_self_edit = request.data["is_self_edit"]  #this flag checks if it is the user editing their own profile or the human resource manager that is doing the editing
        staff_position_id = request.data["staff_position_id"]
        #print(staff_position_id)
        company_branch_id = request.data["company_branch_id"]
        company_department_id = request.data["company_department_id"]
        # print(f'{staff_id_to_edit} here')
        # print(f'{staff_position_id} there')
        # print(f'{company_branch_id} that')
        # print(f'{company_department_id} was')
        first_name = request.data["first_name"]
        last_name = request.data["last_name"]
        #email_address = request.data["email_address"]
        date_of_birth = datetime.strptime(
            request.data["date_of_birth"], date_format).strftime("%Y-%m-%d") if len(request.data["date_of_birth"]) > 0 else None
        country_name = request.data["country_name"]
        identification_number = request.data["identification_number"]
        phone_number = request.data["phone_number"]
        staff_title = request.data["staff_title"]
        employment_start_date = datetime.strptime(
            request.data["employment_start_date"], date_format).strftime("%Y-%m-%d") if len(request.data["employment_start_date"]) > 0 else None
        employment_end_date = datetime.strptime(
            request.data["employment_end_date"], date_format).strftime("%Y-%m-%d") if len(request.data["employment_end_date"]) > 0 else None
        emergency_contact_phone = request.data["emergency_contact_phone"]
        is_head_of_department = True if request.data["is_head_of_department"] else False
        has_read_write_priviledges = True if request.data["has_read_write_priviledges"] == "true" else False
        kra_pin = request.data["kra_pin"]
        staff_additional_info = request.data["staff_additional_info"]
        active_user = request.user
        staff_profile_to_edit = StaffProfile.objects.get(user=active_user)#active_user
        if is_self_edit == "true":
            if staff_profile_to_edit.is_super_admin == True:
                staff_profile_serializer = StaffProfileSerializer(
                    instance=staff_profile_to_edit, data={'staff_position': int(staff_position_id), 'company_branch': int(company_branch_id),
                                                        'company_department': int(company_department_id), 'first_name': first_name, 
                                                        'last_name': last_name, 'date_of_birth': date_of_birth,
                                                        'country_name': country_name, 'identification_number': identification_number, 'phone_number': phone_number,
                                                        'staff_title':staff_title,'employment_start_date':employment_start_date,'employment_end_date':employment_end_date,
                                                          'emergency_contact_phone': emergency_contact_phone, 'kra_pin': kra_pin, 'staff_additional_info': staff_additional_info
                                                        })
            else:
                staff_profile_serializer = StaffProfileSerializer(
                    instance=staff_profile_to_edit, data={'date_of_birth': date_of_birth,
                                                          'country_name': country_name, 'phone_number': phone_number,
                                                          'emergency_contact_phone': emergency_contact_phone,
                                                          })
            if staff_profile_serializer.is_valid():
                staff_profile_serializer.save()
                if staff_profile_to_edit.is_profile_set != True:
                    staff_profile_to_edit.is_profile_set = True
                    staff_profile_to_edit.save()
                return Response({"message": "You have edited your staff profile successfully"}, status=200)
            else:
                #print(staff_profile_serializer.errors)
                return Response({"message": "Error editing your staff profile!"}, status=406)
        else:
            active_staff_profile = StaffProfile.objects.get(user=active_user)
            editPossible = False
            if active_staff_profile.is_super_admin == True:
                editPossible = True 
            else:
                editPossible = checkIfStaffCanEdit(
                    active_staff_profile, company_department_id)
            
            if editPossible == True:
                staff_profile_to_edit = StaffProfile.objects.get(
                    id=int(staff_id_to_edit))
                staff_profile_serializer = StaffProfileSerializer(
                    instance=staff_profile_to_edit, data={'staff_position': int(staff_position_id), 'company_branch': int(company_branch_id),
                                                        'company_department': int(company_department_id), 'first_name': first_name,
                                                        'last_name': last_name, 'date_of_birth': date_of_birth,
                                                        'country_name': country_name, 'identification_number': identification_number, 'phone_number': phone_number,
                                                        'staff_title': staff_title, 'employment_start_date': employment_start_date, 'employment_end_date': employment_end_date,
                                                          'emergency_contact_phone': emergency_contact_phone, 'is_head_of_department': is_head_of_department, 'has_read_write_priviledges': has_read_write_priviledges, 'kra_pin': kra_pin, 'staff_additional_info': staff_additional_info
                                                        })
                if staff_profile_serializer.is_valid():
                    staff_profile_serializer.save()
                    if staff_profile_to_edit.is_profile_set != True:
                        staff_profile_to_edit.is_profile_set = True
                        staff_profile_to_edit.save()
                    return Response({"message": "Staff profile edited successfully"}, status=200)
                else:
                    #print(staff_profile_serializer.errors)
                    return Response({"message": "Error editing staff profile!"}, status=406)
            else:
                return Response({"message": "You are unauthorised to perform this action"}, status=401)
    except Exception as e:
        print(e)
        return Response({"message": "Error editing staff profile"}, status=500)
            
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_staff_position(request):
    company_serial_number = request.data["serial_number"]
    position_title = request.data["position_title"]
    position_description = request.data["position_description"]
    salary = request.data["salary"]
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=request.user)
        if staff_profile.company_department.department_name == "human_resource_management" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            serializers = staffPositionSerializer(data={'company_profile':company_profile.id,'position_title':position_title,'position_description':position_description,'salary':salary})
            if serializers.is_valid():
                staff_position = serializers.save()
                return Response({"message": "Staff position created successfully", }, status=200)
            return Response({"message": "Unable to create staff position", }, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this action", }, status=401)
    except:
        return Response({"message": "Error creating staff position", }, status=500)
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_staff_position(request):
    company_serial_number = request.data["serial_number"]
    staff_position_to_edit_id = request.data["staff_position_to_edit_id"]
    position_title = request.data["position_title"]
    position_description = request.data["position_description"]
    salary = request.data["salary"]
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=request.user)
        staff_position_to_edit = staffPosition.objects.get(
            id=int(staff_position_to_edit_id))
        if staff_profile.company_department.department_name == "human_resource_management" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            serializers = staffPositionSerializer(instance=staff_position_to_edit,data={'company_profile':company_profile.id,'position_title':position_title,'position_description':position_description,'salary':salary})
            if serializers.is_valid():
                staff_position = serializers.save()
                return Response({"message": "Staff position edited successfully", }, status=200)
            return Response({"message": "Unable to edit staff position", }, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this action", }, status=401)
    except:
        return Response({"message": "Error editing staff position", }, status=500)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def super_hr_get_staff_profiles_to_set_up(request):
    payload = {}
    company_serial_number = request.data["serial_number"]
    try:
        # company_profile = CompanyProfile.objects.get(
        #     company_serial_number=company_serial_number)
        criteria = {"is_profile_set":False}
        unset_staff_profiles = StaffProfile.objects.filter(**criteria)
        unset_staff_profiles_list = []
        staff_profile = StaffProfile.objects.get(user=request.user)
        for staff in unset_staff_profiles:
            if staff.recycle_bin == False:
                staff_map = {}
                staff_map["staff_id"] = str(staff.id)
                staff_map["email_address"] = staff.user.username
                staff_map["staff_number"] = staff.staff_number
                #print(staff_map)
                unset_staff_profiles_list.append(staff_map)
        payload["unset_staff_profiles_list"] = unset_staff_profiles_list
        return Response({"message": "true", "payload": payload}, status=200)
    except:# Exception as e:
        #print(e)
        return Response({"message": "false", "payload": payload}, status=500)
            

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_bonus(request):
    date_format = '%d/%m/%Y'
    company_serial_number = request.data["serial_number"]
    bonus_title = request.data["bonus_title"]
    bonus_description = request.data["bonus_description"]
    bonus_type = request.data["bonus_type"]
    bonus_amount = request.data["bonus_amount"]
    date_effective_from = datetime.strptime(
        request.data["date_effective_from"], date_format).strftime("%Y-%m-%d") if len(request.data["date_effective_from"]) > 0 else None
    date_effective_to = datetime.strptime(
        request.data["date_effective_to"], date_format).strftime("%Y-%m-%d") if len(request.data["date_effective_to"]) > 0 else None
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=request.user)
        if staff_profile.company_department.department_name == "human_resource_management" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            serializers = BonusSerializer(data={'company_profile':company_profile.id,'bonus_title': bonus_title, 'bonus_description': bonus_description, 'bonus_type': bonus_type,
                                          'bonus_amount': bonus_amount, 'date_effective_from': date_effective_from, 'date_effective_to': date_effective_to, 'created_by': staff_profile.id, 'last_updated_by': staff_profile.id})
            if serializers.is_valid():
                bonus_instance = serializers.save()
                return Response({"message": "Bonus payment item created successfully", }, status=200)
            #print(serializers.errors)
            return Response({"message": "Unable to create bonus payment item", }, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this action", }, status=401)
    except:
        return Response({"message": "Error creating bonus payment item", }, status=500)
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_deduction(request):
    date_format = '%d/%m/%Y'
    company_serial_number = request.data["serial_number"]
    deduction_title = request.data["deduction_title"]
    deduction_description = request.data["deduction_description"]
    deduction_type = request.data["deduction_type"]
    deduction_module = request.data["deduction_module"]
    deduction_value = request.data["deduction_value"]
    date_effective_from = datetime.strptime(
        request.data["date_effective_from"], date_format).strftime("%Y-%m-%d") if len(request.data["date_effective_from"]) > 0 else None
    date_effective_to = datetime.strptime(
        request.data["date_effective_to"], date_format).strftime("%Y-%m-%d") if len(request.data["date_effective_to"]) > 0 else None
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=request.user)
        if staff_profile.company_department.department_name == "human_resource_management" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            serializers = DeductionSerializer(data={'company_profile': company_profile.id, 'deduction_title': deduction_title, 'deduction_description': deduction_description, 'deduction_type': deduction_type,
                                          'deduction_value': deduction_value, 'deduction_module':deduction_module, 'date_effective_from': date_effective_from, 'date_effective_to': date_effective_to, 'created_by': staff_profile.id, 'last_updated_by': staff_profile.id})
            if serializers.is_valid():
                deduction_instance = serializers.save()
                return Response({"message": "Payment deduction item created successfully", }, status=200)
            #print(serializers.errors)
            return Response({"message": "Unable to create payment deduction item", }, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this action", }, status=401)
    except:
        return Response({"message": "Error creating payment deduction item", }, status=500)
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_work_shift(request):
    date_format = '%d/%m/%Y'
    company_serial_number = request.data["serial_number"]
    shift_name = request.data["shift_name"]
    shift_hours_start = request.data["shift_hours_start"]
    shift_hours_end = request.data["shift_hours_end"]
    shift_description = request.data["shift_description"]
    daysList = request.data.get('daysList', [])
    daysList = json.loads(daysList)
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=request.user)
        if staff_profile.company_department.department_name == "human_resource_management" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            serializers = WorkShiftSerializer(
                data={'company_profile': company_profile.id, 'shift_name': shift_name, 'shift_hours_start': convertTo24HRFormat(shift_hours_start), 'shift_hours_end': convertTo24HRFormat(shift_hours_end), 'shift_description': shift_description})
            if serializers.is_valid():
                work_shift = serializers.save()
                for dayInstance in daysList:
                    day_of_week_identifier = dayInstance["day_of_week_identifier"]
                    daySerializer = WorkingDaysSerializer(
                        data={'work_shift': work_shift.id, 'day_of_week_identifier': day_of_week_identifier})
                    if daySerializer.is_valid():
                        daySerializer.save()
                    # else:
                    #     print(daySerializer.errors)
                return Response({"message": "Work shift created successfully", }, status=200)
            #print(serializers.errors)
            return Response({"message": "Unable to create work shift", }, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this action", }, status=401)
    except:
        return Response({"message": "Error creating work shift", }, status=500)
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_staff_leave(request):
    date_format = '%d/%m/%Y'
    company_serial_number = request.data["serial_number"]
    staff_requesting_leave_id = request.data["staff_requesting_leave_id"]
    leave_type = request.data["leave_type"]
    leave_description = request.data["leave_description"]
    leave_start_date = datetime.strptime(
        request.data["leave_start_date"], date_format).strftime("%Y-%m-%d") if len(request.data["leave_start_date"]) > 0 else None 
    leave_end_date = datetime.strptime(
        request.data["leave_end_date"], date_format).strftime("%Y-%m-%d") if len(request.data["leave_end_date"]) > 0 else None 
    number_of_leave_days = request.data["number_of_leave_days"]
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=request.user)
        staff_requesting_leave = StaffProfile.objects.get(id=int(staff_requesting_leave_id))
        if staff_profile.company_department.department_name == "human_resource_management" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            serializers = StaffLeaveSerializer(
                data={'company_profile': company_profile.id, 'staff_profile': staff_requesting_leave.id, 'leave_type': leave_type, 'leave_description': leave_description, 'leave_start_date': leave_start_date, 'leave_end_date': leave_end_date, 'number_of_leave_days': number_of_leave_days, 'created_by': staff_profile.id, 'last_updated_by': staff_profile.id})
            if serializers.is_valid():
                serializers.save()
                return Response({"message": "Staff leave created successfully", }, status=200)
            #print(serializers.errors)
            return Response({"message": "Unable to create staff leave", }, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this action", }, status=401)
    except:
        return Response({"message": "Error creating staff leave", }, status=500)
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_educational_qualification(request):
    date_format = '%d/%m/%Y'
    company_serial_number = request.data["serial_number"]
    accredited_staff_id = request.data["accredited_staff_id"]
    qualification_title = request.data["qualification_title"]
    accredition_category = request.data["accredition_category"]
    accrediting_institution = request.data["accrediting_institution"]
    year_of_accredition = request.data["year_of_accredition"]
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=request.user)
        accredited_staff = StaffProfile.objects.get(
            id=int(accredited_staff_id))
        if staff_profile.company_department.department_name == "human_resource_management" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            serializers = Educational_QualificationSerializer(data={'company_profile': company_profile.id, 'staff': accredited_staff.id, 'qualification_title': qualification_title,
                                                              'accredition_category': accredition_category, 'accrediting_institution': accrediting_institution, 'year_of_accredition': year_of_accredition})
            if serializers.is_valid():
                education_qualification = serializers.save()
                education_qualification_map = {}
                education_qualification_map["education_qualification_id"] = str(
                    education_qualification.id)
                education_qualification_map["qualification_title"] = education_qualification.qualification_title
                education_qualification_map["accredition_category"] = education_qualification.accredition_category
                education_qualification_map["accrediting_institution"] = education_qualification.accrediting_institution
                education_qualification_map["year_of_accredition"] = education_qualification.year_of_accredition
                education_qualification_map["created_on"] = datetime.strftime(
                        education_qualification.created_on, date_format) if education_qualification.created_on is not None else "" 
                education_qualification_map["last_updated_on"] = datetime.strftime(
                    education_qualification.last_updated_on, date_format) if education_qualification.last_updated_on is not None else ""
                education_qualification_map["message"] = "Education qualification created successfully"
                return Response(education_qualification_map, status=200)
            # print(serializers.errors)
            return Response({"message": "Unable to create education qualification", }, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this action", }, status=401)
    except:
        return Response({"message": "Error creating education qualification", }, status=500)
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_training_record(request):
    date_format = '%d/%m/%Y'
    company_serial_number = request.data["serial_number"]
    trained_staff_id = request.data["trained_staff_id"]
    training_title = request.data["training_title"]
    training_description = request.data["training_description"]
    training_effective_from = datetime.strptime(
        request.data["training_effective_from"], date_format).strftime("%Y-%m-%d") if len(request.data["training_effective_from"]) > 0 else None
    training_effective_to = datetime.strptime(
        request.data["training_effective_to"], date_format).strftime("%Y-%m-%d") if len(request.data["training_effective_to"]) > 0 else None
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=request.user)
        trained_staff = StaffProfile.objects.get(
            id=int(trained_staff_id))
        if staff_profile.company_department.department_name == "human_resource_management" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            serializers = Training_RecordSerializer(
                data={'company_profile': company_profile.id, 'staff': trained_staff.id, 'training_title': training_title, 'training_description': training_description, 'training_effective_from': training_effective_from, 'training_effective_to': training_effective_to})
            if serializers.is_valid():
                staff_training_record = serializers.save()
                staff_training_record_map = {}
                staff_training_record_map["training_record_id"] = str(
                    staff_training_record.id)
                staff_training_record_map["training_title"] = staff_training_record.training_title
                staff_training_record_map["training_description"] = staff_training_record.training_description
                staff_training_record_map["training_effective_from"] = datetime.strftime(
                    staff_training_record.training_effective_from, date_format) if staff_training_record.training_effective_from is not None else ""
                staff_training_record_map["training_effective_to"] = datetime.strftime(
                    staff_training_record.training_effective_to, date_format) if staff_training_record.training_effective_to is not None else ""
                staff_training_record_map["created_on"] = datetime.strftime(
                    staff_training_record.created_on, date_format) if staff_training_record.created_on is not None else ""
                staff_training_record_map["last_updated_on"] = datetime.strftime(
                    staff_training_record.last_updated_on, date_format) if staff_training_record.last_updated_on is not None else ""
                staff_training_record_map["message"] = "Training record created successfully"
                return Response(staff_training_record_map, status=200)
            # print(serializers.errors)
            return Response({"message": "Unable to create training record", }, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this action", }, status=401)
    except:
        return Response({"message": "Error creating training record", }, status=500)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_disciplinary_record(request):
    date_format = '%d/%m/%Y'
    company_serial_number = request.data["serial_number"]
    disciplined_staff_id = request.data["disciplined_staff_id"]
    disciplinary_incidence_title = request.data["disciplinary_incidence_title"]
    disciplinary_incidence_description = request.data["disciplinary_incidence_description"]
    disciplinary_verdict = request.data["disciplinary_verdict"]
    disciplinary_verdict_description = request.data["disciplinary_verdict_description"]
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=request.user)
        disciplined_staff = StaffProfile.objects.get(
            id=int(disciplined_staff_id))
        if staff_profile.company_department.department_name == "human_resource_management" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            serializers = Disciplinary_RecordSerializer(
                data={'company_profile': company_profile.id, 'staff': disciplined_staff.id, 'disciplinary_incidence_title': disciplinary_incidence_title, 'disciplinary_incidence_description': disciplinary_incidence_description, 'disciplinary_verdict': disciplinary_verdict, 'disciplinary_verdict_description': disciplinary_verdict_description})
            if serializers.is_valid():
                staff_disciplinary_record = serializers.save()
                staff_disciplinary_record_map = {}
                staff_disciplinary_record_map["staff_disciplinary_record_id"] = str(
                    staff_disciplinary_record.id)
                staff_disciplinary_record_map[
                    "disciplinary_incidence_title"] = staff_disciplinary_record.disciplinary_incidence_title
                staff_disciplinary_record_map[
                    "disciplinary_incidence_description"] = staff_disciplinary_record.disciplinary_incidence_description
                staff_disciplinary_record_map[
                    "disciplinary_verdict"] = staff_disciplinary_record.disciplinary_verdict
                staff_disciplinary_record_map[
                    "disciplinary_verdict_description"] = staff_disciplinary_record.disciplinary_verdict_description
                staff_disciplinary_record_map[
                    "created_on"] = datetime.strftime(
                    staff_disciplinary_record.created_on, date_format) if staff_disciplinary_record.created_on is not None else ""
                staff_disciplinary_record_map[
                    "last_updated_on"] = datetime.strftime(
                    staff_disciplinary_record.last_updated_on, date_format) if staff_disciplinary_record.last_updated_on is not None else ""
                staff_disciplinary_record_map[
                    "message"] = "Disciplinary record created successfully"
                return Response(staff_disciplinary_record_map, status=200)
            print(serializers.errors)
            return Response({"message": "Unable to create disciplinary record", }, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this action", }, status=401)
    except:
        return Response({"message": "Error creating disciplinary record", }, status=500)
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_task(request):
    date_format = '%d/%m/%Y'
    company_serial_number = request.data["serial_number"]
    task_title = request.data["task_title"]
    task_description = request.data["task_description"]
    task_effective_from = datetime.strptime(
        request.data["task_effective_from"], date_format).strftime("%Y-%m-%d") if len(request.data["task_effective_from"]) > 0 else None 
    task_effective_to = datetime.strptime(
        request.data["task_effective_to"], date_format).strftime("%Y-%m-%d") if len(request.data["task_effective_to"]) > 0 else None  
    staffList = request.data.get('staffList', [])
    staffList = json.loads(staffList)
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=request.user)
        staffIdList = []
        for staffId in staffList:
            staffIdList.append(int(staffId["staff_id"]))
        if staff_profile.company_department.department_name == "human_resource_management" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            serializers = TaskSerializer(
                data={'company_profile': company_profile.id, 'task_title': task_title, 'task_description': task_description, 'task_effective_from': task_effective_from, 'task_effective_to': task_effective_to, 'staff': staffIdList})
            if serializers.is_valid():
                serializers.save()
                return Response({"message": "Task created successfully", }, status=200)
            # print(serializers.errors)
            return Response({"message": "Unable to create task", }, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this action", }, status=401)
    except:
        return Response({"message": "Error creating task", }, status=500)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_engagement(request):
    date_format = '%d/%m/%Y'
    company_serial_number = request.data["serial_number"]
    engagement_title = request.data["engagement_title"]
    engagement_description = request.data["engagement_description"]
    engagement_effective_from = datetime.strptime(
        request.data["engagement_effective_from"], date_format).strftime("%Y-%m-%d") if len(request.data["engagement_effective_from"]) > 0 else None   
    engagement_effective_to = datetime.strptime(
        request.data["engagement_effective_to"], date_format).strftime("%Y-%m-%d") if len(request.data["engagement_effective_to"]) > 0 else None 
    staffList = request.data.get('staffList', [])
    staffList = json.loads(staffList)
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=request.user)
        staffIdList = []
        for staffId in staffList:
            staffIdList.append(int(staffId["staff_id"]))
        if staff_profile.company_department.department_name == "human_resource_management" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            serializers = EngagementSerializer(
                data={'company_profile': company_profile.id, 'engagement_title': engagement_title, 'engagement_description': engagement_description, 'engagement_effective_from': engagement_effective_from, 'engagement_effective_to': engagement_effective_to, 'staff': staffIdList})
            if serializers.is_valid():
                serializers.save()
                return Response({"message": "Engagement created successfully", }, status=200)
            # print(serializers.errors)
            return Response({"message": "Unable to create engagement", }, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this action", }, status=401)
    except:
        return Response({"message": "Error creating engagement", }, status=500)
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_vacancy_record(request):
    date_format = '%d/%m/%Y'
    company_serial_number = request.data["serial_number"]
    vacant_position_id = request.data["vacant_position_id"]
    vacancy_title = request.data["vacancy_title"]
    vacancy_description = request.data["vacancy_description"]
    vacancy_count = request.data["vacancy_count"]
    vacancy_deadline = datetime.strptime(
        request.data["vacancy_deadline"], date_format).strftime("%Y-%m-%d") if len(request.data["vacancy_deadline"]) > 0 else None
    vacant_position_requirement_list = request.data.get(
        'vacant_position_requirement_list', [])
    vacant_position_requirement_list = json.loads(
        vacant_position_requirement_list)
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=request.user)
        vacant_position = VacancyRecord.objects.get(id=int(vacant_position_id))
        if staff_profile.company_department.department_name == "human_resource_management" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            serializers = VacancyRecordSerializer(
                data={'company_profile': company_profile.id, 'vacant_position': vacant_position.id, 'vacancy_title': vacancy_title, 'vacancy_description': vacancy_description, 'vacancy_count': vacancy_count, 'vacancy_deadline': vacancy_deadline})
            if serializers.is_valid():
                new_vacant_position = serializers.save()
                for vacant_position_requirement in vacant_position_requirement_list:
                    requirement_title = vacant_position_requirement["requirement_title"]
                    requirement_description = vacant_position_requirement["requirement_description"]
                    position_requirement_serializer = VacantPositionRequirementSerializer(
                        data={'vacancy_record': new_vacant_position.id, 'requirement_title': requirement_title, 'requirement_description': requirement_description})
                    if position_requirement_serializer.is_valid():
                        position_requirement_serializer.save()
                return Response({"message": "Vacancy record created successfully", }, status=200)
            # print(serializers.errors)
            return Response({"message": "Unable to create vacancy record", }, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this action", }, status=401)
    except:
        return Response({"message": "Error creating vacancy record", }, status=500)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_staff_financial_info(request):  
    date_format = '%d/%m/%Y'
    try:
        company_serial_number = request.data["serial_number"]
        staff_id_to_edit = request.data["staff_id_to_edit"]
        banking_institution_name = request.data["banking_institution_name"]
        bank_account_name = request.data["bank_account_name"]
        bank_account_number = request.data["bank_account_number"]
        nhif_number = request.data["nhif_number"]
        nhif_additional_info = request.data["nhif_additional_info"]
        nssf_number = request.data["nssf_number"]
        nssf_additional_info = request.data["nssf_additional_info"]
        basic_salary = request.data["basic_salary"]
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=request.user)
        staff_profile_to_edit = StaffProfile.objects.get(
            id=int(staff_id_to_edit))
        if staff_profile.company_department.department_name == "human_resource_management" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            serializers = StaffProfileSerializer(instance=staff_profile_to_edit, data={'banking_institution_name':banking_institution_name,
                                                 'bank_account_name': bank_account_name, 'bank_account_number': bank_account_number, 'nhif_number': nhif_number, 'nhif_additional_info': nhif_additional_info, 'nssf_number': nssf_number, 'nssf_additional_info': nssf_additional_info, 'basic_salary': basic_salary})
            if serializers.is_valid():
                serializers.save()
                return Response({"message": "Financial details updated successfully", }, status=200)
            # print(serializers.errors)
            return Response({"message": "Unable to update financial details", }, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this action", }, status=401)
    except:
        return Response({"message": "Error updating financial details", }, status=500)
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_educational_qualification(request):  
    date_format = '%d/%m/%Y'
    try:
        company_serial_number = request.data["serial_number"]
        educational_qualification_id_to_edit = request.data["educational_qualification_id_to_edit"]
        qualification_title = request.data["qualification_title"]
        accredition_category = request.data["accredition_category"]
        accrediting_institution = request.data["accrediting_institution"]
        year_of_accredition = request.data["year_of_accredition"]
        staff_profile = StaffProfile.objects.get(user=request.user)
        educational_qualification_to_edit = Educational_Qualification.objects.get(
            id=int(educational_qualification_id_to_edit))
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        if staff_profile.company_department.department_name == "human_resource_management" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            serializers = Educational_QualificationSerializer(instance=educational_qualification_to_edit,data={'qualification_title': qualification_title,
                                                              'accredition_category': accredition_category, 'accrediting_institution': accrediting_institution, 'year_of_accredition': year_of_accredition})
            if serializers.is_valid():
                serializers.save()
                return Response({"message": "Academic record updated successfully", }, status=200)
            # print(serializers.errors)
            return Response({"message": "Unable to update academic record", }, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this action", }, status=401)
    except:
        return Response({"message": "Error updating academic record", }, status=500)
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_training_record(request):  
    date_format = '%d/%m/%Y'
    try:
        company_serial_number = request.data["serial_number"]
        training_record_id_to_edit = request.data["staff_id_to_edit"]
        training_title = request.data["training_title"]
        training_description = request.data["training_description"]
        training_effective_from = datetime.strptime(
        request.data["training_effective_from"], date_format).strftime("%Y-%m-%d") if len(request.data["training_effective_from"]) > 0 else None 
        training_effective_to = datetime.strptime(
        request.data["training_effective_to"], date_format).strftime("%Y-%m-%d") if len(request.data["training_effective_to"]) > 0 else None 
        staff_profile = StaffProfile.objects.get(user=request.user)
        training_record_to_edit = Training_Record.objects.get(
            id=int(training_record_id_to_edit))
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        if staff_profile.company_department.department_name == "human_resource_management" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            serializers = Training_RecordSerializer(instance=training_record_to_edit,data={'training_title':training_title,'training_description':training_description,'training_effective_from':training_effective_from,'training_effective_to':training_effective_to})
            if serializers.is_valid():
                serializers.save()
                return Response({"message": "Training record updated successfully", }, status=200)
            # print(serializers.errors)
            return Response({"message": "Unable to update training record", }, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this action", }, status=401)
    except:
        return Response({"message": "Error updating training record", }, status=500)
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_payroll_sheet(request):
    company_serial_number = request.data["serial_number"]
    company_branch_id = request.data["company_branch_id"]
    payroll_sheet_title = request.data["payroll_sheet_title"]
    payroll_sheet_description = request.data["payroll_sheet_description"]
    payroll_sheet_for_the_month_of = request.data["payroll_sheet_for_the_month_of"]
    payroll_sheet_for_the_year = request.data["payroll_sheet_for_the_year"]
    #calculate sheet value
    #grab payroll instances data
    payrollSheetInstancesList = request.data.get(
        'payrollSheetInstancesList', [])
    payrollSheetInstancesList = json.loads(payrollSheetInstancesList)
    #print(payrollSheetInstancesList)
    try:
        #create the payroll sheet
        payroll_sheet_value = 0.00
        payroll_sheet_total_net_pay_value = 0.00
        payroll_sheet_total_bonus_value = 0.00
        payroll_sheet_total_deduction_value = 0.00
        payroll_sheet_total_commission_value = 0.00
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        company_branch = CompanyBranch.objects.get(id=int(company_branch_id))
        staff_profile = StaffProfile.objects.get(user=request.user)
        if staff_profile.company_department.department_name == "human_resource_management" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            payroll_sheet_serializer = PayrollSheetSerializer(
                data={'company_profile': company_profile.id, 'company_branch': company_branch.id, 'payroll_sheet_title': payroll_sheet_title, 'payroll_sheet_description': payroll_sheet_description, 'payroll_sheet_for_the_month_of': payroll_sheet_for_the_month_of, 'payroll_sheet_for_the_year': payroll_sheet_for_the_year,'created_by':staff_profile.id,'last_updated_by':staff_profile.id})
            if payroll_sheet_serializer.is_valid():
                new_payroll_sheet = payroll_sheet_serializer.save()
                for payrollSheetInstance in payrollSheetInstancesList:
                    bonus_instance_list = payrollSheetInstance["bonus_instance_list"]
                    payroll_sheet_bonus_instances_ids_list = []
                    for bonus in bonus_instance_list:
                        bonus_id = bonus["bonus_id"]
                        bonus_instance_value = bonus["bonus_instance_value"]
                        bonus_instance_serializer = BonusInstanceSerializer(data={'bonus': int(
                            bonus_id), 'bonus_instance_value': bonus_instance_value, 'created_by': staff_profile.id, 'last_updated_by': staff_profile.id})
                        if bonus_instance_serializer.is_valid():
                            new_bonus_instance = bonus_instance_serializer.save()
                            payroll_sheet_bonus_instances_ids_list.append(new_bonus_instance.id)
                            payroll_sheet_total_bonus_value += float(
                                bonus_instance_value.replace(',', ''))
                            #create bonus scheme if it does not exist
                            validBonusInstance = Bonus.objects.get(id=int(bonus_id))
                            staff_bonus_scheme, created = StaffBonusScheme.objects.get_or_create(
                                staff_profile=staff_profile, bonus=validBonusInstance)
                    #all bonus instances for this payroll sheet are created
                    deduction_instance_list = payrollSheetInstance["deduction_instance_list"]
                    #print(f'Deduction instance list: {deduction_instance_list}')
                    payroll_sheet_deduction_instances_ids_list = []
                    for deduction in deduction_instance_list:
                        deduction_id = deduction["deduction_id"]
                        deduction_instance_value = deduction["deduction_value"]
                        deduction_instance_serializer = DeductionInstanceSerializer(
                            data={'deduction': int(deduction_id), 'deduction_instance_value': deduction_instance_value, 'created_by': staff_profile.id, 'last_updated_by': staff_profile.id})
                        if deduction_instance_serializer.is_valid():
                            new_deduction_instance = deduction_instance_serializer.save()
                            payroll_sheet_deduction_instances_ids_list.append(new_deduction_instance.id)
                            payroll_sheet_total_deduction_value += float(
                                deduction_instance_value.replace(',', ''))
                            #create deduction scheme if it does not exist
                            validDeductionInstance = Deduction.objects.get(id=int(deduction_id))
                            staff_deduction_scheme, created = StaffDeductionScheme.objects.get_or_create(
                                staff_profile=staff_profile, deduction=validDeductionInstance)
                        else:
                            pass
                            #print(deduction_instance_serializer.errors)
                    # all deduction instances for this payroll sheet are created
                    #creating the payroll instance
                    staff_on_payroll = StaffProfile.objects.get(id=int(payrollSheetInstance["staff_id"]))
                    gross_salary = payrollSheetInstance["gross_salary"]
                    commissions_total = payrollSheetInstance["commissions_total"]
                    payroll_sheet_total_commission_value += float(commissions_total.replace(',', ''))
                    payroll_sheet_value += float(gross_salary.replace(',', ''))
                    net_salary = payrollSheetInstance["net_salary"]
                    payroll_sheet_total_net_pay_value += float(
                        net_salary.replace(',', ''))
                    created_payroll_sheet_instance_serializer = StaffPayrollInstanceSerializer(data={'staff_profile':staff_on_payroll.id,'payroll_sheet':new_payroll_sheet.id,'deduction_instance':payroll_sheet_deduction_instances_ids_list,'gross_salary':gross_salary,'bonus_instance':payroll_sheet_bonus_instances_ids_list,'commissions_total':commissions_total,'net_salary':net_salary,'created_by': staff_profile.id, 'last_updated_by': staff_profile.id})
                    if created_payroll_sheet_instance_serializer.is_valid():
                        created_payroll_sheet_instance_serializer.save()
                new_payroll_sheet.payroll_sheet_value = f'{payroll_sheet_value}'
                new_payroll_sheet.payroll_sheet_total_net_pay_value = f'{payroll_sheet_total_net_pay_value}' 
                new_payroll_sheet.payroll_sheet_total_bonus_value = f'{payroll_sheet_total_bonus_value}' 
                new_payroll_sheet.payroll_sheet_total_deduction_value = f'{payroll_sheet_total_deduction_value}' 
                new_payroll_sheet.payroll_sheet_total_commission_value = f'{payroll_sheet_total_commission_value}'
                new_payroll_sheet.save()
                #successful creation
                return Response({"message": "Payroll sheet created successfully", }, status=200)
            else:
                #print(payroll_sheet_serializer.errors)
                return Response({"message": "Unable to create payroll sheet", }, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this action", }, status=401)
    except:# Exception as e:
        #print(e)
        return Response({"message": "Error creating payroll sheet", }, status=500)

