from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from student_account.models import StudentOrClass
from .models import FreelanceTuitionTransactionRecord
from .serializers import FreelanceTuitionTransactionRecordSerializer
from .utils import create_purchased_hours_modification_record_for_tuition_transaction


class FreelanceTuitionTransactionViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsAuthenticated, #IsOwnerOrReadOnly
    )
    queryset = FreelanceTuitionTransactionRecord.objects.all()
    serializer_class = FreelanceTuitionTransactionRecordSerializer
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student_or_class_id = serializer.validated_data['student_or_class']
        student_or_class = get_object_or_404(StudentOrClass, id=student_or_class_id)
        previous_hours_purchased = student_or_class.purchased_class_hours
        #previous_hours_purchased, freelance_tuition_transaction_record
        freelance_tuition_transaction=serializer.save()
        create_purchased_hours_modification_record_for_tuition_transaction(
                previous_hours_purchased=previous_hours_purchased, 
                freelance_tuition_transaction_record=freelance_tuition_transaction
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)