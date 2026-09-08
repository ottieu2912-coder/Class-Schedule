import math
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from server.createSchedule import classSchedule, Course
import json
from .models import ClassSchedule
from. serializers import ClassScheduleSerializer

#Create a list of classes with necessary information about their prerequisites, corequisites, and their potential future classes
Physics7C = Course("Classical Physics I")
Physics7D = Course("Classical Physics II")
Physics7E = Course("Classical Physics III")
Math3A = Course("Linear Algebra")
ICS31 = Course("Intro to Programming")
Math2D = Course("Multivariable Calc. I")
Math2E = Course("Multivariable Calc. II")
Writing50 = Course("Basic Writing")
Writing61 = Course("Argumentative Writing")
Physics7C.Addfu(Physics7D)
Physics7D.Addpre(Physics7C)
Physics7D.Addco(Math2D)
Physics7E.Addpre(Physics7D)
Physics7D.Addfu(Physics7E)
Math2D.Addfu(Math2E)
Math2E.Addpre(Math2D)
Writing50.Addfu(Writing61)
Writing61.Addpre(Writing50)

#Create a dictionary for backend to identify the courses based on the name and another dictionary to rate their difficulty and optimize the balance of difficulty for every quarter in a year
className = {"Classical Physics I": Physics7C, "Classical Physics II": Physics7D, "Classical Physics III": Physics7E, "Multivariable Calc. I": Math2D, "Linear Algebra": Math3A, "Multivariable Calc. II": Math2E, "Basic Writing": Writing50, "Argumentative Writing": Writing61, "Programming": ICS31}
courses = {Physics7C: 2, Physics7D: 3, Physics7E: 2, Math3A: 2, Math2D: 3, Math2E: 3, Writing50: 1, Writing61: 2, ICS31: 1}

#Test API transfer between the frontend and the backend
class Schedule(APIView):
	permission_classes = [AllowAny]
	def post(self, request):
		return Response({'Data': 'Success'})

"""
Login and Register API based on username instead of authentication
class Login(APIView):
	permission_classes = [AllowAny]
	def post(self, request):
		user = User.objects.get(username=request.data['username'])
		if not user.check_password(request.data['password']): return Response({"Valid": "Wrong password"})
		user = authenticate(request, username=request.data['username'], password=request.data['password'])
		if user is not None: login(request, user)
		return Response({"Valid": "Login Success"})

class Register(APIView):
	permission_classes = [AllowAny]
	def post(self, request):
		email = request.data['email']
		username = request.data['username']
		password = request.data['password']
		if User.objects.filter(username=username): return Response({'Valid': 'This username is already taken'})
		user = User.objects.create(username=username, password=password, email=email)
		user = authenticate(request, username=request.data['username'], password=request.data['password']) 
		if user is not None: login(request, user)
		return Response({'Valid': 'Registration Success'})
"""

#Use the algorithm for schedule creation
class createSchedule(APIView):
	permission_classes = [IsAuthenticated]
	def post(self, request):
		if ClassSchedule.objects.filter(student=request.user.username, name=request.data['title']): return Response({"Validity": "This name is already taken"})
		c = {}
		points = [0, 0, 0]
		schedule = [[], [], []]
		data = json.loads(request.body)
		
		for item in data.get('classes'):
			c[className[item]] = courses[className[item]]
			for co in className[item].corequisite:
				c[co] = courses[co]
		c = dict(sorted(c.items(), key=lambda item: item[1]))
		while c:
			course = next(iter(c))
			classSchedule(c, schedule, course, points)
		newSchedule = ClassSchedule.objects.create(student=request.user.username, name=request.data['title'], schedule=schedule)		
		return Response(schedule)

#Delete Schedule
class Delete(APIView):
	permission_classes = [AllowAny]
	def post(self, request):
		schedule = ClassSchedule.objects.filter(student=request.user.username, name=request.data['name'])
		schedule.delete()
		return HttpResponse("")

#Get user's information after logging in
class getUser(APIView):
	permission_classes = [IsAuthenticated]
	def get(self, request):
		return Response({
			'username': request.user.username,
			'email': request.user.email
			})