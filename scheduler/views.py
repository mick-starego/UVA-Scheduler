from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import os
import json
from django.views.decorators.csrf import csrf_exempt

from scheduler.utils import UVAClass, UVASchedule


def index(request):
    return render(request, 'scheduler/index.html')


def get_course_data(request):
    df = pd.read_csv(os.path.join(settings.STATIC_ROOT, 'external/course-data.csv'))[["ClassNumber", "Mnemonic", "Number", "Section", "Days", "Title", "Instructor(s)", "Units"]]
    df.set_index("ClassNumber", drop=False, inplace=True)
    df_as_dict = df.to_dict(orient="index")
    return JsonResponse({'courses': [v for v in df_as_dict.values()]})


@csrf_exempt
def get_possible_schedules(request):
    uva_classes = []
    for c in json.loads(request.POST.get('classesSelected')):
        uva_classes.append(UVAClass(c['ClassNumber'], c['Mnemonic'] + " " + str(c['Number']) + "-" + str(c['Section']), c['Days'], c['Units']))

    # Generate schedules
    schedules = generate_schedules(uva_classes)

    return JsonResponse({"schedules": [{"classes": [vars(c) for c in s.classes]} for s in schedules]})


def generate_schedules(uva_classes):
    # TODO
    # For now, this returns a singleton list of a schedule that contains all
    # classes passed as input. When implemented, this method will generate a list
    # of all schedules that meet the constraints listed in the UVASchedule docstring.
    creds=0
    temp=[]
    schedules=[]
    for i in uva_classes:
        if(creds < 18 and creds+int(i.units)<=18):
            temp.append(i)
            creds+=int(i.units)
            #print(creds)
            #print(temp)  
        if(creds<18 and creds>=15):
            #print(1)
            #print(creds)
            #print(temp)
            schedules.append(UVASchedule(temp))
         
        elif(creds==18):
            #print(2)
            schedules.append(UVASchedule(temp))

    #print(len(schedules))
    #for j in schedules:
        #print(j)
        #print("new")
    return schedules #[UVASchedule(uva_classes)]

