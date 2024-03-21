#from django.shortcuts import render

from system_administration.serializers import UserSerializer
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
from django.contrib.auth import authenticate, login, logout

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def procurement_dashboard(request):
    date_format = '%d/%m/%Y, %H:%M'
    company_serial_number = request.data["serial_number"]
    active_user = request.user
    payload = {}
    supplier_list = []
    supplier_map = {}
    supplied_products_list = []
    supplied_product_map = {}
    company_profile_map = {}
    company_branches_list = []
    company_branch_map = {}
    purchase_order_list = []
    purchase_order_map = {}
    stock_order_list = []
    stock_order_map = {}
    purchase_order_product_instances_list = []
    purchase_order_product_instance_map = {}
    stock_order_instances_list = []
    stock_order_instance_map = {}
    creator_map = {}
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        all_suppliers = Supplier.objects.all()
        all_purchase_orders = PurchaseOrder.objects.all()
        #
        staff_profile = StaffProfile.objects.get(user=active_user)
        if staff_profile.company_department.department_name == "procurement" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and company_profile:
            active_staff_profile_data = get_staff_profile_data(active_user)
            company_profile_map["company_id"] = str(company_profile.id)
            company_profile_map["company_name"] = company_profile.company_name
            company_profile_map["company_phone"] = company_profile.company_phone
            all_branches = company_profile.company_branches.all()
            for branch in all_branches:
                if branch.recycle_bin != True:
                    company_branch_map = {}
                    stock_order_list = []
                    company_branch_map["branch_id"] = str(branch.id)
                    company_branch_map["branch_name"] = branch.branch_name
                    company_branch_map["is_main_branch"] = "true" if branch.main_branch == True else "false"
                    branch_stock_orders = branch.branch_stock_orders.all()
                    for stock_order in branch_stock_orders:
                        if stock_order.recycle_bin != True:
                            stock_order_map = {}
                            stock_order_instances_list = []
                            stock_order_map["stock_order_id"] = str(stock_order.id)
                            stock_order_map["stock_order_number"] = stock_order.stock_order_number
                            stock_order_map["stock_order_approved"] = "true" if stock_order.stock_order_approved == True else "false"
                            creator_map = {}
                            creator_map["staff_id"] = str(
                                stock_order.created_by.id) if stock_order.created_by is not None else ""
                            creator_map["staff_name"] = f'{stock_order.created_by.first_name} {stock_order.created_by.last_name}' if stock_order.created_by is not None else ""
                            creator_map["staff_position"] = stock_order.created_by.staff_position.position_title if stock_order.created_by.staff_position is not None else ""
                            stock_order_map["created_by"] = creator_map
                            creator_map = {}
                            creator_map["staff_id"] = str(
                                stock_order.last_updated_by.id) if stock_order.last_updated_by is not None else ""
                            creator_map["staff_name"] = f'{stock_order.last_updated_by.first_name} {stock_order.last_updated_by.last_name}' if stock_order.last_updated_by is not None else ""
                            creator_map["staff_position"] = stock_order.last_updated_by.staff_position.position_title if stock_order.last_updated_by.staff_position is not None else ""
                            stock_order_map["last_updated_by"] = creator_map
                            stock_order_map["created_on"] = datetime.strftime(
                                stock_order.created_on, date_format) if stock_order.created_on is not None else ""
                            stock_order_map["last_updated_on"] = datetime.strftime(
                                stock_order.last_updated_on, date_format) if stock_order.last_updated_on is not None else ""
                            creator_map = {}
                            creator_map["staff_id"] = str(
                                stock_order.stock_order_approved_by.id) if stock_order.stock_order_approved_by is not None else ""
                            creator_map["staff_name"] = f'{stock_order.stock_order_approved_by.first_name} {stock_order.stock_order_approved_by.last_name}' if stock_order.stock_order_approved_by is not None else ""
                            creator_map["staff_position"] = stock_order.stock_order_approved_by.staff_position.position_title if stock_order.stock_order_approved_by.staff_position is not None else ""
                            stock_order_map["stock_order_approved_by"] = creator_map
                            stock_order_product_instances = stock_order.stock_order_product_instances.all()
                            for stock_order_product_instance in stock_order_product_instances:
                                stock_order_instance_map = {}
                                stock_order_instance_map["stock_order_product_instance_id"] = str(
                                    stock_order_product_instance.id)
                                stock_order_instance_map["stock_requisition_instance_id"] = str(
                                    stock_order_product_instance.stock_requisition_instance.id) if stock_order_product_instance.stock_requisition_instance is not None else ""
                                stock_order_instance_map["stock_order_item_delivered"] = "true" if stock_order_product_instance.stock_order_item_delivered == True else "false"
                                stock_order_instance_map["quantity_delivered"] = stock_order_product_instance.quantity_delivered
                                stock_order_instances_list.append(
                                    stock_order_instance_map)
                            stock_order_map["stock_order_instances_list"] = stock_order_instances_list
                            stock_order_list.append(stock_order_map)
                    company_branch_map["stock_order_list"] = stock_order_list
                    company_branches_list.append(company_branch_map)
            company_profile_map["company_branches_list"] = company_branches_list
            for supplier in all_suppliers:
                if supplier.recycle_bin != True:
                    supplier_map = {}
                    supplied_products_list = []
                    supplier_map["supplier_id"] = str(supplier.id)
                    supplier_map["supplier_name"] = supplier.supplier_name
                    supplier_map["supplier_phone"] = supplier.supplier_phone
                    supplier_map["supplier_email"] = supplier.supplier_email
                    supplier_map["supplier_address"] = supplier.supplier_address
                    supplier["supplier_description"] = supplier.supplier_description
                    creator_map = {}
                    creator_map["staff_id"] = str(
                        supplier.created_by.id) if supplier.created_by is not None else ""
                    creator_map["staff_name"] = f'{supplier.created_by.first_name} {supplier.created_by.last_name}' if supplier.created_by is not None else ""
                    creator_map["staff_position"] = supplier.created_by.staff_position.position_title if supplier.created_by.staff_position is not None else ""
                    supplier_map["created_by"] = creator_map
                    creator_map = {}
                    creator_map["staff_id"] = str(
                        supplier.last_updated_by.id) if supplier.last_updated_by is not None else ""
                    creator_map["staff_name"] = f'{supplier.last_updated_by.first_name} {supplier.last_updated_by.last_name}' if supplier.last_updated_by is not None else ""
                    creator_map["staff_position"] = supplier.last_updated_by.staff_position.position_title if supplier.last_updated_by.staff_position is not None else ""
                    supplier_map["last_updated_by"] = creator_map
                    supplier_map["created_on"] = datetime.strftime(
                        supplier.created_on, date_format) if supplier.created_on is not None else ""
                    supplier_map["last_updated_on"] = datetime.strftime(
                        supplier.last_updated_on, date_format) if supplier.last_updated_on is not None else ""
                    #supplied products
                    supplied_products = supplier.supplied_products.all()
                    for supplied_product in supplied_products:
                        supplied_product_map = {}
                        supplied_product_map["product_id"] = str(supplied_product.id)
                        supplied_product_map["product_name"] = supplied_product.product_name
                        supplied_products_list.append(supplied_product_map)
                    supplier_map["supplied_products_list"] = supplied_products_list
                    supplier_list.append(supplier_map)
            for purchase_order in all_purchase_orders:
                if purchase_order.recycle_bin != True:
                    purchase_order_map = {}
                    purchase_order_product_instances_list = []
                    purchase_order_map["purchase_order_id"] = str(purchase_order.id)
                    purchase_order_map["purchase_order_number"] = purchase_order.purchase_order_number
                    purchase_order_map["purchase_value_overall"] = purchase_order.purchase_value_overall
                    purchase_order_map["purchase_order_approved"] = "true" if purchase_order.purchase_order_approved == True else "false"
                    creator_map = {}
                    creator_map["staff_id"] = str(
                        purchase_order.created_by.id) if purchase_order.created_by is not None else ""
                    creator_map["staff_name"] = f'{purchase_order.created_by.first_name} {purchase_order.created_by.last_name}' if purchase_order.created_by is not None else ""
                    creator_map["staff_position"] = purchase_order.created_by.staff_position.position_title if purchase_order.created_by.staff_position is not None else ""
                    purchase_order_map["created_by"] = creator_map
                    creator_map = {}
                    creator_map["staff_id"] = str(
                        purchase_order.last_updated_by.id) if purchase_order.last_updated_by is not None else ""
                    creator_map["staff_name"] = f'{purchase_order.last_updated_by.first_name} {purchase_order.last_updated_by.last_name}' if purchase_order.last_updated_by is not None else ""
                    creator_map["staff_position"] = purchase_order.last_updated_by.staff_position.position_title if purchase_order.last_updated_by.staff_position is not None else ""
                    purchase_order_map["last_updated_by"] = creator_map
                    purchase_order_map["created_on"] = datetime.strftime(
                        purchase_order.created_on, date_format) if purchase_order.created_on is not None else ""
                    purchase_order_map["last_updated_on"] = datetime.strftime(
                        purchase_order.last_updated_on, date_format) if purchase_order.last_updated_on is not None else ""
                    creator_map = {}
                    creator_map["staff_id"] = str(
                        purchase_order.purchase_order_approved_by.id) if purchase_order.purchase_order_approved_by is not None else ""
                    creator_map["staff_name"] = f'{purchase_order.purchase_order_approved_by.first_name} {purchase_order.purchase_order_approved_by.last_name}' if purchase_order.purchase_order_approved_by is not None else ""
                    creator_map["staff_position"] = purchase_order.purchase_order_approved_by.staff_position.position_title if purchase_order.purchase_order_approved_by.staff_position is not None else ""
                    purchase_order_map["purchase_order_approved_by"] = creator_map
                    purchase_order_product_instances = purchase_order.purchase_order_product_instances.all()
                    for purchase_order_product_instance in purchase_order_product_instances:
                        if purchase_order_product_instance.recycle_bin != True:
                            purchase_order_product_instance_map = {}
                            purchase_order_product_instance_map[
                                "purchase_order_product_instance_id"] = str(purchase_order_product_instance.id)
                            purchase_order_product_instance_map["purchase_requisition_instance_id"] = str(
                                purchase_order_product_instance.purchase_order_product_instance.id) if purchase_order_product_instance.purchase_order_product_instance is not None else ""
                            purchase_order_product_instance_map["supplier_id"] = str(
                                purchase_order_product_instance.supplier.id) if purchase_order_product_instance.supplier is not None else ""
                            purchase_order_product_instance_map[
                                "purchase_value_per_unit"] = purchase_order_product_instance.purchase_value_per_unit
                            purchase_order_product_instance_map[
                                "purchase_value_overall"] = purchase_order_product_instance.purchase_value_overall
                            purchase_order_product_instance_map[
                                "purchase_amount_paid_to_supplier"] = purchase_order_product_instance.purchase_amount_paid_to_supplier
                            purchase_order_product_instance_map[
                                "supplier_payment_settled"] = "true" if purchase_order_product_instance.supplier_payment_settled == True else "false"
                            purchase_order_product_instance_map[
                                "product_purchase_delivered"] = "true" if purchase_order_product_instance.product_purchase_delivered == True else "false"
                            purchase_order_product_instance_map[
                                "quantity_delivered"] = purchase_order_product_instance.quantity_delivered
                            creator_map = {}
                            creator_map["staff_id"] = str(
                                purchase_order_product_instance.created_by.id) if purchase_order_product_instance.created_by is not None else ""
                            creator_map["staff_name"] = f'{purchase_order_product_instance.created_by.first_name} {purchase_order_product_instance.created_by.last_name}' if purchase_order_product_instance.created_by is not None else ""
                            creator_map["staff_position"] = purchase_order_product_instance.created_by.staff_position.position_title if purchase_order_product_instance.created_by.staff_position is not None else ""
                            purchase_order_product_instance_map["created_by"] = creator_map
                            creator_map = {}
                            creator_map["staff_id"] = str(
                                purchase_order_product_instance.last_updated_by.id) if purchase_order_product_instance.last_updated_by is not None else ""
                            creator_map["staff_name"] = f'{purchase_order_product_instance.last_updated_by.first_name} {purchase_order_product_instance.last_updated_by.last_name}' if purchase_order_product_instance.last_updated_by is not None else ""
                            creator_map["staff_position"] = purchase_order_product_instance.last_updated_by.staff_position.position_title if purchase_order_product_instance.last_updated_by.staff_position is not None else ""
                            purchase_order_product_instance_map["last_updated_by"] = creator_map
                            purchase_order_product_instance_map["created_on"] = datetime.strftime(
                                purchase_order_product_instance.created_on, date_format) if purchase_order_product_instance.created_on is not None else ""
                            purchase_order_product_instance_map["last_updated_on"] = datetime.strftime(
                                purchase_order_product_instance.last_updated_on, date_format) if purchase_order_product_instance.last_updated_on is not None else ""
                            purchase_order_product_instances_list.append(
                                purchase_order_product_instance_map)
                    purchase_order_map["purchase_order_product_instances_list"] = purchase_order_product_instances_list
                    purchase_order_list.append(purchase_order_map)
            payload["purchase_order_list"] = purchase_order_list
            payload["supplier_list"] = supplier_list
            payload["company_profile"] = company_profile_map
            payload["active_staff_profile_data"] = active_staff_profile_data
            return Response({"message": "true", "payload": payload}, status=200)
        else:
            return Response({"message": "false", "payload": payload}, status=401)
    except:# Exception as e:
        #print(e)
        return Response({"message": "false", "payload": payload}, status=500)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_supplier(request):
    active_user = request.user
    company_serial_number = request.data["serial_number"]
    supplier_name = request.data["supplier_name"]
    supplier_phone = request.data["supplier_phone"]
    supplier_email = request.data["supplier_email"]
    supplier_address = request.data["supplier_address"]
    supplied_products_id_list = request.data.get('supplied_products_id_list', [])
    supplied_products_id_list = json.loads(supplied_products_id_list)
    supplier_description = request.data["supplier_description"]
    product_ids_list = []
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=active_user)
        if staff_profile.company_department.department_name == "procurement" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and staff_profile.company_branch.main_branch == True and company_profile:
            serializers = UserSerializer(
                data={'username': supplier_email, 'password': supplier_phone})
            if serializers.is_valid():
                user = serializers.save()
                new_user = authenticate(
                    username=supplier_email, password=supplier_phone)
                for product_id in supplied_products_id_list:
                    product_ids_list.append(int(product_id))
                supplier_serializer = SupplierSerializer(
                    data={'user': new_user.id, 'company_profile': company_profile.id, 'supplier_name': supplier_name, 'supplier_phone': supplier_phone, 'supplier_email': supplier_email, 'supplier_address': supplier_address, 'supplier_description': supplier_description, 'supplied_products': product_ids_list, 'created_by': staff_profile.id,'last_updated_by':staff_profile.id})
                if supplier_serializer.is_valid():
                    supplier_serializer.save()
                    return Response({"message": "Supplier account created successfully",}, status=200)
                else:
                    return Response({"message": "Unable to create supplier account", }, status=406)
            else:
                return Response({"message": "Unable to create supplier account", }, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this action",}, status=401)
    except:  # Exception as e:
        # print(e)
        return Response({"message": "Error creating supplier account",}, status=500)
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_purchase_order(request):
    active_user = request.user
    company_serial_number = request.data["serial_number"]
    purchase_value_overall = 0.00
    purchase_order_instance_list = request.data.get(
        'purchase_order_instance_list', [])
    purchase_order_instance_list = json.loads(purchase_order_instance_list)
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=active_user)
        if staff_profile.company_department.department_name == "procurement" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and staff_profile.company_branch.main_branch == True and company_profile:
            purchase_order_serializer = purchaseOrderSerializer(
                data={'purchase_value_overall': str(purchase_value_overall),'created_by':staff_profile.id,'last_updated_by':staff_profile.id})
            if purchase_order_serializer.is_valid():
                new_purchase_order = purchase_order_serializer.save()
                #processing purchase order instance list
                for purchase_order_instance in purchase_order_instance_list:
                    purchase_requisition_instance_id = int(purchase_order_instance[
                        "purchase_requisition_instance_id"])
                    supplier_id = purchase_order_instance["supplier_id"]
                    purchase_value_per_unit = purchase_order_instance["purchase_value_per_unit"]
                    purchase_instance_value_overall = purchase_order_instance["purchase_value_overall"]
                    purchase_amount_paid_to_supplier = purchase_order_instance[
                        "purchase_amount_paid_to_supplier"]
                    supplier_payment_settled = True if purchase_order_instance["supplier_payment_settled"] == "true" else False
                    product_purchase_delivered = True if purchase_order_instance["product_purchase_delivered"] == "true" else False
                    quantity_delivered = purchase_order_instance["quantity_delivered"]
                    quantity_purchased = purchase_order_instance["quantity_purchased"]
                    purchase_order_instance_serializer = productPurchaseInstanceSerializer(data={
                                                                                           'purchase_order': new_purchase_order.id, 'purchase_requisition_instance': purchase_requisition_instance_id, 'supplier': supplier_id, 'purchase_value_per_unit': purchase_value_per_unit, 'purchase_value_overall': purchase_instance_value_overall, 'purchase_amount_paid_to_supplier': purchase_amount_paid_to_supplier, 'supplier_payment_settled': supplier_payment_settled, 'product_purchase_delivered': product_purchase_delivered, 'quantity_delivered': quantity_delivered, 'quantity_purchased': quantity_purchased, 'created_by': staff_profile.id, 'last_updated_by': staff_profile.id})
                    if purchase_order_instance_serializer.is_valid():
                        purchase_order_instance_serializer.save()
                        purchase_value_overall += float(
                            purchase_instance_value_overall)
                new_purchase_order.purchase_value_overall = str(purchase_value_overall)
                new_purchase_order.save()
                return Response({"message": "Purchase order created successfully", }, status=200)
            else:
                return Response({"message": "Unable to create purchase order", }, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this action", }, status=401)
    except:
        return Response({"message": "Error creating purchase order", }, status=500)
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_stock_order(request):
    active_user = request.user
    company_serial_number = request.data["serial_number"]
    stock_order_instance_list = request.data.get(
        'stock_order_instance_list', [])
    stock_order_instance_list = json.loads(stock_order_instance_list)
    company_branch_id = int(request.data["company_branch_id"])
    try:
        company_profile = CompanyProfile.objects.get(
            company_serial_number=company_serial_number)
        staff_profile = StaffProfile.objects.get(user=active_user)
        if staff_profile.company_department.department_name == "procurement" and staff_profile.is_head_of_department == True and staff_profile.has_read_write_priviledges == True and staff_profile.company_branch.main_branch != True and company_profile:
            stock_order_serializer = stockOrderSerializer(data={
                'company_branch': company_branch_id,
                'created_by':staff_profile.id,
                'last_updated_by': staff_profile.id,
            })
            if stock_order_serializer.is_valid():
                new_stock_order = stock_order_serializer.save()
                for stock_order_instance in stock_order_instance_list:
                    stock_requisition_instance_id = int(
                        stock_order_instance_list["stock_requisition_instance"])
                    stock_order_item_delivered = True if stock_order_instance_list[
                        "stock_order_item_delivered"] == "true" else False
                    quantity_ordered = stock_order_instance_list["quantity_ordered"]
                    quantity_delivered = stock_order_instance_list["quantity_delivered"]
                    stock_order_instance_serializer = stockOrderInstanceSerializer(
                        data={'stock_order': new_stock_order.id, 'stock_requisition_instance': stock_requisition_instance_id, 'stock_order_item_delivered': stock_order_item_delivered, 'quantity_ordered': quantity_ordered, 'quantity_delivered': quantity_delivered, 'created_by': staff_profile.id,
                              'last_updated_by': staff_profile.id,})
                    if stock_order_instance_serializer.is_valid():
                        stock_order_instance_serializer.save()
                return Response({"message": "Stock order created successfully", }, status=200)
            else:
                return Response({"message": "Unable to create stock order", }, status=406)
        else:
            return Response({"message": "You are unauthorised to perform this action", }, status=401)
    except:
        return Response({"message": "Error creating stock order", }, status=500)

    
