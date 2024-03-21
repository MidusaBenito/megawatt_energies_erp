from django.contrib import admin

from human_resource.models import Bonus, BonusInstance, Deduction, DeductionInstance, PayrollSheet, StaffBonusScheme, StaffDeductionScheme, StaffLeave, StaffPayrollInstance, StaffProfile, TimeSheet, WorkShift, WorkingDays, staffPosition

# Register your models here.


@admin.register(StaffProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('staff_number',)


@admin.register(staffPosition)
class staffPositionAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(WorkShift)
class WorkShiftAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(WorkingDays)
class WorkingDaysAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(StaffLeave)
class StaffLeaveAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(TimeSheet)
class TimeSheetAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(Bonus)
class BonusAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(Deduction)
class DeductionAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(PayrollSheet)
class PayrollSheetAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(StaffDeductionScheme)
class StaffDeductionSchemeAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(StaffBonusScheme)
class StaffBonusSchemeSchemeAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(StaffPayrollInstance)
class StaffPayrollInstanceAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(DeductionInstance)
class DeductionInstanceAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(BonusInstance)
class BonusInstanceAdmin(admin.ModelAdmin):
    list_display = ('id',)
