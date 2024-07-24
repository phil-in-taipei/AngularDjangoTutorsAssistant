from django.urls import path

from .views import StudentOrClassEditAndDeleteView, StudentOrClassListView

app_name = "student_account"

urlpatterns = [
    path(
        'students-or-classes/',
        StudentOrClassListView.as_view(),
        name="users-students-or-classes"
    ),
    path(
        'student-or-class/<int:id>/',
        StudentOrClassEditAndDeleteView.as_view(),
        name="student-or-class"
    ),
]
