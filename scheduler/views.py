from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import json
from django.views.decorators.csrf import csrf_exempt
from scheduler.utils.UVAClass import UVAClass
from scheduler.utils.schedule_generator import generate_schedules


def index(request):
    return render(request, 'scheduler/index.html')


def get_course_data(request):
    df = pd.read_csv('https://raw.githubusercontent.com/mick-starego/dummy-repo/master/dummy-repo/course-data.csv')[["ClassNumber", "Mnemonic", "Number", "Section", "Days", "Title", "Instructor(s)", "Units"]]
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

    return JsonResponse({"allClasses": [vars(c) for c in uva_classes], "schedules": [{"classes": [vars(c) for c in s.classes]} for s in schedules]})

