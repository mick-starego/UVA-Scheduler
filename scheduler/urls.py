from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('data', views.get_course_data, name='get_data')
]
