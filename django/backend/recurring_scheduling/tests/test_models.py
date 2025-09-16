from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from datetime import time
from decimal import Decimal

from school.models import School
from student_account.models import StudentOrClass
from user_profiles.models import UserProfile
from recurring_scheduling.models import (
    RecurringScheduledClass, RecurringClassAppliedMonthly,
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY,
    JANUARY, FEBRUARY, MARCH, APRIL, MAY, JUNE, JULY, AUGUST, 
    SEPTEMBER, OCTOBER, NOVEMBER, DECEMBER
)


class RecurringScheduledClassModelTests(TestCase):
    """Test the RecurringScheduledClass Model"""

    def setUp(self):
        # Create test users and profiles
        self.test_user1 = get_user_model().objects.create_user(
            'teacher1',
            'password1'
        )
        self.teacher1_profile = UserProfile.objects.create(
            user=self.test_user1,
            contact_email="teacher1@gmx.com",
            surname="Smith",
            given_name="John"
        )

        self.test_user2 = get_user_model().objects.create_user(
            'teacher2',
            'password2'
        )
        self.teacher2_profile = UserProfile.objects.create(
            user=self.test_user2,
            contact_email="teacher2@gmx.com",
            surname="Johnson",
            given_name="Jane"
        )

        # Create test school
        self.test_school = School.objects.create(
            school_name="Test School",
            address_line_1="123 School St",
            address_line_2="Taipei, Taiwan",
            contact_phone="0987654321",
            scheduling_teacher=self.teacher1_profile
        )

        # Create test students
        self.freelance_student = StudentOrClass.objects.create(
            student_or_class_name="Alice Brown",
            account_type='freelance',
            teacher=self.teacher1_profile,
            purchased_class_hours=Decimal('15.00'),
            tuition_per_hour=1000
        )

        self.school_student = StudentOrClass.objects.create(
            student_or_class_name="Bob Wilson",
            account_type='school',
            school=self.test_school,
            teacher=self.teacher1_profile,
            tuition_per_hour=800
        )

        # Create test recurring classes
        self.recurring_class1 = RecurringScheduledClass.objects.create(
            recurring_start_time=time(9, 0),
            recurring_finish_time=time(10, 0),
            recurring_day_of_week=MONDAY,
            student_or_class=self.freelance_student,
            teacher=self.teacher1_profile
        )

        self.recurring_class2 = RecurringScheduledClass.objects.create(
            recurring_start_time=time(14, 30),
            recurring_finish_time=time(16, 0),
            recurring_day_of_week=WEDNESDAY,
            student_or_class=self.school_student,
            teacher=self.teacher1_profile
        )

    def test_recurring_class_fields(self):
        """Test the recurring class fields"""
        print("Test the recurring class fields")
        self.assertEqual(
            self.recurring_class1.recurring_start_time,
            time(9, 0)
        )
        self.assertEqual(
            self.recurring_class1.recurring_finish_time,
            time(10, 0)
        )
        self.assertEqual(
            self.recurring_class1.recurring_day_of_week,
            MONDAY
        )
        self.assertEqual(
            self.recurring_class1.student_or_class,
            self.freelance_student
        )
        self.assertEqual(
            self.recurring_class1.teacher,
            self.teacher1_profile
        )

    def test_recurring_class_str(self):
        """Test the recurring class model string representation"""
        print("Test the recurring class string")
        expected_str = "Freelance student: Alice Brown on Monday from 09:00:00 to 10:00:00"
        self.assertEqual(str(self.recurring_class1), expected_str)

    def test_day_of_week_string_property(self):
        """Test the day_of_week_string property"""
        print("Test day_of_week_string property")
        self.assertEqual(self.recurring_class1.day_of_week_string, "Monday")
        self.assertEqual(self.recurring_class2.day_of_week_string, "Wednesday")

    def test_day_of_week_choices(self):
        """Test all day of week choices work"""
        print("Test day of week choices")
        day_choices = [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY]
        expected_strings = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        for i, day in enumerate(day_choices):
            recurring_class = RecurringScheduledClass.objects.create(
                recurring_start_time=time(10, 0),
                recurring_finish_time=time(11, 0),
                recurring_day_of_week=day,
                student_or_class=self.freelance_student,
                teacher=self.teacher2_profile
            )
            self.assertEqual(recurring_class.recurring_day_of_week, day)
            self.assertEqual(recurring_class.day_of_week_string, expected_strings[i])

    def test_nullable_time_fields(self):
        """Test that time fields can be null/blank"""
        print("Test nullable time fields")
        recurring_class = RecurringScheduledClass.objects.create(
            recurring_day_of_week=FRIDAY,
            student_or_class=self.school_student,
            teacher=self.teacher2_profile
        )
        self.assertIsNone(recurring_class.recurring_start_time)
        self.assertIsNone(recurring_class.recurring_finish_time)

    def test_custom_manager_teacher_classes_on_day(self):
        """Test the custom manager method for teacher's classes on specific day"""
        print("Test custom manager teacher classes on day")
        
        # Create another Monday class for same teacher
        monday_class2 = RecurringScheduledClass.objects.create(
            recurring_start_time=time(11, 0),
            recurring_finish_time=time(12, 0),
            recurring_day_of_week=MONDAY,
            student_or_class=self.school_student,
            teacher=self.teacher1_profile
        )
        
        # Get all Monday classes for teacher1
        monday_classes = RecurringScheduledClass.custom_query.teacher_already_booked_classes_on_day_of_week(
            MONDAY, self.teacher1_profile.id
        )
        
        self.assertEqual(len(monday_classes), 2)
        self.assertIn(self.recurring_class1, monday_classes)
        self.assertIn(monday_class2, monday_classes)

    def test_custom_manager_teacher_no_classes_on_day(self):
        """Test custom manager when teacher has no classes on specific day"""
        print("Test custom manager no classes on day")
        
        # Teacher2 has no Monday classes
        monday_classes = RecurringScheduledClass.custom_query.teacher_already_booked_classes_on_day_of_week(
            MONDAY, self.teacher2_profile.id
        )
        
        self.assertEqual(len(monday_classes), 0)

    def test_custom_manager_different_day(self):
        """Test custom manager for different day"""
        print("Test custom manager different day")
        
        # Teacher1 has no Tuesday classes
        tuesday_classes = RecurringScheduledClass.custom_query.teacher_already_booked_classes_on_day_of_week(
            TUESDAY, self.teacher1_profile.id
        )
        
        self.assertEqual(len(tuesday_classes), 0)


