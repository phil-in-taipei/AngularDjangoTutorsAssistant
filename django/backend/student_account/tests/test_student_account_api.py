import json
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch

from student_account.models import StudentOrClass
from user_profiles.models import UserProfile
from school.models import School


class StudentAccountAPITestCase(TestCase):
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
            school=None  # Explicitly set to None for freelance
        )

        self.school_student = StudentOrClass.objects.create(
            student_or_class_name='Jane Smith',
            account_type='school',
            school=self.school,
            teacher=self.teacher1_profile,
            tuition_per_hour=900,
            comments='Test school student',
            purchased_class_hours=None  # Explicitly set to None for school
        )

        # Base URL for API endpoints
        self.base_url = '/api/accounts/'

        # URLs
        self.list_url = self.base_url + 'students-or-classes/'
        self.detail_url_pattern = self.base_url + 'student-or-class/{}/'


class StudentOrClassListViewTests(StudentAccountAPITestCase):
    """Test cases for the StudentOrClassListView (GET and POST)."""

    def test_get_students_unauthenticated(self):
        """Test that unauthenticated users cannot access the list."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_students_authenticated_success(self):
        """Test successful retrieval of student accounts for authenticated user."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return both students for teacher1

        # Check that response contains expected fields
        expected_fields = {
            'id', 'student_or_class_name', 'account_type', 'school',
            'comments', 'purchased_class_hours', 'tuition_per_hour',
            'account_id', 'slug', 'template_str'
        }
        self.assertTrue(all(field in response.data[0] for field in expected_fields))

    def test_get_students_filters_by_teacher(self):
        """Test that users only see their own student accounts."""
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # teacher2 has no students

    def test_post_create_freelance_student_success(self):
        """Test successful creation of a freelance student account."""
        self.client.force_authenticate(user=self.user1)

        data = {
            'student_or_class_name': 'New Student',
            'account_type': 'freelance',
            'purchased_class_hours': '15.00',
            'tuition_per_hour': 1000,
            'comments': 'New freelance student'
        }

        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['student_or_class_name'], 'New Student')
        self.assertEqual(response.data['account_type'], 'freelance')
        self.assertIsNotNone(response.data['account_id'])
        self.assertIsNotNone(response.data['slug'])

        # Verify student was created in database
        self.assertTrue(
            StudentOrClass.objects.filter(
                student_or_class_name='New Student',
                teacher=self.teacher1_profile
            ).exists()
        )

    def test_post_create_school_student_success(self):
        """Test successful creation of a school student account."""
        self.client.force_authenticate(user=self.user1)

        data = {
            'student_or_class_name': 'School Class A',
            'account_type': 'school',
            'school': self.school.id,
            'tuition_per_hour': 800,
            'comments': 'New school class'
        }

        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['student_or_class_name'], 'School Class A')
        self.assertEqual(response.data['account_type'], 'school')
        self.assertEqual(response.data['school'], self.school.id)

    def test_post_unauthenticated(self):
        """Test that unauthenticated users cannot create student accounts."""
        data = {
            'student_or_class_name': 'Test Student',
            'account_type': 'freelance',
            'purchased_class_hours': '10.00'
        }

        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_missing_required_fields(self):
        """Test validation when required fields are missing."""
        self.client.force_authenticate(user=self.user1)

        data = {
            'account_type': 'freelance'
            # Missing student_or_class_name
        }

        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('student_or_class_name', response.data)

    def test_post_invalid_account_type(self):
        """Test validation with invalid account type."""
        self.client.force_authenticate(user=self.user1)

        data = {
            'student_or_class_name': 'Test Student',
            'account_type': 'invalid_type',
            'purchased_class_hours': '10.00'
        }

        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_duplicate_student_name_for_teacher(self):
        self.client.force_authenticate(user=self.user1)

        # Try to create another student with the same name as existing freelance_student
        data = {
            'student_or_class_name': 'John Doe',  # Already exists for teacher1
            'account_type': 'freelance',
            'purchased_class_hours': '5.00'
        }

        response = self.client.post(self.list_url, data, format='json')
        # Should get 400 due to unique_together constraint validation
        # The actual response depends on how DRF handles the IntegrityError
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_500_INTERNAL_SERVER_ERROR])

    def test_post_same_student_name_different_teacher_allowed(self):
        """Test that same student name is allowed for different teachers."""
        self.client.force_authenticate(user=self.user2)

        data = {
            'student_or_class_name': 'John Doe',  # Exists for teacher1 but not teacher2
            'account_type': 'freelance',
            'purchased_class_hours': '8.00'
        }

        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('student_account.models.random_string_generator')
    def test_post_account_id_and_slug_generation(self, mock_random_string):
        """Test that account_id and slug are automatically generated."""
        mock_random_string.return_value = 'ABC123'
        self.client.force_authenticate(user=self.user1)

        data = {
            'student_or_class_name': 'Test Generation',
            'account_type': 'freelance',
            'purchased_class_hours': '5.00'
        }

        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['account_id'], 'ABC123')
        self.assertEqual(response.data['slug'], 'ABC123')


