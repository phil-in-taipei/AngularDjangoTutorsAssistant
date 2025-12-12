import json
import datetime
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from recurring_scheduling.models import RecurringScheduledClass, RecurringClassAppliedMonthly
from class_scheduling.models import ScheduledClass
from student_account.models import StudentOrClass
from user_profiles.models import UserProfile
from school.models import School


class RecurringSchedulingAPITestCase(TestCase):
    def setUp(self):
        """Set up test data for all test methods."""
        self.client = APIClient()

        # Create test users
        self.user1 = User.objects.create_user(
            username='teacher1',
            email='teacher1@test.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='teacher2',
            email='teacher2@test.com',
            password='testpass123'
        )

        # Create user profiles
        self.teacher1_profile = UserProfile.objects.create(
            user=self.user1,
            given_name='John',
            surname='Teacher',
            contact_email='teacher1@test.com'
        )
        self.teacher2_profile = UserProfile.objects.create(
            user=self.user2,
            given_name='Jane',
            surname='Teacher',
            contact_email='teacher2@test.com'
        )

        # Create test school
        self.school = School.objects.create(
            school_name='Test School',
            address_line_1='123 Test St',
            address_line_2='Suite 100',
            scheduling_teacher=self.teacher1_profile,
            contact_phone='1234567890',
            other_information='Test school information'
        )

        # Create test student accounts
        self.freelance_student = StudentOrClass.objects.create(
            student_or_class_name='John Doe',
            account_type='freelance',
            teacher=self.teacher1_profile,
            purchased_class_hours=Decimal('10.50'),
            tuition_per_hour=1200,
            comments='Test freelance student',
            school=None
        )

        self.school_student = StudentOrClass.objects.create(
            student_or_class_name='Jane Smith',
            account_type='school',
            school=self.school,
            teacher=self.teacher1_profile,
            tuition_per_hour=900,
            comments='Test school student',
            purchased_class_hours=None
        )

        # Create test recurring scheduled classes
        self.recurring_class1 = RecurringScheduledClass.objects.create(
            student_or_class=self.freelance_student,
            teacher=self.teacher1_profile,
            recurring_day_of_week=0,  # Monday
            recurring_start_time=datetime.time(10, 0),
            recurring_finish_time=datetime.time(11, 0)
        )

        self.recurring_class2 = RecurringScheduledClass.objects.create(
            student_or_class=self.school_student,
            teacher=self.teacher1_profile,
            recurring_day_of_week=2,  # Wednesday
            recurring_start_time=datetime.time(14, 0),
            recurring_finish_time=datetime.time(15, 30)
        )

        # Base URL for API endpoints
        self.base_url = '/api/recurring/'


