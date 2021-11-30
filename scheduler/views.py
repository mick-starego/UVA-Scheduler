from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import os
import json
from django.views.decorators.csrf import csrf_exempt
from copy import copy
from typing import List

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

    return JsonResponse({"allClasses": [vars(c) for c in uva_classes], "schedules": [{"classes": [vars(c) for c in s.classes]} for s in schedules]})


def generate_schedules(uva_classes: List[UVAClass]):
    uva_classes.sort(key=lambda x: x.class_num)
    viable_schedules = []
    generate_schedules_helper(uva_classes, viable_schedules, UVASchedule())
    viable_schedules.sort(key=lambda x: len(x.classes), reverse=True)
    return viable_schedules


def generate_schedules_helper(class_list, collector, current):
    for c in class_list:
        if c.class_num > current.get_max_class_num() and c.days != 'TBA':
            if not current.push_class(c):
                continue
            num_credits = sum([int(c.units) for c in current.classes if c.units.isnumeric()])
            if 15 <= num_credits <= 18:
                collector.append(copy(current))
            generate_schedules_helper(class_list, collector, current)
            current.pop_class()
