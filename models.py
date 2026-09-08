from asyncio.windows_events import NULL
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#A class schedule model with a title(name) and the student's name along with a json file that contains the data about the contents for the frontend to display
class ClassSchedule(models.Model):
    student = models.CharField(default='')
    name = models.CharField()
    schedule = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name

