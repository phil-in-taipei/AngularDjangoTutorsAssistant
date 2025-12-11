import json
import datetime
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch

from class_scheduling.models import ScheduledClass
from student_account.models import StudentOrClass
from user_profiles.models import UserProfile
from school.models import School
from accounting.models import PurchasedHoursModificationRecord


class ClassSchedulingAPITestCase(TestCase):
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

        # Create test scheduled classes
        self.scheduled_class1 = ScheduledClass.objects.create(
            student_or_class=self.freelance_student,
            teacher=self.teacher1_profile,
            date=datetime.date(2024, 12, 15),
            start_time=datetime.time(10, 0),
            finish_time=datetime.time(11, 0),
            class_status='scheduled',
            teacher_notes='Test notes',
            class_content='Test content'
        )

        self.scheduled_class2 = ScheduledClass.objects.create(
            student_or_class=self.school_student,
            teacher=self.teacher1_profile,
            date=datetime.date(2024, 12, 15),
            start_time=datetime.time(14, 0),
            finish_time=datetime.time(15, 30),
            class_status='completed',
            teacher_notes='Completed class',
            class_content='Finished lesson'
        )

        # Past class for unconfirmed status tests
        self.past_scheduled_class = ScheduledClass.objects.create(
            student_or_class=self.freelance_student,
            teacher=self.teacher1_profile,
            date=datetime.date.today() - datetime.timedelta(days=2),
            start_time=datetime.time(9, 0),
            finish_time=datetime.time(10, 0),
            class_status='scheduled',
            teacher_notes='Past class',
            class_content='Past content'
        )

        # Base URL for API endpoints
        self.base_url = '/api/scheduling/'


