#from django.shortcuts import render

import base64

from human_resource.models import Deduction, StaffProfile, staffPosition
from human_resource.serializers import DeductionSerializer, StaffDeductionSchemeSerializer
from system_administration.utils import generate_random_string, get_staff_profile_data, send_email_signup
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


@api_view(['POST'])  
def get_admin_creation_status(request):
    serialNumber = request.data["serial_number"]
    # system_admin_already_exist = SystemAdminCreationStatus.objects.exists()
    payload = {}
    payload["company_serial_number"] = ""
    payload["company_name"] = ""
    payload["company_description"] = ""
    payload["company_postal_address"] = ""
    payload["company_country_location"] = ""
    payload["company_phone"] = ""
    payload["company_preferred_currency"] = ""
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=serialNumber)
        try:
            system_admin = SystemAdminCreationStatus.objects.get(
                company_profile=company_profile)
            if system_admin.systemAdminCreated == True:
                payload["company_serial_number"] = company_profile.company_serial_number
                payload["company_name"] = company_profile.company_name
                payload["company_description"] = company_profile.company_description
                payload["company_postal_address"] = company_profile.company_postal_address
                payload["company_country_location"] = company_profile.company_country_location
                payload["company_phone"] = company_profile.company_phone
                payload["company_preferred_currency"] = company_profile.company_preferred_currency
                return Response({"message": "true", "payload": payload,}, status=200)
            else:
                return Response({"message": "false", "payload": payload, }, status=200)
        except:# Exception as e:
            #print (e)
            # print (payload)
            return Response({"message": "false", "payload": payload, }, status=401)
    except:
        return Response({"message": "false", "payload": payload, }, status=406)


@api_view(['POST']) 
def validate_serial_number(request):
    serialNumber = request.data["serial_number"]
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=serialNumber)
        if company_profile.company_serial_number == serialNumber:
            return Response({"message": "true"}, status=200)
    except:
        return Response({"message": "false"}, status=200)
    
