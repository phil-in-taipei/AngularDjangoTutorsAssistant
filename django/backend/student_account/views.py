from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import StudentOrClass
from .serializers import StudentOrClassSerializer
from user_profiles.models import UserProfile


class StudentOrClassEditAndDeleteView(
        generics.RetrieveUpdateDestroyAPIView
        ):
    permission_classes = (
        IsAuthenticated,
    )
    lookup_field = 'id'
    serializer_class = StudentOrClassSerializer
    model = serializer_class.Meta.model
    http_method_names = ['patch', 'delete']
    queryset = StudentOrClass.objects.all()

    def get_queryset(self):
        # Filter by the current user's teacher profile
        teacher = get_object_or_404(UserProfile, user=self.request.user)
        return StudentOrClass.objects.filter(teacher=teacher)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        deleted_object_id = instance.id
        self.perform_destroy(instance)
        return Response(
            data={
                "id": deleted_object_id,
                "message": "Account successfully deleted!"
            }
        )

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = StudentOrClassSerializer(
            instance, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentOrClassListView(APIView):
    permission_classes = (
        IsAuthenticated,
    )

    def get(self, request, *args, **kwargs):
        student_or_class_accounts = StudentOrClass.objects.filter(
            teacher__user=request.user
        )
        serializer = StudentOrClassSerializer(student_or_class_accounts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = StudentOrClassSerializer(data=request.data)
        teacher = get_object_or_404(UserProfile, user=request.user)
        if serializer.is_valid():
            serializer.save(teacher_id=teacher.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
