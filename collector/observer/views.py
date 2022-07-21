from django.shortcuts import render, get_object_or_404
from loader.models import DataFile, Device
from django.http import JsonResponse
import json
import pandas as pd
from django.conf import settings
import os
import zipfile
from io import BytesIO

# Create your views here.


def get_full_data(request):
    devices = Device.objects.filter().all()

    export = {}

    for device in devices:
        device_datafiles = device.datafile_set.values()
        output = parse_device_data(device_datafiles)
        export[str(device.name)] = json.loads(json.dumps(list(output.T.to_dict().values())))

    return JsonResponse(export)


def get_mean_data(request):
    devices = Device.objects.filter().all()
    export = {}


    for device in devices:
        device_datafiles = device.datafile_set.values()
        output = parse_device_data(device_datafiles)
        output = get_mean_df(output)
        # output['datetime'] = output['datetime'].dt.strftime('%Y-%m-%d')
        # output['datetime'] = output['datetime'].astype(str)
        export[str(device.name)] = json.loads(json.dumps(list(output.T.to_dict().values())))

    return JsonResponse(export)


def get_mean_df(df, delta_time = 'H'): # M - minutes

    df['datetime'] = df['date'] + ' ' + df['time']

    try:
        df["datetime"] = pd.to_datetime(df["datetime"], format="%Y-%m-%d %H:%M:%S:%f")
    except ValueError:
        df["datetime"] = pd.to_datetime(df["datetime"], format="%Y-%m-%d %H:%M:%S.%f")

    df['newDateTime'] = df['datetime']
    df.index = df['newDateTime']
    df_p = df.resample(delta_time).mean()
    # df_p['Month'] = df['newDateTime'].dt.month.astype(str)
    # df_p['Year'] = df['newDateTime'].dt.year.astype(str)
    # df_p['Date'] = df['newDateTime'].dt.day.astype(str)
    # df_p['Hour'] = df['newDateTime'].dt.hour.astype(str)
    # df_p['Minute'] = df['newDateTime'].dt.minute.astype(str)
    # df_p['Second'] = df['newDateTime'].dt.second.astype(str)

    return df_p.iloc[:, :]




def parse_device_data(datafiles):
    output = pd.DataFrame()

    if '.' in str(datafiles[0]['file']):
        extension = str(datafiles[0]['file']).split('.')[-1]
    else:
        return output

    if extension == 'dat':
        output = parse_dat_files(datafiles)

    elif extension == 'ghg':
        output = parse_ghg_files(datafiles)

    output.columns= output.columns.str.lower()

    return output


def parse_dat_files(datafiles):
    df = pd.DataFrame()
    for datafile in datafiles:
        try:
            filename = datafile['file']
            file_path = os.path.join(settings.MEDIA_ROOT, str(filename))
            temp_df = pd.read_csv(file_path, sep="\s+")
            df = pd.concat([df, temp_df], axis=0)
        except Exception as e:
            print(e)
    # json_list = json.loads(json.dumps(list(df.T.to_dict().values())))
    return df


def parse_ghg_files(datafiles):
    df = pd.DataFrame()
    for datafile in datafiles:
        try:
            filename = datafile['file']
            file_path = os.path.join(settings.MEDIA_ROOT, str(filename))

            archive = zipfile.ZipFile(file_path, 'r')
            data_filename = ''
            for name in archive.filelist:
                if name.filename.endswith('.data'):
                    data_filename = name.filename
                    break
            file = archive.read(data_filename)
            file_list = str(file).split(r'\n')
            # timezone = file_list[6].replace('Timezone:\\t', '')

            temp_df = pd.read_csv(BytesIO(file), skiprows=7, delimiter='\t')
            df = pd.concat([df, temp_df], axis=0)
        except Exception as e:
            print(e)

    # json_list = json.loads(json.dumps(list(df.T.to_dict().values())))
    return df


