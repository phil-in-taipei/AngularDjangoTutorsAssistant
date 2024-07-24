from django.urls import path

from .views import SchoolEditAndDeleteView, SchoolListView

app_name = "school"


urlpatterns = [
    path(
        'users-schools/', SchoolListView.as_view(), name="users-schools"
    ),
    path(
        'users-school/<int:id>/', SchoolEditAndDeleteView.as_view(), name="school"
    ),
]
