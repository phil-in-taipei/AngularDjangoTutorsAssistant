import datetime
from bisect import insort

from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ScheduledClass
from .pagination import SmallSetPagination
from .serializers import ScheduledClassSerializer
from .utils import (
    adjust_number_of_hours_purchased,
    class_is_double_booked,
    determine_transaction_type,
    determine_duration_of_class_time,
    get_double_booked_by_user,
    is_freelance_account,
    number_of_hours_purchased_should_be_updated
)
from user_profiles.models import UserProfile
from utilities.permissions import IsOwnerOrReadOnly


class ScheduledClassStatusConfirmationViewSet(APIView):
    permission_classes = (
        IsAuthenticated,  # IsOwnerOrReadOnly
    )

    def patch(self, request, *args, **kwargs):
        class_id = request.data['id']
        class_status = request.data['class_status']
        scheduled_class = get_object_or_404(ScheduledClass, id=class_id)

        transaction_type = determine_transaction_type(
            previous_class_status=scheduled_class.class_status,
            updated_class_status=class_status
        )
        scheduled_class.class_status = class_status
        scheduled_class.save()
        student_or_class = scheduled_class.student_or_class
        response = {
          "scheduled_class": {
              "id": scheduled_class.id,
              "class_status": scheduled_class.class_status
          },
          "student_or_class": student_or_class.purchased_class_hours
        }

        if is_freelance_account(scheduled_class.student_or_class) and number_of_hours_purchased_should_be_updated(transaction_type):
            print("******Account must be adjusted*******")
            duration = determine_duration_of_class_time(
                scheduled_class.start_time, scheduled_class.finish_time
            )
            print(duration)
            new_number_of_purchased_hours = adjust_number_of_hours_purchased(
                    transaction_type, duration, student_or_class.purchased_class_hours
            )
            print("This is the new number of purchased hours:")
            print(new_number_of_purchased_hours)
            student_or_class.purchased_class_hours = new_number_of_purchased_hours
            student_or_class.save()
            print("updated")
            response['student_or_class'] = {
              "id": student_or_class.id,
              "purchased_class_hours": student_or_class.purchased_class_hours
             }
        return Response(
            response,
            status=status.HTTP_202_ACCEPTED
        )


class ScheduledClassViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthenticated, #IsOwnerOrReadOnly
    )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        date = serializer.validated_data['date']
        start_time = serializer.validated_data['start_time']
        finish_time = serializer.validated_data['finish_time']
        booked_teacher = serializer.validated_data['teacher']
        classes_booked_on_date = (
            ScheduledClass.custom_query.teacher_already_booked_classes_on_date(
                query_date=date,
                teacher_id=booked_teacher
            )
        )
        if class_is_double_booked(
                classes_booked_on_date=classes_booked_on_date,
                starting_time=start_time,
                finishing_time=finish_time
        ):
            return Response(
                {"Error": "The teacher is unavailable for this time frame!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            new_class = serializer.save()
            daily_classes_list = list(classes_booked_on_date)
            insort(daily_classes_list, new_class, key=lambda x: x.start_time)
            serialized_data = ScheduledClassSerializer(daily_classes_list, many=True).data
            return Response(serialized_data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        date = serializer.validated_data['date']
        start_time = serializer.validated_data['start_time']
        finish_time = serializer.validated_data['finish_time']
        booked_teacher = serializer.validated_data['teacher']
        obj_id = instance.id

        classes_booked_on_date = (
            ScheduledClass.custom_query.teacher_already_booked_classes_on_date(
                query_date=date,
                teacher_id=booked_teacher
            ).exclude(id=obj_id)
        )
        if class_is_double_booked(
                classes_booked_on_date=classes_booked_on_date,
                starting_time=start_time,
                finishing_time=finish_time
        ):
            return Response(
                {"Error": "The teacher is unavailable for this time frame!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            new_class = serializer.save()
            daily_classes_list = list(classes_booked_on_date)
            insort(daily_classes_list, new_class, key=lambda x: x.start_time)
            serialized_data = ScheduledClassSerializer(daily_classes_list, many=True).data
            return Response(serialized_data, status=status.HTTP_202_ACCEPTED)

    queryset = ScheduledClass.objects.all()
    serializer_class = ScheduledClassSerializer
    lookup_field = 'id'


class ScheduledClassByTeacherByDateViewSet(generics.ListAPIView):
    permission_classes = (
        IsAuthenticated,
    )
    queryset = ScheduledClass.objects.all()
    serializer_class = ScheduledClassSerializer
    lookup_field = 'id'
    model = serializer_class.Meta.model
    paginate_by = 100

    def get_queryset(self):
        date_str = self.kwargs.get("date")
        date_list = date_str.split('-')
        date = datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
        queryset = self.model.objects.filter(date=date, teacher__user=self.request.user)
        return queryset.order_by('start_time')


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


class UnconfirmedStatusClassesViewSet(generics.ListAPIView):
    permission_classes = (
        IsAuthenticated,
    )
    queryset = ScheduledClass.objects.all()
    serializer_class = ScheduledClassSerializer
    lookup_field = 'id'
    model = serializer_class.Meta.model
    paginate_by = 100

    def get_queryset(self):
        today = datetime.date.today()
        queryset = self.model.objects.filter(
            teacher__user=self.request.user,
            date__lt=today,
            class_status='scheduled'
        )
        return queryset.order_by('date', 'start_time')
