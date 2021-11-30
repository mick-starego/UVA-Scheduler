from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import os


def index(request):
    return render(request, 'scheduler/index.html')


def get_course_data(request):
    df = pd.read_csv(os.path.join(settings.STATIC_ROOT, 'external/course-data.csv'))[["ClassNumber", "Mnemonic", "Number", "Section", "Title", "Instructor(s)", "Units"]]
    df.set_index("ClassNumber", drop=True, inplace=True)
    df_as_dict = df.to_dict(orient="index")
    return JsonResponse({'courses': [v for v in df_as_dict.values()]})
