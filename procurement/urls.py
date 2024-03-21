from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # path('get-admin-creation-status/', views.get_admin_creation_status),
    path('procurement-dashboard/', views.procurement_dashboard),
    path('create-supplier/', views.create_supplier),
    path('create-purchase-order/', views.create_purchase_order),
    path('create-stock-order/', views.create_stock_order),
]
