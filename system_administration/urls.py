from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('get-admin-creation-status/', views.get_admin_creation_status),
    path('validate-serial-number/', views.validate_serial_number),
    path('create-system-admin/', views.create_system_admin),
    path('staff-login/', views.staff_login),
    path('system-admin-dashboard/', views.system_admin_dashboard),
    path('edit-company-profile/', views.edit_company_profile),
    path('edit-company-branch/', views.edit_company_branch),
    path('create-super-hr-user/', views.create_super_hr_user),
    path('create-other-staff-user/', views.create_other_staff_user),
]