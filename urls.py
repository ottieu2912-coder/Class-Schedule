"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import urls
from django.contrib import admin
from django.urls import path, include
from .apiviews import Schedule, createSchedule, getUser, Delete
from rest_framework.routers import DefaultRouter
from .viewset import ClassScheduleView
from . import views
#Prepare the access and refresh tokens to authenticate the username and password when the user logs in
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

#A route for frontend to receive API about schedules that the logged in user created
router = DefaultRouter()
router.register(r'schedule', ClassScheduleView, basename='class')

#Urls to send API or retrieve data from the frontend
urlpatterns = [
    path('api/', Schedule.as_view(), name="view-api"),
    path('login/', TokenObtainPairView.as_view(), name="login"),
    path('api/refresh/', TokenRefreshView.as_view(), name="refresh"),
    path('api/classSchedule/', include(router.urls)),
    path('api/createSchedule/', createSchedule.as_view(), name="createSchedule"),
    path('delete/', Delete.as_view(), name="delete"),
    path('getUser/', getUser.as_view(), name="getUser")
]
