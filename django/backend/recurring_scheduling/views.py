from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import RecurringScheduledClass
from .serializers import RecurringClassSerializer
from .utils import recurring_class_is_double_booked

from class_scheduling.utils import (
    adjust_number_of_hours_purchased,
    determine_transaction_type,
    determine_duration_of_class_time,
)



class RecurringScheduledClassViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthenticated, #IsOwnerOrReadOnly
    )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        day_of_week = serializer.validated_data['day_of_week']
        recurring_start_time = serializer.validated_data['recurring_start_time']
        recurring_finish_time = serializer.validated_data['recurring_finish_time']
        booked_teacher = serializer.validated_data['teacher']
        recurring_classes_booked_on_day_of_week =  (
            RecurringScheduledClass.custom_query.teacher_already_booked_classes_on_day_of_week(
                query_day_of_week=day_of_week,
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
