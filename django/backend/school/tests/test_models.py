from django.test import TestCase
from django.contrib.auth import get_user_model

from school.models import School
from user_profiles.models import UserProfile


class SchoolModelTests(TestCase):
    """Test the School Model"""

    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            'testuser',
            'testpassword'
        )
        self.test_user_profile = UserProfile.objects.create(
            user=self.test_user,
            contact_email="testemail@gmx.com",
            surname="McTest",
            given_name="Testy"
        )
        self.test_school = School.objects.create(
            school_name="Test School",
            address_line_1="1234 A Street Name",
            address_line_2="Taipei, Taiwan",
            contact_phone="0222222222",
            other_information="This is the test school",
            scheduling_teacher=self.test_user_profile
        )

    def test_school_fields(self):
        """Test the school fields"""
        print("Test the school fields")
        self.assertEqual(
            self.test_school.school_name,
            'Test School'
        )
        self.assertEqual(
            self.test_school.address_line_1,
            '1234 A Street Name'
        )
        self.assertEqual(
            self.test_school.address_line_2,
            'Taipei, Taiwan'
        )
        self.assertEqual(
            self.test_school.contact_phone,
            '0222222222'
        )
        self.assertEqual(
            self.test_school.other_information,
            'This is the test school'
        )
        self.assertEqual(
            self.test_school.scheduling_teacher, self.test_user_profile
        )

    def test_school_str(self):
        """Test the school model string"""
        print("Test the school string")
        self.assertEqual(
            str(self.test_school),
            F"{str(self.test_school.scheduling_teacher)}: {self.test_school.school_name}"
        )

