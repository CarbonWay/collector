from django.contrib import admin
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from django.http import HttpResponse, Http404
import os
from django.conf import settings
from loader.models import *
import pandas as pd

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

    actions = ['download_file', 'download_csv_file', 'download_ghg_csv_file']

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
    download_file.short_description = "Download zip archive with selected files"


    def download_csv_file(self, request, queryset):
        print(queryset[0].device)
        print(dir(queryset[0].device))

        df = pd.DataFrame()

        for query in queryset:
            try:
                file_path = os.path.join(settings.MEDIA_ROOT, str(query.file))
                temp_df = pd.read_csv(file_path, sep="\s+")
                df = pd.concat([df, temp_df], axis=0)
            except Exception as e:
                print(e)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=export.csv'  # alter as needed
        df.to_csv(path_or_buf=response)  # with other applicable parameters
        return response


    def download_ghg_csv_file(self, request, queryset):
        df = pd.DataFrame()
        for query in queryset:
            try:
                file_path = os.path.join(settings.MEDIA_ROOT, str(query.file))

                archive = zipfile.ZipFile(file_path, 'r')
                data_filename = ''
                for name in archive.filelist:
                    if name.filename.endswith('.data'):
                        data_filename = name.filename
                        break
                file = archive.read(data_filename)
                file_list = str(file).split(r'\n')
                timezone = file_list[6].replace('Timezone:\\t', '')

                temp_df = pd.read_csv(BytesIO(file), skiprows=7, delimiter='\t')
                df = pd.concat([df, temp_df], axis=0)
            except Exception as e:
                print(e)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=export.csv'  # alter as needed
        df.to_csv(path_or_buf=response)  # with other applicable parameters
        return response



    def view_device_link(self, obj):
        url = (
            reverse("admin:loader_device_changelist")
            + "?"
            + urlencode({"devices__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{}</a>', url, obj.device.name)

    view_device_link.short_description = "Device"