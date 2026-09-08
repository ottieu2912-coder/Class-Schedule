from django.shortcuts import render
from server.createSchedule import courses, className, classSchedule
from .models import ClassSchedule
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import json

#A basic view for the creation of schedule without API
@csrf_exempt
def createSchedule(request):
    c = {}
    points = [0, 0, 0]
    schedule = [[], [], []]
    data = json.loads(request.body)
    print(data)
    

    for item in data.get('classes'):
        c[className[item]] = courses[className[item]]
    while c:
        course = next(iter(c))
        classSchedule(c, schedule, course, points)
    newSchedule = ClassSchedule.objects.create(student=User.objects.get(username=request.data['student']), name=request.data['title'], schedule=schedule)
    schedule = ClassSchedule.objects.create()
    return Response(schedule)

# Create your views here.
