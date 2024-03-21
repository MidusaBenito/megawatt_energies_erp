from django.shortcuts import render

from system_administration.utils import get_staff_profile_data
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from datetime import datetime
import json
from django.http import JsonResponse

# Create views section
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_warehouse(request): 
    company_serial_number = request.data["serial_number"]
    company_branch_id = request.data["company_branch_id"]
    warehouse_name = request.data["warehouse_name"]
    warehouse_location = request.data["warehouse_location"]
    warehouse_capacity = request.data["warehouse_capacity"]
    warehouse_contact_phone = request.data["warehouse_contact_phone"]
    warehouse_description = request.data["warehouse_description"]
    active_user = request.user
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=active_user)
        if staff_profile.company_department.department_name == "warehouse_management" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            warehouse_serializer = WarehouseSerializer(
                data={'company_branch': int(company_branch_id), 'warehouse_name': warehouse_name, 'warehouse_location': warehouse_location, 'warehouse_capacity': warehouse_capacity, 'warehouse_contact_phone': warehouse_contact_phone, 'warehouse_description': warehouse_description, 'created_by': staff_profile.id, 'last_updated_by': staff_profile.id})
            if warehouse_serializer.is_valid():
                warehouse_serializer.save()
                return Response({"message": "Warehouse created successfully", }, status=200)
            else:
                #print(warehouse_serializer.errors)
                return Response({"message": "Unable to create warehouse", }, status=406)
        else:
            return Response({"message": "You are not authorised to perform this action", }, status=401)
    except:
        return Response({"message": "Error creating warehouse", }, status=200)
    

# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def create_category(request):
#     company_serial_number = request.data["serial_number"]
#     category_name = request.data["category_name"]
#     category_description = request.data["category_description"]
#     active_user = request.user
#     try:
#         company_profile = CompanyProfile.objects.get(
#             company_serial_number=company_serial_number)
#         staff_profile = StaffProfile.objects.get(user=active_user)
#         if staff_profile.company_department.department_name == "warehouse_management" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
#             category_serializer = CategorySerializer(
#                 data={'category_name': category_name, 'category_description': category_description, 'created_by': staff_profile.id,'last_updated_by':staff_profile.id})
#             if category_serializer.is_valid():
#                 category_serializer.save()
#                 return Response({"message": "Product category created successfully", }, status=200)
#             else:
#                 return Response({"message": "Unable to create product category", }, status=406)
#         else:
#             return Response({"message": "You are unauthorised to perform this action", }, status=401)
#     except:
#         return Response({"message": "Error creating product category", }, status=500)
    

# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def create_product(request):
#     company_serial_number = request.data["serial_number"]
#     category_id = request.data["category_id"]
#     product_name = request.data["product_name"]
#     unit_of_measurement = request.data["unit_of_measurement"]
#     product_description = request.data["product_description"]
#     warehouse_id = request.data["warehouse_id"]
#     active_user = request.user
#     try:
#         company_profile = CompanyProfile.objects.get(
#             company_serial_number=company_serial_number)
#         staff_profile = StaffProfile.objects.get(user=active_user)
#         if staff_profile.company_department.department_name == "warehouse_management" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
#             product_serializer = ProductSerializer(
#                 data={'category': int(category_id), 'product_name': product_name, 'unit_of_measurement': unit_of_measurement, 'product_description': product_description, 'created_by': staff_profile.id, 'last_updated_by': staff_profile.id})
#             if product_serializer.is_valid():
#                 new_product = product_serializer.save()
#                 #create inventory for the product
#                 #get warehouse
#                 warehouse = Warehouse.objects.get(id=int(warehouse_id))
#                 inventory_serializer = InventorySerializer(
#                     data={'product': new_product.id, 'warehouse': warehouse.id, 'created_by': staff_profile.id, 'last_updated_by': staff_profile.id})
#                 if inventory_serializer.is_valid():
#                     inventory_serializer.save()
#                     return Response({"message": "Product created successfully", }, status=200)
#                 else:
#                     return Response({"message": "Error creating product inventory", }, status=406)
#             else:
#                 return Response({"message": "Unable to create product", }, status=406)
#         else:
#             return Response({"message": "You are unauthorised to perform this action", }, status=401)
#     except:
#         return Response({"message": "Error creating product", }, status=500)

