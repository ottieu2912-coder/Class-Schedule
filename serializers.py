from rest_framework.serializers import ModelSerializer
from .models import ClassSchedule

#Serialize the class schedule model for API to be processed
class ClassScheduleSerializer(ModelSerializer):
	class Meta:
		model = ClassSchedule
		fields = "__all__"