@api_view(['POST'])
def create_system_admin(request):
    email = request.data['username']
    password = request.data['password']
    company_serial_number = request.data["serial_number"]
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        criteria = {"company_profile": company_profile}
        system_admin_already_exist = SystemAdminCreationStatus.objects.filter(
            **criteria).exists()
        if system_admin_already_exist==False:
            serializers = UserSerializer(data={'username':email,'password':password})
            if serializers.is_valid():
                user = serializers.save()
                user.is_staff = True
                user.save()
                new_user = authenticate(username=email, password=password)
                #create main company branch
                main_branch, created = CompanyBranch.objects.get_or_create(company_profile=company_profile,main_branch=True)
                #create staff position
                staff_position, created = staffPosition.objects.get_or_create(company_profile=company_profile,
                    position_title="System Administrator")
                #create department
                department, created = CompanyDepartment.objects.get_or_create(company_profile=company_profile,
                    department_name="system_and_administration", department_description="Tasked with overseeing the ERP system's health, security, and performance, this department ensures that the organization's technology backbone operates seamlessly to meet business needs.")
                #create staff profile
                staff, created = StaffProfile.objects.get_or_create(
                    user=new_user, staff_position=staff_position, email_address=new_user.username, company_branch=main_branch, company_department=department,has_read_write_priviledges=True,is_head_of_department=True)  # creates the system administrator role
                #create default deduction schemes
                # create default deduction schemes
                # paye
                current_year = datetime.now().year
                date_effective_from = datetime(current_year, 1, 1)
                date_effective_to = datetime(current_year+2, 1, 1)
                paye_deduction_serializer = DeductionSerializer(data={'company_profile': company_profile.id, 'deduction_title': "PAYE", 'deduction_description': "Pay As You Earn tax (Income Tax)", 'deduction_type': "tax",
                                                                      'deduction_value': "0.0", 'deduction_module': 'other', 'date_effective_from': date_effective_from.date(), 'date_effective_to': date_effective_to.date(), 'created_by': staff.id, 'last_updated_by': staff.id})
                if paye_deduction_serializer.is_valid():
                    paye_deduction_instance = paye_deduction_serializer.save()
                else:
                    pass
                    # print(paye_deduction_serializer.errors)
                # shif
                # current_year = datetime.now().year
                date_effective_from = datetime(current_year, 7, 1)
                date_effective_to = datetime(current_year+2, 1, 1)
                shif_deduction_serializer = DeductionSerializer(data={'company_profile': company_profile.id, 'deduction_title': "SHIF", 'deduction_description': "Social Health Insurance Fund", 'deduction_type': "insurance",
                                                                      'deduction_value': "2.75", 'deduction_module': "percentage", 'date_effective_from': date_effective_from.date(), 'date_effective_to': date_effective_to.date(), 'created_by': staff.id, 'last_updated_by': staff.id})
                if shif_deduction_serializer.is_valid():
                    shif_deduction_instance = shif_deduction_serializer.save()
                else:
                    pass
                    # print(shif_deduction_serializer.errors)
                # pension
                # current_year = datetime.now().year
                date_effective_from = datetime(current_year, 1, 1)
                date_effective_to = datetime(current_year+2, 1, 1)
                nssf_deduction_serializer = DeductionSerializer(data={'company_profile': company_profile.id, 'deduction_title': "NSSF", 'deduction_description': "Pension Contribution", 'deduction_type': "pension",
                                                                      'deduction_value': "2,160", 'deduction_module': 'other', 'date_effective_from': date_effective_from.date(), 'date_effective_to': date_effective_to.date(), 'created_by': staff.id, 'last_updated_by': staff.id})
                if nssf_deduction_serializer.is_valid():
                    nssf_deduction_instance = nssf_deduction_serializer.save()
                else:
                    pass
                    # print(nssf_deduction_serializer.errors)
                #nhif
                date_effective_from = datetime(current_year, 1, 1)
                date_effective_to = datetime(current_year, 7, 1)
                nhif_deduction_serializer = DeductionSerializer(data={'company_profile': company_profile.id, 'deduction_title': "NHIF", 'deduction_description': "National Health Insurance Fund", 'deduction_type': "insurance",
                                                                      'deduction_value': "0.0", 'deduction_module': 'other', 'date_effective_from': date_effective_from.date(), 'date_effective_to': date_effective_to.date(), 'created_by': staff.id, 'last_updated_by': staff.id})
                if nhif_deduction_serializer.is_valid():
                    nhif_deduction_instance = nhif_deduction_serializer.save()
                else:
                    pass
                # print(nhif_deduction_serializer.errors)
                # create default deduction schemes for the super hr
                # paye
                paye_deduction_scheme_serializer = StaffDeductionSchemeSerializer(data={
                                                                                  'staff_profile': staff.id, 'deduction': paye_deduction_instance.id})
                if paye_deduction_scheme_serializer.is_valid():
                    paye_deduction_scheme_serializer.save()
                else:
                    pass
                    # print(paye_deduction_scheme_serializer.errors)
                # shif
                shif_deduction_scheme_serializer = StaffDeductionSchemeSerializer(data={
                                                                                  'staff_profile': staff.id, 'deduction': shif_deduction_instance.id})
                if shif_deduction_scheme_serializer.is_valid():
                    shif_deduction_scheme_serializer.save()
                else:
                    pass
                    # print(shif_deduction_scheme_serializer.errors)
                # nssf
                nssf_deduction_scheme_serializer = StaffDeductionSchemeSerializer(data={
                                                                                  'staff_profile': staff.id, 'deduction': nssf_deduction_instance.id})
                if nssf_deduction_scheme_serializer.is_valid():
                    nssf_deduction_scheme_serializer.save()
                else:
                    pass
                    # print(nssf_deduction_scheme_serializer.errors)
                # nhif
                nhif_deduction_scheme_serializer = StaffDeductionSchemeSerializer(data={
                                                                                  'staff_profile': staff.id, 'deduction': nhif_deduction_instance.id})
                if nhif_deduction_scheme_serializer.is_valid():
                    nhif_deduction_scheme_serializer.save()
                else:
                    pass
                    # print(nssf_deduction_scheme_serializer.errors)
                #end
                SystemAdminCreationStatus.objects.create(user=new_user,systemAdminCreated=True,company_profile=company_profile)
                #add send email to super admin with their staff number
                message = f"You have successfully registered on Megawatt Energies ERP. Your staff number is {staff.staff_number}"
                recipient_list = [f'{email}']
                try:
                    send_email_signup(request, message, recipient_list)
                except:
                    pass
                return Response({"message": "System Administrator created successfully",}, status=200)
            else:
                #print(serializers.errors)
                return Response({"message": "Unable to create system administrator account", }, status=406)
        else:
            #system admin already exists
            return Response({"message": "System Admin already exists!", }, status=401)
        
    except:# Exception as e:
        #print(e)
        return Response({"message": "Error creating system administrator account!", }, status=500)
    
