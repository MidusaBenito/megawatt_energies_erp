from rest_framework.serializers import ModelSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import *


class UserSerializer(ModelSerializer): #user model is already serialized here, not to be serialized anywhere else
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {"write_only": True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user
    

class CompanyProfileSerializer(ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = '__all__'


class CompanyBranchSerializer(ModelSerializer):
    class Meta:
        model = CompanyBranch
        fields = '__all__'


class CompanyDepartmentSerializer(ModelSerializer):
    class Meta:
        model = CompanyDepartment
        fields = '__all__'


class SystemAdminCreationStatusSerializer(ModelSerializer):
    class Meta:
        model = SystemAdminCreationStatus
        fields = '__all__'
