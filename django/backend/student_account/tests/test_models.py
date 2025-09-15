from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from decimal import Decimal

from school.models import School
from student_account.models import StudentOrClass
from user_profiles.models import UserProfile


class StudentOrClassModelTests(TestCase):
    """Test the StudentOrClass Model"""

    def setUp(self):
        # Create test user and profile
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

        # Create test school
        self.test_school = School.objects.create(
            school_name="Test School",
            address_line_1="1234 A Street Name",
            address_line_2="Taipei, Taiwan",
            contact_phone="0222222222",
            other_information="This is the test school",
            scheduling_teacher=self.test_user_profile
        )

        # Create freelance student
        self.freelance_student = StudentOrClass.objects.create(
            student_or_class_name="John Doe",
            account_type='freelance',
            teacher=self.test_user_profile,
            comments="Freelance student comments",
            purchased_class_hours=Decimal('10.50'),
            tuition_per_hour=1200
        )

        # Create school student
        self.school_student = StudentOrClass.objects.create(
            student_or_class_name="Jane Smith",
            account_type='school',
            school=self.test_school,
            teacher=self.test_user_profile,
            comments="School student comments",
            tuition_per_hour=800
        )

    def test_freelance_student_fields(self):
        """Test the freelance student fields"""
        print("Test the freelance student fields")
        self.assertEqual(
            self.freelance_student.student_or_class_name,
            'John Doe'
        )
        self.assertEqual(
            self.freelance_student.account_type,
            'freelance'
        )
        self.assertIsNone(self.freelance_student.school)
        self.assertEqual(
            self.freelance_student.teacher,
            self.test_user_profile
        )
        self.assertEqual(
            self.freelance_student.comments,
            'Freelance student comments'
        )
        self.assertEqual(
            self.freelance_student.purchased_class_hours,
            Decimal('10.50')
        )
        self.assertEqual(
            self.freelance_student.tuition_per_hour,
            1200
        )
        # Test that account_id and slug are auto-generated
        self.assertIsNotNone(self.freelance_student.account_id)
        self.assertIsNotNone(self.freelance_student.slug)
        self.assertEqual(len(self.freelance_student.account_id), 10)

    def test_school_student_fields(self):
        """Test the school student fields"""
        print("Test the school student fields")
        self.assertEqual(
            self.school_student.student_or_class_name,
            'Jane Smith'
        )
        self.assertEqual(
            self.school_student.account_type,
            'school'
        )
        self.assertEqual(
            self.school_student.school,
            self.test_school
        )
        self.assertEqual(
            self.school_student.teacher,
            self.test_user_profile
        )
        self.assertEqual(
            self.school_student.comments,
            'School student comments'
        )
        self.assertIsNone(self.school_student.purchased_class_hours)
        self.assertEqual(
            self.school_student.tuition_per_hour,
            800
        )

    def test_freelance_student_str(self):
        """Test the freelance student model string representation"""
        print("Test the freelance student string")
        expected_str = "Freelance student: John Doe"
        self.assertEqual(str(self.freelance_student), expected_str)

    def test_school_student_str(self):
        """Test the school student model string representation"""
        print("Test the school student string")
        expected_str = f"School ({self.test_school.school_name}): Jane Smith"
        self.assertEqual(str(self.school_student), expected_str)

    def test_freelance_template_str(self):
        """Test the freelance student template_str property"""
        print("Test the freelance student template_str")
        expected_template = "John Doe (Freelance)"
        self.assertEqual(self.freelance_student.template_str, expected_template)

    def test_school_template_str(self):
        """Test the school student template_str property"""
        print("Test the school student template_str")
        expected_template = f"Jane Smith ({self.test_school.school_name})"
        self.assertEqual(self.school_student.template_str, expected_template)

    def test_default_values(self):
        """Test model default values"""
        print("Test default values")
        student = StudentOrClass.objects.create(
            student_or_class_name="Default Test",
            teacher=self.test_user_profile,
            purchased_class_hours=Decimal('5.00')
        )
        self.assertEqual(student.account_type, 'freelance')
        self.assertEqual(student.comments, '')
        self.assertEqual(student.tuition_per_hour, 900)

    def test_unique_together_constraint(self):
        """Test that teacher and student_or_class_name must be unique together"""
        print("Test unique together constraint")
        with self.assertRaises(IntegrityError):
            StudentOrClass.objects.create(
                student_or_class_name="John Doe",  # Same name as existing
                account_type='freelance',
                teacher=self.test_user_profile,  # Same teacher as existing
                purchased_class_hours=Decimal('5.00')
            )

    def test_custom_manager_under_two_hours(self):
        """Test the custom manager under_two_hours method"""
        print("Test custom manager under_two_hours")
        # Create student with under 2 hours
        under_two_student = StudentOrClass.objects.create(
            student_or_class_name="Under Two",
            teacher=self.test_user_profile,
            purchased_class_hours=Decimal('1.50')
        )

        under_two_accounts = StudentOrClass.custom_query.under_two_hours()

        # Should include the under_two_student but not freelance_student (10.50 hours)
        account_names = [account.student_or_class_name for account in under_two_accounts]
        self.assertIn("Under Two", account_names)
        self.assertNotIn("John Doe", account_names)

    def test_pre_save_signal_generates_account_id_and_slug(self):
        """Test that pre_save signal generates account_id and slug"""
        print("Test pre_save signal generates account_id and slug")
        new_student = StudentOrClass.objects.create(
            student_or_class_name="Signal Test",
            teacher=self.test_user_profile,
            purchased_class_hours=Decimal('3.00')
        )

        # Both should be generated and equal (from the same random string)
        self.assertIsNotNone(new_student.account_id)
        self.assertIsNotNone(new_student.slug)
        self.assertEqual(new_student.account_id, new_student.slug)
        self.assertEqual(len(new_student.account_id), 10)

    def test_check_constraint_school_type_validation(self):
        """Test that school type requires school and no purchased_class_hours"""
        print("Test school type validation")
        # This should work - school type with school, no purchased_class_hours
        valid_school_student = StudentOrClass.objects.create(
            student_or_class_name="Valid School Student",
            account_type='school',
            school=self.test_school,
            teacher=self.test_user_profile
        )
        self.assertIsNotNone(valid_school_student.id)

    def test_check_constraint_freelance_type_validation(self):
        """Test that freelance type requires purchased_class_hours and no school"""
        print("Test freelance type validation")
        # This should work - freelance type with purchased_class_hours, no school
        valid_freelance_student = StudentOrClass.objects.create(
            student_or_class_name="Valid Freelance Student",
            account_type='freelance',
            teacher=self.test_user_profile,
            purchased_class_hours=Decimal('8.00')
        )
        self.assertIsNotNone(valid_freelance_student.id)

    def test_max_length_validator_comments(self):
        """Test that comments field respects max length validator"""
        print("Test comments max length validation")
        long_comment = "A" * 501  # Exceeds 500 character limit

        student = StudentOrClass(
            student_or_class_name="Comment Test",
            teacher=self.test_user_profile,
            comments=long_comment,
            purchased_class_hours=Decimal('5.00')
        )

        with self.assertRaises(ValidationError):
            student.full_clean()

    def test_ordering(self):
        """Test model ordering"""
        print("Test model ordering")
        # Create another teacher for testing ordering
        another_user = get_user_model().objects.create_user(
            'anotheruser',
            'anotherpassword'
        )
        another_profile = UserProfile.objects.create(
            user=another_user,
            contact_email="another@gmx.com",
            surname="Anderson",  # Comes before "McTest" alphabetically
            given_name="Andy"
        )

        # Create student with the other teacher
        StudentOrClass.objects.create(
            student_or_class_name="Zulu Student",  # Comes after others alphabetically
            teacher=another_profile,
            purchased_class_hours=Decimal('4.00')
        )

        all_students = list(StudentOrClass.objects.all())

        # Should be ordered by teacher surname first, then student name
        # Anderson should come before McTest
        first_teacher_surname = all_students[0].teacher.surname
        self.assertEqual(first_teacher_surname, "Anderson")
