from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('create-warehouse/', views.create_warehouse),
    path('add-equipment/', views.add_equipment),
    path('add-product-categories/', views.add_product_categories),
    path('warehouse-management-dashboard/',
         views.warehouse_management_dashboard),
    path('add-product/', views.add_product),
    path('add-stock-transaction/', views.add_stock_transaction),
    path('add-purchase-requisition/',views.add_purchase_requisition),
    path('add-stock-requisition/', views.add_stock_requisition),
]
