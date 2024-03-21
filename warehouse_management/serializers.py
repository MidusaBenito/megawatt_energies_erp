from rest_framework.serializers import ModelSerializer
from .models import *


class WarehouseSerializer(ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class InventorySerializer(ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'


class StockTransactionSerializer(ModelSerializer):
    class Meta:
        model = StockTransaction
        fields = '__all__'


class StockTransactionInstanceSerializer(ModelSerializer):
    class Meta:
        model = StockTransactionInstance
        fields = '__all__'


class EquipmentSerializer(ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'


class PurchaseRequisitionSerializer(ModelSerializer):
    class Meta:
        model = PurchaseRequisition
        fields = '__all__'


class PurchaseRequisitionInstanceSerializer(ModelSerializer):
    class Meta:
        model = PurchaseRequisitionInstance
        fields = '__all__'


class StockRequisitionSerializer(ModelSerializer):
    class Meta:
        model = StockRequisition
        fields = '__all__'


class StockRequisitionInstanceSerializer(ModelSerializer):
    class Meta:
        model = StockRequisitionInstance
        fields = '__all__'


