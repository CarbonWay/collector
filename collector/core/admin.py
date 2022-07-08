from django.contrib import admin
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from loader.models import *

# Register your models here.

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("name", "description", 'map_link', 'token')

    def map_link(self, obj):
        url = "https://www.google.com/maps/place/" + obj.location
        return format_html('<a href="{}" target="_blank">{}</a>', url, obj.location)

    map_link.short_description = "Map"


@admin.register(DataFile)
class DataFileAdmin(admin.ModelAdmin):
    list_display = ("file", 'date', 'view_device_link')
    list_filter = ("date",)
    search_fields = ("date", 'file')

    def view_device_link(self, obj):
        url = (
            reverse("admin:loader_device_changelist")
            + "?"
            + urlencode({"devices__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{}</a>', url, obj.device.name)

    view_device_link.short_description = "Device"