class RecurringScheduledClassViewSetTests(RecurringSchedulingAPITestCase):
    """Test cases for RecurringScheduledClassViewSet (CRUD operations)."""

    def test_create_recurring_class_unauthenticated(self):
        """Test that unauthenticated users cannot create recurring classes."""
        url = self.base_url + 'recurring-class/'
        data = {
            'student_or_class': self.freelance_student.id,
            'teacher': self.teacher1_profile.id,
            'recurring_day_of_week': 1,  # Tuesday
            'recurring_start_time': '16:00',
            'recurring_finish_time': '17:00'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_recurring_class_success(self):
        """Test successful creation of a recurring class."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'recurring-class/'

        data = {
            'student_or_class': self.freelance_student.id,
            'teacher': self.teacher1_profile.id,
            'recurring_day_of_week': 1,  # Tuesday
            'recurring_start_time': '16:00',
            'recurring_finish_time': '17:00'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['recurring_day_of_week'], 1)
        self.assertEqual(response.data['recurring_start_time'], '16:00:00')

        # Verify class was created in database
        self.assertTrue(
            RecurringScheduledClass.objects.filter(
                student_or_class=self.freelance_student,
                recurring_day_of_week=1
            ).exists()
        )

    def test_create_recurring_class_double_booking_prevented(self):
        """Test that double booking is prevented when creating a recurring class."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'recurring-class/'

        # Try to book at the same time as recurring_class1 (Monday 10:00-11:00)
        data = {
            'student_or_class': self.school_student.id,
            'teacher': self.teacher1_profile.id,
            'recurring_day_of_week': 0,  # Monday
            'recurring_start_time': '10:30',
            'recurring_finish_time': '11:30'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Error', response.data)
        self.assertIn('unavailable', response.data['Error'])

    def test_create_recurring_class_overlapping_start_time(self):
        """Test that overlapping start times are prevented."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'recurring-class/'

        # Existing: Monday 10:00-11:00, try to book Monday 10:30-12:00
        data = {
            'student_or_class': self.school_student.id,
            'teacher': self.teacher1_profile.id,
            'recurring_day_of_week': 0,  # Monday
            'recurring_start_time': '10:30',
            'recurring_finish_time': '12:00'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recurring_class_overlapping_finish_time(self):
        """Test that overlapping finish times are prevented."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'recurring-class/'

        # Existing: Monday 10:00-11:00, try to book Monday 09:00-10:30
        data = {
            'student_or_class': self.school_student.id,
            'teacher': self.teacher1_profile.id,
            'recurring_day_of_week': 0,  # Monday
            'recurring_start_time': '09:00',
            'recurring_finish_time': '10:30'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recurring_class_encompassing_existing_class(self):
        """Test that booking a time that encompasses an existing class is prevented."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'recurring-class/'

        # Existing: Monday 10:00-11:00, try to book Monday 09:00-12:00
        data = {
            'student_or_class': self.school_student.id,
            'teacher': self.teacher1_profile.id,
            'recurring_day_of_week': 0,  # Monday
            'recurring_start_time': '09:00',
            'recurring_finish_time': '12:00'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recurring_class_no_conflict_different_day(self):
        """Test that non-conflicting classes on different days can be created."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'recurring-class/'

        # Existing: Monday 10:00-11:00, book Tuesday 10:00-11:00 (no conflict)
        data = {
            'student_or_class': self.school_student.id,
            'teacher': self.teacher1_profile.id,
            'recurring_day_of_week': 1,  # Tuesday
            'recurring_start_time': '10:00',
            'recurring_finish_time': '11:00'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_recurring_class_no_conflict_same_day_different_time(self):
        """Test that non-conflicting classes on same day but different times can be created."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'recurring-class/'

        # Existing: Monday 10:00-11:00, book Monday 12:00-13:00 (no conflict)
        data = {
            'student_or_class': self.school_student.id,
            'teacher': self.teacher1_profile.id,
            'recurring_day_of_week': 0,  # Monday
            'recurring_start_time': '12:00',
            'recurring_finish_time': '13:00'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_recurring_class_missing_required_fields(self):
        """Test validation when required fields are missing."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'recurring-class/'

        data = {
            'teacher': self.teacher1_profile.id,
            'recurring_day_of_week': 1
            # Missing student_or_class, start_time, finish_time
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_recurring_class_success(self):
        """Test successful deletion of a recurring class."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + f'recurring-class/{self.recurring_class1.id}/'
        class_id = self.recurring_class1.id

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], class_id)
        self.assertEqual(response.data['message'], 'Recurring Class successfully deleted!')

        # Verify class was deleted from database
        self.assertFalse(
            RecurringScheduledClass.objects.filter(id=class_id).exists()
        )

    def test_delete_recurring_class_unauthenticated(self):
        """Test that unauthenticated users cannot delete recurring classes."""
        url = self.base_url + f'recurring-class/{self.recurring_class1.id}/'

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_nonexistent_recurring_class(self):
        """Test deleting a non-existent recurring class."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'recurring-class/99999/'

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_day_of_week_string_property(self):
        """Test that day_of_week_string property is included in response."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + f'recurring-class/{self.recurring_class1.id}/'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('day_of_week_string', response.data)
        self.assertEqual(response.data['day_of_week_string'], 'Monday')


class RecurringClassesByTeacherListViewTests(RecurringSchedulingAPITestCase):
    """Test cases for RecurringClassesByTeacherListView."""

    def test_get_recurring_classes_unauthenticated(self):
        """Test that unauthenticated users cannot access recurring classes list."""
        url = self.base_url + 'schedule/by-teacher/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_recurring_classes_success(self):
        """Test successful retrieval of recurring classes for authenticated user."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'schedule/by-teacher/'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return both recurring classes for teacher1

        # Check that response contains expected fields
        expected_fields = {
            'id', 'student_or_class', 'teacher',
            'recurring_start_time', 'recurring_finish_time',
            'recurring_day_of_week', 'day_of_week_string'
        }
        self.assertTrue(all(field in response.data[0] for field in expected_fields))

    def test_get_recurring_classes_filters_by_teacher(self):
        """Test that users only see their own recurring classes."""
        # Create a recurring class for teacher2
        RecurringScheduledClass.objects.create(
            student_or_class=self.freelance_student,
            teacher=self.teacher2_profile,
            recurring_day_of_week=4,  # Friday
            recurring_start_time=datetime.time(10, 0),
            recurring_finish_time=datetime.time(11, 0)
        )

        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'schedule/by-teacher/'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only return teacher1's classes (2), not teacher2's
        self.assertEqual(len(response.data), 2)

        # Verify all returned classes belong to teacher1
        for class_data in response.data:
            self.assertEqual(class_data['teacher'], self.teacher1_profile.id)

    def test_get_recurring_classes_ordering(self):
        """Test that recurring classes are ordered by day of week and start time."""
        self.client.force_authenticate(user=self.user1)

        # Create additional classes to test ordering
        RecurringScheduledClass.objects.create(
            student_or_class=self.freelance_student,
            teacher=self.teacher1_profile,
            recurring_day_of_week=0,  # Monday
            recurring_start_time=datetime.time(9, 0),
            recurring_finish_time=datetime.time(10, 0)
        )

        url = self.base_url + 'schedule/by-teacher/'
        response = self.client.get(url)

        # Verify ordering by day of week, then start time
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for i in range(len(response.data) - 1):
            current_day = response.data[i]['recurring_day_of_week']
            next_day = response.data[i + 1]['recurring_day_of_week']

            if current_day == next_day:
                current_time = response.data[i]['recurring_start_time']
                next_time = response.data[i + 1]['recurring_start_time']
                self.assertLessEqual(current_time, next_time)
            else:
                self.assertLessEqual(current_day, next_day)


class RecurringClassAppliedMonthlyViewSetTests(RecurringSchedulingAPITestCase):
    """Test cases for RecurringClassAppliedMonthlyViewSet (CRUD operations)."""

    def test_create_applied_monthly_unauthenticated(self):
        """Test that unauthenticated users cannot create applied monthly records."""
        url = self.base_url + 'applied-monthly/'
        data = {
            'scheduling_month': 1,  # January
            'scheduling_year': 2025,
            'recurring_class': self.recurring_class1.id
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_applied_monthly_success(self):
        """Test successful creation of an applied monthly record."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'applied-monthly/'

        data = {
            'scheduling_month': 1,  # January
            'scheduling_year': 2025,
            'recurring_class': self.recurring_class1.id
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['scheduling_month'], 1)
        self.assertEqual(response.data['scheduling_year'], 2025)

        # Verify record was created in database
        self.assertTrue(
            RecurringClassAppliedMonthly.objects.filter(
                scheduling_month=1,
                scheduling_year=2025,
                recurring_class=self.recurring_class1
            ).exists()
        )

    def test_create_applied_monthly_creates_scheduled_classes(self):
        """Test that creating applied monthly also creates scheduled classes."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'applied-monthly/'

        # January 2025 has Mondays on: 6, 13, 20, 27
        data = {
            'scheduling_month': 1,
            'scheduling_year': 2025,
            'recurring_class': self.recurring_class1.id  # Monday class
        }

        initial_scheduled_count = ScheduledClass.objects.count()
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify scheduled classes were created
        final_scheduled_count = ScheduledClass.objects.count()
        self.assertEqual(final_scheduled_count, initial_scheduled_count + 4)  # 4 Mondays in January 2025

    def test_create_applied_monthly_with_scheduling_conflict(self):
        """Test that scheduling conflicts are detected and prevented."""
        self.client.force_authenticate(user=self.user1)

        # Create a conflicting scheduled class on first Monday of January 2025
        ScheduledClass.objects.create(
            student_or_class=self.school_student,
            teacher=self.teacher1_profile,
            date=datetime.date(2025, 1, 6),  # Monday, Jan 6
            start_time=datetime.time(10, 30),
            finish_time=datetime.time(11, 30),
            class_status='scheduled'
        )

        url = self.base_url + 'applied-monthly/'
        data = {
            'scheduling_month': 1,
            'scheduling_year': 2025,
            'recurring_class': self.recurring_class1.id  # Monday 10:00-11:00
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Error', response.data)
        self.assertIn('conflict', response.data['Error'].lower())

    def test_create_applied_monthly_missing_required_fields(self):
        """Test validation when required fields are missing."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'applied-monthly/'

        data = {
            'scheduling_month': 1
            # Missing scheduling_year and recurring_class
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_applied_monthly_duplicate_prevented(self):
        """Test that duplicate applied monthly records are prevented."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'applied-monthly/'

        data = {
            'scheduling_month': 1,
            'scheduling_year': 2025,
            'recurring_class': self.recurring_class1.id
        }

        # First creation should succeed
        response1 = self.client.post(url, data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # Second creation should fail due to unique_together constraint
        response2 = self.client.post(url, data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_applied_monthly_success(self):
        """Test successful deletion of an applied monthly record."""
        self.client.force_authenticate(user=self.user1)

        # Create an applied monthly record first
        applied_monthly = RecurringClassAppliedMonthly.objects.create(
            scheduling_month=1,
            scheduling_year=2025,
            recurring_class=self.recurring_class1
        )

        url = self.base_url + f'applied-monthly/{applied_monthly.id}/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('id', response.data)
        self.assertIn('scheduled_class_batch_deletion_data', response.data)

        # Verify record was deleted
        self.assertFalse(
            RecurringClassAppliedMonthly.objects.filter(id=applied_monthly.id).exists()
        )

    def test_delete_applied_monthly_returns_obsolete_classes(self):
        """Test that deleting applied monthly returns list of obsolete scheduled classes."""
        self.client.force_authenticate(user=self.user1)

        # Create an applied monthly record (this creates scheduled classes)
        url = self.base_url + 'applied-monthly/'
        data = {
            'scheduling_month': 1,
            'scheduling_year': 2025,
            'recurring_class': self.recurring_class1.id
        }
        create_response = self.client.post(url, data, format='json')
        applied_monthly_id = create_response.data['id']

        # Delete the applied monthly record
        delete_url = self.base_url + f'applied-monthly/{applied_monthly_id}/'
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('scheduled_class_batch_deletion_data', response.data)
        self.assertIn('obsolete_class_ids', response.data['scheduled_class_batch_deletion_data'])
        self.assertIn('obsolete_class_strings', response.data['scheduled_class_batch_deletion_data'])

        # Should have 4 classes to delete (4 Mondays in January 2025)
        self.assertEqual(
            len(response.data['scheduled_class_batch_deletion_data']['obsolete_class_ids']),
            4
        )

    def test_delete_applied_monthly_unauthenticated(self):
        """Test that unauthenticated users cannot delete applied monthly records."""
        applied_monthly = RecurringClassAppliedMonthly.objects.create(
            scheduling_month=1,
            scheduling_year=2025,
            recurring_class=self.recurring_class1
        )

        url = self.base_url + f'applied-monthly/{applied_monthly.id}/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_applied_monthly_not_allowed(self):
        """Test that PUT/PATCH updates are not allowed for applied monthly."""
        self.client.force_authenticate(user=self.user1)

        applied_monthly = RecurringClassAppliedMonthly.objects.create(
            scheduling_month=1,
            scheduling_year=2025,
            recurring_class=self.recurring_class1
        )

        url = self.base_url + f'applied-monthly/{applied_monthly.id}/'
        data = {'scheduling_month': 2}

        # Test PUT
        put_response = self.client.put(url, data, format='json')
        self.assertEqual(put_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Test PATCH
        patch_response = self.client.patch(url, data, format='json')
        self.assertEqual(patch_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class RecurringClassAppliedMonthlyListViewTests(RecurringSchedulingAPITestCase):
    """Test cases for RecurringClassAppliedMonthlyListView."""

    def test_get_applied_monthly_list_unauthenticated(self):
        """Test that unauthenticated users cannot access applied monthly list."""
        url = self.base_url + 'monthly/recurring/by-teacher/1/2025/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_applied_monthly_list_success(self):
        """Test successful retrieval of applied monthly records."""
        self.client.force_authenticate(user=self.user1)

        # Create some applied monthly records
        RecurringClassAppliedMonthly.objects.create(
            scheduling_month=1,
            scheduling_year=2025,
            recurring_class=self.recurring_class1
        )
        RecurringClassAppliedMonthly.objects.create(
            scheduling_month=1,
            scheduling_year=2025,
            recurring_class=self.recurring_class2
        )

        url = self.base_url + 'monthly/recurring/by-teacher/1/2025/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Check that response contains expected fields
        expected_fields = {
            'id', 'scheduling_month', 'scheduling_year',
            'recurring_class', 'month_string',
            'recurring_day_of_week', 'recurring_start_time'
        }
        self.assertTrue(all(field in response.data[0] for field in expected_fields))

    def test_get_applied_monthly_list_filters_by_month_year(self):
        """Test that records are filtered by month and year."""
        self.client.force_authenticate(user=self.user1)

        # Create records for different months
        RecurringClassAppliedMonthly.objects.create(
            scheduling_month=1,
            scheduling_year=2025,
            recurring_class=self.recurring_class1
        )
        RecurringClassAppliedMonthly.objects.create(
            scheduling_month=2,
            scheduling_year=2025,
            recurring_class=self.recurring_class1
        )

        url = self.base_url + 'monthly/recurring/by-teacher/1/2025/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only return January records
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['scheduling_month'], 1)

    def test_get_applied_monthly_list_filters_by_teacher(self):
        """Test that records are filtered by teacher."""
        # Create records for both teachers
        RecurringClassAppliedMonthly.objects.create(
            scheduling_month=1,
            scheduling_year=2025,
            recurring_class=self.recurring_class1  # teacher1
        )

        teacher2_recurring_class = RecurringScheduledClass.objects.create(
            student_or_class=self.freelance_student,
            teacher=self.teacher2_profile,
            recurring_day_of_week=0,
            recurring_start_time=datetime.time(14, 0),
            recurring_finish_time=datetime.time(15, 0)
        )
        RecurringClassAppliedMonthly.objects.create(
            scheduling_month=1,
            scheduling_year=2025,
            recurring_class=teacher2_recurring_class  # teacher2
        )

        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'monthly/recurring/by-teacher/1/2025/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only return teacher1's record
        self.assertEqual(len(response.data), 1)

    def test_get_applied_monthly_list_ordering(self):
        """Test that records are ordered correctly."""
        self.client.force_authenticate(user=self.user1)

        # Create records with different days and times
        recurring_monday_early = RecurringScheduledClass.objects.create(
            student_or_class=self.freelance_student,
            teacher=self.teacher1_profile,
            recurring_day_of_week=0,  # Monday
            recurring_start_time=datetime.time(9, 0),
            recurring_finish_time=datetime.time(10, 0)
        )

        recurring_monday_late = RecurringScheduledClass.objects.create(
            student_or_class=self.school_student,
            teacher=self.teacher1_profile,
            recurring_day_of_week=0,  # Monday
            recurring_start_time=datetime.time(15, 0),
            recurring_finish_time=datetime.time(16, 0)
        )

        RecurringClassAppliedMonthly.objects.create(
            scheduling_month=1,
            scheduling_year=2025,
            recurring_class=recurring_monday_late
        )
        RecurringClassAppliedMonthly.objects.create(
            scheduling_month=1,
            scheduling_year=2025,
            recurring_class=recurring_monday_early
        )
        RecurringClassAppliedMonthly.objects.create(
            scheduling_month=1,
            scheduling_year=2025,
            recurring_class=self.recurring_class2  # Wednesday
        )

        url = self.base_url + 'monthly/recurring/by-teacher/1/2025/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify ordering: Monday classes should come before Wednesday
        # Within Monday, earlier start time should come first
        self.assertEqual(response.data[0]['recurring_day_of_week'], 0)  # Monday
        self.assertEqual(response.data[1]['recurring_day_of_week'], 0)  # Monday
        self.assertEqual(response.data[2]['recurring_day_of_week'], 2)  # Wednesday

        # Verify time ordering for Monday classes
        self.assertLess(
            response.data[0]['recurring_start_time'],
            response.data[1]['recurring_start_time']
        )

    def test_get_applied_monthly_list_empty(self):
        """Test retrieval when no records exist for given month/year."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'monthly/recurring/by-teacher/12/2025/'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_applied_monthly_list_month_string_property(self):
        """Test that month_string property is included in response."""
        self.client.force_authenticate(user=self.user1)

        RecurringClassAppliedMonthly.objects.create(
            scheduling_month=1,
            scheduling_year=2025,
            recurring_class=self.recurring_class1
        )

        url = self.base_url + 'monthly/recurring/by-teacher/1/2025/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('month_string', response.data[0])
        self.assertEqual(response.data[0]['month_string'], 'January')


class RecurringSchedulingEdgeCaseTests(RecurringSchedulingAPITestCase):
    """Test edge cases and boundary conditions."""

    def test_create_recurring_class_all_days_of_week(self):
        """Test creating recurring classes for all days of the week."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'recurring-class/'

        # Test all days from Monday (0) to Sunday (6)
        for day in range(7):
            data = {
                'student_or_class': self.freelance_student.id,
                'teacher': self.teacher1_profile.id,
                'recurring_day_of_week': day,
                'recurring_start_time': f'{8 + day}:00',
                'recurring_finish_time': f'{9 + day}:00'
            }

            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_recurring_class_at_midnight(self):
        """Test creating a recurring class starting at midnight."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'recurring-class/'

        data = {
            'student_or_class': self.freelance_student.id,
            'teacher': self.teacher1_profile.id,
            'recurring_day_of_week': 3,  # Thursday
            'recurring_start_time': '00:00',
            'recurring_finish_time': '01:00'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_recurring_class_ending_at_midnight(self):
        """Test creating a recurring class ending at midnight."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'recurring-class/'

        data = {
            'student_or_class': self.freelance_student.id,
            'teacher': self.teacher1_profile.id,
            'recurring_day_of_week': 3,  # Thursday
            'recurring_start_time': '23:00',
            'recurring_finish_time': '23:59'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_applied_monthly_december_boundary(self):
        """Test creating applied monthly for December (year boundary)."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'applied-monthly/'

        data = {
            'scheduling_month': 12,  # December
            'scheduling_year': 2025,
            'recurring_class': self.recurring_class1.id
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_applied_monthly_february_leap_year(self):
        """Test creating applied monthly for February in a leap year."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'applied-monthly/'

        # 2028 is a leap year
        data = {
            'scheduling_month': 2,  # February
            'scheduling_year': 2028,
            'recurring_class': self.recurring_class1.id
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_applied_monthly_february_non_leap_year(self):
        """Test creating applied monthly for February in a non-leap year."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'applied-monthly/'

        # 2025 is not a leap year
        data = {
            'scheduling_month': 2,  # February
            'scheduling_year': 2025,
            'recurring_class': self.recurring_class1.id
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_applied_monthly_month_with_five_occurrences(self):
        """Test creating applied monthly for a month where day occurs 5 times."""
        self.client.force_authenticate(user=self.user1)

        # March 2025 has 5 Mondays (3, 10, 17, 24, 31)
        url = self.base_url + 'applied-monthly/'
        data = {
            'scheduling_month': 3,
            'scheduling_year': 2025,
            'recurring_class': self.recurring_class1.id  # Monday class
        }

        initial_count = ScheduledClass.objects.count()
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Should create 5 scheduled classes
        final_count = ScheduledClass.objects.count()
        self.assertEqual(final_count, initial_count + 5)

    def test_applied_monthly_year_validation_min(self):
        """Test year validation at minimum boundary."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'applied-monthly/'

        # Test year below minimum (2025)
        data = {
            'scheduling_month': 1,
            'scheduling_year': 2024,
            'recurring_class': self.recurring_class1.id
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_applied_monthly_year_validation_max(self):
        """Test year validation at maximum boundary."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'applied-monthly/'

        # Test year above maximum (2035)
        data = {
            'scheduling_month': 1,
            'scheduling_year': 2036,
            'recurring_class': self.recurring_class1.id
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_applied_monthly_year_at_boundaries(self):
        """Test year validation at exact boundaries."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'applied-monthly/'

        # Test minimum valid year (2025)
        data_min = {
            'scheduling_month': 1,
            'scheduling_year': 2025,
            'recurring_class': self.recurring_class1.id
        }
        response_min = self.client.post(url, data_min, format='json')
        self.assertEqual(response_min.status_code, status.HTTP_201_CREATED)

        # Create a different recurring class for max year test
        recurring_class_for_max = RecurringScheduledClass.objects.create(
            student_or_class=self.school_student,
            teacher=self.teacher1_profile,
            recurring_day_of_week=1,
            recurring_start_time=datetime.time(10, 0),
            recurring_finish_time=datetime.time(11, 0)
        )

        # Test maximum valid year (2035)
        data_max = {
            'scheduling_month': 1,
            'scheduling_year': 2035,
            'recurring_class': recurring_class_for_max.id
        }
        response_max = self.client.post(url, data_max, format='json')
        self.assertEqual(response_max.status_code, status.HTTP_201_CREATED)


class RecurringSchedulingModelTests(RecurringSchedulingAPITestCase):
    """Test model properties and methods."""

    def test_recurring_class_day_of_week_string_property(self):
        """Test day_of_week_string property for all days."""
        days_mapping = {
            0: 'Monday',
            1: 'Tuesday',
            2: 'Wednesday',
            3: 'Thursday',
            4: 'Friday',
            5: 'Saturday',
            6: 'Sunday'
        }

        for day_num, day_name in days_mapping.items():
            recurring_class = RecurringScheduledClass.objects.create(
                student_or_class=self.freelance_student,
                teacher=self.teacher1_profile,
                recurring_day_of_week=day_num,
                recurring_start_time=datetime.time(10, 0),
                recurring_finish_time=datetime.time(11, 0)
            )
            self.assertEqual(recurring_class.day_of_week_string, day_name)

    def test_recurring_class_string_representation(self):
        """Test __str__ method of RecurringScheduledClass."""
        string_repr = str(self.recurring_class1)

        self.assertIn('Monday', string_repr)
        self.assertIn('10:00', string_repr)
        self.assertIn('11:00', string_repr)
        self.assertIn(str(self.freelance_student), string_repr)

    def test_applied_monthly_month_string_property(self):
        """Test month_string property for all months."""
        months_mapping = {
            1: 'January', 2: 'February', 3: 'March', 4: 'April',
            5: 'May', 6: 'June', 7: 'July', 8: 'August',
            9: 'September', 10: 'October', 11: 'November', 12: 'December'
        }

        for month_num, month_name in months_mapping.items():
            applied_monthly = RecurringClassAppliedMonthly.objects.create(
                scheduling_month=month_num,
                scheduling_year=2025,
                recurring_class=self.recurring_class1
            )
            self.assertEqual(applied_monthly.month_string, month_name)

    def test_applied_monthly_recurring_properties(self):
        """Test that applied monthly exposes recurring class properties."""
        applied_monthly = RecurringClassAppliedMonthly.objects.create(
            scheduling_month=1,
            scheduling_year=2025,
            recurring_class=self.recurring_class1
        )

        # Test recurring_day_of_week property
        self.assertEqual(
            applied_monthly.recurring_day_of_week,
            self.recurring_class1.recurring_day_of_week
        )

        # Test recurring_start_time property
        self.assertEqual(
            applied_monthly.recurring_start_time,
            self.recurring_class1.recurring_start_time
        )

    def test_applied_monthly_string_representation(self):
        """Test __str__ method of RecurringClassAppliedMonthly."""
        applied_monthly = RecurringClassAppliedMonthly.objects.create(
            scheduling_month=1,
            scheduling_year=2025,
            recurring_class=self.recurring_class1
        )

        string_repr = str(applied_monthly)
        self.assertIn('January', string_repr)
        self.assertIn('2025', string_repr)


class RecurringSchedulingIntegrationTests(RecurringSchedulingAPITestCase):
    """Test integration scenarios involving multiple operations."""

    def test_full_workflow_create_recurring_then_apply_monthly(self):
        """Test complete workflow: create recurring class, then apply to month."""
        self.client.force_authenticate(user=self.user1)

        # Step 1: Create a new recurring class
        recurring_url = self.base_url + 'recurring-class/'
        recurring_data = {
            'student_or_class': self.freelance_student.id,
            'teacher': self.teacher1_profile.id,
            'recurring_day_of_week': 4,  # Friday
            'recurring_start_time': '13:00',
            'recurring_finish_time': '14:00'
        }
        recurring_response = self.client.post(recurring_url, recurring_data, format='json')
        self.assertEqual(recurring_response.status_code, status.HTTP_201_CREATED)
        recurring_id = recurring_response.data['id']

        # Step 2: Apply it to a month
        applied_url = self.base_url + 'applied-monthly/'
        applied_data = {
            'scheduling_month': 1,
            'scheduling_year': 2025,
            'recurring_class': recurring_id
        }
        applied_response = self.client.post(applied_url, applied_data, format='json')
        self.assertEqual(applied_response.status_code, status.HTTP_201_CREATED)

        # Step 3: Verify scheduled classes were created
        # January 2025 Fridays: 3, 10, 17, 24, 31
        scheduled_classes = ScheduledClass.objects.filter(
            teacher=self.teacher1_profile,
            date__year=2025,
            date__month=1,
            start_time=datetime.time(13, 0)
        )
        self.assertEqual(scheduled_classes.count(), 5)

    def test_delete_recurring_class_with_applied_monthly(self):
        """Test that deleting recurring class also deletes applied monthly records."""
        self.client.force_authenticate(user=self.user1)

        # Create applied monthly record
        applied_monthly = RecurringClassAppliedMonthly.objects.create(
            scheduling_month=1,
            scheduling_year=2025,
            recurring_class=self.recurring_class1
        )

        # Delete the recurring class
        url = self.base_url + f'recurring-class/{self.recurring_class1.id}/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify applied monthly record was also deleted (CASCADE)
        self.assertFalse(
            RecurringClassAppliedMonthly.objects.filter(id=applied_monthly.id).exists()
        )

    def test_apply_same_recurring_class_to_multiple_months(self):
        """Test applying the same recurring class to multiple different months."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'applied-monthly/'

        # Apply to January
        data_jan = {
            'scheduling_month': 1,
            'scheduling_year': 2025,
            'recurring_class': self.recurring_class1.id
        }
        response_jan = self.client.post(url, data_jan, format='json')
        self.assertEqual(response_jan.status_code, status.HTTP_201_CREATED)

        # Apply to February
        data_feb = {
            'scheduling_month': 2,
            'scheduling_year': 2025,
            'recurring_class': self.recurring_class1.id
        }
        response_feb = self.client.post(url, data_feb, format='json')
        self.assertEqual(response_feb.status_code, status.HTTP_201_CREATED)

        # Verify both exist
        applied_count = RecurringClassAppliedMonthly.objects.filter(
            recurring_class=self.recurring_class1,
            scheduling_year=2025
        ).count()
        self.assertEqual(applied_count, 2)

    def test_conflict_between_recurring_and_one_time_class(self):
        """Test that recurring applied monthly detects conflicts with one-time classes."""
        self.client.force_authenticate(user=self.user1)

        # Create a one-time scheduled class that conflicts
        ScheduledClass.objects.create(
            student_or_class=self.school_student,
            teacher=self.teacher1_profile,
            date=datetime.date(2025, 1, 6),  # First Monday of January 2025
            start_time=datetime.time(10, 0),
            finish_time=datetime.time(11, 0),
            class_status='scheduled'
        )

        # Try to apply recurring class (also Monday 10:00-11:00)
        url = self.base_url + 'applied-monthly/'
        data = {
            'scheduling_month': 1,
            'scheduling_year': 2025,
            'recurring_class': self.recurring_class1.id
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('conflict', response.data['Error'].lower())
