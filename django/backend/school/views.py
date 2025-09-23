
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import IntegrityError

from .models import School
from user_profiles.models import UserProfile
from .serializers import SchoolSerializer


class SchoolEditAndDeleteView(
        generics.RetrieveUpdateDestroyAPIView
        ):
    permission_classes = (
        IsAuthenticated,
    )
    lookup_field = 'id'
    serializer_class = SchoolSerializer
    model = serializer_class.Meta.model
    http_method_names = ['patch', 'delete']
    queryset = School.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        deleted_object_id = instance.id
        self.perform_destroy(instance)
        return Response(data={"id": deleted_object_id,
                        "message": "School successfully deleted!"})

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data)
            except IntegrityError as e:
                return Response(
                    {"error": "A school with this name already exists for this teacher."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SchoolListView(APIView):
    permission_classes = (
        IsAuthenticated,
    )

    def get(self, request, *args, **kwargs):
        teachers_schools = School.objects.filter(scheduling_teacher__user=request.user)
        serializer = SchoolSerializer(teachers_schools, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = SchoolSerializer(data=request.data)
        teacher = get_object_or_404(UserProfile, user=request.user)
        if serializer.is_valid():
            try:
                serializer.save(scheduling_teacher_id=teacher.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                # Handle unique_together constraint violation
                return Response(
                    {"error": "A school with this name already exists for this teacher."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
