
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

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
        return self.update(request, *args, **kwargs)


class SchoolListView(APIView):
    permission_classes = (
        IsAuthenticated,
    )

    def get(self, request, *args, **kwargs):
        print(request.user)
        teachers_schools = School.objects.filter(scheduling_teacher__user=request.user)
        serializer = SchoolSerializer(teachers_schools, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = SchoolSerializer(data=request.data)
        teacher = get_object_or_404(UserProfile, user=request.user)
        if serializer.is_valid():
            serializer.save(scheduling_teacher_id=teacher.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
