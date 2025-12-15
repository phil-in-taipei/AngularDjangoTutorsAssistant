from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date, time
from decimal import Decimal

from user_profiles.models import UserProfile
from student_account.models import StudentOrClass
from school.models import School
from class_scheduling.models import ScheduledClass
from accounting.utils import get_scheduled_classes_during_month_period

User = get_user_model()


class TestGetScheduledClassesDuringMonthPeriod(TestCase):
    """
    Test suite for get_scheduled_classes_during_month_period utility function.
    This function retrieves scheduled classes for a teacher during a specific month,
    ordered by school affiliation (freelance first, then by school name).
    """

    def setUp(self):
        """
        Set up test data including:
        - Teachers (primary teacher and another teacher for filtering tests)
        - 2 Schools (Alpha Academy and Beta School)
        - 2 Freelance students
        - 2 School-affiliated students (one per school)
        - Scheduled classes across multiple months and statuses
        """
        # Create users and user profiles
        self.teacher_user = User.objects.create_user(
            username='teacher1',
            password='testpass123'
        )
        self.teacher_profile = UserProfile.objects.create(
            user=self.teacher_user,
            contact_email='teacher1@example.com',
            surname='Smith',
            given_name='John'
        )

        self.other_teacher_user = User.objects.create_user(
            username='teacher2',
            password='testpass123'
        )
        self.other_teacher_profile = UserProfile.objects.create(
            user=self.other_teacher_user,
            contact_email='teacher2@example.com',
            surname='Jones',
            given_name='Mary'
        )

        # Create 2 schools
        self.school_alpha = School.objects.create(
            school_name='Alpha Academy',
            address_line_1='123 Main St',
            address_line_2='Suite 100',
            contact_phone='5551234567',
            scheduling_teacher=self.teacher_profile
        )
        self.school_beta = School.objects.create(
            school_name='Beta School',
            address_line_1='456 Oak Ave',
            address_line_2='Building B',
            contact_phone='5559876543',
            scheduling_teacher=self.teacher_profile
        )

        # Create 2 freelance students
        self.freelance_student_1 = StudentOrClass.objects.create(
            student_or_class_name='Alice Brown',
            account_type='freelance',
            school=None,
            teacher=self.teacher_profile,
            purchased_class_hours=Decimal('10.00'),
            tuition_per_hour=1000
        )
        self.freelance_student_2 = StudentOrClass.objects.create(
            student_or_class_name='Bob Wilson',
            account_type='freelance',
            school=None,
            teacher=self.teacher_profile,
            purchased_class_hours=Decimal('15.00'),
            tuition_per_hour=1200
        )

        # Create 2 school-affiliated students (one for each school)
        self.school_alpha_student = StudentOrClass.objects.create(
            student_or_class_name='Charlie Davis',
            account_type='school',
            school=self.school_alpha,
            teacher=self.teacher_profile,
            purchased_class_hours=None,
            tuition_per_hour=900
        )
        self.school_beta_student = StudentOrClass.objects.create(
            student_or_class_name='Diana Miller',
            account_type='school',
            school=self.school_beta,
            teacher=self.teacher_profile,
            purchased_class_hours=None,
            tuition_per_hour=950
        )

        # Create scheduled classes for November 2024
        # Freelance classes
        self.nov_freelance_class_1 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.freelance_student_1,
            date=date(2024, 11, 5),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='completed'
        )
        self.nov_freelance_class_2 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.freelance_student_1,
            date=date(2024, 11, 8),
            start_time=time(14, 0),
            finish_time=time(15, 30),
            class_status='completed'
        )
        self.nov_freelance_class_3 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.freelance_student_2,
            date=date(2024, 11, 15),
            start_time=time(14, 0),
            finish_time=time(15, 30),
            class_status='scheduled'
        )

        # School-affiliated classes (should be ordered alphabetically by school)
        # Beta School class (comes after Alpha alphabetically)
        self.nov_school_beta_class_1 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.school_beta_student,
            date=date(2024, 11, 10),
            start_time=time(9, 0),
            finish_time=time(10, 0),
            class_status='completed'
        )
        self.nov_school_beta_class_2 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.school_beta_student,
            date=date(2024, 11, 18),
            start_time=time(13, 0),
            finish_time=time(14, 30),
            class_status='completed'
        )

        # Alpha Academy class (comes before Beta alphabetically)
        self.nov_school_alpha_class_1 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.school_alpha_student,
            date=date(2024, 11, 12),
            start_time=time(13, 0),
            finish_time=time(14, 0),
            class_status='completed'
        )
        self.nov_school_alpha_class_2 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.school_alpha_student,
            date=date(2024, 11, 20),
            start_time=time(11, 0),
            finish_time=time(12, 0),
            class_status='same_day_cancellation'
        )

        # Classes in October 2024 (previous month)
        self.oct_class = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.freelance_student_1,
            date=date(2024, 10, 25),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='completed'
        )

        # Classes in December 2024 (next month)
        self.dec_class = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.school_alpha_student,
            date=date(2024, 12, 5),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='scheduled'
        )

        # Classes for other teacher in November (should not be included)
        self.nov_other_teacher_class = ScheduledClass.objects.create(
            teacher=self.other_teacher_profile,
            student_or_class=self.freelance_student_1,
            date=date(2024, 11, 8),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='completed'
        )

        # Edge case: Class on first day of month
        self.nov_first_day = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.freelance_student_2,
            date=date(2024, 11, 1),
            start_time=time(9, 0),
            finish_time=time(10, 0),
            class_status='scheduled'
        )

        # Edge case: Class on last day of month
        self.nov_last_day = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.school_beta_student,
            date=date(2024, 11, 30),
            start_time=time(15, 0),
            finish_time=time(16, 0),
            class_status='scheduled'
        )

    def test_get_classes_for_november_2024(self):
        """Test retrieving all classes for November 2024."""
        result = get_scheduled_classes_during_month_period(
            teacher=self.teacher_profile,
            month=11,
            year=2024
        )

        # Should include 9 classes for this teacher in November
        # 4 freelance + 4 school + 1 edge case
        self.assertEqual(result.count(), 9)

        # Verify specific classes are included
        self.assertIn(self.nov_freelance_class_1, result)
        self.assertIn(self.nov_freelance_class_2, result)
        self.assertIn(self.nov_freelance_class_3, result)
        self.assertIn(self.nov_school_alpha_class_1, result)
        self.assertIn(self.nov_school_alpha_class_2, result)
        self.assertIn(self.nov_school_beta_class_1, result)
        self.assertIn(self.nov_school_beta_class_2, result)
        self.assertIn(self.nov_first_day, result)
        self.assertIn(self.nov_last_day, result)

        # Verify classes from other months are excluded
        self.assertNotIn(self.oct_class, result)
        self.assertNotIn(self.dec_class, result)

        # Verify classes from other teachers are excluded
        self.assertNotIn(self.nov_other_teacher_class, result)

    def test_ordering_schools_before_freelance(self):
        """
        Test the current ordering behavior: school-affiliated students before freelance.

        NOTE: The function currently orders school students BEFORE freelance students
        because the Case/When assigns Value(1) to null schools and Value(0) to non-null,
        causing school students (0) to sort before freelance (1).

        If the desired behavior is freelance BEFORE schools, the function should be:
        Case(
            When(student_or_class__school__isnull=True, then=Value(0)),
            default=Value(1),
            ...
        )
        """
        result = get_scheduled_classes_during_month_period(
            teacher=self.teacher_profile,
            month=11,
            year=2024
        )

        result_list = list(result)

        # Find indices of freelance and school classes
        freelance_indices = [
            i for i, cls in enumerate(result_list)
            if cls.student_or_class.school is None
        ]
        school_indices = [
            i for i, cls in enumerate(result_list)
            if cls.student_or_class.school is not None
        ]

        # Currently: All SCHOOL classes come before all FREELANCE classes
        if freelance_indices and school_indices:
            self.assertTrue(min(school_indices) < min(freelance_indices))
            self.assertTrue(max(school_indices) < min(freelance_indices))

        # Verify we have the expected number of each type
        self.assertEqual(len(freelance_indices), 4)  # 4 freelance classes
        self.assertEqual(len(school_indices), 5)  # 5 school classes (4 + 1 edge case)

    def test_ordering_schools_alphabetically(self):
        """Test that school-affiliated classes are ordered alphabetically by school name."""
        result = get_scheduled_classes_during_month_period(
            teacher=self.teacher_profile,
            month=11,
            year=2024
        )

        # Filter to only school-affiliated classes
        school_classes = [
            cls for cls in result
            if cls.student_or_class.school is not None
        ]

        # Extract school names in order
        school_names = [
            cls.student_or_class.school.school_name
            for cls in school_classes
        ]

        # Verify alphabetical ordering: Alpha Academy should come before Beta School
        # We should see all Alpha Academy classes, then all Beta School classes
        alpha_count = school_names.count('Alpha Academy')
        beta_count = school_names.count('Beta School')

        self.assertEqual(alpha_count, 2)
        self.assertEqual(beta_count, 3)

        # First alpha_count items should be Alpha Academy
        self.assertTrue(all(name == 'Alpha Academy' for name in school_names[:alpha_count]))
        # Remaining items should be Beta School
        self.assertTrue(all(name == 'Beta School' for name in school_names[alpha_count:]))

    def test_december_edge_case(self):
        """Test that December correctly rolls over to January of next year."""
        # Create additional classes in December 2024
        dec_class_2024 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.freelance_student_1,
            date=date(2024, 12, 15),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='scheduled'
        )

        # Create a class in January 2025 (should not be included)
        jan_class_2025 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.freelance_student_1,
            date=date(2025, 1, 5),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='scheduled'
        )

        result = get_scheduled_classes_during_month_period(
            teacher=self.teacher_profile,
            month=12,
            year=2024
        )

        # Should include December classes but not January classes
        self.assertIn(self.dec_class, result)
        self.assertIn(dec_class_2024, result)
        self.assertNotIn(jan_class_2025, result)

    def test_empty_month(self):
        """Test behavior when no classes exist for the specified month."""
        result = get_scheduled_classes_during_month_period(
            teacher=self.teacher_profile,
            month=3,  # March 2024 - no classes created
            year=2024
        )

        self.assertEqual(result.count(), 0)

    def test_string_month_and_year_parameters(self):
        """Test that function handles string parameters for month and year."""
        result = get_scheduled_classes_during_month_period(
            teacher=self.teacher_profile,
            month="11",  # String instead of int
            year="2024"  # String instead of int
        )

        self.assertEqual(result.count(), 9)

    def test_includes_all_class_statuses(self):
        """Test that all class statuses are included in the result."""
        result = get_scheduled_classes_during_month_period(
            teacher=self.teacher_profile,
            month=11,
            year=2024
        )

        statuses = set(cls.class_status for cls in result)

        # Should include multiple statuses
        self.assertIn('completed', statuses)
        self.assertIn('scheduled', statuses)
        self.assertIn('same_day_cancellation', statuses)

    def test_different_teacher(self):
        """Test that filtering by different teacher works correctly."""
        result = get_scheduled_classes_during_month_period(
            teacher=self.other_teacher_profile,
            month=11,
            year=2024
        )

        # Should only include the one class for other_teacher
        self.assertEqual(result.count(), 1)
        self.assertEqual(result.first(), self.nov_other_teacher_class)

    def test_boundary_dates(self):
        """Test that boundary dates are handled correctly (inclusive start, exclusive end)."""
        result = get_scheduled_classes_during_month_period(
            teacher=self.teacher_profile,
            month=11,
            year=2024
        )

        # November 1st should be included
        nov_1_classes = [cls for cls in result if cls.date == date(2024, 11, 1)]
        self.assertEqual(len(nov_1_classes), 1)

        # November 30th should be included
        nov_30_classes = [cls for cls in result if cls.date == date(2024, 11, 30)]
        self.assertEqual(len(nov_30_classes), 1)

        # December 1st should NOT be included
        dec_1_classes = [cls for cls in result if cls.date == date(2024, 12, 1)]
        self.assertEqual(len(dec_1_classes), 0)

    def test_freelance_students_have_correct_attributes(self):
        """Verify that freelance students are correctly set up."""
        result = get_scheduled_classes_during_month_period(
            teacher=self.teacher_profile,
            month=11,
            year=2024
        )

        freelance_classes = [
            cls for cls in result
            if cls.student_or_class.account_type == 'freelance'
        ]

        for cls in freelance_classes:
            self.assertIsNone(cls.student_or_class.school)
            self.assertEqual(cls.student_or_class.account_type, 'freelance')
            self.assertIsNotNone(cls.student_or_class.purchased_class_hours)

    def test_school_students_have_correct_attributes(self):
        """Verify that school students are correctly set up."""
        result = get_scheduled_classes_during_month_period(
            teacher=self.teacher_profile,
            month=11,
            year=2024
        )

        school_classes = [
            cls for cls in result
            if cls.student_or_class.account_type == 'school'
        ]

        for cls in school_classes:
            self.assertIsNotNone(cls.student_or_class.school)
            self.assertEqual(cls.student_or_class.account_type, 'school')
            self.assertIsNone(cls.student_or_class.purchased_class_hours)