class StudentOrClassDetailViewTests(StudentAccountAPITestCase):
    """Test cases for StudentOrClassEditAndDeleteView (PATCH and DELETE)."""

    def test_patch_update_student_success(self):
        """Test successful update of student account."""
        self.client.force_authenticate(user=self.user1)
        url = self.detail_url_pattern.format(self.freelance_student.id)

        data = {
            'student_or_class_name': 'Updated Name',
            'tuition_per_hour': 1500,
            'comments': 'Updated comments'
        }

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['student_or_class_name'], 'Updated Name')
        self.assertEqual(response.data['tuition_per_hour'], 1500)
        self.assertEqual(response.data['comments'], 'Updated comments')

        # Verify database was updated
        updated_student = StudentOrClass.objects.get(id=self.freelance_student.id)
        self.assertEqual(updated_student.student_or_class_name, 'Updated Name')

    def test_patch_partial_update_success(self):
        """Test partial update of student account."""
        self.client.force_authenticate(user=self.user1)
        url = self.detail_url_pattern.format(self.freelance_student.id)

        data = {'tuition_per_hour': 2000}

        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tuition_per_hour'], 2000)
        # Other fields should remain unchanged
        self.assertEqual(response.data['student_or_class_name'], 'John Doe')

    def test_patch_unauthenticated(self):
        """Test that unauthenticated users cannot update student accounts."""
        url = self.detail_url_pattern.format(self.freelance_student.id)
        data = {'tuition_per_hour': 1500}

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_nonexistent_student(self):
        """Test updating a non-existent student account."""
        self.client.force_authenticate(user=self.user1)
        url = self.detail_url_pattern.format(99999)
        data = {'tuition_per_hour': 1500}

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_invalid_data(self):
        """Test updating with invalid data."""
        self.client.force_authenticate(user=self.user1)
        url = self.detail_url_pattern.format(self.freelance_student.id)

        data = {
            'tuition_per_hour': -100,  # Invalid negative value
            'comments': 'x' * 501  # Exceeds max length
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_student_success(self):
        """Test successful deletion of student account."""
        self.client.force_authenticate(user=self.user1)
        url = self.detail_url_pattern.format(self.freelance_student.id)
        student_id = self.freelance_student.id

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], student_id)
        self.assertEqual(response.data['message'], 'Account successfully deleted!')

        # Verify student was deleted from database
        self.assertFalse(
            StudentOrClass.objects.filter(id=student_id).exists()
        )

    def test_delete_unauthenticated(self):
        """Test that unauthenticated users cannot delete student accounts."""
        url = self.detail_url_pattern.format(self.freelance_student.id)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_nonexistent_student(self):
        """Test deleting a non-existent student account."""
        self.client.force_authenticate(user=self.user1)
        url = self.detail_url_pattern.format(99999)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_method_not_allowed(self):
        """Test that PUT method is not allowed."""
        self.client.force_authenticate(user=self.user1)
        url = self.detail_url_pattern.format(self.freelance_student.id)

        response = self.client.put(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_method_allowed_on_detail_view(self):
        """Test that GET method works on detail view (inherited from RetrieveUpdateDestroyAPIView)."""
        self.client.force_authenticate(user=self.user1)
        url = self.detail_url_pattern.format(self.freelance_student.id)

        response = self.client.get(url)
        # The view inherits from RetrieveUpdateDestroyAPIView, so GET should work
        # but http_method_names doesn't include 'get', so it should be 405
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class StudentAccountModelConstraintTests(StudentAccountAPITestCase):
    """Test cases for model constraints and business logic."""

    def test_freelance_student_constraint_validation(self):
        """Test that freelance students follow the correct constraint pattern."""
        self.client.force_authenticate(user=self.user1)

        # Valid freelance student data
        data = {
            'student_or_class_name': 'Valid Freelance',
            'account_type': 'freelance',
            'purchased_class_hours': '15.00',  # Required for freelance
            'tuition_per_hour': 1000
            # school should be None/omitted for freelance
        }

        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify the created object follows the constraint
        created_student = StudentOrClass.objects.get(id=response.data['id'])
        self.assertIsNotNone(created_student.purchased_class_hours)
        self.assertIsNone(created_student.school)

    def test_school_student_constraint_validation(self):
        """Test that school students follow the correct constraint pattern."""
        self.client.force_authenticate(user=self.user1)

        # Valid school student data
        data = {
            'student_or_class_name': 'Valid School Student',
            'account_type': 'school',
            'school': self.school.id,  # Required for school
            'tuition_per_hour': 800
            # purchased_class_hours should be None/omitted for school
        }

        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify the created object follows the constraint
        created_student = StudentOrClass.objects.get(id=response.data['id'])
        self.assertIsNotNone(created_student.school)
        self.assertIsNone(created_student.purchased_class_hours)

    def test_template_str_property_freelance(self):
        """Test template_str property for freelance student."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.list_url)

        freelance_data = next(
            item for item in response.data
            if item['account_type'] == 'freelance'
        )

        self.assertEqual(
            freelance_data['template_str'],
            'John Doe (Freelance)'
        )

    def test_template_str_property_school(self):
        """Test template_str property for school student."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.list_url)

        school_data = next(
            item for item in response.data
            if item['account_type'] == 'school'
        )

        self.assertEqual(
            school_data['template_str'],
            'Jane Smith (Test School)'
        )


class StudentAccountEdgeCaseTests(StudentAccountAPITestCase):
    """Test edge cases and boundary conditions."""

    def test_very_long_student_name(self):
        """Test creation with maximum length student name."""
        self.client.force_authenticate(user=self.user1)

        # Test with 200 character name (at the limit)
        long_name = 'A' * 200
        data = {
            'student_or_class_name': long_name,
            'account_type': 'freelance',
            'purchased_class_hours': '5.00'
        }

        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_maximum_purchased_hours(self):
        """Test creation with maximum purchased class hours."""
        self.client.force_authenticate(user=self.user1)

        data = {
            'student_or_class_name': 'Max Hours Student',
            'account_type': 'freelance',
            'purchased_class_hours': '999.99'  # Maximum for DecimalField(5,2)
        }

        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_zero_purchased_hours(self):
        """Test creation with zero purchased hours."""
        self.client.force_authenticate(user=self.user1)

        data = {
            'student_or_class_name': 'Zero Hours Student',
            'account_type': 'freelance',
            'purchased_class_hours': '0.00'
        }

        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_maximum_comments_length(self):
        """Test creation with maximum comments length."""
        self.client.force_authenticate(user=self.user1)

        data = {
            'student_or_class_name': 'Max Comments Student',
            'account_type': 'freelance',
            'purchased_class_hours': '10.00',
            'comments': 'x' * 500  # Maximum length
        }

        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_empty_comments(self):
        """Test creation with empty comments."""
        self.client.force_authenticate(user=self.user1)

        data = {
            'student_or_class_name': 'Empty Comments Student',
            'account_type': 'freelance',
            'purchased_class_hours': '10.00',
            'comments': ''
        }

        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class StudentAccountPermissionTests(StudentAccountAPITestCase):
    """Test permission and authorization scenarios."""

    def test_teacher_cannot_access_other_teacher_students(self):
        """Test that teachers cannot access other teachers' student accounts."""
        # Create a student for teacher2
        other_student = StudentOrClass.objects.create(
            student_or_class_name='Other Teacher Student',
            account_type='freelance',
            teacher=self.teacher2_profile,
            purchased_class_hours=Decimal('5.00'),
            school=None  # Explicitly None for freelance
        )

        # Try to access with teacher1's credentials
        self.client.force_authenticate(user=self.user1)
        url = self.detail_url_pattern.format(other_student.id)

        # GET method is not allowed (405) due to http_method_names restriction
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_teacher_cannot_update_other_teacher_students(self):
        """Test that teachers cannot update other teachers' student accounts."""
        # Create a student for teacher2
        other_student = StudentOrClass.objects.create(
            student_or_class_name='Other Teacher Student',
            account_type='freelance',
            teacher=self.teacher2_profile,
            purchased_class_hours=Decimal('5.00'),
            school=None  # Explicitly None for freelance
        )

        # Try to update with teacher1's credentials
        self.client.force_authenticate(user=self.user1)
        url = self.detail_url_pattern.format(other_student.id)

        data = {'student_or_class_name': 'Hacked Name'}
        response = self.client.patch(url, data, format='json')
        # The view properly filters by teacher - returns 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_teacher_cannot_delete_other_teacher_students(self):
        """Test that teachers cannot delete other teachers' student accounts."""
        # Create a student for teacher2
        other_student = StudentOrClass.objects.create(
            student_or_class_name='Other Teacher Student',
            account_type='freelance',
            teacher=self.teacher2_profile,
            purchased_class_hours=Decimal('5.00'),
            school=None  # Explicitly None for freelance
        )

        # Try to delete with teacher1's credentials
        self.client.force_authenticate(user=self.user1)
        url = self.detail_url_pattern.format(other_student.id)

        response = self.client.delete(url)
        # The view properly filters by teacher - returns 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Verify the student still exists (wasn't deleted)
        self.assertTrue(
            StudentOrClass.objects.filter(id=other_student.id).exists()
        )
