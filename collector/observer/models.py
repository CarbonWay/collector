from django.db import models
from loader.models import Device, DataFile

# Create your models here.
class ObserverDat(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    def __str__(self):
        return f"Observer: {self.device.id} {self.device.name}"