@api_view(['POST'])
def staff_login(request):
    staff_number = request.data['staff_number']
    password = request.data['password']
    payload = {}
    payload["user_token"] = ""
    payload["company_department"] = ""
    payload["full_name"] = ""
    payload["user_role"] = ""
    try:
        staff_profile = StaffProfile.objects.get(staff_number=staff_number)
        username = staff_profile.user.username
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token = token, created = Token.objects.get_or_create(user=user)
            payload["user_token"] = token.key
            payload["company_department"] = staff_profile.company_department.department_name if staff_profile.company_department is not None else "not_assigned"
            full_name = f'{staff_profile.first_name} {staff_profile.last_name}' if len(staff_profile.first_name) > 0 and len(staff_profile.last_name) > 0 else "No Name"
            user_role = f'{staff_profile.staff_position.position_title}' if staff_profile.staff_position is not None else "Not Assigned"
            payload["full_name"] = full_name
            payload["user_role"] = user_role
            return Response({"message": "Login successful","payload":payload }, status=200)
        else:
            return Response({"message": "Invalid credentials", "payload": payload}, status=406)
    except:
        return Response({"message": "Invalid credentials", "payload": payload}, status=500)
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def system_admin_dashboard(request):
    date_format = '%d/%m/%Y, %H:%M'
    company_serial_number = request.data["serial_number"]
    active_user = request.user
    payload = {}
    company_profile_map = {}
    company_departments_list = []
    company_branches_list = []
    company_suppliers_list = []
    company_customers_list = []
    
    #
    # company_profile["company_name"] = ""
    # company_profile["company_description"] = ""
    # company_profile["company_postal_address"] = ""
    # company_profile["company_country_location"] = ""
    # company_profile["company_phone"] = ""
    # company_profile["company_preferred_currency"] = ""
    # company_profile["company_profile_set"] = ""
    # company_profile["created_on"] = ""
    # company_profile["last_updated_on"] = ""
    try:
        company_profile = CompanyProfile.objects.get(company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=request.user)
        if staff_profile.staff_position.position_title == "System Administrator" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            active_staff_profile_data = get_staff_profile_data(active_user)
            #print(active_staff_profile_data)
            company_profile_map["company_name"] = company_profile.company_name
            company_profile_map["company_description"] = company_profile.company_description
            company_profile_map["company_postal_address"] = company_profile.company_postal_address
            company_profile_map["company_country_location"] = company_profile.company_country_location
            company_profile_map["company_phone"] = company_profile.company_phone
            company_profile_map["company_preferred_currency"] = company_profile.company_preferred_currency
            company_profile_map["company_profile_set"] = "true" if company_profile.company_profile_set == True else "false"
            company_profile_map["company_super_hr_created"] = "true" if company_profile.company_super_hr_created == True else "false"
            company_profile_map["created_on"] = datetime.strftime(
                company_profile.created_on, date_format)
            company_profile_map["last_updated_on"] = datetime.strftime(
                company_profile.last_updated_on, date_format)
            #company_departments
            company_departments = company_profile.company_departments.all()
            #print(company_departments)
            for department in company_departments:
                if department.recycle_bin == False:
                    department_map = {}
                    department_map["department_id"] = str(department.id)
                    department_map["department_name"] = department.department_name
                    department_map["department_description"] = department.department_name
                    department_map["created_on"] = datetime.strftime(
                        department.created_on, date_format)
                    department_map["last_updated_on"] = datetime.strftime(
                        department.last_updated_on, date_format)
                    company_departments_list.append(department_map)
            company_branches = company_profile.company_branches.all()
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
                    company_branches_list.append(branch_map)
                    #users
                    company_branch_staffs_list = []
                    branch_staffs = branch.company_branch_staffs.all()
                    for staff in branch_staffs:
                        if staff.recycle_bin == False:
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
                            staff_map["created_on"] = datetime.strftime(
                                staff.created_on, date_format)
                            staff_map["last_updated_on"] = datetime.strftime(
                                staff.last_updated_on, date_format)
                            #added info
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
                            staff_map["time_sheets_list"] = []
                            staff_map["education_qualifications_list"] = []
                            staff_map["staff_training_records_list"] = []
                            staff_map["staff_disciplinary_records_list"] = []
                            staff_map["staff_leaves_list"] = []
                            staff_map["staff_bonus_schemes_list"] = []
                            staff_map["staff_deduction_schemes_list"] = []
                            #end
                            company_branch_staffs_list.append(staff_map)
                    branch_map["branch_staff_profiles"] = company_branch_staffs_list
            company_suppliers = company_profile.company_suppliers.all()
            for supplier in company_suppliers:
                supplier_map = {}
                supplier_map["supplier_id"] = str(supplier.id)
                supplier_map["supplier_name"] = supplier.supplier_name
                supplier_map["supplier_phone"] = supplier.supplier_phone
                supplier_map["supplier_email"] = supplier.supplier_email
                supplier_map["supplier_address"] = supplier.supplier_address
                supplier_map["supplier_description"] = supplier.supplier_description
                supplier_map["created_by"] = f'{supplier.created_by.first_name} {supplier.created_by.last_name}'
                supplier_map["last_updated_by"] = f'{supplier.last_updated_by.first_name} {supplier.last_updated_by.last_name}'
                supplier_map["created_on"] = datetime.strftime(
                    supplier.created_on, date_format)
                supplier_map["last_updated_on"] = datetime.strftime(
                    supplier.last_updated_on, date_format)
                company_suppliers_list.append(supplier_map)
            company_customers = company_profile.company_customers.all()
            for customer in company_customers:
                if customer.recycle_bin == False:
                    customer_map = {}
                    customer_map["customer_id"] = str(customer.id)
                    customer_map["customer_name"] = f'{customer.first_name} {customer.last_name}'
                    customer_map["email_address"] = customer.email_address
                    customer_map["phone_number"] = customer.phone_number
                    customer_map["customer_title"] = customer.customer_title
                    customer_map["is_profile_set"] = "true" if customer.is_profile_set == True else "false"
                    customer_map["created_on"] = datetime.strftime(
                        customer.created_on, date_format)
                    customer_map["last_updated_on"] = datetime.strftime(
                        customer.last_updated_on, date_format)
            payload["company_profile"] = company_profile_map
            payload["active_staff_profile_data"] = active_staff_profile_data
            payload["company_departments_list"] = company_departments_list
            payload["company_branches_list"] = company_branches_list
            payload["company_suppliers_list"] = company_suppliers_list
            payload["company_customers_list"] = company_customers_list
            #print(payload)
            return Response({"message": "true", "payload": payload}, status=200)
        else:
            return Response({"message": "false", "payload": payload}, status=401)
    except:# Exception as e:
        # payload["company_profile"] = company_profile
        # payload["active_staff_profile_data"] = active_staff_profile_data
        # payload["company_departments_list"] = company_departments_list
        # payload["company_branches_list "] = company_branches_list
        # payload["company_suppliers_list"] = company_suppliers_list
        # payload["company_customers_list"] = company_customers_list
       # print(e)
        return Response({"message": "false", "payload": payload}, status=500)
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_company_profile(request):
    company_serial_number = request.data["serial_number"]
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=request.user)
        if staff_profile.staff_position.position_title == "System Administrator" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            company_name = request.data['company_name']
            company_description = request.data['company_description']
            company_postal_address = request.data['company_postal_address']
            company_country_location = request.data['company_country_location']
            company_phone = request.data['company_phone']
            company_preferred_currency = request.data['company_preferred_currency']
            serializer = CompanyProfileSerializer(instance=company_profile,
                data={'company_name': company_name, 'company_description': company_description, 'company_postal_address': company_postal_address, 'company_country_location': company_country_location, 'company_phone': company_phone, 'company_preferred_currency': company_preferred_currency})
            if serializer.is_valid():
                company_profile = serializer.save()
                company_profile.company_profile_set = True
                company_profile.save()
                return Response({"message": "Company profile set up successful"}, status=200)
            else:
                return Response({"message": "Error setting up company profile"}, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this function"}, status=401)
    except:# Exception as e:
        #print(e)
        return Response({"message": "Unable to set up company profile"}, status=500)
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_company_branch(request):
    company_serial_number = request.data["serial_number"]
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=request.user)
        if staff_profile.staff_position.position_title == "System Administrator" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            branch_id = request.data['branch_id']
            branchInstance = CompanyBranch.objects.get(id=int(branch_id),company_profile=company_profile)
            branch_name = request.data['branch_name']
            branch_description = request.data['branch_description']
            branch_county_location = request.data['branch_county_location']
            branch_phone = request.data['branch_phone']
            serializer = CompanyBranchSerializer(instance=branchInstance,
                                                  data={'branch_name': branch_name, 'branch_description': branch_description, 'branch_county_location': branch_county_location, 'branch_phone': branch_phone,})
            if serializer.is_valid():
                company_branch = serializer.save()
                #automatically create the remaining departments
                departments_list = [{"department_name": "procurement", "department_description":
                                     "Responsible for receiving and reviewing purchase requisitions from various departments within the organization, especialy the warehouse management department. The department creates purchase orders from the purchase requisitions it receives."},
                                    {"department_name": "human_resource_management", "department_description": "Responsible for overseeing personnel-related functions, including recruitment, employee onboarding and performance management"},
                                    {"department_name": "warehouse_management", "department_description": "This department is tasked with efficiently overseeing and optimizing the movement and storage of goods within the organization's warehouses. It utilizes the ERP system to manage inventory levels, track shipments, and enhance overall supply chain visibility."}, {"department_name": "sales_and_marketing", "department_description": "The sales and marketing department focuses on driving revenue and promoting products or services. It utilizes the ERP system to manage customer relationships, track sales activities, and analyze marketing campaigns to enhance overall business growth."}, {"department_name": "finance_and_accounting", "department_description": "Responsible for managing financial transactions, budgeting, and financial reporting."}, {"department_name": "support_services", "department_description": "Encompasses a range of functions that support the day-to-day operations of an organization"}, {"department_name": "management", "department_description": "Collaborates with various departments to ensure alignment with organizational objectives and effective implementation of policies and initiatives."}]
                for department in departments_list:
                    new_department, created = CompanyDepartment.objects.get_or_create(company_profile=company_profile,
                                                                                      department_name=department["department_name"], department_description=department["department_description"])
                company_profile.company_departments_set = True
                company_profile.save()
                return Response({"message": "Company main branch set up successful"}, status=200)
            else:
                return Response({"message": "Error setting up company main branch"}, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this function"}, status=401)
    except:# Exception as e:
        #print(e)
        return Response({"message": "Unable to set up company main branch"}, status=500)
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_super_hr_user(request):
    company_serial_number = request.data["serial_number"]
    email = request.data['username']
    password = generate_random_string(6)
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=request.user)
        if staff_profile.staff_position.position_title == "System Administrator" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            serializers = UserSerializer(
                data={'username': email, 'password': password})
            if serializers.is_valid():
                user = serializers.save()
                user.is_staff = True
                user.save()
                new_user = authenticate(username=email, password=password)
                staff_position, created = staffPosition.objects.get_or_create(company_profile=company_profile,
                    position_title="Head of Human Resource")
                main_branch = CompanyBranch.objects.get(
                    company_profile=company_profile, main_branch=True)
                department = CompanyDepartment.objects.get(
                    department_name="human_resource_management")
                # print(main_branch)
                # print(department)
                staff, created = StaffProfile.objects.get_or_create(
                    user=new_user, staff_position=staff_position, email_address=new_user.username, company_branch=main_branch, company_department=department, has_read_write_priviledges=True, is_head_of_department=True,is_super_admin=True)  # creates the system administrator role
                #print("running well")
                company_profile.company_super_hr_created = True
                company_profile.save()
                
                #create default deduction schemes for the super hr
                # retrive paye
                paye_scheme = Deduction.objects.get(
                    deduction_title="PAYE", company_profile=company_profile)
                # retrive shif
                shif_scheme = Deduction.objects.get(
                    deduction_title="SHIF", company_profile=company_profile)
                # retrive nssf
                nssf_scheme = Deduction.objects.get(
                    deduction_title="NSSF", company_profile=company_profile)
                #retirve nhif
                nhif_scheme = Deduction.objects.get(
                    deduction_title="NHIF", company_profile=company_profile)
                # paye
                paye_deduction_scheme_serializer = StaffDeductionSchemeSerializer(data={
                                                                                  'staff_profile': staff.id, 'deduction': paye_scheme.id})
                if paye_deduction_scheme_serializer.is_valid():
                    paye_deduction_scheme_serializer.save()
                # shif
                shif_deduction_scheme_serializer = StaffDeductionSchemeSerializer(data={
                                                                                  'staff_profile': staff.id, 'deduction': shif_scheme.id})
                if shif_deduction_scheme_serializer.is_valid():
                    shif_deduction_scheme_serializer.save()
                # nssf
                nssf_deduction_scheme_serializer = StaffDeductionSchemeSerializer(data={
                                                                                  'staff_profile': staff.id, 'deduction': nssf_scheme.id})
                if nssf_deduction_scheme_serializer.is_valid():
                    nssf_deduction_scheme_serializer.save()
                # nhif
                nhif_deduction_scheme_serializer = StaffDeductionSchemeSerializer(data={
                                                                                  'staff_profile': staff.id, 'deduction': nhif_scheme.id})
                if nhif_deduction_scheme_serializer.is_valid():
                    nhif_deduction_scheme_serializer.save()
                message = f"You have successfully registered on Megawatt Energies ERP. Your staff number is {staff.staff_number}. Your autogenerated password is {password}. Once logged in, change your password."
                recipient_list = [f'{email}']
                try:
                    send_email_signup(request, message, recipient_list)
                except:
                    pass
                return Response({"message": "Head of Human Resource account created successfully", }, status=200)
            else:
                return Response({"message": "Unable to create account for Head of Human Resource", }, status=406)
        else:
            return Response({"message": "You are unauthorized to perform this action", }, status=401)
    except:# Exception as e:
        #print(e)
        return Response({"message": "Error creating account for Head of Human Resource", }, status=500)
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_other_staff_user(request):
    company_serial_number = request.data["serial_number"]
    email = request.data['username']
    password = generate_random_string(6)
    try:
        company_profile = CompanyProfile.objects.get(
        company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=request.user)
        if staff_profile.staff_position.position_title == "System Administrator" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            serializers = UserSerializer(
            data={'username': email, 'password': password})
            if serializers.is_valid():
                user = serializers.save()
                user.is_staff = True
                user.save()
                new_user = authenticate(username=email, password=password)
                staff, created = StaffProfile.objects.get_or_create(
                    user=new_user, email_address=new_user.username,)
                # create default deduction schemes for the super hr
                # retrive paye
                paye_scheme = Deduction.objects.get(
                    deduction_title="PAYE", company_profile=company_profile)
                # retrive shif
                shif_scheme = Deduction.objects.get(
                    deduction_title="SHIF", company_profile=company_profile)
                # retrive nssf
                nssf_scheme = Deduction.objects.get(
                    deduction_title="NSSF", company_profile=company_profile)
                # retirve nhif
                nhif_scheme = Deduction.objects.get(
                    deduction_title="NHIF", company_profile=company_profile)
                # paye
                paye_deduction_scheme_serializer = StaffDeductionSchemeSerializer(data={
                                                                                  'staff_profile': staff.id, 'deduction': paye_scheme.id})
                if paye_deduction_scheme_serializer.is_valid():
                    paye_deduction_scheme_serializer.save()
                # shif
                shif_deduction_scheme_serializer = StaffDeductionSchemeSerializer(data={
                                                                                  'staff_profile': staff.id, 'deduction': shif_scheme.id})
                if shif_deduction_scheme_serializer.is_valid():
                    shif_deduction_scheme_serializer.save()
                # nssf
                nssf_deduction_scheme_serializer = StaffDeductionSchemeSerializer(data={
                                                                                  'staff_profile': staff.id, 'deduction': nssf_scheme.id})
                if nssf_deduction_scheme_serializer.is_valid():
                    nssf_deduction_scheme_serializer.save()
                # nhif
                nhif_deduction_scheme_serializer = StaffDeductionSchemeSerializer(data={
                                                                                  'staff_profile': staff.id, 'deduction': nhif_scheme.id})
                if nhif_deduction_scheme_serializer.is_valid():
                    nhif_deduction_scheme_serializer.save()
                message = f"You have successfully registered on Megawatt Energies ERP. Your staff number is {staff.staff_number}. Your autogenerated password is {password}. Once logged in, change your password."
                recipient_list = [f'{email}']
                try:
                    send_email_signup(request, message, recipient_list)
                except:
                    pass
                return Response({"message": "User account created successfully", }, status=200)
            else:
                return Response({"message": "Unable to create user account", }, status=406)
        else:
            return Response({"message": "You are unauthorized to perform this action", }, status=401)
    except:  # Exception as e:
        # print(e)
        return Response({"message": "Error creating user account", }, status=500)
        

    


