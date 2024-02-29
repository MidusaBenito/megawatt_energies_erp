from django.contrib import admin

from system_administration.models import CompanyBranch, CompanyDepartment, CompanyProfile

# Register your models here.


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'company_serial_number',
                    'company_postal_address', 'company_country_location')
    
@admin.register(CompanyDepartment)
class CompanyDepartmentAdmin(admin.ModelAdmin):
    list_display = ('id','department_name',)


@admin.register(CompanyBranch)
class CompanyBranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'branch_name',)



