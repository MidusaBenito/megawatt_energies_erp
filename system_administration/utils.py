#from django.shortcuts import render
#from django.http import HttpResponse
from datetime import datetime
from django.core.mail import send_mail
import random
import string

from human_resource.models import StaffProfile


def send_email_signup(request, message, recipient_list):
    subject = 'Successfully registered'
    # message = 'Body of the email.'
    from_email = 'scarlettbenz101@gmail.com'
    # recipient_list = ['recipient@example.com']

    send_mail(subject, message, from_email, recipient_list)

def get_staff_profile_data(userActive):
    staff_profile_data = {}
    date_format = '%d/%m/%Y, %H:%M'
    staff_profile_data["email_address"] = userActive.username
    if userActive.user_staff_profile is not None and userActive.user_staff_profile.recycle_bin == False:
        staff_profile_data["staff_id"] = str(userActive.user_staff_profile.id)
        staff_profile_data["staff_position"] = userActive.user_staff_profile.staff_position.position_title if userActive.user_staff_profile.staff_position is not None else ""
        staff_profile_data["staff_number"] = userActive.user_staff_profile.staff_number 
        staff_profile_data["first_name"] = userActive.user_staff_profile.first_name
        staff_profile_data["last_name"] = userActive.user_staff_profile.last_name
        staff_profile_data["date_of_birth"] = userActive.user_staff_profile.date_of_birth if userActive.user_staff_profile.date_of_birth is not None else ''
        staff_profile_data["country_name"] = userActive.user_staff_profile.country_name
        staff_profile_data["identification_number"] = userActive.user_staff_profile.identification_number
        staff_profile_data["phone_number"] = userActive.user_staff_profile.phone_number
        staff_profile_data["staff_title"] = userActive.user_staff_profile.staff_title
        staff_profile_data["employment_start_date"] = userActive.user_staff_profile.employment_start_date if userActive.user_staff_profile.employment_start_date is not None else ''
        staff_profile_data["employment_end_date"] = userActive.user_staff_profile.employment_end_date if userActive.user_staff_profile.employment_end_date is not None else ''
        staff_profile_data["emergency_contact_phone"] = userActive.user_staff_profile.emergency_contact_phone
        staff_profile_data["company_branch_name"] = userActive.user_staff_profile.company_branch.branch_name if userActive.user_staff_profile.company_branch is not None else ""
        staff_profile_data["company_department"] = userActive.user_staff_profile.company_department.department_name if userActive.user_staff_profile.company_department is not None else ""
        staff_profile_data["is_profile_set"] = "true" if userActive.user_staff_profile.is_profile_set else "false"
        staff_profile_data["is_head_of_department"] = "true" if userActive.user_staff_profile.is_head_of_department else "false"
        staff_profile_data["has_read_write_priviledges"] = "true" if userActive.user_staff_profile.has_read_write_priviledges else "false"
        staff_profile_data["is_super_admin"] = "true" if userActive.user_staff_profile.is_super_admin else "false"
        staff_profile_data["is_on_leave"] = "true" if userActive.user_staff_profile.is_on_leave else "false"
        #added info
        staff_profile_data["kra_pin"] = userActive.user_staff_profile.kra_pin
        staff_profile_data["type_of_employment"] = userActive.user_staff_profile.type_of_employment
        staff_profile_data["banking_institution_name"] = userActive.user_staff_profile.banking_institution_name
        staff_profile_data["bank_account_name"] = userActive.user_staff_profile.bank_account_name
        staff_profile_data["bank_account_number"] = userActive.user_staff_profile.bank_account_number
        #added banking institution
        staff_profile_data["bank_branch_name"] = userActive.user_staff_profile.bank_branch_name
        staff_profile_data["bank_branch_code"] = userActive.user_staff_profile.bank_branch_code
        staff_profile_data["bank_swift_code"] = userActive.user_staff_profile.bank_swift_code
        #end
        staff_profile_data["nhif_number"] = userActive.user_staff_profile.nhif_number
        staff_profile_data["nhif_additional_info"] = userActive.user_staff_profile.nhif_additional_info
        staff_profile_data["nssf_number"] = userActive.user_staff_profile.nssf_number
        staff_profile_data["nssf_additional_info"] = userActive.user_staff_profile.nssf_additional_info
        staff_profile_data["staff_additional_info"] = userActive.user_staff_profile.staff_additional_info
        staff_profile_data["basic_salary"] = userActive.user_staff_profile.basic_salary
        #end
        staff_profile_data["created_on"] = datetime.strftime(
            userActive.user_staff_profile.created_on, date_format)
        staff_profile_data["last_updated_on"] = datetime.strftime(
            userActive.user_staff_profile.last_updated_on, date_format)
        #
        staff_profile_data["time_sheets_list"] = []
        staff_profile_data["education_qualifications_list"] = []
        staff_profile_data["staff_training_records_list"] = []
        staff_profile_data["staff_disciplinary_records_list"] = []
        staff_profile_data["staff_leaves_list"] = []
        staff_profile_data["staff_bonus_schemes_list"] = []
        staff_profile_data["staff_deduction_schemes_list"] = []
        #added
        staff_profile_data["personal_email"] = userActive.user_staff_profile.personal_email
    else:
        staff_profile_data["email_address"] = ""
        staff_profile_data["staff_id"] = ""
        staff_profile_data["staff_position"] = ""
        staff_profile_data["staff_number"] = ""
        staff_profile_data["first_name"] = ""
        staff_profile_data["last_name"] = ""
        staff_profile_data["date_of_birth"] = ""
        staff_profile_data["country_name"] = ""
        staff_profile_data["identification_number"] = ""
        staff_profile_data["phone_number"] = ""
        staff_profile_data["staff_title"] = ""
        staff_profile_data["employment_start_date"] = ""
        staff_profile_data["employment_end_date"] = ""
        staff_profile_data["emergency_contact_phone"] = ""
        staff_profile_data["is_profile_set"] = ""
        staff_profile_data["is_head_of_department"] = ""
        staff_profile_data["has_read_write_priviledges"] = ""
        staff_profile_data["is_super_admin"] = ""
        staff_profile_data["is_on_leave"] = ""
        staff_profile_data["company_branch_name"] = ""
        staff_profile_data["company_department"] = ""
        staff_profile_data["created_on"] = ""
        staff_profile_data["last_updated_on"] = ""
        staff_profile_data["kra_pin"] = ""
        staff_profile_data["type_of_employment"] = ""
        staff_profile_data["userActive.user_staff_profile"] = ""
        staff_profile_data["bank_account_name"] = ""
        staff_profile_data["bank_account_number"] = ""
        staff_profile_data["bank_branch_name"] = ""
        staff_profile_data["bank_branch_code"] = ""
        staff_profile_data["bank_swift_code"] = ""
        staff_profile_data["nhif_number"] = ""
        staff_profile_data["nhif_additional_info"] = ""
        staff_profile_data["nssf_number"] = ""
        staff_profile_data["nssf_additional_info"] = ""
        staff_profile_data["staff_additional_info"] = ""
        staff_profile_data["basic_salary"] = ""
        staff_profile_data["time_sheets_list"] = []
        staff_profile_data["education_qualifications_list"] = []
        staff_profile_data["staff_training_records_list"] = []
        staff_profile_data["staff_disciplinary_records_list"] = []
        staff_profile_data["staff_leaves_list"] = []
        staff_profile_data["staff_bonus_schemes_list"] = []
        staff_profile_data["staff_deduction_schemes_list"] = []
        staff_profile_data["personal_email"] = ""
    return staff_profile_data


