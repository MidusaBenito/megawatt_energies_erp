from rest_framework.serializers import ModelSerializer
from .models import *


class SupplierSerializer(ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class purchaseOrderSerializer(ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class productPurchaseInstanceSerializer(ModelSerializer):
    class Meta:
        model = ProductPurchaseInstance
        fields = '__all__'


class stockOrderSerializer(ModelSerializer):
    class Meta:
        model = StockOrder
        fields = '__all__'


class stockOrderInstanceSerializer(ModelSerializer):
    class Meta:
        model = StockOrderInstance
        fields = '__all__'