class ScheduledClassViewSetTests(ClassSchedulingAPITestCase):
    """Test cases for ScheduledClassViewSet (CRUD operations)."""

    def test_create_scheduled_class_unauthenticated(self):
        """Test that unauthenticated users cannot create scheduled classes."""
        url = self.base_url + 'class/submit/'
        data = {
            'student_or_class': self.freelance_student.id,
            'teacher': self.teacher1_profile.id,
            'date': '2024-12-20',
            'start_time': '16:00',
            'finish_time': '17:00',
            'class_status': 'scheduled'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_scheduled_class_success(self):
        """Test successful creation of a scheduled class."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'class/submit/'

        data = {
            'student_or_class': self.freelance_student.id,
            'teacher': self.teacher1_profile.id,
            'date': '2024-12-20',
            'start_time': '16:00',
            'finish_time': '17:00',
            'class_status': 'scheduled',
            'teacher_notes': 'New class notes',
            'class_content': 'New class content'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(isinstance(response.data, list))
        
        # Verify class was created in database
        self.assertTrue(
            ScheduledClass.objects.filter(
                student_or_class=self.freelance_student,
                date=datetime.date(2024, 12, 20),
                start_time=datetime.time(16, 0)
            ).exists()
        )

    def test_create_scheduled_class_double_booking_prevented(self):
        """Test that double booking is prevented when creating a class."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'class/submit/'

        # Try to book at the same time as scheduled_class1 (10:00-11:00)
        data = {
            'student_or_class': self.school_student.id,
            'teacher': self.teacher1_profile.id,
            'date': '2024-12-15',
            'start_time': '10:30',
            'finish_time': '11:30',
            'class_status': 'scheduled'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Error', response.data)
        self.assertIn('unavailable', response.data['Error'])

    def test_create_scheduled_class_overlapping_start_time(self):
        """Test that overlapping start times are prevented."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'class/submit/'

        # Existing class: 10:00-11:00, try to book 10:30-12:00
        data = {
            'student_or_class': self.school_student.id,
            'teacher': self.teacher1_profile.id,
            'date': '2024-12-15',
            'start_time': '10:30',
            'finish_time': '12:00',
            'class_status': 'scheduled'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_scheduled_class_overlapping_finish_time(self):
        """Test that overlapping finish times are prevented."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'class/submit/'

        # Existing class: 10:00-11:00, try to book 9:00-10:30
        data = {
            'student_or_class': self.school_student.id,
            'teacher': self.teacher1_profile.id,
            'date': '2024-12-15',
            'start_time': '09:00',
            'finish_time': '10:30',
            'class_status': 'scheduled'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_scheduled_class_encompassing_existing_class(self):
        """Test that booking a time that encompasses an existing class is prevented."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'class/submit/'

        # Existing class: 10:00-11:00, try to book 9:00-12:00
        data = {
            'student_or_class': self.school_student.id,
            'teacher': self.teacher1_profile.id,
            'date': '2024-12-15',
            'start_time': '09:00',
            'finish_time': '12:00',
            'class_status': 'scheduled'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_scheduled_class_no_conflict(self):
        """Test that non-conflicting classes can be created."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'class/submit/'

        # Existing class: 10:00-11:00, book 12:00-13:00 (no conflict)
        data = {
            'student_or_class': self.school_student.id,
            'teacher': self.teacher1_profile.id,
            'date': '2024-12-15',
            'start_time': '12:00',
            'finish_time': '13:00',
            'class_status': 'scheduled'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_scheduled_class_missing_required_fields(self):
        """Test validation when required fields are missing."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'class/submit/'

        data = {
            'teacher': self.teacher1_profile.id,
            'date': '2024-12-20'
            # Missing student_or_class, start_time, finish_time
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_scheduled_class_success(self):
        """Test successful update of a scheduled class."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + f'class/submit/{self.scheduled_class1.id}/'

        data = {
            'student_or_class': self.freelance_student.id,
            'teacher': self.teacher1_profile.id,
            'date': '2024-12-15',
            'start_time': '11:00',
            'finish_time': '12:00',
            'class_status': 'scheduled',
            'teacher_notes': 'Updated notes',
            'class_content': 'Updated content'
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        
        # Verify database was updated
        updated_class = ScheduledClass.objects.get(id=self.scheduled_class1.id)
        self.assertEqual(updated_class.start_time, datetime.time(11, 0))
        self.assertEqual(updated_class.teacher_notes, 'Updated notes')

    def test_update_scheduled_class_double_booking_prevented(self):
        """Test that double booking is prevented when updating a class."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + f'class/submit/{self.scheduled_class1.id}/'

        # Try to update to conflict with scheduled_class2 (14:00-15:30)
        data = {
            'student_or_class': self.freelance_student.id,
            'teacher': self.teacher1_profile.id,
            'date': '2024-12-15',
            'start_time': '14:30',
            'finish_time': '16:00',
            'class_status': 'scheduled'
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Error', response.data)

    def test_update_scheduled_class_to_same_time_allowed(self):
        """Test that updating a class to keep the same time is allowed."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + f'class/submit/{self.scheduled_class1.id}/'

        # Update other fields but keep same time
        data = {
            'student_or_class': self.freelance_student.id,
            'teacher': self.teacher1_profile.id,
            'date': '2024-12-15',
            'start_time': '10:00',
            'finish_time': '11:00',
            'class_status': 'scheduled',
            'teacher_notes': 'Different notes'
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_partial_update_scheduled_class_success(self):
        """Test successful partial update of a scheduled class."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + f'class/submit/{self.scheduled_class1.id}/'

        # For partial updates, the view's update method still requires
        # date, start_time, finish_time, and teacher to check for conflicts
        data = {
            'student_or_class': self.scheduled_class1.student_or_class.id,
            'teacher': self.scheduled_class1.teacher.id,
            'date': str(self.scheduled_class1.date),
            'start_time': str(self.scheduled_class1.start_time),
            'finish_time': str(self.scheduled_class1.finish_time),
            'class_status': self.scheduled_class1.class_status,
            'teacher_notes': 'Partially updated notes'
        }

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        
        # Verify database was updated
        updated_class = ScheduledClass.objects.get(id=self.scheduled_class1.id)
        self.assertEqual(updated_class.teacher_notes, 'Partially updated notes')

    def test_delete_scheduled_class_success(self):
        """Test successful deletion of a scheduled class."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + f'class/submit/{self.scheduled_class1.id}/'
        class_id = self.scheduled_class1.id

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], class_id)
        self.assertEqual(response.data['message'], 'Class successfully deleted!')

        # Verify class was deleted from database
        self.assertFalse(
            ScheduledClass.objects.filter(id=class_id).exists()
        )

    def test_delete_scheduled_class_unauthenticated(self):
        """Test that unauthenticated users cannot delete scheduled classes."""
        url = self.base_url + f'class/submit/{self.scheduled_class1.id}/'

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_nonexistent_scheduled_class(self):
        """Test deleting a non-existent scheduled class."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'class/submit/99999/'

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ScheduledClassStatusConfirmationTests(ClassSchedulingAPITestCase):
    """Test cases for ScheduledClassStatusConfirmationViewSet."""

    def test_update_class_status_unauthenticated(self):
        """Test that unauthenticated users cannot update class status."""
        url = self.base_url + 'class-status-confirmation/'
        data = {
            'id': self.scheduled_class1.id,
            'class_status': 'completed',
            'teacher_notes': 'Updated notes',
            'class_content': 'Updated content'
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_class_status_to_completed_success(self):
        """Test successful update of class status from scheduled to completed."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'class-status-confirmation/'

        data = {
            'id': self.scheduled_class1.id,
            'class_status': 'completed',
            'teacher_notes': 'Class completed successfully',
            'class_content': 'Covered all topics'
        }

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn('scheduled_class', response.data)
        self.assertEqual(response.data['scheduled_class']['class_status'], 'completed')

        # Verify database was updated
        updated_class = ScheduledClass.objects.get(id=self.scheduled_class1.id)
        self.assertEqual(updated_class.class_status, 'completed')

    def test_update_class_status_deducts_freelance_hours(self):
        """Test that completing a freelance class deducts purchased hours."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'class-status-confirmation/'

        initial_hours = self.freelance_student.purchased_class_hours

        data = {
            'id': self.scheduled_class1.id,
            'class_status': 'completed',
            'teacher_notes': 'Class completed',
            'class_content': 'Lesson finished'
        }

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIsNotNone(response.data['student_or_class_update'])
        
        # Class is 1 hour (10:00-11:00, calibrated to 1.02 hours)
        updated_student = StudentOrClass.objects.get(id=self.freelance_student.id)
        self.assertLess(updated_student.purchased_class_hours, initial_hours)

    def test_update_class_status_to_same_day_cancellation_deducts_hours(self):
        """Test that same day cancellation deducts hours for freelance students."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'class-status-confirmation/'

        initial_hours = self.freelance_student.purchased_class_hours

        data = {
            'id': self.scheduled_class1.id,
            'class_status': 'same_day_cancellation',
            'teacher_notes': 'Student cancelled same day',
            'class_content': ''
        }

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIsNotNone(response.data['student_or_class_update'])
        
        updated_student = StudentOrClass.objects.get(id=self.freelance_student.id)
        self.assertLess(updated_student.purchased_class_hours, initial_hours)

    def test_update_class_status_to_cancelled_no_deduction(self):
        """Test that regular cancellation does not deduct hours."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'class-status-confirmation/'

        initial_hours = self.freelance_student.purchased_class_hours

        data = {
            'id': self.scheduled_class1.id,
            'class_status': 'cancelled',
            'teacher_notes': 'Cancelled in advance',
            'class_content': ''
        }

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIsNone(response.data['student_or_class_update'])
        
        updated_student = StudentOrClass.objects.get(id=self.freelance_student.id)
        self.assertEqual(updated_student.purchased_class_hours, initial_hours)

    def test_update_class_status_from_completed_to_scheduled_adds_hours_back(self):
        """Test that changing from completed to scheduled adds hours back."""
        self.client.force_authenticate(user=self.user1)
        
        # First complete the class
        url = self.base_url + 'class-status-confirmation/'
        data = {
            'id': self.scheduled_class1.id,
            'class_status': 'completed',
            'teacher_notes': 'Completed',
            'class_content': 'Done'
        }
        self.client.patch(url, data, format='json')

        # Get hours after completion
        student_after_completion = StudentOrClass.objects.get(id=self.freelance_student.id)
        hours_after_completion = student_after_completion.purchased_class_hours

        # Now change back to scheduled
        data['class_status'] = 'scheduled'
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIsNotNone(response.data['student_or_class_update'])
        
        updated_student = StudentOrClass.objects.get(id=self.freelance_student.id)
        self.assertGreater(updated_student.purchased_class_hours, hours_after_completion)

    def test_update_class_status_school_student_no_hour_changes(self):
        """Test that school students don't have hour deductions."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'class-status-confirmation/'

        # Change status back to scheduled first
        ScheduledClass.objects.filter(id=self.scheduled_class2.id).update(
            class_status='scheduled'
        )

        data = {
            'id': self.scheduled_class2.id,
            'class_status': 'completed',
            'teacher_notes': 'School class completed',
            'class_content': 'Lesson done'
        }

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIsNone(response.data['student_or_class_update'])

    def test_update_class_status_creates_modification_record(self):
        """Test that hour modifications create a record."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'class-status-confirmation/'

        initial_record_count = PurchasedHoursModificationRecord.objects.count()

        data = {
            'id': self.scheduled_class1.id,
            'class_status': 'completed',
            'teacher_notes': 'Completed',
            'class_content': 'Done'
        }

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        
        # Verify a modification record was created
        final_record_count = PurchasedHoursModificationRecord.objects.count()
        self.assertEqual(final_record_count, initial_record_count + 1)

    def test_update_class_status_nonexistent_class(self):
        """Test updating status of non-existent class."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'class-status-confirmation/'

        data = {
            'id': 99999,
            'class_status': 'completed',
            'teacher_notes': 'Test',
            'class_content': 'Test'
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ScheduledClassBatchDeletionTests(ClassSchedulingAPITestCase):
    """Test cases for ScheduledClassBatchDeletionView."""

    def test_batch_delete_unauthenticated(self):
        """Test that unauthenticated users cannot batch delete classes."""
        url = self.base_url + 'classes/batch-delete/'
        data = {'obsolete_class_ids': [self.scheduled_class1.id]}

        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_batch_delete_success(self):
        """Test successful batch deletion of scheduled classes."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'classes/batch-delete/'

        # Create additional classes to delete
        class3 = ScheduledClass.objects.create(
            student_or_class=self.freelance_student,
            teacher=self.teacher1_profile,
            date=datetime.date(2024, 12, 16),
            start_time=datetime.time(10, 0),
            finish_time=datetime.time(11, 0),
            class_status='scheduled'
        )

        ids_to_delete = [self.scheduled_class1.id, class3.id]
        data = {'obsolete_class_ids': ids_to_delete}

        response = self.client.delete(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ids'], ids_to_delete)
        self.assertEqual(response.data['message'], 'Batch Deletion Successful!')

        # Verify classes were deleted
        self.assertFalse(
            ScheduledClass.objects.filter(id__in=ids_to_delete).exists()
        )

    def test_batch_delete_nonexistent_classes(self):
        """Test batch deletion of non-existent classes."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'classes/batch-delete/'

        data = {'obsolete_class_ids': [99999, 99998]}

        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Error', response.data)

    def test_batch_delete_empty_list(self):
        """Test batch deletion with empty list."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'classes/batch-delete/'

        data = {'obsolete_class_ids': []}

        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_batch_delete_single_class(self):
        """Test batch deletion with single class."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'classes/batch-delete/'

        data = {'obsolete_class_ids': [self.scheduled_class1.id]}

        response = self.client.delete(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            ScheduledClass.objects.filter(id=self.scheduled_class1.id).exists()
        )


class ScheduledClassByTeacherByDateTests(ClassSchedulingAPITestCase):
    """Test cases for ScheduledClassByTeacherByDateViewSet."""

    def test_get_classes_by_date_unauthenticated(self):
        """Test that unauthenticated users cannot access classes by date."""
        url = self.base_url + 'classes/by-teacher/by-date/2024-12-15/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_classes_by_date_success(self):
        """Test successful retrieval of classes for a specific date."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'classes/by-teacher/by-date/2024-12-15/'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Both classes on this date
        
        # Verify ordering by start_time
        self.assertLessEqual(
            response.data[0]['start_time'],
            response.data[1]['start_time']
        )

    def test_get_classes_by_date_no_classes(self):
        """Test retrieval of classes for a date with no classes."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'classes/by-teacher/by-date/2024-12-25/'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_classes_by_date_filters_by_teacher(self):
        """Test that classes are filtered by the authenticated teacher."""
        # Create a class for teacher2
        ScheduledClass.objects.create(
            student_or_class=self.freelance_student,
            teacher=self.teacher2_profile,
            date=datetime.date(2024, 12, 15),
            start_time=datetime.time(13, 0),
            finish_time=datetime.time(14, 0),
            class_status='scheduled'
        )

        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'classes/by-teacher/by-date/2024-12-15/'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only return teacher1's classes (2), not teacher2's
        self.assertEqual(len(response.data), 2)


class ScheduledClassByTeacherByMonthTests(ClassSchedulingAPITestCase):
    """Test cases for ScheduledClassByTeacherByMonthViewSet."""

    def test_get_classes_by_month_unauthenticated(self):
        """Test that unauthenticated users cannot access classes by month."""
        url = self.base_url + 'classes/by-teacher/by-month-year/12/2024/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_classes_by_month_success(self):
        """Test successful retrieval of classes for a specific month."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'classes/by-teacher/by-month-year/12/2024/'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should include scheduled_class1 and scheduled_class2 from December
        self.assertGreaterEqual(len(response.data), 2)

    def test_get_classes_by_month_december_boundary(self):
        """Test retrieval for December (special case for year boundary)."""
        self.client.force_authenticate(user=self.user1)
        
        # Create a class in December 2024
        ScheduledClass.objects.create(
            student_or_class=self.freelance_student,
            teacher=self.teacher1_profile,
            date=datetime.date(2024, 12, 31),
            start_time=datetime.time(10, 0),
            finish_time=datetime.time(11, 0),
            class_status='scheduled'
        )

        url = self.base_url + 'classes/by-teacher/by-month-year/12/2024/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should include the December 31 class
        dates = [item['date'] for item in response.data]
        self.assertIn('2024-12-31', dates)

    def test_get_classes_by_month_filters_by_teacher(self):
        """Test that classes are filtered by the authenticated teacher."""
        # Create classes for teacher2 in December
        ScheduledClass.objects.create(
            student_or_class=self.freelance_student,
            teacher=self.teacher2_profile,
            date=datetime.date(2024, 12, 20),
            start_time=datetime.time(10, 0),
            finish_time=datetime.time(11, 0),
            class_status='scheduled'
        )

        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'classes/by-teacher/by-month-year/12/2024/'

        response = self.client.get(url)

        # Verify all returned classes belong to teacher1
        for class_data in response.data:
            self.assertEqual(class_data['teacher'], self.teacher1_profile.id)

    def test_get_classes_by_month_ordering(self):
        """Test that classes are ordered by date and start_time."""
        self.client.force_authenticate(user=self.user1)
        
        # Create classes on different dates
        ScheduledClass.objects.create(
            student_or_class=self.freelance_student,
            teacher=self.teacher1_profile,
            date=datetime.date(2024, 12, 10),
            start_time=datetime.time(15, 0),
            finish_time=datetime.time(16, 0),
            class_status='scheduled'
        )
        
        ScheduledClass.objects.create(
            student_or_class=self.freelance_student,
            teacher=self.teacher1_profile,
            date=datetime.date(2024, 12, 10),
            start_time=datetime.time(9, 0),
            finish_time=datetime.time(10, 0),
            class_status='scheduled'
        )

        url = self.base_url + 'classes/by-teacher/by-month-year/12/2024/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify ordering
        for i in range(len(response.data) - 1):
            current_date = response.data[i]['date']
            next_date = response.data[i + 1]['date']
            self.assertLessEqual(current_date, next_date)


class ScheduledClassGoogleCalendarTests(ClassSchedulingAPITestCase):
    """Test cases for ScheduledClassGoogleCalendarViewSet."""

    def test_get_google_calendar_classes_unauthenticated(self):
        """Test that unauthenticated users cannot access Google Calendar view."""
        url = self.base_url + 'classes/google-calendar/by-month-year/12/2024/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_google_calendar_classes_success(self):
        """Test successful retrieval of classes for Google Calendar."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'classes/google-calendar/by-month-year/12/2024/'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)
        
        # Verify response contains expected fields
        if len(response.data) > 0:
            expected_fields = {
                'id', 'student_or_class', 'date', 'teacher',
                'start_time', 'finish_time', 'class_status'
            }
            self.assertTrue(all(field in response.data[0] for field in expected_fields))

    def test_get_google_calendar_classes_nested_serializers(self):
        """Test that nested serializers are used for teacher and student."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'classes/google-calendar/by-month-year/12/2024/'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if len(response.data) > 0:
            # Teacher should be nested object, not just ID
            self.assertIsInstance(response.data[0]['teacher'], dict)
            self.assertIsInstance(response.data[0]['student_or_class'], dict)


class StudentOrClassAttendanceTests(ClassSchedulingAPITestCase):
    """Test cases for StudentOrClassAttendanceViewSet."""

    def test_get_attendance_unauthenticated(self):
        """Test that unauthenticated users cannot access attendance records."""
        url = self.base_url + f'classes/student-or-class-attendance/{self.freelance_student.id}/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_attendance_success(self):
        """Test successful retrieval of attendance records."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + f'classes/student-or-class-attendance/{self.freelance_student.id}/'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should include past_scheduled_class (past date)
        self.assertGreaterEqual(len(response.data['results']), 1)

    def test_get_attendance_only_past_classes(self):
        """Test that only past classes are returned."""
        self.client.force_authenticate(user=self.user1)
        
        # Create a future class
        future_class = ScheduledClass.objects.create(
            student_or_class=self.freelance_student,
            teacher=self.teacher1_profile,
            date=datetime.date.today() + datetime.timedelta(days=5),
            start_time=datetime.time(10, 0),
            finish_time=datetime.time(11, 0),
            class_status='scheduled'
        )

        url = self.base_url + f'classes/student-or-class-attendance/{self.freelance_student.id}/'
        response = self.client.get(url)

        # Verify future class is not in results
        class_ids = [item['id'] for item in response.data['results']]
        self.assertNotIn(future_class.id, class_ids)

    def test_get_attendance_pagination(self):
        """Test that attendance records are paginated."""
        self.client.force_authenticate(user=self.user1)
        
        # Create multiple past classes (more than page_size of 3)
        for i in range(5):
            ScheduledClass.objects.create(
                student_or_class=self.freelance_student,
                teacher=self.teacher1_profile,
                date=datetime.date.today() - datetime.timedelta(days=i+3),
                start_time=datetime.time(10, 0),
                finish_time=datetime.time(11, 0),
                class_status='completed'
            )

        url = self.base_url + f'classes/student-or-class-attendance/{self.freelance_student.id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should have pagination fields
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('results', response.data)
        # First page should have max 3 results (page_size)
        self.assertLessEqual(len(response.data['results']), 3)

    def test_get_attendance_ordering(self):
        """Test that attendance records are ordered by date descending."""
        self.client.force_authenticate(user=self.user1)
        
        # Create classes on different past dates
        class1 = ScheduledClass.objects.create(
            student_or_class=self.freelance_student,
            teacher=self.teacher1_profile,
            date=datetime.date.today() - datetime.timedelta(days=5),
            start_time=datetime.time(10, 0),
            finish_time=datetime.time(11, 0),
            class_status='completed'
        )
        
        class2 = ScheduledClass.objects.create(
            student_or_class=self.freelance_student,
            teacher=self.teacher1_profile,
            date=datetime.date.today() - datetime.timedelta(days=3),
            start_time=datetime.time(10, 0),
            finish_time=datetime.time(11, 0),
            class_status='completed'
        )

        url = self.base_url + f'classes/student-or-class-attendance/{self.freelance_student.id}/'
        response = self.client.get(url)

        # Most recent date should come first
        dates = [item['date'] for item in response.data['results']]
        self.assertEqual(dates, sorted(dates, reverse=True))


class UnconfirmedStatusClassesTests(ClassSchedulingAPITestCase):
    """Test cases for UnconfirmedStatusClassesViewSet."""

    def test_get_unconfirmed_classes_unauthenticated(self):
        """Test that unauthenticated users cannot access unconfirmed classes."""
        url = self.base_url + 'classes/unconfirmed-status/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_unconfirmed_classes_success(self):
        """Test successful retrieval of unconfirmed status classes."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'classes/unconfirmed-status/'

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should include past_scheduled_class (past date with 'scheduled' status)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_unconfirmed_classes_includes_all_statuses_on_date_with_scheduled(self):
        """Test that all classes on dates with scheduled classes are returned."""
        self.client.force_authenticate(user=self.user1)
        
        past_date = datetime.date.today() - datetime.timedelta(days=5)
        
        # Create a scheduled class (unconfirmed)
        scheduled = ScheduledClass.objects.create(
            student_or_class=self.freelance_student,
            teacher=self.teacher1_profile,
            date=past_date,
            start_time=datetime.time(10, 0),
            finish_time=datetime.time(11, 0),
            class_status='scheduled'
        )
        
        # Create a completed class on the same date
        completed = ScheduledClass.objects.create(
            student_or_class=self.school_student,
            teacher=self.teacher1_profile,
            date=past_date,
            start_time=datetime.time(14, 0),
            finish_time=datetime.time(15, 0),
            class_status='completed'
        )

        url = self.base_url + 'classes/unconfirmed-status/'
        response = self.client.get(url)

        class_ids = [item['id'] for item in response.data]
        # Both classes should be included
        self.assertIn(scheduled.id, class_ids)
        self.assertIn(completed.id, class_ids)

    def test_get_unconfirmed_classes_excludes_future_dates(self):
        """Test that future classes are not included."""
        self.client.force_authenticate(user=self.user1)
        
        # Create a scheduled class in the future
        future_class = ScheduledClass.objects.create(
            student_or_class=self.freelance_student,
            teacher=self.teacher1_profile,
            date=datetime.date.today() + datetime.timedelta(days=5),
            start_time=datetime.time(10, 0),
            finish_time=datetime.time(11, 0),
            class_status='scheduled'
        )

        url = self.base_url + 'classes/unconfirmed-status/'
        response = self.client.get(url)

        class_ids = [item['id'] for item in response.data]
        self.assertNotIn(future_class.id, class_ids)

    def test_get_unconfirmed_classes_excludes_dates_with_all_confirmed(self):
        """Test that dates with only confirmed classes are excluded."""
        self.client.force_authenticate(user=self.user1)
        
        past_date = datetime.date.today() - datetime.timedelta(days=10)
        
        # Create only completed/cancelled classes on this date
        completed_only = ScheduledClass.objects.create(
            student_or_class=self.freelance_student,
            teacher=self.teacher1_profile,
            date=past_date,
            start_time=datetime.time(10, 0),
            finish_time=datetime.time(11, 0),
            class_status='completed'
        )

        url = self.base_url + 'classes/unconfirmed-status/'
        response = self.client.get(url)

        class_ids = [item['id'] for item in response.data]
        # Should not include classes from dates with no 'scheduled' status
        self.assertNotIn(completed_only.id, class_ids)

    def test_get_unconfirmed_classes_filters_by_teacher(self):
        """Test that classes are filtered by the authenticated teacher."""
        past_date = datetime.date.today() - datetime.timedelta(days=3)
        
        # Create a scheduled class for teacher2
        teacher2_class = ScheduledClass.objects.create(
            student_or_class=self.freelance_student,
            teacher=self.teacher2_profile,
            date=past_date,
            start_time=datetime.time(10, 0),
            finish_time=datetime.time(11, 0),
            class_status='scheduled'
        )

        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'classes/unconfirmed-status/'

        response = self.client.get(url)

        # Verify teacher2's class is not in results
        class_ids = [item['id'] for item in response.data]
        self.assertNotIn(teacher2_class.id, class_ids)


class ClassSchedulingEdgeCaseTests(ClassSchedulingAPITestCase):
    """Test edge cases and boundary conditions."""

    def test_create_class_at_midnight(self):
        """Test creating a class starting at midnight."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'class/submit/'

        data = {
            'student_or_class': self.freelance_student.id,
            'teacher': self.teacher1_profile.id,
            'date': '2024-12-20',
            'start_time': '00:00',
            'finish_time': '01:00',
            'class_status': 'scheduled'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_class_ending_at_midnight(self):
        """Test creating a class ending at midnight."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'class/submit/'

        data = {
            'student_or_class': self.freelance_student.id,
            'teacher': self.teacher1_profile.id,
            'date': '2024-12-20',
            'start_time': '23:00',
            'finish_time': '23:59',
            'class_status': 'scheduled'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_very_short_class_duration(self):
        """Test creating a very short class (1 minute)."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'class/submit/'

        data = {
            'student_or_class': self.freelance_student.id,
            'teacher': self.teacher1_profile.id,
            'date': '2024-12-20',
            'start_time': '10:00',
            'finish_time': '10:01',
            'class_status': 'scheduled'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_very_long_class_duration(self):
        """Test creating a very long class (8 hours)."""
        self.client.force_authenticate(user=self.user1)
        url = self.base_url + 'class/submit/'

        data = {
            'student_or_class': self.freelance_student.id,
            'teacher': self.teacher1_profile.id,
            'date': '2024-12-20',
            'start_time': '09:00',
            'finish_time': '17:00',
            'class_status': 'scheduled'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_hour_deduction_precision(self):
        """Test that hour deduction maintains proper decimal precision."""
        self.client.force_authenticate(user=self.user1)
        
        # Create a class with specific duration (1.5 hours)
        class_obj = ScheduledClass.objects.create(
            student_or_class=self.freelance_student,
            teacher=self.teacher1_profile,
            date=datetime.date.today() - datetime.timedelta(days=1),
            start_time=datetime.time(10, 0),
            finish_time=datetime.time(11, 30),
            class_status='scheduled'
        )

        initial_hours = self.freelance_student.purchased_class_hours
        
        url = self.base_url + 'class-status-confirmation/'
        data = {
            'id': class_obj.id,
            'class_status': 'completed',
            'teacher_notes': 'Test',
            'class_content': 'Test'
        }

        response = self.client.patch(url, data, format='json')
        
        updated_student = StudentOrClass.objects.get(id=self.freelance_student.id)
        # Verify precision is maintained (should be close to 1.52 hours with calibration)
        difference = initial_hours - updated_student.purchased_class_hours
        self.assertGreater(difference, Decimal('1.5'))
        self.assertLess(difference, Decimal('1.6'))
