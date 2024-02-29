from rest_framework.serializers import ModelSerializer
from .models import *


class staffPositionSerializer(ModelSerializer):
    class Meta:
        model = staffPosition
        fields = '__all__'


class StaffProfileSerializer(ModelSerializer):
    class Meta:
        model = StaffProfile
        fields = '__all__'


class BonusSerializer(ModelSerializer):
    class Meta:
        model = Bonus
        fields = '__all__'


class DeductionSerializer(ModelSerializer):
    class Meta:
        model = Deduction
        fields = '__all__'


class WorkShiftSerializer(ModelSerializer):
    class Meta:
        model = WorkShift
        fields = '__all__'


class WorkingDaysSerializer(ModelSerializer):
    class Meta:
        model = WorkingDays
        fields = '__all__'


class StaffLeaveSerializer(ModelSerializer):
    class Meta:
        model = StaffLeave
        fields = '__all__'


class Educational_QualificationSerializer(ModelSerializer):
    class Meta:
        model = Educational_Qualification
        fields = '__all__'


class Training_RecordSerializer(ModelSerializer):
    class Meta:
        model = Training_Record
        fields = '__all__'


class Disciplinary_RecordSerializer(ModelSerializer):
    class Meta:
        model = Disciplinary_Record
        fields = '__all__'


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class EngagementSerializer(ModelSerializer):
    class Meta:
        model = Engagement
        fields = '__all__'


class VacancyRecordSerializer(ModelSerializer):
    class Meta:
        model = VacancyRecord
        fields = '__all__'


class VacantPositionRequirementSerializer(ModelSerializer):
    class Meta:
        model = VacantPositionRequirement
        fields = '__all__'


class JobApplicationSerializer(ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'


class StaffBonusSchemeSerializer(ModelSerializer):
    class Meta:
        model = StaffBonusScheme
        fields = '__all__'


class StaffDeductionSchemeSerializer(ModelSerializer):
    class Meta:
        model = StaffDeductionScheme
        fields = '__all__'


class PayrollSheetSerializer(ModelSerializer):
    class Meta:
        model = PayrollSheet
        fields = '__all__'


class BonusInstanceSerializer(ModelSerializer):
    class Meta:
        model = BonusInstance
        fields = '__all__'


class DeductionInstanceSerializer(ModelSerializer):
    class Meta:
        model = DeductionInstance
        fields = '__all__'


class StaffPayrollInstanceSerializer(ModelSerializer):
    class Meta:
        model = StaffPayrollInstance
        fields = '__all__'
