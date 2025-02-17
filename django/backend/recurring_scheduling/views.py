from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import RecurringScheduledClass, RecurringClassAppliedMonthly
from .serializers import RecurringClassSerializer, RecurringClassAppliedMonthlySerializer
from .utils import (
    create_date_list,
    book_classes_for_specified_month,
    get_classes_for_deletion_for_specified_month,
    recurring_class_applied_monthly_has_scheduling_conflict,
    recurring_class_is_double_booked
)


# no put or patch -- user must delete and create a new object
class RecurringClassAppliedMonthlyViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthenticated,
    )
    queryset = RecurringClassAppliedMonthly.objects.all()
    serializer_class = RecurringClassAppliedMonthlySerializer
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        scheduling_month = serializer.validated_data['scheduling_month']
        scheduling_year = serializer.validated_data['scheduling_year']
        recurring_class_id = serializer.validated_data['recurring_class']
        recurring_class = get_object_or_404(RecurringClass, id=recurring_class_id)

        monthly_booking_date_list = create_date_list(
            year=scheduling_year, month=scheduling_month, 
            day_of_week=recurring_class.day_of_week
        )

        if recurring_class_applied_monthly_has_scheduling_conflict(
            list_of_dates_on_day_in_given_month=monthly_booking_date_list,
            recurring_class=recurring_class
        ):
            return Response(
                    { "Error": "Scheduling conflict" },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            serializer.save()
            # pass function to book classes in the dates for the pay period
            book_classes_for_specified_month(
                year=scheduling_year,
                month=scheduling_month,
                recurring_class=recurring_class
            )
            # trigger api call on front end to get newly booked classes
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        #finds the corresponding booked classes to the monthly recurring being deleted
        #sends back to the user, and user can determine whether or not to batch delete them
        recurring_for_specific_month_obj = self.get_object()
        deleted_recurring_applied_monthly_id=recurring_for_specific_month_obj.id
        monthly_booking_date_list = create_date_list(
            year=recurring_for_specific_month_obj.scheduling_year, 
            month=recurring_for_specific_month_obj.scheduling_month, 
            day_of_week=recurring_class.day_of_week
        )
        obsolete_classes_to_be_deleted = get_classes_for_deletion_for_specified_month(
            date_list=monthly_booking_date_list,
            recurring_class=recurring_for_specific_month_obj.recurring_class
        )
        list_of_classes_to_be_deleted_strings = [str(obj) for obj in obsolete_classes_to_be_deleted]
        list_of_classes_to_be_deleted_ids = [obj.id for obj in obsolete_classes_to_be_deleted]
        recurring_for_specific_month_obj.delete()
        return Response(
                {
                    "message": "Recurring monthly class successfully deleted",
                    "id": deleted_recurring_applied_monthly_id,
                    "scheduled_class_batch_deletion_data": {
                        "obsolete_class_strings": ', '.join(list_of_classes_to_be_deleted_strings),
                        "obsolete_class_ids": list_of_classes_to_be_deleted_ids
                    }            
                }
            )

    def update(self, request,  *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
class RecurringClassAppliedMonthlyListView(generics.ListAPIView):
    permission_classes = (
        IsAuthenticated,
    )
    queryset = RecurringClassAppliedMonthly.objects.all()
    serializer_class = RecurringClassAppliedMonthlySerializer
    lookup_field = 'id'
    model = serializer_class.Meta.model
    paginate_by = 100

    def get_queryset(self):
        #print('User:')
        #print(self.request.user.profile)
        #print('getting qs...')
        month = self.kwargs.get("month")
        year = self.kwargs.get("year")
        queryset = self.model.objects.filter(
            recurring_class__teacher__user=self.request.user,
            scheduling_month=month,
            scheduling_year=year
        )
        return queryset.order_by(
            'scheduling_year', 'scheduling_month',
            'recurring_class__student_or_class__student_or_class_name'
        )


class RecurringScheduledClassViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthenticated, #IsOwnerOrReadOnly
    )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recurring_day_of_week = serializer.validated_data['recurring_day_of_week']
        recurring_start_time = serializer.validated_data['recurring_start_time']
        recurring_finish_time = serializer.validated_data['recurring_finish_time']
        booked_teacher = serializer.validated_data['teacher']
        recurring_classes_booked_on_day_of_week =  (
            RecurringScheduledClass.custom_query.teacher_already_booked_classes_on_day_of_week(
                query_day_of_week=recurring_day_of_week,
                teacher_id=booked_teacher
            )
        )
        if recurring_class_is_double_booked(
                recurring_classes_booked_on_day_of_week=recurring_classes_booked_on_day_of_week,
                recurring_start_time=recurring_start_time,
                recurring_finish_time=recurring_finish_time
        ):
            return Response(
                {"Error": "The teacher is unavailable for this time frame!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        id = instance.id
        self.perform_destroy(instance)
        return Response(data={
            "id": id,
            "message": "Recurring Class successfully deleted!"}
        )

    queryset = RecurringScheduledClass.objects.all()
    serializer_class = RecurringClassSerializer
    lookup_field = 'id'


class RecurringClassesByTeacherListView(generics.ListAPIView):
    permission_classes = (
        IsAuthenticated,
    )
    queryset = RecurringScheduledClass.objects.all()
    serializer_class = RecurringClassSerializer
    lookup_field = 'id'
    model = serializer_class.Meta.model
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(teacher__user=self.request.user)
        return queryset.order_by('recurring_day_of_week', 'recurring_start_time')
