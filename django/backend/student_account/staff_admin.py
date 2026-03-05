from staff_admin.sites import staff_admin_site
from django import forms
from django.contrib import admin, messages

from .models import StudentOrClass
from school.models import School


class StaffStudentOrClassForm(forms.ModelForm):
    class Meta:
        model = StudentOrClass
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['school'].queryset = School.objects.filter(
            school_name="David's English Center"
        ).order_by(
            'scheduling_teacher__surname',
            'scheduling_teacher__given_name',
        )
        self.fields['school'].label = 'Teacher / School'


class StaffStudentOrClassAdmin(admin.ModelAdmin):
    form = StaffStudentOrClassForm
    exclude = ('teacher', 'account_type', 'purchased_class_hours')  # hides the field from the form

    list_display = (
        'teacher', 'student_or_class_name', 'school',
    )

    search_fields = (
        'student_or_class_name',
        'teacher__user__username', 'teacher__surname',
        'teacher__given_name','school__school_name'
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(
            school__school_name="David's English Center"
        )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.teacher = obj.school.scheduling_teacher
            obj.account_type = 'school'
        super().save_model(request, obj, form, change)


staff_admin_site.register(StudentOrClass, StaffStudentOrClassAdmin)