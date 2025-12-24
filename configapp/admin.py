from django.contrib import admin
from .models import Employee, Client, Product, Order, OrderItem


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'birth_date', 'hired_at')
    search_fields = ('full_name',)
    list_filter = ('hired_at',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'birth_date', 'created_at')
    search_fields = ('full_name',)
    list_filter = ('created_at',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    search_fields = ('name',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'employee', 'created_at', 'get_total_price')

    def get_total_price(self, obj):
        return obj.total_price

    get_total_price.short_description = "Total price"