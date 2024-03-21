from django.contrib import admin

from warehouse_management.models import Category, StockTransaction, StockTransactionInstance

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(StockTransactionInstance)
class StockTransactionInstanceAdmin(admin.ModelAdmin):
    list_display = ('id',)
