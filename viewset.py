from .serializers import ClassScheduleSerializer
from .models import ClassSchedule
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

#Send the data about a student's schedules through API
class ClassScheduleView(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ClassScheduleSerializer

    def get_queryset(self):
        queryset = ClassSchedule.objects.filter(student=self.request.user.username)

        return queryset