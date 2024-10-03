import datetime

from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ScheduledClass
from .pagination import SmallSetPagination
from .serializers import ScheduledClassSerializer
from .utils import get_double_booked_by_user
from user_profiles.models import UserProfile
from utilities.permissions import IsOwnerOrReadOnly


class ScheduledClassViewSet(viewsets.ModelViewSet):
    permission_classes = (
        #IsAuthenticated, #IsOwnerOrReadOnly
    )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        date = serializer.validated_data['date']
        start_time = serializer.validated_data['start_time']
        finish_time = serializer.validated_data['finish_time']
        booked_teacher = serializer.validated_data['teacher']
        booked_student = serializer.validated_data['student_or_class']
        obj_id = None
        concurrent_booked_classes = (
            ScheduledClass.custom_query.already_booked_classes_during_date_and_time(
                query_date=date,
                starting_time=start_time,
                finishing_time=finish_time
            )
        )
        unavailable_teachers = get_double_booked_by_user(
            obj_id=obj_id,
            student_or_teacher='teacher',
            queried_user=booked_teacher,
            concurrent_booked_classes=concurrent_booked_classes
        )
        unavailable_students = get_double_booked_by_user(
            obj_id=obj_id,
            student_or_teacher='student',
            queried_user=booked_student,
            concurrent_booked_classes=concurrent_booked_classes
        )
        if booked_teacher in unavailable_teachers:
            return Response(
                {"Error": "The teacher is unavailable for this time frame!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif booked_student in unavailable_students:
            return Response(
                {"Error": "The student is unavailable for this time frame!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        date = serializer.validated_data['date']
        start_time = serializer.validated_data['start_time']
        finish_time = serializer.validated_data['finish_time']
        booked_teacher = serializer.validated_data['teacher']
        booked_student = serializer.validated_data['student_or_class']
        obj_id = instance.id
        concurrent_booked_classes = (
            ScheduledClass.
            custom_query.already_booked_classes_during_date_and_time(
                        query_date=date,
                        starting_time=start_time,
                        finishing_time=finish_time
            )
        )
        unavailable_teachers = get_double_booked_by_user(
            obj_id=obj_id,
            student_or_teacher='teacher',
            queried_user=booked_teacher,
            concurrent_booked_classes=concurrent_booked_classes
        )
        unavailable_students = get_double_booked_by_user(
            obj_id=obj_id,
            student_or_teacher='student',
            queried_user=booked_student,
            concurrent_booked_classes=concurrent_booked_classes
        )
        if booked_teacher in unavailable_teachers:
            return Response({"Error": "The teacher is unavailable for this time frame!"},
                            status=status.HTTP_400_BAD_REQUEST)
        elif booked_student in unavailable_students:
            return Response({"Error": "The student is unavailable for this time frame!"},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    queryset = ScheduledClass.objects.all()
    serializer_class = ScheduledClassSerializer
    lookup_field = 'id'


class ScheduledClassByTeacherByMonthViewSet(generics.ListAPIView):
    permission_classes = (
        IsAuthenticated,
    )
    queryset = ScheduledClass.objects.all()
    serializer_class = ScheduledClassSerializer
    lookup_field = 'id'
    model = serializer_class.Meta.model

    def get_queryset(self):
        month = self.kwargs.get("month")
        year = self.kwargs.get("year")
        start_date = datetime.date(int(year), int(month), 1)
        if int(month) == 12:
            finish_date = datetime.date(int(year) + 1, 1, 1)
        else:
            finish_date = datetime.date(int(year), int(month) + 1, 1)

        queryset = self.model.objects.filter(
                date__gte=start_date,
                date__lt=finish_date,
                teacher__user=self.request.user
        )
        return queryset.order_by('date', 'start_time')
