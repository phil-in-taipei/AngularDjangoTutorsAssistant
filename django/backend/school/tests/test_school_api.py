import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from school.models import School
from school.serializers import SchoolSerializer
from user_profiles.models import UserProfile

User = get_user_model()

SCHOOLS_LIST_URL = '/api/schools/users-schools/'
SCHOOL_DETAIL_URL = '/api/schools/users-school/{id}/'


def get_test_user():
    return User.objects.create_user(
        'testuser',
        'testpassword'
    )


def get_test_user_profile(user):
    return UserProfile.objects.create(
        user=user,
        contact_email="testemail@gmx.com",
        surname="McTest",
        given_name="Testy"
    )


def get_test_school_data(teacher_id):
    return {
        'school_name': 'Test Elementary School',
        'address_line_1': '123 Main Street',
        'address_line_2': 'Suite 100',
        'contact_phone': '1234567890',
        'other_information': 'A great school for testing'
    }


class SchoolPublicApiTests(TestCase):
    """Test the publicly available schools API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required_schools_list(self):
        """Test that login required for retrieving schools list"""
        print("Test that login required for retrieving schools list")
        res = self.client.get(SCHOOLS_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_school_detail(self):
        """Test that login required for retrieving school detail"""
        print("Test that login required for retrieving school detail")
        res = self.client.get(SCHOOL_DETAIL_URL.format(id=1))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_school_create(self):
        """Test that login required for creating school"""
        print("Test that login required for creating school")
        payload = get_test_school_data(1)
        res = self.client.post(
            SCHOOLS_LIST_URL,
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_school_update(self):
        """Test that login required for updating school"""
        print("Test that login required for updating school")
        payload = {'school_name': 'Updated School Name'}
        res = self.client.patch(
            SCHOOL_DETAIL_URL.format(id=1),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_school_delete(self):
        """Test that login required for deleting school"""
        print("Test that login required for deleting school")
        res = self.client.delete(SCHOOL_DETAIL_URL.format(id=1))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class SchoolPrivateApiTests(TestCase):
    """Test the privately available schools API"""

    def setUp(self):
        self.client = APIClient()
        self.test_user = get_test_user()
        self.test_user_profile = get_test_user_profile(self.test_user)
        self.client.force_authenticate(self.test_user)

        # Create a test school
        self.test_school = School.objects.create(
            school_name='Test Elementary School',
            address_line_1='123 Main Street',
            address_line_2='Suite 100',
            contact_phone='1234567890',
            other_information='A great school for testing',
            scheduling_teacher=self.test_user_profile
        )

    def test_retrieve_schools_list(self):
        """Test retrieving schools list for authenticated user"""
        print("Test retrieving schools list for authenticated user")

        res = self.client.get(SCHOOLS_LIST_URL)

        schools = School.objects.filter(scheduling_teacher__user=self.test_user)
        serializer = SchoolSerializer(schools, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 1)

    def test_create_school_success(self):
        """Test creating a new school successfully"""
        print("Test creating a new school successfully")

        payload = {
            'school_name': 'New Test School',
            'address_line_1': '456 Oak Avenue',
            'address_line_2': 'Building B',
            'contact_phone': '9876543210',
            'other_information': 'Another great school'
        }

        res = self.client.post(
            SCHOOLS_LIST_URL,
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['school_name'], payload['school_name'])
        self.assertEqual(res.data['address_line_1'], payload['address_line_1'])

        # Verify school was created in database
        school_exists = School.objects.filter(
            school_name=payload['school_name'],
            scheduling_teacher=self.test_user_profile
        ).exists()
        self.assertTrue(school_exists)

    def test_create_school_invalid_phone(self):
        """Test creating school with invalid phone number"""
        print("Test creating school with invalid phone number")

        payload = get_test_school_data(self.test_user_profile.id)
        payload['contact_phone'] = '123'  # Invalid phone number

        res = self.client.post(
            SCHOOLS_LIST_URL,
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('contact_phone', res.data)

    def test_create_school_missing_required_fields(self):
        """Test creating school with missing required fields"""
        print("Test creating school with missing required fields")

        payload = {
            'address_line_1': '456 Oak Avenue',
        }

        res = self.client.post(
            SCHOOLS_LIST_URL,
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('school_name', res.data)

    def test_update_school_success(self):
        """Test updating school successfully"""
        print("Test updating school successfully")

        # Include all required fields as your frontend would
        payload = {
            'school_name': 'Updated School Name',
            'address_line_1': 'Updated Address',
            'address_line_2': 'Updated Address Line 2',
            'contact_phone': '9876543210',
            'other_information': 'Updated information'
        }

        res = self.client.patch(
            SCHOOL_DETAIL_URL.format(id=self.test_school.id),
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.test_school.refresh_from_db()
        self.assertEqual(self.test_school.school_name, payload['school_name'])
        self.assertEqual(self.test_school.address_line_1, payload['address_line_1'])
        self.assertEqual(self.test_school.address_line_2, payload['address_line_2'])
        self.assertEqual(self.test_school.contact_phone, payload['contact_phone'])
        self.assertEqual(self.test_school.other_information, payload['other_information'])

    def test_update_school_partial(self):
        """Test updating school with all fields (simulating frontend behavior)"""
        print("Test updating school with all fields (simulating frontend behavior)")

        original_name = self.test_school.school_name

        # Send all fields but only change some values (as frontend would do)
        payload = {
            'school_name': original_name,  # Keep original
            'address_line_1': 'New Address Only',  # Change this
            'address_line_2': self.test_school.address_line_2,  # Keep original
            'contact_phone': self.test_school.contact_phone,  # Keep original
            'other_information': self.test_school.other_information  # Keep original
        }

        res = self.client.patch(
            SCHOOL_DETAIL_URL.format(id=self.test_school.id),
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.test_school.refresh_from_db()
        self.assertEqual(self.test_school.address_line_1, payload['address_line_1'])
        # Other fields should remain unchanged
        self.assertEqual(self.test_school.school_name, original_name)

    def test_delete_school_success(self):
        """Test deleting school successfully"""
        print("Test deleting school successfully")

        school_id = self.test_school.id

        res = self.client.delete(SCHOOL_DETAIL_URL.format(id=school_id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['id'], school_id)
        self.assertEqual(res.data['message'], "School successfully deleted!")

        # Verify school was deleted from database
        school_exists = School.objects.filter(id=school_id).exists()
        self.assertFalse(school_exists)

    def test_update_nonexistent_school(self):
        """Test updating non-existent school"""
        print("Test updating non-existent school")

        payload = {'school_name': 'Updated Name'}

        res = self.client.patch(
            SCHOOL_DETAIL_URL.format(id=9999),  # Non-existent ID
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_school(self):
        """Test deleting non-existent school"""
        print("Test deleting non-existent school")

        res = self.client.delete(SCHOOL_DETAIL_URL.format(id=9999))  # Non-existent ID

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_only_see_own_schools(self):
        """Test that user can only see their own schools"""
        print("Test that user can only see their own schools")

        # Create another user and their school
        other_user = User.objects.create_user('otheruser', 'password')
        other_profile = get_test_user_profile(other_user)
        other_school = School.objects.create(
            school_name='Other User School',
            address_line_1='999 Other Street',
            address_line_2='Other Suite',
            contact_phone='5555555555',
            scheduling_teacher=other_profile
        )

        res = self.client.get(SCHOOLS_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)  # Should only see own school
        self.assertEqual(res.data[0]['id'], self.test_school.id)
        self.assertNotEqual(res.data[0]['id'], other_school.id)

    def test_create_duplicate_school_name_for_same_teacher(self):
        """Test creating duplicate school name for same teacher (should fail due to unique_together)"""
        print("Test creating duplicate school name for same teacher")

        payload = {
            'school_name': self.test_school.school_name,  # Same name as existing school
            'address_line_1': '456 Different Street',
            'address_line_2': 'Different Suite',
            'contact_phone': '9876543210',
        }

        res = self.client.post(
            SCHOOLS_LIST_URL,
            data=json.dumps(payload),
            content_type='application/json'
        )

        # With improved view, this should return 400 with proper error message
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', res.data)

    def test_empty_schools_list(self):
        """Test retrieving empty schools list"""
        print("Test retrieving empty schools list")

        # Delete the test school
        self.test_school.delete()

        res = self.client.get(SCHOOLS_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 0)
