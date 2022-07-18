from django.contrib import admin
from observer.models import ObserverDat

class ObserverDatAdmin(admin.ModelAdmin):
    # list_display = ('Device',)
    # list_filter = ('Device',)
    # search_fields = ('Device')
    pass

admin.site.register(ObserverDat, ObserverDatAdmin)