class RecurringClassAppliedMonthlyModelTests(TestCase):
    """Test the RecurringClassAppliedMonthly Model"""

    def setUp(self):
        # Create test user and profile
        self.test_user = get_user_model().objects.create_user(
            'teacher1',
            'password1'
        )
        self.teacher_profile = UserProfile.objects.create(
            user=self.test_user,
            contact_email="teacher1@gmx.com",
            surname="Smith",
            given_name="John"
        )

        # Create test student
        self.freelance_student = StudentOrClass.objects.create(
            student_or_class_name="Alice Brown",
            account_type='freelance',
            teacher=self.teacher_profile,
            purchased_class_hours=Decimal('15.00'),
            tuition_per_hour=1000
        )

        # Create test recurring class
        self.recurring_class = RecurringScheduledClass.objects.create(
            recurring_start_time=time(9, 0),
            recurring_finish_time=time(10, 0),
            recurring_day_of_week=MONDAY,
            student_or_class=self.freelance_student,
            teacher=self.teacher_profile
        )

        # Create test monthly application
        self.monthly_application = RecurringClassAppliedMonthly.objects.create(
            scheduling_month=MARCH,
            scheduling_year=2025,
            recurring_class=self.recurring_class
        )

    def test_monthly_application_fields(self):
        """Test the monthly application fields"""
        print("Test the monthly application fields")
        self.assertEqual(
            self.monthly_application.scheduling_month,
            MARCH
        )
        self.assertEqual(
            self.monthly_application.scheduling_year,
            2025
        )
        self.assertEqual(
            self.monthly_application.recurring_class,
            self.recurring_class
        )

    def test_monthly_application_str(self):
        """Test the monthly application model string representation"""
        print("Test the monthly application string")
        expected_str = f"March 2025 for {self.recurring_class}"
        self.assertEqual(str(self.monthly_application), expected_str)

    def test_month_string_property(self):
        """Test the month_string property"""
        print("Test month_string property")
        self.assertEqual(self.monthly_application.month_string, "March")

    def test_recurring_day_of_week_property(self):
        """Test the recurring_day_of_week property"""
        print("Test recurring_day_of_week property")
        self.assertEqual(self.monthly_application.recurring_day_of_week, MONDAY)

    def test_recurring_start_time_property(self):
        """Test the recurring_start_time property"""
        print("Test recurring_start_time property")
        self.assertEqual(self.monthly_application.recurring_start_time, time(9, 0))

    def test_default_year_value(self):
        """Test the default year value"""
        print("Test default year value")
        # Create without specifying year
        monthly_app = RecurringClassAppliedMonthly.objects.create(
            scheduling_month=APRIL,
            recurring_class=self.recurring_class
        )
        # Should default to current year (at least 2025 based on MinValueValidator)
        self.assertGreaterEqual(monthly_app.scheduling_year, 2025)

    def test_year_validators(self):
        """Test year field validators"""
        print("Test year validators")
        
        # Test minimum validator (should fail for year < 2025)
        monthly_app = RecurringClassAppliedMonthly(
            scheduling_month=MAY,
            scheduling_year=2024,  # Below minimum
            recurring_class=self.recurring_class
        )
        with self.assertRaises(ValidationError):
            monthly_app.full_clean()

        # Test maximum validator (should fail for year > 2035)
        monthly_app2 = RecurringClassAppliedMonthly(
            scheduling_month=MAY,
            scheduling_year=2036,  # Above maximum
            recurring_class=self.recurring_class
        )
        with self.assertRaises(ValidationError):
            monthly_app2.full_clean()

    def test_month_choices(self):
        """Test all month choices work"""
        print("Test month choices")
        month_choices = [
            JANUARY, FEBRUARY, MARCH, APRIL, MAY, JUNE,
            JULY, AUGUST, SEPTEMBER, OCTOBER, NOVEMBER, DECEMBER
        ]
        expected_strings = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        
        for i, month in enumerate(month_choices):
            monthly_app = RecurringClassAppliedMonthly.objects.create(
                scheduling_month=month,
                scheduling_year=2026,
                recurring_class=self.recurring_class
            )
            self.assertEqual(monthly_app.scheduling_month, month)
            self.assertEqual(monthly_app.month_string, expected_strings[i])

    def test_unique_together_constraint(self):
        """Test unique together constraint"""
        print("Test unique together constraint")
        
        # Try to create duplicate month/year/recurring_class combination
        with self.assertRaises(IntegrityError):
            RecurringClassAppliedMonthly.objects.create(
                scheduling_month=MARCH,  # Same as existing
                scheduling_year=2025,    # Same as existing
                recurring_class=self.recurring_class  # Same as existing
            )

    def test_unique_together_allows_different_combinations(self):
        """Test that unique together allows different combinations"""
        print("Test unique together allows different combinations")
        
        # Different month should work
        april_app = RecurringClassAppliedMonthly.objects.create(
            scheduling_month=APRIL,
            scheduling_year=2025,
            recurring_class=self.recurring_class
        )
        self.assertIsNotNone(april_app.id)

        # Different year should work
        march_2026_app = RecurringClassAppliedMonthly.objects.create(
            scheduling_month=MARCH,
            scheduling_year=2026,
            recurring_class=self.recurring_class
        )
        self.assertIsNotNone(march_2026_app.id)

    def test_ordering(self):
        """Test model ordering"""
        print("Test model ordering")
        
        # Create another user with different username for testing ordering
        user2 = get_user_model().objects.create_user('ateacher', 'password')
        teacher2_profile = UserProfile.objects.create(
            user=user2,
            contact_email="teacher2@gmx.com",
            surname="Anderson",
            given_name="Amy"
        )
        
        student2 = StudentOrClass.objects.create(
            student_or_class_name="Beta Student",
            account_type='freelance',
            teacher=teacher2_profile,
            purchased_class_hours=Decimal('10.00')
        )
        
        recurring_class2 = RecurringScheduledClass.objects.create(
            recurring_start_time=time(11, 0),
            recurring_finish_time=time(12, 0),
            recurring_day_of_week=TUESDAY,
            student_or_class=student2,
            teacher=teacher2_profile
        )
        
        # Create monthly applications for different scenarios
        # Same month/year, different teacher (should be ordered by username)
        monthly_app2 = RecurringClassAppliedMonthly.objects.create(
            scheduling_month=MARCH,
            scheduling_year=2025,
            recurring_class=recurring_class2
        )
        
        # Different year (should come first due to -scheduling_year)
        monthly_app3 = RecurringClassAppliedMonthly.objects.create(
            scheduling_month=FEBRUARY,
            scheduling_year=2026,
            recurring_class=self.recurring_class
        )
        
        all_apps = list(RecurringClassAppliedMonthly.objects.all())
        
        # Should be ordered by: -scheduling_year, -scheduling_month, username, student_name
        # 2026 should come before 2025
        self.assertEqual(all_apps[0], monthly_app3)
        
        # Within same year, March should come before other months due to -scheduling_month
        # And "ateacher" should come before "teacher1"
        march_2025_apps = [app for app in all_apps if app.scheduling_year == 2025 and app.scheduling_month == MARCH]
        if len(march_2025_apps) >= 2:
            # Teacher with username "ateacher" should come before "teacher1"
            usernames = [app.recurring_class.teacher.user.username for app in march_2025_apps]
            self.assertEqual(usernames, sorted(usernames))

    def test_cascade_deletion(self):
        """Test that deleting recurring class deletes monthly applications"""
        print("Test cascade deletion")
        
        # Verify the monthly application exists
        self.assertTrue(
            RecurringClassAppliedMonthly.objects.filter(id=self.monthly_application.id).exists()
        )
        
        # Delete the recurring class
        self.recurring_class.delete()
        
        # Verify the monthly application is also deleted
        self.assertFalse(
            RecurringClassAppliedMonthly.objects.filter(id=self.monthly_application.id).exists()
        )
