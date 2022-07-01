from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import DataFile, Device
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return HttpResponse("This is the page for uploading data files")

@csrf_exempt
def upload(request):
    if request.method == 'POST':
        print('_____________________________________________')
        data = request.POST
        print('*****', data)


        deveice_id = data.get('device', '')

        token_sent = data.get('token', '')

        date = data.get('date', '')

        # device = Device.objects.filter(id=deveice_id).first()

        device = get_object_or_404(Device, pk=deveice_id)

        if token_sent != device.token:
            return JsonResponse({'status':'token error'})

        file = request.FILES['file']

        dataFile = DataFile(device=device, file=file, date=date)
        dataFile.save()

        return JsonResponse({'status':'success'})
    return HttpResponse("This is the page for uploading data files")
