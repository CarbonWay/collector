from lib2to3.pgen2 import token
from pydoc import describe
from django.db import models
from django.utils import timezone
import datetime
import secrets

class Device(models.Model):
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=2000)
    location = models.CharField(max_length=2000, default='-1')
    token = models.CharField(max_length=512, default=secrets.token_urlsafe())

    def __str__(self):
        return f"Device: {self.name}, location: {self.location}, description: {self.description}, pk: {self.pk}"


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'device_{0}_{1}/{2}/{3}'.format(instance.device.id, instance.device.name, datetime.date.today().isoformat(), filename)


class DataFile(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Device: {self.device.id} {self.device.name}, date: {self.date} file: {self.file}"