def generate_random_string(length):
    alphanumeric_chars = string.ascii_letters + string.digits
    return ''.join(random.choice(alphanumeric_chars) for _ in range(length))

def checkIfStaffCanEdit(staffProfile,editedStaffDepId):
    staffCanEdit = False
    if (staffProfile.is_head_of_department == True or staffProfile.has_read_write_priviledges == True) and str(staffProfile.company_department.id) == editedStaffDepId:
        staffCanEdit = True 
    return staffCanEdit

def convertTo24HRFormat(time_string):
    time_object_12hr = datetime.strptime(time_string, '%I:%M %p').time()
    hour_24hr = time_object_12hr.hour if time_object_12hr.hour != 12 else 0
    minute = time_object_12hr.minute
    time_object_24hr = datetime.strptime(
        f'{hour_24hr:02d}:{minute:02d}', '%H:%M').time()
    return time_object_24hr

#to be added
def generateNextStaffNumber(company_id):
    all_staff = StaffProfile.objects.all()
    largest_id = 0
    staff_to_use = None
    newNumber = 'MEL000'
    superHrNumber = ''
    for staff in all_staff:
        if staff.company_branch.company_profile.id == company_id:
            if staff.id > largest_id and staff.is_super_admin != True:
                largest_id = staff.id
                staff_to_use = staff
        if staff.is_super_admin:
            superHrNumber = staff.staff_number
            superHrNumber = superHrNumber[3:]
    if staff_to_use is not None:
        staff_number = staff_to_use.staff_number
        stripped_string = staff_number[3:]
        #print(stripped_string)
        newSuffix = int(stripped_string) + 1
        if int(superHrNumber) == newSuffix:
            newSuffix += 1
        if newSuffix <10:
            newNumber = f'MEL00{newSuffix}'
        elif newSuffix < 100:
            newNumber = f'MEL0{newSuffix}'
        else:
            newNumber = f'MEL{newSuffix}'
    return newNumber





    