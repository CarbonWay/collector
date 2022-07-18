from django.contrib import admin
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from django.http import HttpResponse, Http404
import os
from django.conf import settings
from loader.models import *

import os
import zipfile
from io import BytesIO


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

    actions = ['download_file']

    def download_file(self, request, queryset):

        filenames = []

        for query in queryset:
            file_path = os.path.join(settings.MEDIA_ROOT, str(query.file))
            filenames.append(file_path)

        zip_subdir = "export"
        zip_filename = "%s.zip" % zip_subdir
        s = BytesIO()
        zf = zipfile.ZipFile(s, "w")

        for fpath in filenames:
            fdir, fname = os.path.split(fpath)
            zip_path = os.path.join(zip_subdir, fname)
            zf.write(fpath, zip_path)

        zf.close()

        resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
        resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

        return resp
    download_file.short_description = "Download CSV file for selected files"

    def view_device_link(self, obj):
        url = (
            reverse("admin:loader_device_changelist")
            + "?"
            + urlencode({"devices__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{}</a>', url, obj.device.name)

    view_device_link.short_description = "Device"