# #get all views section


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def warehouse_management_dashboard(request):
    date_format = '%d/%m/%Y, %H:%M'
    company_serial_number = request.data["serial_number"]
    active_user = request.user
    payload = {}
    warehouse_list = []
    warehouse_map = {}
    company_profile_map = {}
    company_branches_list = []
    company_branch_map = {}
    category_map = {}
    category_list = []
    product_map = {}
    product_list = []
    warehouse_inventory_map = {}
    warehouse_inventory_list = []
    outgoing_warehouse_stock_transactions_map = {}
    outgoing_warehouse_stock_transactions_list = []
    incoming_warehouse_stock_transactions_map = {}
    incoming_warehouse_stock_transactions_list = []
    stock_transaction_instances_map = {}
    stock_transaction_instances_map = {}
    stock_transaction_instances_list = []
    warehouse_equipment_map = {}
    warehouse_equipment_list = []
    purchase_requisition_map = {}
    purchase_requisition_list = []
    purchase_requisition_instances_map = {}
    purchase_requisition_instances_list = []
    warehouse_stock_requisitions_map = {}
    warehouse_stock_requisitions_list = []
    stock_requisition_instances_map = {}
    stock_requisition_instances_list = []
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        all_branches = company_profile.company_branches.all()
        #
        staff_profile = StaffProfile.objects.get(user=active_user)
        if staff_profile.company_department.department_name == "warehouse_management" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            active_staff_profile_data = get_staff_profile_data(active_user)
            company_profile_map["company_id"] = str(company_profile.id)
            company_profile_map["company_name"] = company_profile.company_name
            company_profile_map["company_phone"] = company_profile.company_phone
            #get all product categories
            all_categories = Category.objects.all().order_by("-id")
            for category in all_categories:
                if category.recycle_bin != True:
                    category_map = {}
                    product_list = []
                    category_map["category_id"] = str(category.id)
                    category_map["category_name"] = category.category_name
                    category_map["category_description"] = category.category_description
                    category_products = category.category_products.all().order_by("-id")
                    for product in category_products:
                        if product.recycle_bin != True:
                            product_map = {}
                            product_map["product_id"] = str(product.id)
                            product_map["product_name"] = product.product_name
                            product_map["stock_keeping_unit"] = product.stock_keeping_unit
                            product_map["unit_of_measurement"] = product.unit_of_measurement
                            product_map["product_description"] = product.product_description
                            #product_map["product_description"] = product.product_description
                            product_list.append(product_map)
                    category_map["product_list"] = product_list
                    category_list.append(category_map)
        
            for branch in all_branches:
                company_branch_map = {}
                company_branch_map["branch_id"] = str(branch.id)
                company_branch_map["branch_name"] = branch.branch_name
                company_branch_map["is_main_branch"] = "true" if branch.main_branch == True else "false"
                all_branch_warehouses = branch.branch_warehouses.all()
                for warehouse in all_branch_warehouses:
                    if warehouse.recycle_bin != True:
                        warehouse_map = {}
                        warehouse_inventory_list = []
                        outgoing_warehouse_stock_transactions_list = []
                        incoming_warehouse_stock_transactions_list = []
                        warehouse_equipment_list = []
                        purchase_requisition_list = []
                        warehouse_stock_requisitions_list = []
                        warehouse_map["warehouse_id"] = str(warehouse.id)
                        warehouse_map["warehouse_company_branch_id"] = str(warehouse.company_branch.id)
                        warehouse_map["warehouse_company_branch_name"] = warehouse.company_branch.branch_name
                        warehouse_map["warehouse_name"] = warehouse.warehouse_name
                        warehouse_map["warehouse_location"] = warehouse.warehouse_location
                        warehouse_map["warehouse_capacity"] = warehouse.warehouse_capacity
                        warehouse_map["warehouse_contact_phone"] = warehouse.warehouse_contact_phone
                        warehouse_map["warehouse_description"] = warehouse.warehouse_description
                        #
                        creator_map = {}
                        creator_map["staff_id"] = str(
                            warehouse.created_by.id) if warehouse.created_by is not None else ""
                        creator_map["staff_name"] = f'{warehouse.created_by.first_name} {warehouse.created_by.last_name}' if warehouse.created_by is not None else ""
                        creator_map["staff_position"] = warehouse.created_by.staff_position.position_title if warehouse.created_by.staff_position is not None else ""
                        warehouse_map["created_by"] = creator_map
                        creator_map = {}
                        creator_map["staff_id"] = str(
                            warehouse.last_updated_by.id) if warehouse.last_updated_by is not None else ""
                        creator_map["staff_name"] = f'{warehouse.last_updated_by.first_name} {warehouse.last_updated_by.last_name}' if warehouse.last_updated_by is not None else ""
                        creator_map["staff_position"] = warehouse.last_updated_by.staff_position.position_title if warehouse.last_updated_by.staff_position is not None else ""
                        warehouse_map["last_updated_by"] = creator_map
                        warehouse_map["created_on"] = datetime.strftime(
                        warehouse.created_on, date_format) if warehouse.created_on is not None else ""
                        warehouse_map["last_updated_on"] = datetime.strftime(
                        warehouse.last_updated_on, date_format) if warehouse.last_updated_on is not None else ""
                        #attach invetories
                        warehouse_inventories = warehouse.warehouse_inventories.all().order_by("-id")
                        for warehouse_inventory in warehouse_inventories:
                            if warehouse_inventory.product is not None and warehouse_inventory.recycle_bin != True:
                                warehouse_inventory_map = {}
                                warehouse_inventory_map["product_id"] = str(warehouse_inventory.product.id)
                                warehouse_inventory_map["warehouse_id"] = str(
                                    warehouse_inventory.warehouse.id)
                                warehouse_inventory_map["quantity"] = warehouse_inventory.quantity
                                warehouse_inventory_map["minimum_stock_level"] = warehouse_inventory.minimum_stock_level
                                warehouse_inventory_map["inventory_description"] = warehouse_inventory.inventory_description
                                #warehouse_inventory_map["inventory_description"] = warehouse_inventory.inventory_description
                                #
                                creator_map = {}
                                creator_map["staff_id"] = str(
                                    warehouse_inventory.created_by.id) if warehouse_inventory.created_by is not None else ""
                                creator_map["staff_name"] = f'{warehouse_inventory.created_by.first_name} {warehouse_inventory.created_by.last_name}' if warehouse_inventory.created_by is not None else ""
                                creator_map["staff_position"] = warehouse_inventory.created_by.staff_position.position_title if warehouse_inventory.created_by.staff_position is not None else ""
                                warehouse_inventory_map["created_by"] = creator_map
                                creator_map = {}
                                creator_map["staff_id"] = str(
                                    warehouse_inventory.last_updated_by.id) if warehouse_inventory.last_updated_by is not None else ""
                                creator_map["staff_name"] = f'{warehouse_inventory.last_updated_by.first_name} {warehouse_inventory.last_updated_by.last_name}' if warehouse_inventory.last_updated_by is not None else ""
                                creator_map["staff_position"] = warehouse_inventory.last_updated_by.staff_position.position_title if warehouse_inventory.last_updated_by.staff_position is not None else ""
                                warehouse_inventory_map["last_updated_by"] = creator_map
                                warehouse_inventory_map["created_on"] = datetime.strftime(
                                    warehouse_inventory.created_on, date_format) if warehouse_inventory.created_on is not None else ""
                                warehouse_inventory_map["last_updated_on"] = datetime.strftime(
                                    warehouse_inventory.last_updated_on, date_format) if warehouse_inventory.last_updated_on is not None else ""
                                warehouse_inventory_list.append(
                                    warehouse_inventory_map)
                                #
                        warehouse_map["warehouse_inventory_list"] = warehouse_inventory_list
                        outgoing_warehouse_stock_transactions = warehouse.source_warehouse_stock_transactions.all().order_by("-id")
                        for outgoing_stock_transaction in outgoing_warehouse_stock_transactions:
                            if outgoing_stock_transaction.recycle_bin != True:
                                outgoing_warehouse_stock_transactions_map = {}
                                outgoing_warehouse_stock_transactions_map["outgoing_stock_transaction_id"] = str(
                                    outgoing_stock_transaction.id)
                                outgoing_warehouse_stock_transactions_map[
                                    "stock_transaction_number"] = outgoing_stock_transaction.stock_transaction_number
                                outgoing_warehouse_stock_transactions_map[
                                    "recipient_warehouse_id"] = str(outgoing_stock_transaction.recipient_warehouse.id) if outgoing_stock_transaction.recipient_warehouse is not None else ""
                                outgoing_warehouse_stock_transactions_map[
                                    "transaction_type"] = outgoing_stock_transaction.transaction_type
                                outgoing_warehouse_stock_transactions_map[
                                    "transaction_description"] = outgoing_stock_transaction.transaction_description
                                outgoing_warehouse_stock_transactions_map[
                                    "stock_transaction_reference"] = outgoing_stock_transaction.stock_transaction_reference
                                outgoing_warehouse_stock_transactions_map[
                                    "stock_transaction_added_to_inventory"] = "true" if outgoing_stock_transaction.stock_transaction_added_to_inventory == True else "false"
                                creator_map = {}
                                creator_map["staff_id"] = str(
                                    outgoing_stock_transaction.created_by.id) if outgoing_stock_transaction.created_by is not None else ""
                                creator_map["staff_name"] = f'{outgoing_stock_transaction.created_by.first_name} {outgoing_stock_transaction.created_by.last_name}' if outgoing_stock_transaction.created_by is not None else ""
                                creator_map["staff_position"] = outgoing_stock_transaction.created_by.staff_position.position_title if outgoing_stock_transaction.created_by.staff_position is not None else ""
                                outgoing_warehouse_stock_transactions_map["created_by"] = creator_map
                                creator_map = {}
                                creator_map["staff_id"] = str(
                                    outgoing_stock_transaction.last_updated_by.id) if outgoing_stock_transaction.last_updated_by is not None else ""
                                creator_map["staff_name"] = f'{outgoing_stock_transaction.last_updated_by.first_name} {outgoing_stock_transaction.last_updated_by.last_name}' if outgoing_stock_transaction.last_updated_by is not None else ""
                                creator_map["staff_position"] = outgoing_stock_transaction.last_updated_by.staff_position.position_title if outgoing_stock_transaction.last_updated_by.staff_position is not None else ""
                                outgoing_warehouse_stock_transactions_map["last_updated_by"] = creator_map
                                outgoing_warehouse_stock_transactions_map["created_on"] = datetime.strftime(
                                    outgoing_stock_transaction.created_on, date_format) if outgoing_stock_transaction.created_on is not None else ""
                                outgoing_warehouse_stock_transactions_map["last_updated_on"] = datetime.strftime(
                                    outgoing_stock_transaction.last_updated_on, date_format) if outgoing_stock_transaction.last_updated_on is not None else ""
                                #getting stock transaction instances
                                stock_transaction_instances_list = []
                                stock_transaction_instances = outgoing_stock_transaction.stock_transaction_instances.all().order_by("-id")
                                for stock_transaction_instance in stock_transaction_instances:
                                    stock_transaction_instances_map["stock_transaction_instance_id"] = str(stock_transaction_instance.id)
                                    stock_transaction_instances_map["product_id"] = str(
                                        stock_transaction_instance.product.id) if stock_transaction_instance.product is not None else ""
                                    stock_transaction_instances_map["quantity"] = stock_transaction_instance.quantity
                                    stock_transaction_instances_list.append(stock_transaction_instances_map)
                                outgoing_warehouse_stock_transactions_map[
                                    "stock_transaction_instances_list"] = stock_transaction_instances_list
                                outgoing_warehouse_stock_transactions_list.append(
                                    outgoing_warehouse_stock_transactions_map)
                        warehouse_map["outgoing_warehouse_stock_transactions_list"] = outgoing_warehouse_stock_transactions_list
                        #incoming
                        incoming_warehouse_stock_transactions = warehouse.recipient_warehouse_stock_transactions.all().order_by("-id")
                        for incoming_stock_transaction in incoming_warehouse_stock_transactions:
                            if incoming_stock_transaction.recycle_bin != True:
                                incoming_warehouse_stock_transactions_map = {}
                                incoming_warehouse_stock_transactions_map["incoming_stock_transaction_id"] = str(
                                    incoming_stock_transaction.id)
                                incoming_warehouse_stock_transactions_map[
                                    "stock_transaction_number"] = incoming_stock_transaction.stock_transaction_number
                                incoming_warehouse_stock_transactions_map[
                                    "source_warehouse_id"] = str(incoming_stock_transaction.source_warehouse.id) if incoming_stock_transaction.source_warehouse is not None else ""
                                #print("running!")
                                incoming_warehouse_stock_transactions_map[
                                    "transaction_type"] = incoming_stock_transaction.transaction_type
                                incoming_warehouse_stock_transactions_map[
                                    "transaction_description"] = incoming_stock_transaction.transaction_description
                                incoming_warehouse_stock_transactions_map[
                                    "stock_transaction_reference"] = incoming_stock_transaction.stock_transaction_reference
                                incoming_warehouse_stock_transactions_map[
                                    "stock_transaction_added_to_inventory"] = "true" if incoming_stock_transaction.stock_transaction_added_to_inventory == True else "false"
                                creator_map = {}
                                creator_map["staff_id"] = str(
                                    incoming_stock_transaction.created_by.id) if incoming_stock_transaction.created_by is not None else ""
                                creator_map["staff_name"] = f'{incoming_stock_transaction.created_by.first_name} {incoming_stock_transaction.created_by.last_name}' if incoming_stock_transaction.created_by is not None else ""
                                creator_map["staff_position"] = incoming_stock_transaction.created_by.staff_position.position_title if incoming_stock_transaction.created_by.staff_position is not None else ""
                                incoming_warehouse_stock_transactions_map["created_by"] = creator_map
                                creator_map = {}
                                creator_map["staff_id"] = str(
                                    incoming_stock_transaction.last_updated_by.id) if incoming_stock_transaction.last_updated_by is not None else ""
                                creator_map["staff_name"] = f'{incoming_stock_transaction.last_updated_by.first_name} {incoming_stock_transaction.last_updated_by.last_name}' if incoming_stock_transaction.last_updated_by is not None else ""
                                creator_map["staff_position"] = incoming_stock_transaction.last_updated_by.staff_position.position_title if incoming_stock_transaction.last_updated_by.staff_position is not None else ""
                                incoming_warehouse_stock_transactions_map["last_updated_by"] = creator_map
                                incoming_warehouse_stock_transactions_map["created_on"] = datetime.strftime(
                                    incoming_stock_transaction.created_on, date_format) if incoming_stock_transaction.created_on is not None else ""
                                incoming_warehouse_stock_transactions_map["last_updated_on"] = datetime.strftime(
                                    incoming_stock_transaction.last_updated_on, date_format) if incoming_stock_transaction.last_updated_on is not None else ""
                                #getting stock transaction instances
                                stock_transaction_instances_list = []
                                stock_transaction_instances = incoming_stock_transaction.stock_transaction_instances.all().order_by("-id")
                                for stock_transaction_instance in stock_transaction_instances:
                                    stock_transaction_instances_map = {}
                                    stock_transaction_instances_map["stock_transaction_instance_id"] = str(
                                        stock_transaction_instance.id)
                                    stock_transaction_instances_map["product_id"] = str(
                                        stock_transaction_instance.product.id) if stock_transaction_instance.product is not None else ""
                                    stock_transaction_instances_map["quantity"] = stock_transaction_instance.quantity
                                    stock_transaction_instances_list.append(
                                        stock_transaction_instances_map)
                                incoming_warehouse_stock_transactions_map[
                                    "stock_transaction_instances_list"] = stock_transaction_instances_list
                                incoming_warehouse_stock_transactions_list.append(
                                    incoming_warehouse_stock_transactions_map)
                        warehouse_map["incoming_warehouse_stock_transactions_list"] = incoming_warehouse_stock_transactions_list
                        #warehouse equipment
                        warehouse_equipment = warehouse.warehouse_equipment.all().order_by("-id")
                        for equipment in warehouse_equipment:
                            if equipment.recycle_bin != True:
                                warehouse_equipment_map = {}
                                warehouse_equipment_map["equipment_id"] = str(equipment.id)
                                warehouse_equipment_map["equipment_serial_number"] = equipment.equipment_serial_number
                                warehouse_equipment_map["equipment_description"] = equipment.equipment_description
                                warehouse_equipment_map["status"] = equipment.status
                                creator_map = {}
                                creator_map["staff_id"] = str(
                                    equipment.created_by.id) if equipment.created_by is not None else ""
                                creator_map["staff_name"] = f'{equipment.created_by.first_name} {equipment.created_by.last_name}' if equipment.created_by is not None else ""
                                creator_map["staff_position"] = equipment.created_by.staff_position.position_title if equipment.created_by.staff_position is not None else ""
                                warehouse_equipment_map["created_by"] = creator_map
                                creator_map = {}
                                creator_map["staff_id"] = str(
                                    equipment.last_updated_by.id) if equipment.last_updated_by is not None else ""
                                creator_map["staff_name"] = f'{equipment.last_updated_by.first_name} {equipment.last_updated_by.last_name}' if equipment.last_updated_by is not None else ""
                                creator_map["staff_position"] = equipment.last_updated_by.staff_position.position_title if equipment.last_updated_by.staff_position is not None else ""
                                warehouse_equipment_map["last_updated_by"] = creator_map
                                warehouse_equipment_map["created_on"] = datetime.strftime(
                                    equipment.created_on, date_format) if equipment.created_on is not None else ""
                                warehouse_equipment_map["last_updated_on"] = datetime.strftime(
                                    equipment.last_updated_on, date_format) if equipment.last_updated_on is not None else ""
                                warehouse_equipment_list.append(warehouse_equipment_map)
                        warehouse_map["warehouse_equipment_list"] = warehouse_equipment_list
                        warehouse_purchase_requisitions = warehouse.warehouse_purchase_requisitions.all().order_by("-id")
                        for purchase_requisition in warehouse_purchase_requisitions:
                            if purchase_requisition.recycle_bin != True:
                                purchase_requisition_map = {}
                                purchase_requisition_instances_list = []
                                purchase_requisition_map["purchase_requisition_id"] = str(
                                    purchase_requisition.id)
                                purchase_requisition_map["purchase_requisition_number"] = purchase_requisition.purchase_requisition_number
                                purchase_requisition_map["purchase_requisition_description"] = purchase_requisition.purchase_requisition_description
                                purchase_requisition_map["purchase_requisition_approved"] = "true" if purchase_requisition.purchase_requisition_approved == True else "false"
                                creator_map = {}
                                creator_map["staff_id"] = str(
                                    purchase_requisition.created_by.id) if purchase_requisition.created_by is not None else ""
                                creator_map["staff_name"] = f'{purchase_requisition.created_by.first_name} {purchase_requisition.created_by.last_name}' if purchase_requisition.created_by is not None else ""
                                creator_map["staff_position"] = purchase_requisition.created_by.staff_position.position_title if purchase_requisition.created_by.staff_position is not None else ""
                                purchase_requisition_map["created_by"] = creator_map
                                creator_map = {}
                                creator_map["staff_id"] = str(
                                    purchase_requisition.last_updated_by.id) if purchase_requisition.last_updated_by is not None else ""
                                creator_map["staff_name"] = f'{purchase_requisition.last_updated_by.first_name} {purchase_requisition.last_updated_by.last_name}' if purchase_requisition.last_updated_by is not None else ""
                                creator_map["staff_position"] = purchase_requisition.last_updated_by.staff_position.position_title if purchase_requisition.last_updated_by.staff_position is not None else ""
                                purchase_requisition_map["last_updated_by"] = creator_map
                                purchase_requisition_map["created_on"] = datetime.strftime(
                                    purchase_requisition.created_on, date_format) if purchase_requisition.created_on is not None else ""
                                purchase_requisition_map["last_updated_on"] = datetime.strftime(
                                    purchase_requisition.last_updated_on, date_format) if purchase_requisition.last_updated_on is not None else ""
                                purchase_requisition_instances = purchase_requisition.purchase_requisition_instances.all().order_by("id")
                                for purchase_requisition_instance in purchase_requisition_instances:
                                    if purchase_requisition_instance.recycle_bin != True:
                                        purchase_requisition_instances_map = {}
                                        purchase_requisition_instances_map["purchase_requisition_instance_id"] = str(
                                            purchase_requisition_instance.id)
                                        purchase_requisition_instances_map["product_id"] = str(purchase_requisition_instance.product.id) if purchase_requisition_instance.product is not None else ""
                                        purchase_requisition_instances_map[
                                            "quantity"] = purchase_requisition_instance.quantity
                                        purchase_requisition_instances_map[
                                            "purchase_requisition_items_purchased"] = "true" if purchase_requisition_instance.purchase_requisition_items_purchased == True else "false"
                                        purchase_requisition_instances_list.append(
                                            purchase_requisition_instances_map)
                                purchase_requisition_map["purchase_requisition_instances_list"] = purchase_requisition_instances_list
                                purchase_requisition_list.append(
                                    purchase_requisition_map)
                        warehouse_map["purchase_requisition_list"] = purchase_requisition_list
                        warehouse_stock_requisitions = warehouse.warehouse_stock_requisitions.all().order_by("-id")
                        for warehouse_stock_requisition in warehouse_stock_requisitions:
                            if warehouse_stock_requisition.recycle_bin != True:
                                warehouse_stock_requisitions_map = {}
                                stock_requisition_instances_list = []
                                warehouse_stock_requisitions_map["warehouse_stock_requisition_id"] = str(
                                    warehouse_stock_requisition.id)
                                warehouse_stock_requisitions_map[
                                    "stock_requisition_number"] = warehouse_stock_requisition.stock_requisition_number
                                warehouse_stock_requisitions_map[
                                    "stock_requisition_description"] = warehouse_stock_requisition.stock_requisition_description
                                warehouse_stock_requisitions_map[
                                    "stock_requisition_approved"] = "true" if warehouse_stock_requisition.stock_requisition_approved == True else "false"
                                creator_map = {}
                                creator_map["staff_id"] = str(
                                    warehouse_stock_requisition.created_by.id) if warehouse_stock_requisition.created_by is not None else ""
                                creator_map["staff_name"] = f'{warehouse_stock_requisition.created_by.first_name} {warehouse_stock_requisition.created_by.last_name}' if warehouse_stock_requisition.created_by is not None else ""
                                creator_map["staff_position"] = warehouse_stock_requisition.created_by.staff_position.position_title if warehouse_stock_requisition.created_by.staff_position is not None else ""
                                warehouse_stock_requisitions_map["created_by"] = creator_map
                                creator_map = {}
                                creator_map["staff_id"] = str(
                                    warehouse_stock_requisition.last_updated_by.id) if warehouse_stock_requisition.last_updated_by is not None else ""
                                creator_map["staff_name"] = f'{warehouse_stock_requisition.last_updated_by.first_name} {warehouse_stock_requisition.last_updated_by.last_name}' if warehouse_stock_requisition.last_updated_by is not None else ""
                                creator_map["staff_position"] = warehouse_stock_requisition.last_updated_by.staff_position.position_title if warehouse_stock_requisition.last_updated_by.staff_position is not None else ""
                                warehouse_stock_requisitions_map["last_updated_by"] = creator_map
                                warehouse_stock_requisitions_map["created_on"] = datetime.strftime(
                                    warehouse_stock_requisition.created_on, date_format) if warehouse_stock_requisition.created_on is not None else ""
                                warehouse_stock_requisitions_map["last_updated_on"] = datetime.strftime(
                                    warehouse_stock_requisition.last_updated_on, date_format) if warehouse_stock_requisition.last_updated_on is not None else ""
                                stock_requisition_instances = warehouse_stock_requisition.stock_requisition_instances.all().order_by("-id")
                                for stock_requisition_instance in stock_requisition_instances:
                                    if stock_requisition_instance.recycle_bin != True:
                                        stock_requisition_instances_map = {}
                                        stock_requisition_instances_map["stock_requisition_instance_id"] = str(
                                            stock_requisition_instance.id)
                                        stock_requisition_instances_map["product_id"] = str(
                                            stock_requisition_instance.product.id) if stock_requisition_instance.product is not None else ""
                                        stock_requisition_instances_map["quantity"] = stock_requisition_instance.quantity
                                        stock_requisition_instances_map[
                                            "stock_requisition_items_delivered"] = "true" if stock_requisition_instance.stock_requisition_items_delivered else "false"
                                        stock_requisition_instances_list.append(
                                            stock_requisition_instances_map)
                                warehouse_stock_requisitions_map[
                                    "stock_requisition_instances_list"] = stock_requisition_instances_list
                                warehouse_stock_requisitions_list.append(
                                    warehouse_stock_requisitions_map)
                        warehouse_map["warehouse_stock_requisitions_list"] = warehouse_stock_requisitions_list
                        if staff_profile.company_branch.main_branch == True:
                            warehouse_list.append(warehouse_map)
                        else:
                            if staff_profile.company_branch.id == branch.id:
                                warehouse_list.append(warehouse_map)
                company_branches_list.append(company_branch_map)
            company_profile_map["company_branches_list"] = company_branches_list
            payload["active_staff_profile_data"] = active_staff_profile_data
            payload["warehouse_list"] = warehouse_list
            payload["company_profile"] = company_profile_map
            payload["category_list"] = category_list
            return Response({"message": "true", "payload": payload}, status=200)
        else:
            return Response({"message": "false", "payload": payload}, status=401)
    except Exception as e:
        print(e)
        return Response({"message": "false", "payload": payload}, status=500)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_equipment(request):
    active_user = request.user
    warehouse_id = request.data["warehouse_id"]
    company_serial_number = request.data["serial_number"]
    equipment_name = request.data["equipment_name"]
    equipment_serial_number = request.data["equipment_serial_number"]
    equipment_description = request.data["equipment_description"]
    status = request.data["status"]
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=active_user)
        if staff_profile.company_department.department_name == "warehouse_management" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            equipment_serializer = EquipmentSerializer(
                data={'warehouse': int(warehouse_id), 'equipment_name': equipment_name,'equipment_serial_number':equipment_serial_number, 'equipment_description': equipment_description, 'status': status, 'created_by': staff_profile.id, 'last_updated_by': staff_profile.id})
            if equipment_serializer.is_valid():
                equipment_serializer.save()
                return Response({"message": "Equipment added successfully", }, status=200)
            else:
                return Response({"message": "Unable to add equipment", }, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this action", }, status=401)
    except:
        return Response({"message": "Error adding equipment", }, status=500)
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_product_categories(request):
    active_user = request.user
    category_name = request.data["category_name"]
    category_description = request.data["category_description"]
    company_serial_number = request.data["serial_number"]
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=active_user)
        if staff_profile.company_department.department_name == "warehouse_management" and staff_profile.company_branch.main_branch == True and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            category_serializer = CategorySerializer(
                data={'category_name': category_name, 'category_description': category_description, 'created_by': staff_profile.id, 'last_updated_by': staff_profile.id})
            if category_serializer.is_valid():
                category_serializer.save()
                return Response({"message": "Product category added successfully", }, status=200)
            else:
                return Response({"message": "Unable to add product category", }, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this action", }, status=401)
    except:# Exception as e:
        #print(e)
        return Response({"message": "Error adding product category", }, status=500)
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_product(request):
    active_user = request.user
    company_serial_number = request.data["serial_number"]
    category_id = request.data["category_id"]
    product_name = request.data["product_name"]
    stock_keeping_unit = request.data["stock_keeping_unit"]
    unit_of_measurement = request.data["unit_of_measurement"]
    product_description = request.data["product_description"]
    # minimum_stock_level = request.data["minimum_stock_level"]
    # quantity = request.data["quantity"]
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=active_user)
        if staff_profile.company_department.department_name == "warehouse_management" and staff_profile.company_branch.main_branch == True and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            product_serializer = ProductSerializer(
                data={'category': int(category_id), 'product_name': product_name, 'unit_of_measurement': unit_of_measurement, 'product_description': product_description, 'created_by': staff_profile.id, 'last_updated_by': staff_profile.id})
            if product_serializer.is_valid():
                new_product = product_serializer.save()
                if len(stock_keeping_unit) > 0:
                    new_product.stock_keeping_unit = stock_keeping_unit
                    new_product.save()
                    #new_product_inventory = Inventory.objects.get_or_create(product=new_product.id,warehouse=)
                return Response({"message": "Product added successfully", }, status=200)
            else:
                return Response({"message": "Unable to add product", }, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this action", }, status=401)
    except:# Exception as e:
        #print(e)
        return Response({"message": "Error adding product", }, status=500)
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_stock_transaction(request):
    active_user = request.user
    company_serial_number = request.data["serial_number"]
    transaction_type = request.data["transaction_type"]
    recipient_warehouse_id  = request.data["recipient_warehouse_id"]
    try:
        if transaction_type == "in_bound":
            source_warehouse_id = None
            recipient_warehouse_id = int(recipient_warehouse_id) if len(
                recipient_warehouse_id) > 0 else None
        else:
            source_warehouse_id = int(request.data["source_warehouse_id"]) if len(request.data["source_warehouse_id"]) > 0 else None
            if recipient_warehouse_id != "sales_order":
                recipient_warehouse_id = int(recipient_warehouse_id) if len(
                    recipient_warehouse_id) > 0 else None
            else:
                recipient_warehouse_id = None
        transaction_description = request.data["transaction_description"]
        stock_transaction_reference = request.data["stock_transaction_reference"]
        stock_transaction_added_to_inventory = True if request.data["stock_transaction_added_to_inventory"] == "true" else False
        stock_transaction_instance_list = request.data.get(
            'stock_transaction_instance_list', [])
        stock_transaction_instance_list = json.loads(
            stock_transaction_instance_list)
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=active_user)
        if staff_profile.company_department.department_name == "warehouse_management" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            stock_transaction_serializer = StockTransactionSerializer(
                data={'source_warehouse': source_warehouse_id, 'recipient_warehouse': recipient_warehouse_id, 'transaction_type': transaction_type, 'transaction_description': transaction_description, 'stock_transaction_reference': stock_transaction_reference, 'stock_transaction_added_to_inventory': stock_transaction_added_to_inventory, 'created_by': staff_profile.id,
                      'last_updated_by': staff_profile.id, })
            if stock_transaction_serializer.is_valid():
                new_stock_transaction = stock_transaction_serializer.save()
                for stock_transaction in stock_transaction_instance_list:
                    product_id = int(stock_transaction["product_id"])
                    quantity = stock_transaction["quantity"]
                    stock_transaction_instance_serializer = StockTransactionInstanceSerializer(data={'stock_transaction':new_stock_transaction.id,'product':product_id,'quantity':quantity,})
                    if stock_transaction_instance_serializer.is_valid():
                        stock_transaction_instance_serializer.save()
                return Response({"message": "Stock transaction created successfully", }, status=200)
            else:
                print(stock_transaction_serializer.errors)
                return Response({"message": "Unable to create stock transaction", }, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this action", }, status=401)
    except Exception as e:
        print(e)
        return Response({"message": "Error creating stock transaction", }, status=500)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_purchase_requisition(request):
    active_user = request.user
    company_serial_number = request.data["serial_number"]
    warehouse_id = int(request.data["warehouse_id"])
    purchase_requisition_description = request.data["purchase_requisition_description"]
    purchase_requisition_instance_list = request.data.get(
        'purchase_requisition_instance_list', [])
    purchase_requisition_instance_list = json.loads(
        purchase_requisition_instance_list)
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=active_user)
        if staff_profile.company_department.department_name == "warehouse_management" and staff_profile.company_branch.main_branch == True and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            purchase_requisition_serializer = PurchaseRequisitionSerializer(
                data={'warehouse': warehouse_id, 'purchase_requisition_description': purchase_requisition_description, 'created_by': staff_profile.id,
                    'last_updated_by': staff_profile.id,})
            if purchase_requisition_serializer.is_valid():
                new_purchase_requisition = purchase_requisition_serializer.save()
                for purchase_requisition_instance in purchase_requisition_instance_list:
                    product_id = int(purchase_requisition_instance["product_id"])
                    quantity = purchase_requisition_instance["quantity"]
                    purchase_requisition_instance_serializer = PurchaseRequisitionInstanceSerializer(
                        data={'purchase_requisition': new_purchase_requisition.id, 'product': product_id, 'quantity': quantity, 'created_by': staff_profile.id,
                            'last_updated_by': staff_profile.id,})
                    if purchase_requisition_instance_serializer.is_valid():
                        purchase_requisition_instance_serializer.save()
                return Response({"message": "Purchase requisition created successfully", }, status=200)
            else:
                return Response({"message": "Unable to create purchase requisition", }, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this action", }, status=401)
    except:  # Exception as e:
        # print(e)
        return Response({"message": "Error creating purchase requisition", }, status=500)
    

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_stock_requisition(request):
    active_user = request.user
    company_serial_number = request.data["serial_number"]
    warehouse_id = int(request.data["warehouse_id"])
    stock_requisition_description = request.data["stock_requisition_description"]
    stock_requisition_instance_list = request.data.get(
        'stock_requisition_instance_list', [])
    stock_requisition_instance_list = json.loads(
        stock_requisition_instance_list)
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=active_user)
        if staff_profile.company_department.department_name == "warehouse_management" and staff_profile.company_branch.main_branch != True and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            stock_requisition_serializer = StockRequisitionSerializer(
                data={'warehouse': warehouse_id, 'stock_requisition_description': stock_requisition_description, 'created_by': staff_profile.id,
                      'last_updated_by': staff_profile.id,})
            if stock_requisition_serializer.is_valid():
                new_stock_requisition = stock_requisition_serializer.save()
                for stock_requisition_instance in stock_requisition_instance_list:
                    product_id = int(stock_requisition_instance["product_id"])
                    quantity = stock_requisition_instance["quantity"]
                    stock_requisition_instance_serializer = StockRequisitionInstanceSerializer(
                        data={'stock_requisition':new_stock_requisition.id,'product': product_id, 'quantity': quantity, 'created_by': staff_profile.id,
                              'last_updated_by': staff_profile.id,})
                    if stock_requisition_instance_serializer.is_valid():
                        stock_requisition_instance_serializer.save()
                return Response({"message": "Stock requisition created successfully", }, status=200)
            else:
                return Response({"message": "Unable to create stock requisition", }, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this action", }, status=401)
    except:  # Exception as e:
        # print(e)
        return Response({"message": "Error creating stock requisition", }, status=500)
            




    



