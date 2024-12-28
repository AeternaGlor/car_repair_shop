from django.contrib import admin
from .models import Customer, Order, Box, TimeSlot, Master, Service


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Box)
class BoxModelAdmin(admin.ModelAdmin):
    pass


@admin.register(TimeSlot)
class TimeSlotModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Master)
class MasterModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Service)
class ServiceModelAdmin(admin.ModelAdmin):
    pass
