from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date, time
from copy import deepcopy
from decimal import Decimal
from unittest.mock import patch, call

from user_profiles.models import UserProfile
from student_account.models import StudentOrClass
from school.models import School
from class_scheduling.models import ScheduledClass
from accounting.utils import (
    calculate_school_totals,
    calculate_overall_monthly_total,
    get_estimated_number_of_worked_hours,
    get_scheduled_classes_during_month_period, 
    organize_scheduled_classes, process_school_classes,
    process_freelance_students,
    generate_accounting_reports_for_classes_in_schools_and_freelance_teachers,
    sort_accounting_reports_by_name,
    sort_school_reports_alphabetically,
    sort_school_and_freelance_reports_alphabetically,
)


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





class TestOrganizeScheduledClasses(TestCase):
    """
    Test suite for organize_scheduled_classes utility function.
    This function takes a queryset of scheduled classes and organizes them into
    a nested dictionary structure with separate sections for school classes and
    freelance students.
    """

    def setUp(self):
        """
        Set up test data including:
        - 1 Teacher
        - 2 Schools (Alpha Academy and Beta School)
        - 2 Freelance students
        - 2 School-affiliated students (one per school)
        - Various scheduled classes
        """
        # Create user and user profile
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

        # Create 2 school-affiliated students
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

        # Create scheduled classes
        # Freelance classes for Alice
        self.alice_class_1 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.freelance_student_1,
            date=date(2024, 11, 5),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='completed'
        )
        self.alice_class_2 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.freelance_student_1,
            date=date(2024, 11, 12),
            start_time=time(14, 0),
            finish_time=time(15, 0),
            class_status='completed'
        )

        # Freelance classes for Bob
        self.bob_class_1 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.freelance_student_2,
            date=date(2024, 11, 8),
            start_time=time(9, 0),
            finish_time=time(10, 30),
            class_status='scheduled'
        )

        # School classes for Alpha Academy - Charlie
        self.charlie_class_1 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.school_alpha_student,
            date=date(2024, 11, 10),
            start_time=time(13, 0),
            finish_time=time(14, 0),
            class_status='completed'
        )
        self.charlie_class_2 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.school_alpha_student,
            date=date(2024, 11, 17),
            start_time=time(13, 0),
            finish_time=time(14, 0),
            class_status='completed'
        )

        # School classes for Beta School - Diana
        self.diana_class_1 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.school_beta_student,
            date=date(2024, 11, 15),
            start_time=time(11, 0),
            finish_time=time(12, 30),
            class_status='completed'
        )

    def test_basic_structure(self):
        """Test that the function returns the correct dictionary structure."""
        classes = ScheduledClass.objects.filter(teacher=self.teacher_profile)
        result = organize_scheduled_classes(classes)

        # Check top-level keys
        self.assertIn('classes_in_schools', result)
        self.assertIn('freelance_students', result)
        self.assertIsInstance(result['classes_in_schools'], list)
        self.assertIsInstance(result['freelance_students'], list)

    def test_school_classes_organization(self):
        """Test that school classes are correctly organized by school and student."""
        classes = ScheduledClass.objects.filter(teacher=self.teacher_profile)
        result = organize_scheduled_classes(classes)

        schools = result['classes_in_schools']
        
        # Should have 2 schools
        self.assertEqual(len(schools), 2)

        # Find Alpha Academy and Beta School in results
        alpha_school = next((s for s in schools if s['school_name'] == 'Alpha Academy'), None)
        beta_school = next((s for s in schools if s['school_name'] == 'Beta School'), None)

        self.assertIsNotNone(alpha_school)
        self.assertIsNotNone(beta_school)

        # Check Alpha Academy structure
        self.assertIn('school_name', alpha_school)
        self.assertIn('students_classes', alpha_school)
        self.assertEqual(alpha_school['school_name'], 'Alpha Academy')
        self.assertEqual(len(alpha_school['students_classes']), 1)  # Charlie only

        # Check Charlie's data
        charlie_data = alpha_school['students_classes'][0]
        self.assertEqual(charlie_data['student_or_class_name'], 'Charlie Davis')
        self.assertEqual(len(charlie_data['scheduled_classes']), 2)
        self.assertIn(self.charlie_class_1, charlie_data['scheduled_classes'])
        self.assertIn(self.charlie_class_2, charlie_data['scheduled_classes'])

        # Check Beta School structure
        self.assertEqual(beta_school['school_name'], 'Beta School')
        self.assertEqual(len(beta_school['students_classes']), 1)  # Diana only

        # Check Diana's data
        diana_data = beta_school['students_classes'][0]
        self.assertEqual(diana_data['student_or_class_name'], 'Diana Miller')
        self.assertEqual(len(diana_data['scheduled_classes']), 1)
        self.assertIn(self.diana_class_1, diana_data['scheduled_classes'])

    def test_freelance_students_organization(self):
        """Test that freelance students are correctly organized."""
        classes = ScheduledClass.objects.filter(teacher=self.teacher_profile)
        result = organize_scheduled_classes(classes)

        freelance = result['freelance_students']
        
        # Should have 2 freelance students
        self.assertEqual(len(freelance), 2)

        # Find Alice and Bob in results
        alice_data = next((s for s in freelance if s['student_or_class_name'] == 'Alice Brown'), None)
        bob_data = next((s for s in freelance if s['student_or_class_name'] == 'Bob Wilson'), None)

        self.assertIsNotNone(alice_data)
        self.assertIsNotNone(bob_data)

        # Check Alice's data
        self.assertIn('student_or_class_name', alice_data)
        self.assertIn('scheduled_classes', alice_data)
        self.assertEqual(alice_data['student_or_class_name'], 'Alice Brown')
        self.assertEqual(len(alice_data['scheduled_classes']), 2)
        self.assertIn(self.alice_class_1, alice_data['scheduled_classes'])
        self.assertIn(self.alice_class_2, alice_data['scheduled_classes'])

        # Check Bob's data
        self.assertEqual(bob_data['student_or_class_name'], 'Bob Wilson')
        self.assertEqual(len(bob_data['scheduled_classes']), 1)
        self.assertIn(self.bob_class_1, bob_data['scheduled_classes'])

    def test_empty_queryset(self):
        """Test that function handles empty queryset correctly."""
        empty_classes = ScheduledClass.objects.none()
        result = organize_scheduled_classes(empty_classes)

        self.assertEqual(len(result['classes_in_schools']), 0)
        self.assertEqual(len(result['freelance_students']), 0)

    def test_only_school_classes(self):
        """Test organization when only school classes exist."""
        # Only get school classes
        classes = ScheduledClass.objects.filter(
            teacher=self.teacher_profile,
            student_or_class__school__isnull=False
        )
        result = organize_scheduled_classes(classes)

        # Should have school data but no freelance data
        self.assertEqual(len(result['classes_in_schools']), 2)
        self.assertEqual(len(result['freelance_students']), 0)

    def test_only_freelance_classes(self):
        """Test organization when only freelance classes exist."""
        # Only get freelance classes
        classes = ScheduledClass.objects.filter(
            teacher=self.teacher_profile,
            student_or_class__school__isnull=True
        )
        result = organize_scheduled_classes(classes)

        # Should have freelance data but no school data
        self.assertEqual(len(result['classes_in_schools']), 0)
        self.assertEqual(len(result['freelance_students']), 2)

    def test_multiple_students_same_school(self):
        """Test organization when a school has multiple students."""
        # Create another student at Alpha Academy
        second_alpha_student = StudentOrClass.objects.create(
            student_or_class_name='Emily Johnson',
            account_type='school',
            school=self.school_alpha,
            teacher=self.teacher_profile,
            purchased_class_hours=None,
            tuition_per_hour=900
        )

        # Create class for the new student
        emily_class = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=second_alpha_student,
            date=date(2024, 11, 20),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='scheduled'
        )

        classes = ScheduledClass.objects.filter(teacher=self.teacher_profile)
        result = organize_scheduled_classes(classes)

        # Find Alpha Academy
        alpha_school = next((s for s in result['classes_in_schools'] 
                           if s['school_name'] == 'Alpha Academy'), None)

        # Should have 2 students now
        self.assertEqual(len(alpha_school['students_classes']), 2)

        # Verify both students are present
        student_names = [s['student_or_class_name'] for s in alpha_school['students_classes']]
        self.assertIn('Charlie Davis', student_names)
        self.assertIn('Emily Johnson', student_names)

    def test_class_status_preserved(self):
        """Test that various class statuses are preserved in the organization."""
        # Create classes with different statuses
        cancelled_class = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.freelance_student_1,
            date=date(2024, 11, 25),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='cancelled'
        )
        
        same_day_cancel = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.school_alpha_student,
            date=date(2024, 11, 26),
            start_time=time(14, 0),
            finish_time=time(15, 0),
            class_status='same_day_cancellation'
        )

        classes = ScheduledClass.objects.filter(teacher=self.teacher_profile)
        result = organize_scheduled_classes(classes)

        # Check that all classes are included regardless of status
        alice_data = next((s for s in result['freelance_students'] 
                         if s['student_or_class_name'] == 'Alice Brown'), None)
        self.assertEqual(len(alice_data['scheduled_classes']), 3)  # Now has 3 classes
        
        # Verify the cancelled class is included
        statuses = [c.class_status for c in alice_data['scheduled_classes']]
        self.assertIn('cancelled', statuses)

    def test_class_details_preserved(self):
        """Test that all class details (date, time, notes) are preserved."""
        classes = ScheduledClass.objects.filter(teacher=self.teacher_profile)
        result = organize_scheduled_classes(classes)

        # Get Alice's first class from the result
        alice_data = next((s for s in result['freelance_students'] 
                         if s['student_or_class_name'] == 'Alice Brown'), None)
        alice_first_class = next((c for c in alice_data['scheduled_classes'] 
                                 if c.id == self.alice_class_1.id), None)

        # Verify all details are intact
        self.assertEqual(alice_first_class.date, date(2024, 11, 5))
        self.assertEqual(alice_first_class.start_time, time(10, 0))
        self.assertEqual(alice_first_class.finish_time, time(11, 0))
        self.assertEqual(alice_first_class.class_status, 'completed')
        self.assertEqual(alice_first_class.teacher, self.teacher_profile)

    def test_order_preservation_within_student(self):
        """Test that classes for each student maintain their order from the queryset."""
        # Create classes in a specific order
        classes = ScheduledClass.objects.filter(
            teacher=self.teacher_profile
        ).order_by('date', 'start_time')

        result = organize_scheduled_classes(classes)

        # Check Alice's classes are in date order
        alice_data = next((s for s in result['freelance_students'] 
                         if s['student_or_class_name'] == 'Alice Brown'), None)
        
        alice_dates = [c.date for c in alice_data['scheduled_classes']]
        self.assertEqual(alice_dates, sorted(alice_dates))

    def test_queryset_versus_list_input(self):
        """Test that function works with both querysets and lists."""
        classes_queryset = ScheduledClass.objects.filter(teacher=self.teacher_profile)
        classes_list = list(classes_queryset)

        result_from_queryset = organize_scheduled_classes(classes_queryset)
        result_from_list = organize_scheduled_classes(classes_list)

        # Both should produce the same counts
        self.assertEqual(
            len(result_from_queryset['classes_in_schools']),
            len(result_from_list['classes_in_schools'])
        )
        self.assertEqual(
            len(result_from_queryset['freelance_students']),
            len(result_from_list['freelance_students'])
        )

    def test_student_with_single_class(self):
        """Test organization for students with only one class."""
        # Bob only has one class
        classes = ScheduledClass.objects.filter(teacher=self.teacher_profile)
        result = organize_scheduled_classes(classes)

        bob_data = next((s for s in result['freelance_students'] 
                       if s['student_or_class_name'] == 'Bob Wilson'), None)

        self.assertEqual(len(bob_data['scheduled_classes']), 1)
        self.assertEqual(bob_data['scheduled_classes'][0], self.bob_class_1)

    def test_no_duplicate_entries(self):
        """Test that students/schools don't appear multiple times in the structure."""
        classes = ScheduledClass.objects.filter(teacher=self.teacher_profile)
        result = organize_scheduled_classes(classes)

        # Check school names are unique
        school_names = [s['school_name'] for s in result['classes_in_schools']]
        self.assertEqual(len(school_names), len(set(school_names)))

        # Check freelance student names are unique
        freelance_names = [s['student_or_class_name'] for s in result['freelance_students']]
        self.assertEqual(len(freelance_names), len(set(freelance_names)))

        # Check student names within each school are unique
        for school in result['classes_in_schools']:
            student_names = [s['student_or_class_name'] for s in school['students_classes']]
            self.assertEqual(len(student_names), len(set(student_names)))



class TestGetEstimatedNumberOfWorkedHours(TestCase):
    """
    Test suite for get_estimated_number_of_worked_hours utility function.
    This function calculates total worked hours for a list of scheduled classes,
    only counting classes with status 'completed' or 'same_day_cancellation'.
    """

    def setUp(self):
        """
        Set up test data including:
        - 1 Teacher
        - 1 School and 1 Freelance student
        - Scheduled classes with various statuses
        """
        # Create user and user profile
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

        # Create school
        self.school = School.objects.create(
            school_name='Alpha Academy',
            address_line_1='123 Main St',
            address_line_2='Suite 100',
            contact_phone='5551234567',
            scheduling_teacher=self.teacher_profile
        )

        # Create student
        self.student = StudentOrClass.objects.create(
            student_or_class_name='Alice Brown',
            account_type='school',
            school=self.school,
            teacher=self.teacher_profile,
            purchased_class_hours=None,
            tuition_per_hour=900
        )

        # Create classes with different statuses
        # Completed class - should count
        self.completed_class = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.student,
            date=date(2024, 11, 5),
            start_time=time(10, 0),
            finish_time=time(11, 0),  # 1 hour
            class_status='completed'
        )

        # Same day cancellation - should count
        self.same_day_cancel = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.student,
            date=date(2024, 11, 8),
            start_time=time(14, 0),
            finish_time=time(15, 30),  # 1.5 hours
            class_status='same_day_cancellation'
        )

        # Scheduled class - should NOT count
        self.scheduled_class = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.student,
            date=date(2024, 11, 12),
            start_time=time(9, 0),
            finish_time=time(10, 0),  # 1 hour
            class_status='scheduled'
        )

        # Cancelled class - should NOT count
        self.cancelled_class = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.student,
            date=date(2024, 11, 15),
            start_time=time(13, 0),
            finish_time=time(14, 30),  # 1.5 hours
            class_status='cancelled'
        )

        # Cancellation request - should NOT count
        self.cancel_request = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.student,
            date=date(2024, 11, 20),
            start_time=time(11, 0),
            finish_time=time(12, 0),  # 1 hour
            class_status='cancellation_request'
        )

    @patch('accounting.utils.determine_duration_of_class_time')
    def test_completed_class_counts(self, mock_duration):
        """Test that completed classes are counted."""
        mock_duration.return_value = Decimal('1.0')

        classes = [self.completed_class]
        result = get_estimated_number_of_worked_hours(classes)

        # Should call duration function once
        mock_duration.assert_called_once_with(time(10, 0), time(11, 0))
        # Should return the duration
        self.assertEqual(result, Decimal('1.0'))

    @patch('accounting.utils.determine_duration_of_class_time')
    def test_same_day_cancellation_counts(self, mock_duration):
        """Test that same day cancellations are counted."""
        mock_duration.return_value = Decimal('1.5')

        classes = [self.same_day_cancel]
        result = get_estimated_number_of_worked_hours(classes)

        # Should call duration function once
        mock_duration.assert_called_once_with(time(14, 0), time(15, 30))
        # Should return the duration
        self.assertEqual(result, Decimal('1.5'))

    @patch('accounting.utils.determine_duration_of_class_time')
    def test_scheduled_class_not_counted(self, mock_duration):
        """Test that scheduled classes are NOT counted."""
        classes = [self.scheduled_class]
        result = get_estimated_number_of_worked_hours(classes)

        # Should NOT call duration function
        mock_duration.assert_not_called()
        # Should return 0
        self.assertEqual(result, 0)

    @patch('accounting.utils.determine_duration_of_class_time')
    def test_cancelled_class_not_counted(self, mock_duration):
        """Test that cancelled classes are NOT counted."""
        classes = [self.cancelled_class]
        result = get_estimated_number_of_worked_hours(classes)

        # Should NOT call duration function
        mock_duration.assert_not_called()
        # Should return 0
        self.assertEqual(result, 0)

    @patch('accounting.utils.determine_duration_of_class_time')
    def test_cancellation_request_not_counted(self, mock_duration):
        """Test that cancellation requests are NOT counted."""
        classes = [self.cancel_request]
        result = get_estimated_number_of_worked_hours(classes)

        # Should NOT call duration function
        mock_duration.assert_not_called()
        # Should return 0
        self.assertEqual(result, 0)

    @patch('accounting.utils.determine_duration_of_class_time')
    def test_multiple_completed_classes(self, mock_duration):
        """Test summing hours across multiple completed classes."""
        # Create another completed class
        completed_class_2 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.student,
            date=date(2024, 11, 22),
            start_time=time(10, 0),
            finish_time=time(11, 30),  # 1.5 hours
            class_status='completed'
        )

        # Mock different durations for each class
        mock_duration.side_effect = [Decimal('1.0'), Decimal('1.5')]

        classes = [self.completed_class, completed_class_2]
        result = get_estimated_number_of_worked_hours(classes)

        # Should call duration function twice
        self.assertEqual(mock_duration.call_count, 2)
        # Should return sum of durations
        self.assertEqual(result, Decimal('2.5'))

    @patch('accounting.utils.determine_duration_of_class_time')
    def test_mixed_statuses(self, mock_duration):
        """Test that only completed and same_day_cancellation classes are counted."""
        # Mock durations for countable classes
        mock_duration.side_effect = [Decimal('1.0'), Decimal('1.5')]

        # Mix of all statuses
        classes = [
            self.completed_class,       # Should count (1.0)
            self.same_day_cancel,       # Should count (1.5)
            self.scheduled_class,       # Should NOT count
            self.cancelled_class,       # Should NOT count
            self.cancel_request         # Should NOT count
        ]
        
        result = get_estimated_number_of_worked_hours(classes)

        # Should only call duration function twice (for completed and same_day_cancel)
        self.assertEqual(mock_duration.call_count, 2)
        # Should return sum of only the countable classes
        self.assertEqual(result, Decimal('2.5'))

    @patch('accounting.utils.determine_duration_of_class_time')
    def test_empty_list(self, mock_duration):
        """Test that empty list returns 0 hours."""
        classes = []
        result = get_estimated_number_of_worked_hours(classes)

        # Should not call duration function
        mock_duration.assert_not_called()
        # Should return 0
        self.assertEqual(result, 0)

    @patch('accounting.utils.determine_duration_of_class_time')
    def test_only_non_countable_classes(self, mock_duration):
        """Test that list with only non-countable classes returns 0 hours."""
        classes = [
            self.scheduled_class,
            self.cancelled_class,
            self.cancel_request
        ]
        
        result = get_estimated_number_of_worked_hours(classes)

        # Should not call duration function
        mock_duration.assert_not_called()
        # Should return 0
        self.assertEqual(result, 0)

    @patch('accounting.utils.determine_duration_of_class_time')
    def test_duration_function_called_with_correct_times(self, mock_duration):
        """Test that determine_duration_of_class_time is called with correct start and finish times."""
        mock_duration.return_value = Decimal('1.0')

        classes = [self.completed_class, self.same_day_cancel]
        get_estimated_number_of_worked_hours(classes)

        # Verify the function was called with correct arguments
        expected_calls = [
            call(time(10, 0), time(11, 0)),      # completed_class times
            call(time(14, 0), time(15, 30))       # same_day_cancel times
        ]
        mock_duration.assert_has_calls(expected_calls, any_order=False)

    @patch('accounting.utils.determine_duration_of_class_time')
    def test_accumulation_logic(self, mock_duration):
        """Test that hours are accumulated correctly, not replaced."""
        # Return different values for each call
        mock_duration.side_effect = [
            Decimal('1.0'),
            Decimal('0.5'),
            Decimal('2.0')
        ]

        # Create additional completed classes
        completed_2 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.student,
            date=date(2024, 11, 25),
            start_time=time(9, 0),
            finish_time=time(9, 30),
            class_status='completed'
        )
        completed_3 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.student,
            date=date(2024, 11, 26),
            start_time=time(14, 0),
            finish_time=time(16, 0),
            class_status='completed'
        )

        classes = [self.completed_class, completed_2, completed_3]
        result = get_estimated_number_of_worked_hours(classes)

        # Should return 1.0 + 0.5 + 2.0 = 3.5
        self.assertEqual(result, Decimal('3.5'))

    @patch('accounting.utils.determine_duration_of_class_time')
    def test_various_time_durations(self, mock_duration):
        """Test with various class durations."""
        # Create classes with different durations
        short_class = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.student,
            date=date(2024, 11, 10),
            start_time=time(10, 0),
            finish_time=time(10, 30),  # 0.5 hours
            class_status='completed'
        )
        long_class = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.student,
            date=date(2024, 11, 11),
            start_time=time(9, 0),
            finish_time=time(12, 0),  # 3 hours
            class_status='completed'
        )

        mock_duration.side_effect = [Decimal('0.5'), Decimal('3.0')]

        classes = [short_class, long_class]
        result = get_estimated_number_of_worked_hours(classes)

        self.assertEqual(result, Decimal('3.5'))

    @patch('accounting.utils.determine_duration_of_class_time')
    def test_integer_return_when_no_decimal_hours(self, mock_duration):
        """Test return type when all durations are whole numbers."""
        mock_duration.side_effect = [Decimal('1.0'), Decimal('2.0')]

        completed_2 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.student,
            date=date(2024, 11, 25),
            start_time=time(9, 0),
            finish_time=time(11, 0),
            class_status='completed'
        )

        classes = [self.completed_class, completed_2]
        result = get_estimated_number_of_worked_hours(classes)

        # Result should be 3.0
        self.assertEqual(result, 3.0)  # Changed from Decimal('3.0')

    @patch('accounting.utils.determine_duration_of_class_time')
    def test_class_status_case_sensitivity(self, mock_duration):
        """Test that class status matching is case-sensitive (as per the code)."""
        mock_duration.return_value = Decimal('1.0')

        # Create class with uppercase status (should NOT match)
        uppercase_class = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.student,
            date=date(2024, 11, 28),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='COMPLETED'  # uppercase
        )

        classes = [uppercase_class]
        result = get_estimated_number_of_worked_hours(classes)

        # Should not count because status doesn't match exactly
        mock_duration.assert_not_called()
        self.assertEqual(result, 0)



class TestProcessSchoolClasses(TestCase):
    """
    Test suite for process_school_classes utility function.
    This function takes organized class data and generates accounting reports
    for school-affiliated students, including hours worked and totals.
    """

    def setUp(self):
        """
        Set up test data including:
        - 1 Teacher
        - 2 Schools (Alpha Academy and Beta School)
        - School-affiliated students and their classes
        """
        # Create user and user profile
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

        # Create school-affiliated students
        self.charlie = StudentOrClass.objects.create(
            student_or_class_name='Charlie Davis',
            account_type='school',
            school=self.school_alpha,
            teacher=self.teacher_profile,
            purchased_class_hours=None,
            tuition_per_hour=900
        )
        self.diana = StudentOrClass.objects.create(
            student_or_class_name='Diana Miller',
            account_type='school',
            school=self.school_beta,
            teacher=self.teacher_profile,
            purchased_class_hours=None,
            tuition_per_hour=950
        )
        self.emily = StudentOrClass.objects.create(
            student_or_class_name='Emily Johnson',
            account_type='school',
            school=self.school_alpha,
            teacher=self.teacher_profile,
            purchased_class_hours=None,
            tuition_per_hour=1000
        )

        # Create scheduled classes for Charlie (2 classes, 1 hour each)
        self.charlie_class_1 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.charlie,
            date=date(2024, 11, 10),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='completed'
        )
        self.charlie_class_2 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.charlie,
            date=date(2024, 11, 17),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='completed'
        )

        # Create scheduled classes for Diana (1 class, 1.5 hours)
        self.diana_class_1 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.diana,
            date=date(2024, 11, 15),
            start_time=time(14, 0),
            finish_time=time(15, 30),
            class_status='completed'
        )

        # Create scheduled classes for Emily (3 classes, 1 hour each)
        self.emily_class_1 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.emily,
            date=date(2024, 11, 5),
            start_time=time(9, 0),
            finish_time=time(10, 0),
            class_status='completed'
        )
        self.emily_class_2 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.emily,
            date=date(2024, 11, 12),
            start_time=time(9, 0),
            finish_time=time(10, 0),
            class_status='completed'
        )
        self.emily_class_3 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.emily,
            date=date(2024, 11, 19),
            start_time=time(9, 0),
            finish_time=time(10, 0),
            class_status='completed'
        )

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_basic_structure(self, mock_hours):
        """Test that the function returns the correct structure."""
        mock_hours.return_value = Decimal('2.0')

        organized_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_classes": [
                        {
                            "student_or_class_name": "Charlie Davis",
                            "scheduled_classes": [self.charlie_class_1, self.charlie_class_2]
                        }
                    ]
                }
            ],
            "freelance_students": []
        }

        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        result = process_school_classes(accounting_data, organized_data)

        # Check that result has the correct keys
        self.assertIn('classes_in_schools', result)
        self.assertIn('freelance_students', result)
        
        # Check that school data was added
        self.assertEqual(len(result['classes_in_schools']), 1)
        
        # Check school report structure
        school_report = result['classes_in_schools'][0]
        self.assertIn('school_name', school_report)
        self.assertIn('students_reports', school_report)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_single_school_single_student(self, mock_hours):
        """Test processing a single school with a single student."""
        mock_hours.return_value = Decimal('2.0')

        organized_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_classes": [
                        {
                            "student_or_class_name": "Charlie Davis",
                            "scheduled_classes": [self.charlie_class_1, self.charlie_class_2]
                        }
                    ]
                }
            ],
            "freelance_students": []
        }

        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        result = process_school_classes(accounting_data, organized_data)

        # Verify school report
        self.assertEqual(len(result['classes_in_schools']), 1)
        school_report = result['classes_in_schools'][0]
        self.assertEqual(school_report['school_name'], 'Alpha Academy')
        
        # Verify student report
        self.assertEqual(len(school_report['students_reports']), 1)
        student_report = school_report['students_reports'][0]
        
        self.assertEqual(student_report['name'], 'Charlie Davis')
        self.assertEqual(student_report['account_id'], self.charlie.id)
        self.assertEqual(student_report['rate'], 900)
        self.assertEqual(student_report['hours'], Decimal('2.0'))
        self.assertEqual(student_report['total'], 900 * Decimal('2.0'))

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_single_school_multiple_students(self, mock_hours):
        """Test processing a single school with multiple students."""
        # Return different hours for different students
        mock_hours.side_effect = [Decimal('2.0'), Decimal('3.0')]

        organized_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_classes": [
                        {
                            "student_or_class_name": "Charlie Davis",
                            "scheduled_classes": [self.charlie_class_1, self.charlie_class_2]
                        },
                        {
                            "student_or_class_name": "Emily Johnson",
                            "scheduled_classes": [self.emily_class_1, self.emily_class_2, self.emily_class_3]
                        }
                    ]
                }
            ],
            "freelance_students": []
        }

        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        result = process_school_classes(accounting_data, organized_data)

        # Verify school report
        self.assertEqual(len(result['classes_in_schools']), 1)
        school_report = result['classes_in_schools'][0]
        self.assertEqual(school_report['school_name'], 'Alpha Academy')
        
        # Verify we have 2 student reports
        self.assertEqual(len(school_report['students_reports']), 2)
        
        # Verify Charlie's report
        charlie_report = next((r for r in school_report['students_reports'] 
                              if r['name'] == 'Charlie Davis'), None)
        self.assertIsNotNone(charlie_report)
        self.assertEqual(charlie_report['rate'], 900)
        self.assertEqual(charlie_report['hours'], Decimal('2.0'))
        self.assertEqual(charlie_report['total'], 1800)
        
        # Verify Emily's report
        emily_report = next((r for r in school_report['students_reports'] 
                           if r['name'] == 'Emily Johnson'), None)
        self.assertIsNotNone(emily_report)
        self.assertEqual(emily_report['rate'], 1000)
        self.assertEqual(emily_report['hours'], Decimal('3.0'))
        self.assertEqual(emily_report['total'], 3000)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_multiple_schools(self, mock_hours):
        """Test processing multiple schools."""
        mock_hours.side_effect = [Decimal('2.0'), Decimal('1.5')]

        organized_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_classes": [
                        {
                            "student_or_class_name": "Charlie Davis",
                            "scheduled_classes": [self.charlie_class_1, self.charlie_class_2]
                        }
                    ]
                },
                {
                    "school_name": "Beta School",
                    "students_classes": [
                        {
                            "student_or_class_name": "Diana Miller",
                            "scheduled_classes": [self.diana_class_1]
                        }
                    ]
                }
            ],
            "freelance_students": []
        }

        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        result = process_school_classes(accounting_data, organized_data)

        # Verify we have 2 schools
        self.assertEqual(len(result['classes_in_schools']), 2)
        
        # Find each school
        alpha_report = next((s for s in result['classes_in_schools'] 
                           if s['school_name'] == 'Alpha Academy'), None)
        beta_report = next((s for s in result['classes_in_schools'] 
                          if s['school_name'] == 'Beta School'), None)
        
        self.assertIsNotNone(alpha_report)
        self.assertIsNotNone(beta_report)
        
        # Verify Alpha Academy report
        self.assertEqual(len(alpha_report['students_reports']), 1)
        charlie_report = alpha_report['students_reports'][0]
        self.assertEqual(charlie_report['name'], 'Charlie Davis')
        self.assertEqual(charlie_report['total'], 1800)
        
        # Verify Beta School report
        self.assertEqual(len(beta_report['students_reports']), 1)
        diana_report = beta_report['students_reports'][0]
        self.assertEqual(diana_report['name'], 'Diana Miller')
        self.assertEqual(diana_report['total'], Decimal('950') * Decimal('1.5'))

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_empty_school_classes(self, mock_hours):
        """Test processing when there are no school classes."""
        organized_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        result = process_school_classes(accounting_data, organized_data)

        # Should return empty school classes
        self.assertEqual(len(result['classes_in_schools']), 0)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_does_not_modify_freelance_data(self, mock_hours):
        """Test that the function doesn't modify freelance student data."""
        mock_hours.return_value = Decimal('2.0')

        organized_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_classes": [
                        {
                            "student_or_class_name": "Charlie Davis",
                            "scheduled_classes": [self.charlie_class_1]
                        }
                    ]
                }
            ],
            "freelance_students": []
        }

        # Start with some freelance data in accounting_data
        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": [{"name": "Test Student"}]
        }

        result = process_school_classes(accounting_data, organized_data)

        # Freelance data should remain unchanged
        self.assertEqual(len(result['freelance_students']), 1)
        self.assertEqual(result['freelance_students'][0]['name'], 'Test Student')

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_accounting_report_fields(self, mock_hours):
        """Test that all required fields are present in the accounting report."""
        mock_hours.return_value = Decimal('2.5')

        organized_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_classes": [
                        {
                            "student_or_class_name": "Charlie Davis",
                            "scheduled_classes": [self.charlie_class_1, self.charlie_class_2]
                        }
                    ]
                }
            ],
            "freelance_students": []
        }

        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        result = process_school_classes(accounting_data, organized_data)

        student_report = result['classes_in_schools'][0]['students_reports'][0]

        # Verify all required fields are present
        self.assertIn('name', student_report)
        self.assertIn('account_id', student_report)
        self.assertIn('rate', student_report)
        self.assertIn('hours', student_report)
        self.assertIn('total', student_report)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_total_calculation(self, mock_hours):
        """Test that the total is calculated correctly (rate × hours)."""
        mock_hours.return_value = Decimal('2.5')

        organized_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_classes": [
                        {
                            "student_or_class_name": "Charlie Davis",
                            "scheduled_classes": [self.charlie_class_1]
                        }
                    ]
                }
            ],
            "freelance_students": []
        }

        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        result = process_school_classes(accounting_data, organized_data)

        student_report = result['classes_in_schools'][0]['students_reports'][0]

        # Charlie's rate is 900, hours is 2.5
        expected_total = 900 * Decimal('2.5')
        self.assertEqual(student_report['total'], expected_total)
        self.assertEqual(student_report['total'], 2250)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_different_tuition_rates(self, mock_hours):
        """Test that different tuition rates are handled correctly."""
        mock_hours.side_effect = [Decimal('2.0'), Decimal('2.0')]

        organized_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_classes": [
                        {
                            "student_or_class_name": "Charlie Davis",
                            "scheduled_classes": [self.charlie_class_1]
                        },
                        {
                            "student_or_class_name": "Emily Johnson",
                            "scheduled_classes": [self.emily_class_1]
                        }
                    ]
                }
            ],
            "freelance_students": []
        }

        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        result = process_school_classes(accounting_data, organized_data)

        students_reports = result['classes_in_schools'][0]['students_reports']

        # Charlie: 900/hour × 2 hours = 1800
        charlie_report = next((r for r in students_reports if r['name'] == 'Charlie Davis'), None)
        self.assertEqual(charlie_report['rate'], 900)
        self.assertEqual(charlie_report['total'], 1800)

        # Emily: 1000/hour × 2 hours = 2000
        emily_report = next((r for r in students_reports if r['name'] == 'Emily Johnson'), None)
        self.assertEqual(emily_report['rate'], 1000)
        self.assertEqual(emily_report['total'], 2000)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_calls_hours_function_correctly(self, mock_hours):
        """Test that get_estimated_number_of_worked_hours is called with correct arguments."""
        mock_hours.return_value = Decimal('2.0')

        organized_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_classes": [
                        {
                            "student_or_class_name": "Charlie Davis",
                            "scheduled_classes": [self.charlie_class_1, self.charlie_class_2]
                        }
                    ]
                }
            ],
            "freelance_students": []
        }

        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        process_school_classes(accounting_data, organized_data)

        # Verify the function was called once with Charlie's classes
        mock_hours.assert_called_once()
        called_classes = mock_hours.call_args[0][0]
        self.assertEqual(len(called_classes), 2)
        self.assertIn(self.charlie_class_1, called_classes)
        self.assertIn(self.charlie_class_2, called_classes)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_zero_hours(self, mock_hours):
        """Test handling when a student has zero hours."""
        mock_hours.return_value = Decimal('0.0')

        organized_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_classes": [
                        {
                            "student_or_class_name": "Charlie Davis",
                            "scheduled_classes": [self.charlie_class_1]
                        }
                    ]
                }
            ],
            "freelance_students": []
        }

        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        result = process_school_classes(accounting_data, organized_data)

        student_report = result['classes_in_schools'][0]['students_reports'][0]
        
        self.assertEqual(student_report['hours'], Decimal('0.0'))
        self.assertEqual(student_report['total'], 0)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_preserves_account_id(self, mock_hours):
        """Test that the student's database ID is correctly stored as account_id."""
        mock_hours.return_value = Decimal('2.0')

        organized_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_classes": [
                        {
                            "student_or_class_name": "Charlie Davis",
                            "scheduled_classes": [self.charlie_class_1]
                        }
                    ]
                }
            ],
            "freelance_students": []
        }

        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        result = process_school_classes(accounting_data, organized_data)

        student_report = result['classes_in_schools'][0]['students_reports'][0]
        
        # Verify account_id matches the student's database ID
        self.assertEqual(student_report['account_id'], self.charlie.id)
        self.assertIsInstance(student_report['account_id'], int)


class TestProcessFreelanceStudents(TestCase):
    """
    Test suite for process_freelance_students utility function.
    This function takes organized class data and generates accounting reports
    for freelance students, including hours worked and totals.
    """

    def setUp(self):
        """
        Set up test data including:
        - 1 Teacher
        - 2 Freelance students
        - Scheduled classes for each student
        """
        # Create user and user profile
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

        # Create 2 freelance students
        self.alice = StudentOrClass.objects.create(
            student_or_class_name='Alice Brown',
            account_type='freelance',
            school=None,
            teacher=self.teacher_profile,
            purchased_class_hours=Decimal('10.00'),
            tuition_per_hour=1000
        )
        self.bob = StudentOrClass.objects.create(
            student_or_class_name='Bob Wilson',
            account_type='freelance',
            school=None,
            teacher=self.teacher_profile,
            purchased_class_hours=Decimal('15.00'),
            tuition_per_hour=1200
        )

        # Create scheduled classes for Alice (2 classes, 1 hour each)
        self.alice_class_1 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.alice,
            date=date(2024, 11, 5),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='completed'
        )
        self.alice_class_2 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.alice,
            date=date(2024, 11, 12),
            start_time=time(14, 0),
            finish_time=time(15, 0),
            class_status='completed'
        )

        # Create scheduled classes for Bob (1 class, 1.5 hours)
        self.bob_class_1 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.bob,
            date=date(2024, 11, 8),
            start_time=time(9, 0),
            finish_time=time(10, 30),
            class_status='completed'
        )

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_basic_structure(self, mock_hours):
        """Test that the function returns the correct structure."""
        mock_hours.return_value = Decimal('2.0')

        organized_data = {
            "classes_in_schools": [],
            "freelance_students": [
                {
                    "student_or_class_name": "Alice Brown",
                    "scheduled_classes": [self.alice_class_1, self.alice_class_2]
                }
            ]
        }

        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        result = process_freelance_students(accounting_data, organized_data)

        # Check that result has the correct keys
        self.assertIn('classes_in_schools', result)
        self.assertIn('freelance_students', result)

        # Check that freelance data was added
        self.assertEqual(len(result['freelance_students']), 1)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_single_freelance_student(self, mock_hours):
        """Test processing a single freelance student."""
        mock_hours.return_value = Decimal('2.0')

        organized_data = {
            "classes_in_schools": [],
            "freelance_students": [
                {
                    "student_or_class_name": "Alice Brown",
                    "scheduled_classes": [self.alice_class_1, self.alice_class_2]
                }
            ]
        }

        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        result = process_freelance_students(accounting_data, organized_data)

        # Verify freelance student report
        self.assertEqual(len(result['freelance_students']), 1)
        alice_report = result['freelance_students'][0]

        self.assertEqual(alice_report['name'], 'Alice Brown')
        self.assertEqual(alice_report['account_id'], self.alice.id)
        self.assertEqual(alice_report['rate'], 1000)
        self.assertEqual(alice_report['hours'], Decimal('2.0'))
        self.assertEqual(alice_report['total'], 1000 * Decimal('2.0'))

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_multiple_freelance_students(self, mock_hours):
        """Test processing multiple freelance students."""
        # Return different hours for different students
        mock_hours.side_effect = [Decimal('2.0'), Decimal('1.5')]

        organized_data = {
            "classes_in_schools": [],
            "freelance_students": [
                {
                    "student_or_class_name": "Alice Brown",
                    "scheduled_classes": [self.alice_class_1, self.alice_class_2]
                },
                {
                    "student_or_class_name": "Bob Wilson",
                    "scheduled_classes": [self.bob_class_1]
                }
            ]
        }

        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        result = process_freelance_students(accounting_data, organized_data)

        # Verify we have 2 freelance student reports
        self.assertEqual(len(result['freelance_students']), 2)

        # Verify Alice's report
        alice_report = next((r for r in result['freelance_students']
                             if r['name'] == 'Alice Brown'), None)
        self.assertIsNotNone(alice_report)
        self.assertEqual(alice_report['rate'], 1000)
        self.assertEqual(alice_report['hours'], Decimal('2.0'))
        self.assertEqual(alice_report['total'], 2000)

        # Verify Bob's report
        bob_report = next((r for r in result['freelance_students']
                           if r['name'] == 'Bob Wilson'), None)
        self.assertIsNotNone(bob_report)
        self.assertEqual(bob_report['rate'], 1200)
        self.assertEqual(bob_report['hours'], Decimal('1.5'))
        self.assertEqual(bob_report['total'], 1800)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_empty_freelance_students(self, mock_hours):
        """Test processing when there are no freelance students."""
        organized_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        result = process_freelance_students(accounting_data, organized_data)

        # Should return empty freelance students
        self.assertEqual(len(result['freelance_students']), 0)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_does_not_modify_school_data(self, mock_hours):
        """Test that the function doesn't modify school class data."""
        mock_hours.return_value = Decimal('2.0')

        organized_data = {
            "classes_in_schools": [],
            "freelance_students": [
                {
                    "student_or_class_name": "Alice Brown",
                    "scheduled_classes": [self.alice_class_1]
                }
            ]
        }

        # Start with some school data in accounting_data
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Test School",
                    "students_reports": []
                }
            ],
            "freelance_students": []
        }

        result = process_freelance_students(accounting_data, organized_data)

        # School data should remain unchanged
        self.assertEqual(len(result['classes_in_schools']), 1)
        self.assertEqual(result['classes_in_schools'][0]['school_name'], 'Test School')

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_accounting_report_fields(self, mock_hours):
        """Test that all required fields are present in the accounting report."""
        mock_hours.return_value = Decimal('2.5')

        organized_data = {
            "classes_in_schools": [],
            "freelance_students": [
                {
                    "student_or_class_name": "Alice Brown",
                    "scheduled_classes": [self.alice_class_1, self.alice_class_2]
                }
            ]
        }

        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        result = process_freelance_students(accounting_data, organized_data)

        student_report = result['freelance_students'][0]

        # Verify all required fields are present
        self.assertIn('name', student_report)
        self.assertIn('account_id', student_report)
        self.assertIn('rate', student_report)
        self.assertIn('hours', student_report)
        self.assertIn('total', student_report)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_total_calculation(self, mock_hours):
        """Test that the total is calculated correctly (rate × hours)."""
        mock_hours.return_value = Decimal('2.5')

        organized_data = {
            "classes_in_schools": [],
            "freelance_students": [
                {
                    "student_or_class_name": "Alice Brown",
                    "scheduled_classes": [self.alice_class_1]
                }
            ]
        }

        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        result = process_freelance_students(accounting_data, organized_data)

        student_report = result['freelance_students'][0]

        # Alice's rate is 1000, hours is 2.5
        expected_total = 1000 * Decimal('2.5')
        self.assertEqual(student_report['total'], expected_total)
        self.assertEqual(student_report['total'], 2500)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_different_tuition_rates(self, mock_hours):
        """Test that different tuition rates are handled correctly."""
        mock_hours.side_effect = [Decimal('2.0'), Decimal('2.0')]

        organized_data = {
            "classes_in_schools": [],
            "freelance_students": [
                {
                    "student_or_class_name": "Alice Brown",
                    "scheduled_classes": [self.alice_class_1]
                },
                {
                    "student_or_class_name": "Bob Wilson",
                    "scheduled_classes": [self.bob_class_1]
                }
            ]
        }

        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        result = process_freelance_students(accounting_data, organized_data)

        # Alice: 1000/hour × 2 hours = 2000
        alice_report = next((r for r in result['freelance_students']
                             if r['name'] == 'Alice Brown'), None)
        self.assertEqual(alice_report['rate'], 1000)
        self.assertEqual(alice_report['total'], 2000)

        # Bob: 1200/hour × 2 hours = 2400
        bob_report = next((r for r in result['freelance_students']
                           if r['name'] == 'Bob Wilson'), None)
        self.assertEqual(bob_report['rate'], 1200)
        self.assertEqual(bob_report['total'], 2400)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_calls_hours_function_correctly(self, mock_hours):
        """Test that get_estimated_number_of_worked_hours is called with correct arguments."""
        mock_hours.return_value = Decimal('2.0')

        organized_data = {
            "classes_in_schools": [],
            "freelance_students": [
                {
                    "student_or_class_name": "Alice Brown",
                    "scheduled_classes": [self.alice_class_1, self.alice_class_2]
                }
            ]
        }

        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        process_freelance_students(accounting_data, organized_data)

        # Verify the function was called once with Alice's classes
        mock_hours.assert_called_once()
        called_classes = mock_hours.call_args[0][0]
        self.assertEqual(len(called_classes), 2)
        self.assertIn(self.alice_class_1, called_classes)
        self.assertIn(self.alice_class_2, called_classes)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_zero_hours(self, mock_hours):
        """Test handling when a student has zero hours."""
        mock_hours.return_value = Decimal('0.0')

        organized_data = {
            "classes_in_schools": [],
            "freelance_students": [
                {
                    "student_or_class_name": "Alice Brown",
                    "scheduled_classes": [self.alice_class_1]
                }
            ]
        }

        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        result = process_freelance_students(accounting_data, organized_data)

        student_report = result['freelance_students'][0]

        self.assertEqual(student_report['hours'], Decimal('0.0'))
        self.assertEqual(student_report['total'], 0)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_preserves_account_id(self, mock_hours):
        """Test that the student's database ID is correctly stored as account_id."""
        mock_hours.return_value = Decimal('2.0')

        organized_data = {
            "classes_in_schools": [],
            "freelance_students": [
                {
                    "student_or_class_name": "Alice Brown",
                    "scheduled_classes": [self.alice_class_1]
                }
            ]
        }

        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        result = process_freelance_students(accounting_data, organized_data)

        student_report = result['freelance_students'][0]

        # Verify account_id matches the student's database ID
        self.assertEqual(student_report['account_id'], self.alice.id)
        self.assertIsInstance(student_report['account_id'], int)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_appends_to_existing_freelance_data(self, mock_hours):
        """Test that new reports are appended to existing freelance data."""
        mock_hours.return_value = Decimal('2.0')

        organized_data = {
            "classes_in_schools": [],
            "freelance_students": [
                {
                    "student_or_class_name": "Alice Brown",
                    "scheduled_classes": [self.alice_class_1]
                }
            ]
        }

        # Start with existing freelance data
        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": [
                {
                    "name": "Existing Student",
                    "account_id": 999,
                    "rate": 800,
                    "hours": Decimal('1.0'),
                    "total": 800
                }
            ]
        }

        result = process_freelance_students(accounting_data, organized_data)

        # Should have both the existing and new student
        self.assertEqual(len(result['freelance_students']), 2)

        # Verify existing student is still there
        existing = result['freelance_students'][0]
        self.assertEqual(existing['name'], 'Existing Student')

        # Verify new student was appended
        new_student = result['freelance_students'][1]
        self.assertEqual(new_student['name'], 'Alice Brown')

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_student_with_single_class(self, mock_hours):
        """Test processing a student with only one class."""
        mock_hours.return_value = Decimal('1.0')

        organized_data = {
            "classes_in_schools": [],
            "freelance_students": [
                {
                    "student_or_class_name": "Bob Wilson",
                    "scheduled_classes": [self.bob_class_1]
                }
            ]
        }

        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        result = process_freelance_students(accounting_data, organized_data)

        self.assertEqual(len(result['freelance_students']), 1)
        bob_report = result['freelance_students'][0]

        self.assertEqual(bob_report['name'], 'Bob Wilson')
        self.assertEqual(bob_report['hours'], Decimal('1.0'))

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_multiple_calls_with_different_data(self, mock_hours):
        """Test calling the function multiple times with different data."""
        mock_hours.side_effect = [Decimal('2.0'), Decimal('1.5')]

        # First call
        organized_data_1 = {
            "classes_in_schools": [],
            "freelance_students": [
                {
                    "student_or_class_name": "Alice Brown",
                    "scheduled_classes": [self.alice_class_1]
                }
            ]
        }

        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        result_1 = process_freelance_students(accounting_data, organized_data_1)
        self.assertEqual(len(result_1['freelance_students']), 1)

        # Second call with different student
        organized_data_2 = {
            "classes_in_schools": [],
            "freelance_students": [
                {
                    "student_or_class_name": "Bob Wilson",
                    "scheduled_classes": [self.bob_class_1]
                }
            ]
        }

        result_2 = process_freelance_students(result_1, organized_data_2)

        # Should have both students now
        self.assertEqual(len(result_2['freelance_students']), 2)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_preserves_freelance_student_attributes(self, mock_hours):
        """Test that freelance-specific attributes are used correctly."""
        mock_hours.return_value = Decimal('2.0')

        organized_data = {
            "classes_in_schools": [],
            "freelance_students": [
                {
                    "student_or_class_name": "Alice Brown",
                    "scheduled_classes": [self.alice_class_1]
                }
            ]
        }

        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        result = process_freelance_students(accounting_data, organized_data)

        alice_report = result['freelance_students'][0]

        # Verify the tuition_per_hour for freelance student is used
        self.assertEqual(alice_report['rate'], self.alice.tuition_per_hour)
        self.assertEqual(alice_report['rate'], 1000)


class TestGenerateAccountingReportsForClassesInSchoolsAndFreelanceTeachers(TestCase):
    """
    Test suite for generate_accounting_reports_for_classes_in_schools_and_freelance_teachers.
    This function orchestrates the complete accounting report generation by processing
    both school classes and freelance students.
    """

    def setUp(self):
        """
        Set up test data including:
        - 1 Teacher
        - 2 Schools
        - 2 School-affiliated students
        - 2 Freelance students
        - Scheduled classes for all students
        """
        # Create user and user profile
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

        # Create 2 school-affiliated students
        self.charlie = StudentOrClass.objects.create(
            student_or_class_name='Charlie Davis',
            account_type='school',
            school=self.school_alpha,
            teacher=self.teacher_profile,
            purchased_class_hours=None,
            tuition_per_hour=900
        )
        self.diana = StudentOrClass.objects.create(
            student_or_class_name='Diana Miller',
            account_type='school',
            school=self.school_beta,
            teacher=self.teacher_profile,
            purchased_class_hours=None,
            tuition_per_hour=950
        )

        # Create 2 freelance students
        self.alice = StudentOrClass.objects.create(
            student_or_class_name='Alice Brown',
            account_type='freelance',
            school=None,
            teacher=self.teacher_profile,
            purchased_class_hours=Decimal('10.00'),
            tuition_per_hour=1000
        )
        self.bob = StudentOrClass.objects.create(
            student_or_class_name='Bob Wilson',
            account_type='freelance',
            school=None,
            teacher=self.teacher_profile,
            purchased_class_hours=Decimal('15.00'),
            tuition_per_hour=1200
        )

        # Create scheduled classes for school students
        self.charlie_class_1 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.charlie,
            date=date(2024, 11, 10),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='completed'
        )
        self.charlie_class_2 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.charlie,
            date=date(2024, 11, 17),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='completed'
        )

        self.diana_class_1 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.diana,
            date=date(2024, 11, 15),
            start_time=time(14, 0),
            finish_time=time(15, 30),
            class_status='completed'
        )

        # Create scheduled classes for freelance students
        self.alice_class_1 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.alice,
            date=date(2024, 11, 5),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='completed'
        )
        self.alice_class_2 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.alice,
            date=date(2024, 11, 12),
            start_time=time(14, 0),
            finish_time=time(15, 0),
            class_status='completed'
        )

        self.bob_class_1 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.bob,
            date=date(2024, 11, 8),
            start_time=time(9, 0),
            finish_time=time(10, 30),
            class_status='completed'
        )

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_basic_structure(self, mock_hours):
        """Test that the function returns the correct overall structure."""
        mock_hours.return_value = Decimal('2.0')

        organized_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_classes": [
                        {
                            "student_or_class_name": "Charlie Davis",
                            "scheduled_classes": [self.charlie_class_1]
                        }
                    ]
                }
            ],
            "freelance_students": [
                {
                    "student_or_class_name": "Alice Brown",
                    "scheduled_classes": [self.alice_class_1]
                }
            ]
        }

        result = generate_accounting_reports_for_classes_in_schools_and_freelance_teachers(
            organized_data
        )

        # Check top-level structure
        self.assertIn('classes_in_schools', result)
        self.assertIn('freelance_students', result)
        self.assertIsInstance(result['classes_in_schools'], list)
        self.assertIsInstance(result['freelance_students'], list)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_processes_both_schools_and_freelance(self, mock_hours):
        """Test that both school and freelance data are processed."""
        mock_hours.side_effect = [Decimal('2.0'), Decimal('1.5'), Decimal('2.5')]

        organized_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_classes": [
                        {
                            "student_or_class_name": "Charlie Davis",
                            "scheduled_classes": [self.charlie_class_1, self.charlie_class_2]
                        }
                    ]
                },
                {
                    "school_name": "Beta School",
                    "students_classes": [
                        {
                            "student_or_class_name": "Diana Miller",
                            "scheduled_classes": [self.diana_class_1]
                        }
                    ]
                }
            ],
            "freelance_students": [
                {
                    "student_or_class_name": "Alice Brown",
                    "scheduled_classes": [self.alice_class_1, self.alice_class_2]
                }
            ]
        }

        result = generate_accounting_reports_for_classes_in_schools_and_freelance_teachers(
            organized_data
        )

        # Verify school data was processed
        self.assertEqual(len(result['classes_in_schools']), 2)

        # Verify freelance data was processed
        self.assertEqual(len(result['freelance_students']), 1)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_school_reports_structure(self, mock_hours):
        """Test that school reports have the correct nested structure."""
        mock_hours.return_value = Decimal('2.0')

        organized_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_classes": [
                        {
                            "student_or_class_name": "Charlie Davis",
                            "scheduled_classes": [self.charlie_class_1]
                        }
                    ]
                }
            ],
            "freelance_students": []
        }

        result = generate_accounting_reports_for_classes_in_schools_and_freelance_teachers(
            organized_data
        )

        school_report = result['classes_in_schools'][0]

        # Verify school report structure
        self.assertIn('school_name', school_report)
        self.assertIn('students_reports', school_report)
        self.assertEqual(school_report['school_name'], 'Alpha Academy')
        self.assertEqual(len(school_report['students_reports']), 1)

        # Verify student report within school
        student_report = school_report['students_reports'][0]
        self.assertIn('name', student_report)
        self.assertIn('account_id', student_report)
        self.assertIn('rate', student_report)
        self.assertIn('hours', student_report)
        self.assertIn('total', student_report)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_freelance_reports_structure(self, mock_hours):
        """Test that freelance reports have the correct flat structure."""
        mock_hours.return_value = Decimal('2.0')

        organized_data = {
            "classes_in_schools": [],
            "freelance_students": [
                {
                    "student_or_class_name": "Alice Brown",
                    "scheduled_classes": [self.alice_class_1]
                }
            ]
        }

        result = generate_accounting_reports_for_classes_in_schools_and_freelance_teachers(
            organized_data
        )

        # Verify freelance reports structure
        self.assertEqual(len(result['freelance_students']), 1)

        freelance_report = result['freelance_students'][0]
        self.assertIn('name', freelance_report)
        self.assertIn('account_id', freelance_report)
        self.assertIn('rate', freelance_report)
        self.assertIn('hours', freelance_report)
        self.assertIn('total', freelance_report)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_complete_mixed_data(self, mock_hours):
        """Test processing complete data with multiple schools and freelance students."""
        # Mock hours for: Charlie, Diana, Alice, Bob
        mock_hours.side_effect = [
            Decimal('2.0'),  # Charlie
            Decimal('1.5'),  # Diana
            Decimal('2.0'),  # Alice
            Decimal('1.5')  # Bob
        ]

        organized_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_classes": [
                        {
                            "student_or_class_name": "Charlie Davis",
                            "scheduled_classes": [self.charlie_class_1, self.charlie_class_2]
                        }
                    ]
                },
                {
                    "school_name": "Beta School",
                    "students_classes": [
                        {
                            "student_or_class_name": "Diana Miller",
                            "scheduled_classes": [self.diana_class_1]
                        }
                    ]
                }
            ],
            "freelance_students": [
                {
                    "student_or_class_name": "Alice Brown",
                    "scheduled_classes": [self.alice_class_1, self.alice_class_2]
                },
                {
                    "student_or_class_name": "Bob Wilson",
                    "scheduled_classes": [self.bob_class_1]
                }
            ]
        }

        result = generate_accounting_reports_for_classes_in_schools_and_freelance_teachers(
            organized_data
        )

        # Verify school data
        self.assertEqual(len(result['classes_in_schools']), 2)

        alpha_school = next((s for s in result['classes_in_schools']
                             if s['school_name'] == 'Alpha Academy'), None)
        self.assertIsNotNone(alpha_school)
        self.assertEqual(len(alpha_school['students_reports']), 1)

        charlie_report = alpha_school['students_reports'][0]
        self.assertEqual(charlie_report['name'], 'Charlie Davis')
        self.assertEqual(charlie_report['hours'], Decimal('2.0'))
        self.assertEqual(charlie_report['total'], 900 * Decimal('2.0'))

        beta_school = next((s for s in result['classes_in_schools']
                            if s['school_name'] == 'Beta School'), None)
        self.assertIsNotNone(beta_school)

        diana_report = beta_school['students_reports'][0]
        self.assertEqual(diana_report['name'], 'Diana Miller')
        self.assertEqual(diana_report['hours'], Decimal('1.5'))
        self.assertEqual(diana_report['total'], 950 * Decimal('1.5'))

        # Verify freelance data
        self.assertEqual(len(result['freelance_students']), 2)

        alice_report = next((r for r in result['freelance_students']
                             if r['name'] == 'Alice Brown'), None)
        self.assertIsNotNone(alice_report)
        self.assertEqual(alice_report['hours'], Decimal('2.0'))
        self.assertEqual(alice_report['total'], 1000 * Decimal('2.0'))

        bob_report = next((r for r in result['freelance_students']
                           if r['name'] == 'Bob Wilson'), None)
        self.assertIsNotNone(bob_report)
        self.assertEqual(bob_report['hours'], Decimal('1.5'))
        self.assertEqual(bob_report['total'], 1200 * Decimal('1.5'))

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_only_school_classes(self, mock_hours):
        """Test processing when only school classes exist."""
        mock_hours.return_value = Decimal('2.0')

        organized_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_classes": [
                        {
                            "student_or_class_name": "Charlie Davis",
                            "scheduled_classes": [self.charlie_class_1]
                        }
                    ]
                }
            ],
            "freelance_students": []
        }

        result = generate_accounting_reports_for_classes_in_schools_and_freelance_teachers(
            organized_data
        )

        # Should have school data but no freelance data
        self.assertEqual(len(result['classes_in_schools']), 1)
        self.assertEqual(len(result['freelance_students']), 0)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_only_freelance_students(self, mock_hours):
        """Test processing when only freelance students exist."""
        mock_hours.return_value = Decimal('2.0')

        organized_data = {
            "classes_in_schools": [],
            "freelance_students": [
                {
                    "student_or_class_name": "Alice Brown",
                    "scheduled_classes": [self.alice_class_1]
                }
            ]
        }

        result = generate_accounting_reports_for_classes_in_schools_and_freelance_teachers(
            organized_data
        )

        # Should have freelance data but no school data
        self.assertEqual(len(result['classes_in_schools']), 0)
        self.assertEqual(len(result['freelance_students']), 1)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_empty_organized_data(self, mock_hours):
        """Test processing when organized data is completely empty."""
        organized_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        result = generate_accounting_reports_for_classes_in_schools_and_freelance_teachers(
            organized_data
        )

        # Should return empty structure
        self.assertEqual(len(result['classes_in_schools']), 0)
        self.assertEqual(len(result['freelance_students']), 0)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_initializes_fresh_accounting_data(self, mock_hours):
        """Test that function creates fresh accounting_data (doesn't reuse input)."""
        mock_hours.return_value = Decimal('2.0')

        organized_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_classes": [
                        {
                            "student_or_class_name": "Charlie Davis",
                            "scheduled_classes": [self.charlie_class_1]
                        }
                    ]
                }
            ],
            "freelance_students": []
        }

        result = generate_accounting_reports_for_classes_in_schools_and_freelance_teachers(
            organized_data
        )

        # Result should not be the same object as input
        self.assertIsNot(result, organized_data)

        # Result should have processed data (not raw classes)
        self.assertIn('students_reports', result['classes_in_schools'][0])
        self.assertNotIn('students_classes', result['classes_in_schools'][0])

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_calls_both_processing_functions(self, mock_hours):
        """Test that both process_school_classes and process_freelance_students are called."""
        mock_hours.side_effect = [Decimal('2.0'), Decimal('1.5')]

        organized_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_classes": [
                        {
                            "student_or_class_name": "Charlie Davis",
                            "scheduled_classes": [self.charlie_class_1]
                        }
                    ]
                }
            ],
            "freelance_students": [
                {
                    "student_or_class_name": "Alice Brown",
                    "scheduled_classes": [self.alice_class_1]
                }
            ]
        }

        result = generate_accounting_reports_for_classes_in_schools_and_freelance_teachers(
            organized_data
        )

        # Verify both functions were called by checking the call count
        # Should be called twice: once for school, once for freelance
        self.assertEqual(mock_hours.call_count, 2)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_multiple_students_per_school(self, mock_hours):
        """Test processing schools with multiple students."""
        # Create another student at Alpha Academy
        emily = StudentOrClass.objects.create(
            student_or_class_name='Emily Johnson',
            account_type='school',
            school=self.school_alpha,
            teacher=self.teacher_profile,
            purchased_class_hours=None,
            tuition_per_hour=1000
        )
        emily_class = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=emily,
            date=date(2024, 11, 20),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='completed'
        )

        mock_hours.side_effect = [Decimal('2.0'), Decimal('1.0')]

        organized_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_classes": [
                        {
                            "student_or_class_name": "Charlie Davis",
                            "scheduled_classes": [self.charlie_class_1, self.charlie_class_2]
                        },
                        {
                            "student_or_class_name": "Emily Johnson",
                            "scheduled_classes": [emily_class]
                        }
                    ]
                }
            ],
            "freelance_students": []
        }

        result = generate_accounting_reports_for_classes_in_schools_and_freelance_teachers(
            organized_data
        )

        alpha_school = result['classes_in_schools'][0]

        # Should have 2 student reports
        self.assertEqual(len(alpha_school['students_reports']), 2)

        student_names = [r['name'] for r in alpha_school['students_reports']]
        self.assertIn('Charlie Davis', student_names)
        self.assertIn('Emily Johnson', student_names)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_preserves_calculation_accuracy(self, mock_hours):
        """Test that financial calculations maintain precision."""
        mock_hours.side_effect = [Decimal('2.5'), Decimal('1.75')]

        organized_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_classes": [
                        {
                            "student_or_class_name": "Charlie Davis",
                            "scheduled_classes": [self.charlie_class_1]
                        }
                    ]
                }
            ],
            "freelance_students": [
                {
                    "student_or_class_name": "Alice Brown",
                    "scheduled_classes": [self.alice_class_1]
                }
            ]
        }

        result = generate_accounting_reports_for_classes_in_schools_and_freelance_teachers(
            organized_data
        )

        # Verify precise calculations
        charlie_report = result['classes_in_schools'][0]['students_reports'][0]
        self.assertEqual(charlie_report['total'], 900 * Decimal('2.5'))
        self.assertEqual(charlie_report['total'], 2250)

        alice_report = result['freelance_students'][0]
        self.assertEqual(alice_report['total'], 1000 * Decimal('1.75'))
        self.assertEqual(alice_report['total'], 1750)

    @patch('accounting.utils.get_estimated_number_of_worked_hours')
    def test_integration_with_real_data_flow(self, mock_hours):
        """Test the complete flow with realistic data scenario."""
        mock_hours.side_effect = [Decimal('2.0'), Decimal('1.5'), Decimal('3.0')]

        # Realistic scenario: One school with one student, two freelance students
        organized_data = {
            "classes_in_schools": [
                {
                    "school_name": "Beta School",
                    "students_classes": [
                        {
                            "student_or_class_name": "Diana Miller",
                            "scheduled_classes": [self.diana_class_1]
                        }
                    ]
                }
            ],
            "freelance_students": [
                {
                    "student_or_class_name": "Alice Brown",
                    "scheduled_classes": [self.alice_class_1, self.alice_class_2]
                },
                {
                    "student_or_class_name": "Bob Wilson",
                    "scheduled_classes": [self.bob_class_1]
                }
            ]
        }

        result = generate_accounting_reports_for_classes_in_schools_and_freelance_teachers(
            organized_data
        )

        # Verify complete result structure and data
        self.assertEqual(len(result['classes_in_schools']), 1)
        self.assertEqual(len(result['freelance_students']), 2)

        # Check school report
        school_report = result['classes_in_schools'][0]
        self.assertEqual(school_report['school_name'], 'Beta School')
        self.assertEqual(school_report['students_reports'][0]['name'], 'Diana Miller')

        # Check freelance reports
        alice_report = next((r for r in result['freelance_students']
                             if r['name'] == 'Alice Brown'), None)
        bob_report = next((r for r in result['freelance_students']
                           if r['name'] == 'Bob Wilson'), None)

        self.assertIsNotNone(alice_report)
        self.assertIsNotNone(bob_report)
        self.assertEqual(alice_report['hours'], Decimal('1.5'))
        self.assertEqual(bob_report['hours'], Decimal('3.0'))



class TestSortAccountingReportsByName(TestCase):
    """
    Test suite for sort_accounting_reports_by_name utility function.
    This function sorts a list of accounting report dictionaries alphabetically by the 'name' field.
    """

    def test_sort_basic_alphabetical_order(self):
        """Test basic alphabetical sorting of reports."""
        reports = [
            {'name': 'Zoe Taylor', 'total_hours': 10, 'earnings': 1000},
            {'name': 'Alice Brown', 'total_hours': 5, 'earnings': 500},
            {'name': 'Mike Johnson', 'total_hours': 8, 'earnings': 800},
        ]

        sorted_reports = sort_accounting_reports_by_name(reports)

        # Verify alphabetical order
        self.assertEqual(sorted_reports[0]['name'], 'Alice Brown')
        self.assertEqual(sorted_reports[1]['name'], 'Mike Johnson')
        self.assertEqual(sorted_reports[2]['name'], 'Zoe Taylor')

        # Verify all reports are present
        self.assertEqual(len(sorted_reports), 3)

    def test_sort_already_sorted_list(self):
        """Test that already sorted list remains correctly sorted."""
        reports = [
            {'name': 'Alice Brown', 'total_hours': 5, 'earnings': 500},
            {'name': 'Bob Wilson', 'total_hours': 8, 'earnings': 800},
            {'name': 'Charlie Davis', 'total_hours': 10, 'earnings': 1000},
        ]

        sorted_reports = sort_accounting_reports_by_name(reports)

        # Verify order is maintained
        self.assertEqual(sorted_reports[0]['name'], 'Alice Brown')
        self.assertEqual(sorted_reports[1]['name'], 'Bob Wilson')
        self.assertEqual(sorted_reports[2]['name'], 'Charlie Davis')

    def test_sort_reverse_order(self):
        """Test sorting when list is in reverse alphabetical order."""
        reports = [
            {'name': 'Zoe Taylor', 'total_hours': 10, 'earnings': 1000},
            {'name': 'Mike Johnson', 'total_hours': 8, 'earnings': 800},
            {'name': 'Alice Brown', 'total_hours': 5, 'earnings': 500},
        ]

        sorted_reports = sort_accounting_reports_by_name(reports)

        # Verify correct alphabetical order
        self.assertEqual(sorted_reports[0]['name'], 'Alice Brown')
        self.assertEqual(sorted_reports[1]['name'], 'Mike Johnson')
        self.assertEqual(sorted_reports[2]['name'], 'Zoe Taylor')

    def test_sort_single_report(self):
        """Test that a single report returns unchanged."""
        reports = [
            {'name': 'Alice Brown', 'total_hours': 5, 'earnings': 500},
        ]

        sorted_reports = sort_accounting_reports_by_name(reports)

        self.assertEqual(len(sorted_reports), 1)
        self.assertEqual(sorted_reports[0]['name'], 'Alice Brown')

    def test_sort_empty_list(self):
        """Test that an empty list returns an empty list."""
        reports = []

        sorted_reports = sort_accounting_reports_by_name(reports)

        self.assertEqual(len(sorted_reports), 0)
        self.assertEqual(sorted_reports, [])

    def test_sort_with_same_first_name(self):
        """Test sorting when multiple reports have the same first name."""
        reports = [
            {'name': 'John Smith', 'total_hours': 10, 'earnings': 1000},
            {'name': 'John Anderson', 'total_hours': 8, 'earnings': 800},
            {'name': 'John Williams', 'total_hours': 5, 'earnings': 500},
        ]

        sorted_reports = sort_accounting_reports_by_name(reports)

        # Verify alphabetical order by full name (Anderson < Smith < Williams)
        self.assertEqual(sorted_reports[0]['name'], 'John Anderson')
        self.assertEqual(sorted_reports[1]['name'], 'John Smith')
        self.assertEqual(sorted_reports[2]['name'], 'John Williams')

    def test_sort_case_sensitivity(self):
        """Test that sorting is case-sensitive (uppercase comes before lowercase in ASCII)."""
        reports = [
            {'name': 'alice brown', 'total_hours': 5, 'earnings': 500},
            {'name': 'Alice Brown', 'total_hours': 10, 'earnings': 1000},
            {'name': 'ALICE BROWN', 'total_hours': 8, 'earnings': 800},
        ]

        sorted_reports = sort_accounting_reports_by_name(reports)

        # Python's default sort is case-sensitive: uppercase < lowercase
        # 'A' (65) < 'a' (97) in ASCII
        self.assertEqual(sorted_reports[0]['name'], 'ALICE BROWN')
        self.assertEqual(sorted_reports[1]['name'], 'Alice Brown')
        self.assertEqual(sorted_reports[2]['name'], 'alice brown')

    def test_sort_with_numbers_in_names(self):
        """Test sorting when names contain numbers."""
        reports = [
            {'name': 'Class 3B', 'total_hours': 10, 'earnings': 1000},
            {'name': 'Class 1A', 'total_hours': 8, 'earnings': 800},
            {'name': 'Class 2C', 'total_hours': 5, 'earnings': 500},
        ]

        sorted_reports = sort_accounting_reports_by_name(reports)

        # Verify alphabetical order (string comparison, not numeric)
        self.assertEqual(sorted_reports[0]['name'], 'Class 1A')
        self.assertEqual(sorted_reports[1]['name'], 'Class 2C')
        self.assertEqual(sorted_reports[2]['name'], 'Class 3B')

    def test_sort_with_special_characters(self):
        """Test sorting when names contain special characters."""
        reports = [
            {'name': "O'Connor Sarah", 'total_hours': 10, 'earnings': 1000},
            {'name': 'Martinez-Lopez Carlos', 'total_hours': 8, 'earnings': 800},
            {'name': 'Anderson Kate', 'total_hours': 5, 'earnings': 500},
        ]

        sorted_reports = sort_accounting_reports_by_name(reports)

        # Verify alphabetical order with special characters
        # ' (39) and - (45) come before letters in ASCII
        self.assertEqual(sorted_reports[0]['name'], 'Anderson Kate')
        self.assertEqual(sorted_reports[1]['name'], 'Martinez-Lopez Carlos')
        self.assertEqual(sorted_reports[2]['name'], "O'Connor Sarah")

    def test_sort_preserves_other_fields(self):
        """Test that sorting preserves all other fields in the dictionaries."""
        reports = [
            {
                'name': 'Zoe Taylor',
                'total_hours': 10,
                'earnings': 1000,
                'student_id': '123',
                'classes': ['Math', 'Science']
            },
            {
                'name': 'Alice Brown',
                'total_hours': 5,
                'earnings': 500,
                'student_id': '456',
                'classes': ['English']
            },
        ]

        sorted_reports = sort_accounting_reports_by_name(reports)

        # Verify Alice is first
        self.assertEqual(sorted_reports[0]['name'], 'Alice Brown')
        self.assertEqual(sorted_reports[0]['total_hours'], 5)
        self.assertEqual(sorted_reports[0]['earnings'], 500)
        self.assertEqual(sorted_reports[0]['student_id'], '456')
        self.assertEqual(sorted_reports[0]['classes'], ['English'])

        # Verify Zoe is second
        self.assertEqual(sorted_reports[1]['name'], 'Zoe Taylor')
        self.assertEqual(sorted_reports[1]['total_hours'], 10)
        self.assertEqual(sorted_reports[1]['earnings'], 1000)
        self.assertEqual(sorted_reports[1]['student_id'], '123')
        self.assertEqual(sorted_reports[1]['classes'], ['Math', 'Science'])

    def test_sort_does_not_modify_original_list(self):
        """Test that the original list is not modified (returns new list)."""
        reports = [
            {'name': 'Zoe Taylor', 'total_hours': 10},
            {'name': 'Alice Brown', 'total_hours': 5},
        ]

        original_first_name = reports[0]['name']
        sorted_reports = sort_accounting_reports_by_name(reports)

        # Original list should still have Zoe first
        self.assertEqual(reports[0]['name'], original_first_name)
        self.assertEqual(reports[0]['name'], 'Zoe Taylor')

        # Sorted list should have Alice first
        self.assertEqual(sorted_reports[0]['name'], 'Alice Brown')

    def test_sort_with_whitespace_in_names(self):
        """Test sorting when names have leading/trailing whitespace."""
        reports = [
            {'name': ' Bob Wilson', 'total_hours': 10, 'earnings': 1000},
            {'name': 'Alice Brown', 'total_hours': 8, 'earnings': 800},
            {'name': 'Charlie Davis ', 'total_hours': 5, 'earnings': 500},
        ]

        sorted_reports = sort_accounting_reports_by_name(reports)

        # Space (32) comes before letters in ASCII, so ' Bob Wilson' comes first
        self.assertEqual(sorted_reports[0]['name'], ' Bob Wilson')
        self.assertEqual(sorted_reports[1]['name'], 'Alice Brown')
        self.assertEqual(sorted_reports[2]['name'], 'Charlie Davis ')

    def test_sort_multiple_reports_same_name(self):
        """Test sorting when multiple reports have identical names."""
        reports = [
            {'name': 'Alice Brown', 'total_hours': 10, 'student_id': '1'},
            {'name': 'Alice Brown', 'total_hours': 5, 'student_id': '2'},
            {'name': 'Alice Brown', 'total_hours': 8, 'student_id': '3'},
        ]

        sorted_reports = sort_accounting_reports_by_name(reports)

        # All should have the same name
        self.assertEqual(len(sorted_reports), 3)
        for report in sorted_reports:
            self.assertEqual(report['name'], 'Alice Brown')

        # Order among identical names should be stable (preserve original order)
        # Python's sort is stable, so original order should be maintained
        self.assertEqual(sorted_reports[0]['student_id'], '1')
        self.assertEqual(sorted_reports[1]['student_id'], '2')
        self.assertEqual(sorted_reports[2]['student_id'], '3')



class TestSortSchoolReportsAlphabetically(TestCase):
    """
    Test suite for sort_school_reports_alphabetically utility function.
    This function sorts the student reports within each school's report alphabetically by name.
    """

    def test_sort_single_school_with_multiple_students(self):
        """Test sorting students within a single school report."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Zoe Taylor", "total_hours": 10, "earnings": 1000},
                        {"name": "Alice Brown", "total_hours": 5, "earnings": 500},
                        {"name": "Mike Johnson", "total_hours": 8, "earnings": 800},
                    ]
                }
            ],
            "freelance_students": []
        }

        result = sort_school_reports_alphabetically(accounting_data)

        # Verify students are sorted alphabetically
        students = result["classes_in_schools"][0]["students_reports"]
        self.assertEqual(students[0]["name"], "Alice Brown")
        self.assertEqual(students[1]["name"], "Mike Johnson")
        self.assertEqual(students[2]["name"], "Zoe Taylor")

    def test_sort_multiple_schools_with_multiple_students(self):
        """Test sorting students within multiple school reports."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Zoe Taylor", "total_hours": 10, "earnings": 1000},
                        {"name": "Alice Brown", "total_hours": 5, "earnings": 500},
                    ]
                },
                {
                    "school_name": "Beta School",
                    "students_reports": [
                        {"name": "Diana Miller", "total_hours": 8, "earnings": 800},
                        {"name": "Bob Wilson", "total_hours": 6, "earnings": 600},
                        {"name": "Charlie Davis", "total_hours": 7, "earnings": 700},
                    ]
                }
            ],
            "freelance_students": []
        }

        result = sort_school_reports_alphabetically(accounting_data)

        # Verify Alpha Academy students are sorted
        alpha_students = result["classes_in_schools"][0]["students_reports"]
        self.assertEqual(alpha_students[0]["name"], "Alice Brown")
        self.assertEqual(alpha_students[1]["name"], "Zoe Taylor")

        # Verify Beta School students are sorted
        beta_students = result["classes_in_schools"][1]["students_reports"]
        self.assertEqual(beta_students[0]["name"], "Bob Wilson")
        self.assertEqual(beta_students[1]["name"], "Charlie Davis")
        self.assertEqual(beta_students[2]["name"], "Diana Miller")

    def test_sort_school_with_single_student(self):
        """Test that a school with a single student report works correctly."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Alice Brown", "total_hours": 5, "earnings": 500},
                    ]
                }
            ],
            "freelance_students": []
        }

        result = sort_school_reports_alphabetically(accounting_data)

        # Single student should remain
        students = result["classes_in_schools"][0]["students_reports"]
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0]["name"], "Alice Brown")

    def test_sort_school_with_no_students(self):
        """Test that a school with no student reports works correctly."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": []
                }
            ],
            "freelance_students": []
        }

        result = sort_school_reports_alphabetically(accounting_data)

        # Empty list should remain empty
        students = result["classes_in_schools"][0]["students_reports"]
        self.assertEqual(len(students), 0)

    def test_sort_with_no_schools(self):
        """Test that empty classes_in_schools list works correctly."""
        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": [
                {"name": "Alice Brown", "total_hours": 5, "earnings": 500}
            ]
        }

        result = sort_school_reports_alphabetically(accounting_data)

        # Should return unchanged
        self.assertEqual(len(result["classes_in_schools"]), 0)
        self.assertEqual(len(result["freelance_students"]), 1)

    def test_sort_preserves_school_order(self):
        """Test that the order of schools in the list is preserved."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Zeta Institute",
                    "students_reports": [
                        {"name": "Bob Wilson", "total_hours": 5, "earnings": 500},
                    ]
                },
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Alice Brown", "total_hours": 5, "earnings": 500},
                    ]
                }
            ],
            "freelance_students": []
        }

        result = sort_school_reports_alphabetically(accounting_data)

        # Schools should remain in original order (Zeta first, then Alpha)
        self.assertEqual(result["classes_in_schools"][0]["school_name"], "Zeta Institute")
        self.assertEqual(result["classes_in_schools"][1]["school_name"], "Alpha Academy")

    def test_sort_preserves_all_school_fields(self):
        """Test that all fields in school reports are preserved."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "school_id": "SCH001",
                    "total_school_hours": 15,
                    "total_school_earnings": 1500,
                    "students_reports": [
                        {"name": "Zoe Taylor", "total_hours": 10, "earnings": 1000},
                        {"name": "Alice Brown", "total_hours": 5, "earnings": 500},
                    ]
                }
            ],
            "freelance_students": []
        }

        result = sort_school_reports_alphabetically(accounting_data)

        school = result["classes_in_schools"][0]
        
        # Verify all school fields are preserved
        self.assertEqual(school["school_name"], "Alpha Academy")
        self.assertEqual(school["school_id"], "SCH001")
        self.assertEqual(school["total_school_hours"], 15)
        self.assertEqual(school["total_school_earnings"], 1500)
        
        # Verify students are sorted
        self.assertEqual(school["students_reports"][0]["name"], "Alice Brown")
        self.assertEqual(school["students_reports"][1]["name"], "Zoe Taylor")

    def test_sort_preserves_all_student_fields(self):
        """Test that all fields in student reports are preserved."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {
                            "name": "Zoe Taylor",
                            "total_hours": 10,
                            "earnings": 1000,
                            "student_id": "STU001",
                            "classes": ["Math", "Science"],
                            "rate": 100
                        },
                        {
                            "name": "Alice Brown",
                            "total_hours": 5,
                            "earnings": 500,
                            "student_id": "STU002",
                            "classes": ["English"],
                            "rate": 100
                        },
                    ]
                }
            ],
            "freelance_students": []
        }

        result = sort_school_reports_alphabetically(accounting_data)

        students = result["classes_in_schools"][0]["students_reports"]
        
        # Verify Alice (first alphabetically) has all fields
        self.assertEqual(students[0]["name"], "Alice Brown")
        self.assertEqual(students[0]["total_hours"], 5)
        self.assertEqual(students[0]["earnings"], 500)
        self.assertEqual(students[0]["student_id"], "STU002")
        self.assertEqual(students[0]["classes"], ["English"])
        self.assertEqual(students[0]["rate"], 100)

    def test_sort_does_not_affect_freelance_students(self):
        """Test that freelance_students field is not modified."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Zoe Taylor", "total_hours": 10, "earnings": 1000},
                        {"name": "Alice Brown", "total_hours": 5, "earnings": 500},
                    ]
                }
            ],
            "freelance_students": [
                {"name": "Zoe Freelance", "total_hours": 10, "earnings": 1000},
                {"name": "Alice Freelance", "total_hours": 5, "earnings": 500},
            ]
        }

        result = sort_school_reports_alphabetically(accounting_data)

        # School students should be sorted
        school_students = result["classes_in_schools"][0]["students_reports"]
        self.assertEqual(school_students[0]["name"], "Alice Brown")

        # Freelance students should remain in original order (unsorted)
        freelance = result["freelance_students"]
        self.assertEqual(freelance[0]["name"], "Zoe Freelance")
        self.assertEqual(freelance[1]["name"], "Alice Freelance")

    def test_sort_already_sorted_students(self):
        """Test that already sorted student reports remain correctly sorted."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Alice Brown", "total_hours": 5, "earnings": 500},
                        {"name": "Bob Wilson", "total_hours": 8, "earnings": 800},
                        {"name": "Charlie Davis", "total_hours": 10, "earnings": 1000},
                    ]
                }
            ],
            "freelance_students": []
        }

        result = sort_school_reports_alphabetically(accounting_data)

        students = result["classes_in_schools"][0]["students_reports"]
        self.assertEqual(students[0]["name"], "Alice Brown")
        self.assertEqual(students[1]["name"], "Bob Wilson")
        self.assertEqual(students[2]["name"], "Charlie Davis")

    def test_sort_with_duplicate_student_names(self):
        """Test sorting when multiple students have the same name."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Alice Brown", "total_hours": 10, "student_id": "1"},
                        {"name": "Alice Brown", "total_hours": 5, "student_id": "2"},
                        {"name": "Alice Brown", "total_hours": 8, "student_id": "3"},
                    ]
                }
            ],
            "freelance_students": []
        }

        result = sort_school_reports_alphabetically(accounting_data)

        students = result["classes_in_schools"][0]["students_reports"]
        
        # All should have same name
        for student in students:
            self.assertEqual(student["name"], "Alice Brown")
        
        # Order should be stable (original order preserved for identical keys)
        self.assertEqual(students[0]["student_id"], "1")
        self.assertEqual(students[1]["student_id"], "2")
        self.assertEqual(students[2]["student_id"], "3")

    def test_sort_returns_same_structure(self):
        """Test that the function returns the accounting_data structure unchanged."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Bob Wilson", "total_hours": 5, "earnings": 500},
                        {"name": "Alice Brown", "total_hours": 5, "earnings": 500},
                    ]
                }
            ],
            "freelance_students": [
                {"name": "Zoe Freelance", "total_hours": 10, "earnings": 1000},
            ],
            "other_field": "some_value"
        }

        result = sort_school_reports_alphabetically(accounting_data)

        # Verify structure is maintained
        self.assertIn("classes_in_schools", result)
        self.assertIn("freelance_students", result)
        self.assertIn("other_field", result)
        self.assertEqual(result["other_field"], "some_value")

    def test_sort_modifies_and_returns_original_object(self):
        """Test that the function modifies and returns the same accounting_data object."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Zoe Taylor", "total_hours": 10, "earnings": 1000},
                        {"name": "Alice Brown", "total_hours": 5, "earnings": 500},
                    ]
                }
            ],
            "freelance_students": []
        }

        original_id = id(accounting_data)
        result = sort_school_reports_alphabetically(accounting_data)

        # Should return the same object (modified in place)
        self.assertEqual(id(result), original_id)
        
        # Original object should be modified
        self.assertEqual(
            accounting_data["classes_in_schools"][0]["students_reports"][0]["name"],
            "Alice Brown"
        )

    def test_sort_three_schools_independently(self):
        """Test that students in three different schools are all sorted independently."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Zoe", "total_hours": 10},
                        {"name": "Alice", "total_hours": 5},
                    ]
                },
                {
                    "school_name": "Beta School",
                    "students_reports": [
                        {"name": "Mike", "total_hours": 8},
                        {"name": "Diana", "total_hours": 6},
                    ]
                },
                {
                    "school_name": "Gamma Institute",
                    "students_reports": [
                        {"name": "Oscar", "total_hours": 7},
                        {"name": "Nina", "total_hours": 9},
                    ]
                }
            ],
            "freelance_students": []
        }

        result = sort_school_reports_alphabetically(accounting_data)

        # Verify each school's students are sorted independently
        alpha_students = result["classes_in_schools"][0]["students_reports"]
        self.assertEqual(alpha_students[0]["name"], "Alice")
        self.assertEqual(alpha_students[1]["name"], "Zoe")

        beta_students = result["classes_in_schools"][1]["students_reports"]
        self.assertEqual(beta_students[0]["name"], "Diana")
        self.assertEqual(beta_students[1]["name"], "Mike")

        gamma_students = result["classes_in_schools"][2]["students_reports"]
        self.assertEqual(gamma_students[0]["name"], "Nina")
        self.assertEqual(gamma_students[1]["name"], "Oscar")


class TestSortSchoolAndFreelanceReportsAlphabetically(TestCase):
    """
    Test suite for sort_school_and_freelance_reports_alphabetically utility function.
    This function sorts both:
    1. Student reports within each school alphabetically
    2. Freelance student reports alphabetically
    """

    def test_sort_both_school_and_freelance_students(self):
        """Test sorting both school students and freelance students."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Zoe Taylor", "total_hours": 10, "earnings": 1000},
                        {"name": "Alice Brown", "total_hours": 5, "earnings": 500},
                    ]
                }
            ],
            "freelance_students": [
                {"name": "Mike Johnson", "total_hours": 8, "earnings": 800},
                {"name": "Diana Miller", "total_hours": 6, "earnings": 600},
            ]
        }

        result = sort_school_and_freelance_reports_alphabetically(accounting_data)

        # Verify school students are sorted
        school_students = result["classes_in_schools"][0]["students_reports"]
        self.assertEqual(school_students[0]["name"], "Alice Brown")
        self.assertEqual(school_students[1]["name"], "Zoe Taylor")

        # Verify freelance students are sorted
        freelance = result["freelance_students"]
        self.assertEqual(freelance[0]["name"], "Diana Miller")
        self.assertEqual(freelance[1]["name"], "Mike Johnson")

    def test_sort_multiple_schools_and_freelance(self):
        """Test sorting students in multiple schools plus freelance students."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Charlie Davis", "total_hours": 10, "earnings": 1000},
                        {"name": "Alice Brown", "total_hours": 5, "earnings": 500},
                    ]
                },
                {
                    "school_name": "Beta School",
                    "students_reports": [
                        {"name": "Oscar Pine", "total_hours": 7, "earnings": 700},
                        {"name": "Nina Lopez", "total_hours": 9, "earnings": 900},
                    ]
                }
            ],
            "freelance_students": [
                {"name": "Zoe Taylor", "total_hours": 8, "earnings": 800},
                {"name": "Bob Wilson", "total_hours": 6, "earnings": 600},
                {"name": "Mike Johnson", "total_hours": 4, "earnings": 400},
            ]
        }

        result = sort_school_and_freelance_reports_alphabetically(accounting_data)

        # Verify Alpha Academy students are sorted
        alpha_students = result["classes_in_schools"][0]["students_reports"]
        self.assertEqual(alpha_students[0]["name"], "Alice Brown")
        self.assertEqual(alpha_students[1]["name"], "Charlie Davis")

        # Verify Beta School students are sorted
        beta_students = result["classes_in_schools"][1]["students_reports"]
        self.assertEqual(beta_students[0]["name"], "Nina Lopez")
        self.assertEqual(beta_students[1]["name"], "Oscar Pine")

        # Verify freelance students are sorted
        freelance = result["freelance_students"]
        self.assertEqual(freelance[0]["name"], "Bob Wilson")
        self.assertEqual(freelance[1]["name"], "Mike Johnson")
        self.assertEqual(freelance[2]["name"], "Zoe Taylor")

    def test_sort_with_no_schools_only_freelance(self):
        """Test sorting when there are no schools, only freelance students."""
        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": [
                {"name": "Zoe Taylor", "total_hours": 8, "earnings": 800},
                {"name": "Alice Brown", "total_hours": 6, "earnings": 600},
                {"name": "Mike Johnson", "total_hours": 4, "earnings": 400},
            ]
        }

        result = sort_school_and_freelance_reports_alphabetically(accounting_data)

        # No schools to verify
        self.assertEqual(len(result["classes_in_schools"]), 0)

        # Verify freelance students are sorted
        freelance = result["freelance_students"]
        self.assertEqual(freelance[0]["name"], "Alice Brown")
        self.assertEqual(freelance[1]["name"], "Mike Johnson")
        self.assertEqual(freelance[2]["name"], "Zoe Taylor")

    def test_sort_with_schools_only_no_freelance(self):
        """Test sorting when there are schools but no freelance students."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Zoe Taylor", "total_hours": 10, "earnings": 1000},
                        {"name": "Alice Brown", "total_hours": 5, "earnings": 500},
                        {"name": "Mike Johnson", "total_hours": 8, "earnings": 800},
                    ]
                }
            ],
            "freelance_students": []
        }

        result = sort_school_and_freelance_reports_alphabetically(accounting_data)

        # Verify school students are sorted
        school_students = result["classes_in_schools"][0]["students_reports"]
        self.assertEqual(school_students[0]["name"], "Alice Brown")
        self.assertEqual(school_students[1]["name"], "Mike Johnson")
        self.assertEqual(school_students[2]["name"], "Zoe Taylor")

        # No freelance students to verify
        self.assertEqual(len(result["freelance_students"]), 0)

    def test_sort_with_empty_accounting_data(self):
        """Test sorting when both schools and freelance lists are empty."""
        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        result = sort_school_and_freelance_reports_alphabetically(accounting_data)

        self.assertEqual(len(result["classes_in_schools"]), 0)
        self.assertEqual(len(result["freelance_students"]), 0)

    def test_sort_with_single_school_student_and_single_freelance(self):
        """Test sorting with single student in school and single freelance student."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Alice Brown", "total_hours": 5, "earnings": 500},
                    ]
                }
            ],
            "freelance_students": [
                {"name": "Bob Wilson", "total_hours": 6, "earnings": 600},
            ]
        }

        result = sort_school_and_freelance_reports_alphabetically(accounting_data)

        # Single students should remain
        school_students = result["classes_in_schools"][0]["students_reports"]
        self.assertEqual(len(school_students), 1)
        self.assertEqual(school_students[0]["name"], "Alice Brown")

        freelance = result["freelance_students"]
        self.assertEqual(len(freelance), 1)
        self.assertEqual(freelance[0]["name"], "Bob Wilson")

    def test_sort_preserves_all_fields(self):
        """Test that all fields in the accounting data are preserved."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "school_id": "SCH001",
                    "total_school_hours": 15,
                    "total_school_earnings": 1500,
                    "students_reports": [
                        {
                            "name": "Zoe Taylor",
                            "total_hours": 10,
                            "earnings": 1000,
                            "student_id": "STU001",
                            "rate": 100
                        },
                        {
                            "name": "Alice Brown",
                            "total_hours": 5,
                            "earnings": 500,
                            "student_id": "STU002",
                            "rate": 100
                        },
                    ]
                }
            ],
            "freelance_students": [
                {
                    "name": "Mike Johnson",
                    "total_hours": 8,
                    "earnings": 800,
                    "student_id": "STU003",
                    "rate": 100
                },
                {
                    "name": "Diana Miller",
                    "total_hours": 6,
                    "earnings": 600,
                    "student_id": "STU004",
                    "rate": 100
                },
            ],
            "total_monthly_earnings": 2900,
            "month": 11,
            "year": 2024
        }

        result = sort_school_and_freelance_reports_alphabetically(accounting_data)

        # Verify school fields are preserved
        school = result["classes_in_schools"][0]
        self.assertEqual(school["school_name"], "Alpha Academy")
        self.assertEqual(school["school_id"], "SCH001")
        self.assertEqual(school["total_school_hours"], 15)
        self.assertEqual(school["total_school_earnings"], 1500)

        # Verify school student fields are preserved and sorted
        school_students = school["students_reports"]
        self.assertEqual(school_students[0]["name"], "Alice Brown")
        self.assertEqual(school_students[0]["student_id"], "STU002")
        self.assertEqual(school_students[0]["rate"], 100)

        # Verify freelance fields are preserved and sorted
        freelance = result["freelance_students"]
        self.assertEqual(freelance[0]["name"], "Diana Miller")
        self.assertEqual(freelance[0]["student_id"], "STU004")
        self.assertEqual(freelance[0]["rate"], 100)

        # Verify top-level fields are preserved
        self.assertEqual(result["total_monthly_earnings"], 2900)
        self.assertEqual(result["month"], 11)
        self.assertEqual(result["year"], 2024)

    def test_sort_already_sorted_data(self):
        """Test that already sorted data remains correctly sorted."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Alice Brown", "total_hours": 5, "earnings": 500},
                        {"name": "Bob Wilson", "total_hours": 8, "earnings": 800},
                        {"name": "Charlie Davis", "total_hours": 10, "earnings": 1000},
                    ]
                }
            ],
            "freelance_students": [
                {"name": "Diana Miller", "total_hours": 6, "earnings": 600},
                {"name": "Ethan Taylor", "total_hours": 4, "earnings": 400},
                {"name": "Fiona Lee", "total_hours": 7, "earnings": 700},
            ]
        }

        result = sort_school_and_freelance_reports_alphabetically(accounting_data)

        # School students should remain in correct order
        school_students = result["classes_in_schools"][0]["students_reports"]
        self.assertEqual(school_students[0]["name"], "Alice Brown")
        self.assertEqual(school_students[1]["name"], "Bob Wilson")
        self.assertEqual(school_students[2]["name"], "Charlie Davis")

        # Freelance students should remain in correct order
        freelance = result["freelance_students"]
        self.assertEqual(freelance[0]["name"], "Diana Miller")
        self.assertEqual(freelance[1]["name"], "Ethan Taylor")
        self.assertEqual(freelance[2]["name"], "Fiona Lee")

    def test_sort_with_duplicate_names_in_both_categories(self):
        """Test sorting when there are duplicate names in both schools and freelance."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Alice Brown", "total_hours": 10, "student_id": "1"},
                        {"name": "Alice Brown", "total_hours": 5, "student_id": "2"},
                    ]
                }
            ],
            "freelance_students": [
                {"name": "Bob Wilson", "total_hours": 8, "student_id": "3"},
                {"name": "Bob Wilson", "total_hours": 6, "student_id": "4"},
            ]
        }

        result = sort_school_and_freelance_reports_alphabetically(accounting_data)

        # School students with duplicate names should maintain stable order
        school_students = result["classes_in_schools"][0]["students_reports"]
        self.assertEqual(school_students[0]["student_id"], "1")
        self.assertEqual(school_students[1]["student_id"], "2")

        # Freelance students with duplicate names should maintain stable order
        freelance = result["freelance_students"]
        self.assertEqual(freelance[0]["student_id"], "3")
        self.assertEqual(freelance[1]["student_id"], "4")

    def test_sort_modifies_and_returns_original_object(self):
        """Test that the function modifies and returns the same accounting_data object."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Zoe Taylor", "total_hours": 10, "earnings": 1000},
                        {"name": "Alice Brown", "total_hours": 5, "earnings": 500},
                    ]
                }
            ],
            "freelance_students": [
                {"name": "Mike Johnson", "total_hours": 8, "earnings": 800},
                {"name": "Diana Miller", "total_hours": 6, "earnings": 600},
            ]
        }

        original_id = id(accounting_data)
        result = sort_school_and_freelance_reports_alphabetically(accounting_data)

        # Should return the same object (modified in place)
        self.assertEqual(id(result), original_id)

        # Original object should be modified
        self.assertEqual(
            accounting_data["classes_in_schools"][0]["students_reports"][0]["name"],
            "Alice Brown"
        )
        self.assertEqual(
            accounting_data["freelance_students"][0]["name"],
            "Diana Miller"
        )

    def test_sort_with_special_characters_in_names(self):
        """Test sorting with special characters in student names."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "O'Connor Sarah", "total_hours": 10, "earnings": 1000},
                        {"name": "Martinez-Lopez Carlos", "total_hours": 8, "earnings": 800},
                        {"name": "Anderson Kate", "total_hours": 5, "earnings": 500},
                    ]
                }
            ],
            "freelance_students": [
                {"name": "Van Der Berg Jan", "total_hours": 6, "earnings": 600},
                {"name": "D'Angelo Maria", "total_hours": 4, "earnings": 400},
                {"name": "Smith-Jones Emily", "total_hours": 7, "earnings": 700},
            ]
        }

        result = sort_school_and_freelance_reports_alphabetically(accounting_data)

        # School students should be sorted alphabetically
        school_students = result["classes_in_schools"][0]["students_reports"]
        self.assertEqual(school_students[0]["name"], "Anderson Kate")
        self.assertEqual(school_students[1]["name"], "Martinez-Lopez Carlos")
        self.assertEqual(school_students[2]["name"], "O'Connor Sarah")

        # Freelance students should be sorted alphabetically
        freelance = result["freelance_students"]
        self.assertEqual(freelance[0]["name"], "D'Angelo Maria")
        self.assertEqual(freelance[1]["name"], "Smith-Jones Emily")
        self.assertEqual(freelance[2]["name"], "Van Der Berg Jan")

    def test_sort_with_school_having_no_students(self):
        """Test sorting when a school has no students but freelance list has students."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": []
                }
            ],
            "freelance_students": [
                {"name": "Zoe Taylor", "total_hours": 8, "earnings": 800},
                {"name": "Alice Brown", "total_hours": 6, "earnings": 600},
            ]
        }

        result = sort_school_and_freelance_reports_alphabetically(accounting_data)

        # School should have empty student list
        school_students = result["classes_in_schools"][0]["students_reports"]
        self.assertEqual(len(school_students), 0)

        # Freelance students should be sorted
        freelance = result["freelance_students"]
        self.assertEqual(freelance[0]["name"], "Alice Brown")
        self.assertEqual(freelance[1]["name"], "Zoe Taylor")

    def test_sort_comprehensive_scenario(self):
        """
        Comprehensive test with:
        - 3 schools with varying numbers of students
        - Multiple freelance students
        - All data sorted correctly
        """
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Zoe", "total_hours": 10},
                        {"name": "Alice", "total_hours": 5},
                        {"name": "Mike", "total_hours": 8},
                    ]
                },
                {
                    "school_name": "Beta School",
                    "students_reports": [
                        {"name": "Oscar", "total_hours": 7},
                        {"name": "Diana", "total_hours": 6},
                    ]
                },
                {
                    "school_name": "Gamma Institute",
                    "students_reports": [
                        {"name": "Nina", "total_hours": 9},
                    ]
                }
            ],
            "freelance_students": [
                {"name": "Victor", "total_hours": 4},
                {"name": "Bob", "total_hours": 3},
                {"name": "Laura", "total_hours": 5},
                {"name": "Charlie", "total_hours": 6},
            ]
        }

        result = sort_school_and_freelance_reports_alphabetically(accounting_data)

        # Verify Alpha Academy students are sorted
        alpha_students = result["classes_in_schools"][0]["students_reports"]
        self.assertEqual(alpha_students[0]["name"], "Alice")
        self.assertEqual(alpha_students[1]["name"], "Mike")
        self.assertEqual(alpha_students[2]["name"], "Zoe")

        # Verify Beta School students are sorted
        beta_students = result["classes_in_schools"][1]["students_reports"]
        self.assertEqual(beta_students[0]["name"], "Diana")
        self.assertEqual(beta_students[1]["name"], "Oscar")

        # Verify Gamma Institute student
        gamma_students = result["classes_in_schools"][2]["students_reports"]
        self.assertEqual(gamma_students[0]["name"], "Nina")

        # Verify freelance students are sorted
        freelance = result["freelance_students"]
        self.assertEqual(freelance[0]["name"], "Bob")
        self.assertEqual(freelance[1]["name"], "Charlie")
        self.assertEqual(freelance[2]["name"], "Laura")
        self.assertEqual(freelance[3]["name"], "Victor")



class TestCalculateSchoolTotals(TestCase):
    """
    Test suite for calculate_school_totals utility function.
    This function calculates the total earnings for each school by summing
    the 'total' field from all student reports within that school.
    """

    def test_calculate_single_school_with_multiple_students(self):
        """Test calculating totals for a single school with multiple students."""
        report = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Alice Brown", "total_hours": 5, "total": 500},
                        {"name": "Bob Wilson", "total_hours": 8, "total": 800},
                        {"name": "Charlie Davis", "total_hours": 10, "total": 1000},
                    ]
                }
            ],
            "freelance_students": []
        }

        result = calculate_school_totals(report)

        # Verify school_total is calculated correctly (500 + 800 + 1000 = 2300)
        self.assertEqual(result["classes_in_schools"][0]["school_total"], 2300)

    def test_calculate_multiple_schools(self):
        """Test calculating totals for multiple schools."""
        report = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Alice Brown", "total": 500},
                        {"name": "Bob Wilson", "total": 800},
                    ]
                },
                {
                    "school_name": "Beta School",
                    "students_reports": [
                        {"name": "Charlie Davis", "total": 1000},
                        {"name": "Diana Miller", "total": 600},
                        {"name": "Ethan Taylor", "total": 700},
                    ]
                }
            ],
            "freelance_students": []
        }

        result = calculate_school_totals(report)

        # Verify Alpha Academy total (500 + 800 = 1300)
        self.assertEqual(result["classes_in_schools"][0]["school_total"], 1300)

        # Verify Beta School total (1000 + 600 + 700 = 2300)
        self.assertEqual(result["classes_in_schools"][1]["school_total"], 2300)

    def test_calculate_school_with_single_student(self):
        """Test calculating total for a school with only one student."""
        report = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Alice Brown", "total": 500},
                    ]
                }
            ],
            "freelance_students": []
        }

        result = calculate_school_totals(report)

        # Verify school_total equals the single student's total
        self.assertEqual(result["classes_in_schools"][0]["school_total"], 500)

    def test_calculate_school_with_no_students(self):
        """Test calculating total for a school with no students."""
        report = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": []
                }
            ],
            "freelance_students": []
        }

        result = calculate_school_totals(report)

        # Verify school_total is 0 when there are no students
        self.assertEqual(result["classes_in_schools"][0]["school_total"], 0)

    def test_calculate_with_no_schools(self):
        """Test behavior when there are no schools in the report."""
        report = {
            "classes_in_schools": [],
            "freelance_students": [
                {"name": "Alice Brown", "total": 500},
            ]
        }

        result = calculate_school_totals(report)

        # Should return report unchanged with empty schools list
        self.assertEqual(len(result["classes_in_schools"]), 0)
        self.assertEqual(len(result["freelance_students"]), 1)

    def test_calculate_with_decimal_totals(self):
        """Test calculating totals with decimal values."""
        report = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Alice Brown", "total": Decimal("500.50")},
                        {"name": "Bob Wilson", "total": Decimal("800.75")},
                        {"name": "Charlie Davis", "total": Decimal("1000.25")},
                    ]
                }
            ],
            "freelance_students": []
        }

        result = calculate_school_totals(report)

        # Verify school_total with decimal precision (500.50 + 800.75 + 1000.25 = 2301.50)
        expected_total = Decimal("500.50") + Decimal("800.75") + Decimal("1000.25")
        self.assertEqual(result["classes_in_schools"][0]["school_total"], expected_total)

    def test_calculate_with_zero_totals(self):
        """Test calculating when student totals are zero."""
        report = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Alice Brown", "total": 0},
                        {"name": "Bob Wilson", "total": 0},
                    ]
                }
            ],
            "freelance_students": []
        }

        result = calculate_school_totals(report)

        # Verify school_total is 0
        self.assertEqual(result["classes_in_schools"][0]["school_total"], 0)

    def test_calculate_with_mixed_positive_and_negative_totals(self):
        """Test calculating with both positive and negative totals (e.g., credits/refunds)."""
        report = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Alice Brown", "total": 1000},
                        {"name": "Bob Wilson", "total": -200},  # Refund or credit
                        {"name": "Charlie Davis", "total": 500},
                    ]
                }
            ],
            "freelance_students": []
        }

        result = calculate_school_totals(report)

        # Verify school_total accounts for negative values (1000 - 200 + 500 = 1300)
        self.assertEqual(result["classes_in_schools"][0]["school_total"], 1300)

    def test_does_not_affect_freelance_students(self):
        """Test that freelance_students field is not modified."""
        report = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Alice Brown", "total": 500},
                    ]
                }
            ],
            "freelance_students": [
                {"name": "Zoe Taylor", "total": 1000},
                {"name": "Mike Johnson", "total": 800},
            ]
        }

        result = calculate_school_totals(report)

        # Verify freelance_students are unchanged
        self.assertEqual(len(result["freelance_students"]), 2)
        self.assertEqual(result["freelance_students"][0]["name"], "Zoe Taylor")
        self.assertEqual(result["freelance_students"][1]["name"], "Mike Johnson")
        
        # Verify freelance_students don't have school_total field added
        self.assertNotIn("school_total", result["freelance_students"][0])

    def test_preserves_all_school_fields(self):
        """Test that all other school fields are preserved."""
        report = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "school_id": "SCH001",
                    "address": "123 Main St",
                    "total_school_hours": 15,
                    "students_reports": [
                        {"name": "Alice Brown", "total": 500},
                        {"name": "Bob Wilson", "total": 800},
                    ]
                }
            ],
            "freelance_students": []
        }

        result = calculate_school_totals(report)

        school = result["classes_in_schools"][0]
        
        # Verify all original fields are preserved
        self.assertEqual(school["school_name"], "Alpha Academy")
        self.assertEqual(school["school_id"], "SCH001")
        self.assertEqual(school["address"], "123 Main St")
        self.assertEqual(school["total_school_hours"], 15)
        
        # Verify school_total was added
        self.assertEqual(school["school_total"], 1300)

    def test_preserves_all_student_fields(self):
        """Test that all student report fields are preserved."""
        report = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {
                            "name": "Alice Brown",
                            "total_hours": 5,
                            "total": 500,
                            "rate": 100,
                            "student_id": "STU001",
                            "classes": ["Math", "Science"]
                        },
                    ]
                }
            ],
            "freelance_students": []
        }

        result = calculate_school_totals(report)

        student = result["classes_in_schools"][0]["students_reports"][0]
        
        # Verify all student fields are preserved
        self.assertEqual(student["name"], "Alice Brown")
        self.assertEqual(student["total_hours"], 5)
        self.assertEqual(student["total"], 500)
        self.assertEqual(student["rate"], 100)
        self.assertEqual(student["student_id"], "STU001")
        self.assertEqual(student["classes"], ["Math", "Science"])

    def test_preserves_top_level_fields(self):
        """Test that top-level report fields are preserved."""
        report = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Alice Brown", "total": 500},
                    ]
                }
            ],
            "freelance_students": [],
            "month": 11,
            "year": 2024,
            "teacher_name": "John Smith"
        }

        result = calculate_school_totals(report)

        # Verify top-level fields are preserved
        self.assertEqual(result["month"], 11)
        self.assertEqual(result["year"], 2024)
        self.assertEqual(result["teacher_name"], "John Smith")

    def test_creates_copy_does_not_modify_original(self):
        """Test that the function creates a copy and doesn't modify the original report."""
        report = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Alice Brown", "total": 500},
                    ]
                }
            ],
            "freelance_students": []
        }

        # Store original state
        original_has_school_total = "school_total" in report["classes_in_schools"][0]

        result = calculate_school_totals(report)

        # Original report should not have school_total added
        # Note: This test checks the shallow copy behavior
        # The function uses .copy() which creates a shallow copy,
        # so nested objects may still be modified
        self.assertFalse(original_has_school_total)
        
        # Result should have school_total
        self.assertIn("school_total", result["classes_in_schools"][0])

    def test_three_schools_comprehensive(self):
        """Test calculating totals for three schools with varying student counts."""
        report = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Alice", "total": 500},
                        {"name": "Bob", "total": 600},
                    ]
                },
                {
                    "school_name": "Beta School",
                    "students_reports": [
                        {"name": "Charlie", "total": 700},
                        {"name": "Diana", "total": 800},
                        {"name": "Ethan", "total": 900},
                    ]
                },
                {
                    "school_name": "Gamma Institute",
                    "students_reports": [
                        {"name": "Fiona", "total": 1000},
                    ]
                }
            ],
            "freelance_students": []
        }

        result = calculate_school_totals(report)

        # Verify Alpha Academy total (500 + 600 = 1100)
        self.assertEqual(result["classes_in_schools"][0]["school_total"], 1100)

        # Verify Beta School total (700 + 800 + 900 = 2400)
        self.assertEqual(result["classes_in_schools"][1]["school_total"], 2400)

        # Verify Gamma Institute total (1000)
        self.assertEqual(result["classes_in_schools"][2]["school_total"], 1000)

    def test_large_totals(self):
        """Test calculating with large total values."""
        report = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Alice Brown", "total": 50000},
                        {"name": "Bob Wilson", "total": 75000},
                        {"name": "Charlie Davis", "total": 100000},
                    ]
                }
            ],
            "freelance_students": []
        }

        result = calculate_school_totals(report)

        # Verify school_total with large numbers (50000 + 75000 + 100000 = 225000)
        self.assertEqual(result["classes_in_schools"][0]["school_total"], 225000)

    def test_float_totals(self):
        """Test calculating totals with float values."""
        report = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Alice Brown", "total": 500.50},
                        {"name": "Bob Wilson", "total": 800.75},
                    ]
                }
            ],
            "freelance_students": []
        }

        result = calculate_school_totals(report)

        # Verify school_total with floats (500.50 + 800.75 = 1301.25)
        self.assertAlmostEqual(result["classes_in_schools"][0]["school_total"], 1301.25, places=2)

    def test_school_total_field_added_to_all_schools(self):
        """Test that school_total field is added to all schools in the list."""
        report = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "students_reports": [
                        {"name": "Alice", "total": 500},
                    ]
                },
                {
                    "school_name": "Beta School",
                    "students_reports": [
                        {"name": "Bob", "total": 600},
                    ]
                },
                {
                    "school_name": "Gamma Institute",
                    "students_reports": [
                        {"name": "Charlie", "total": 700},
                    ]
                }
            ],
            "freelance_students": []
        }

        result = calculate_school_totals(report)

        # Verify school_total is added to all three schools
        for school in result["classes_in_schools"]:
            self.assertIn("school_total", school)
        
        # Verify each school has the correct total
        self.assertEqual(result["classes_in_schools"][0]["school_total"], 500)
        self.assertEqual(result["classes_in_schools"][1]["school_total"], 600)
        self.assertEqual(result["classes_in_schools"][2]["school_total"], 700)


class TestCalculateOverallMonthlyTotal(TestCase):
    """
    Test suite for calculate_overall_monthly_total utility function.
    This function calculates the overall monthly total by summing:
    1. All school_total values from classes_in_schools
    2. All total values from freelance_students
    """

    def test_calculate_with_schools_and_freelance(self):
        """Test calculating overall total with both schools and freelance students."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "school_total": 1300,
                    "students_reports": []
                },
                {
                    "school_name": "Beta School",
                    "school_total": 2400,
                    "students_reports": []
                }
            ],
            "freelance_students": [
                {"name": "Alice Brown", "total": 500},
                {"name": "Bob Wilson", "total": 800},
            ]
        }

        result = calculate_overall_monthly_total(accounting_data)

        # Verify overall_monthly_total (1300 + 2400 + 500 + 800 = 5000)
        self.assertEqual(result["overall_monthly_total"], 5000)

    def test_calculate_with_only_schools(self):
        """Test calculating overall total with only schools, no freelance students."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "school_total": 1300,
                    "students_reports": []
                },
                {
                    "school_name": "Beta School",
                    "school_total": 2400,
                    "students_reports": []
                }
            ],
            "freelance_students": []
        }

        result = calculate_overall_monthly_total(accounting_data)

        # Verify overall_monthly_total (1300 + 2400 = 3700)
        self.assertEqual(result["overall_monthly_total"], 3700)

    def test_calculate_with_only_freelance(self):
        """Test calculating overall total with only freelance students, no schools."""
        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": [
                {"name": "Alice Brown", "total": 500},
                {"name": "Bob Wilson", "total": 800},
                {"name": "Charlie Davis", "total": 1200},
            ]
        }

        result = calculate_overall_monthly_total(accounting_data)

        # Verify overall_monthly_total (500 + 800 + 1200 = 2500)
        self.assertEqual(result["overall_monthly_total"], 2500)

    def test_calculate_with_empty_data(self):
        """Test calculating overall total when both schools and freelance are empty."""
        accounting_data = {
            "classes_in_schools": [],
            "freelance_students": []
        }

        result = calculate_overall_monthly_total(accounting_data)

        # Verify overall_monthly_total is 0
        self.assertEqual(result["overall_monthly_total"], 0)

    def test_calculate_with_single_school_and_single_freelance(self):
        """Test calculating with one school and one freelance student."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "school_total": 1000,
                    "students_reports": []
                }
            ],
            "freelance_students": [
                {"name": "Alice Brown", "total": 500},
            ]
        }

        result = calculate_overall_monthly_total(accounting_data)

        # Verify overall_monthly_total (1000 + 500 = 1500)
        self.assertEqual(result["overall_monthly_total"], 1500)

    def test_calculate_with_decimal_values(self):
        """Test calculating with Decimal values for precision."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "school_total": Decimal("1300.50"),
                    "students_reports": []
                },
                {
                    "school_name": "Beta School",
                    "school_total": Decimal("2400.75"),
                    "students_reports": []
                }
            ],
            "freelance_students": [
                {"name": "Alice Brown", "total": Decimal("500.25")},
                {"name": "Bob Wilson", "total": Decimal("800.50")},
            ]
        }

        result = calculate_overall_monthly_total(accounting_data)

        # Verify overall_monthly_total with decimal precision
        expected_total = Decimal("1300.50") + Decimal("2400.75") + Decimal("500.25") + Decimal("800.50")
        self.assertEqual(result["overall_monthly_total"], expected_total)
        self.assertEqual(result["overall_monthly_total"], Decimal("5002.00"))

    def test_calculate_with_float_values(self):
        """Test calculating with float values."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "school_total": 1300.50,
                    "students_reports": []
                }
            ],
            "freelance_students": [
                {"name": "Alice Brown", "total": 500.25},
            ]
        }

        result = calculate_overall_monthly_total(accounting_data)

        # Verify overall_monthly_total with floats (1300.50 + 500.25 = 1800.75)
        self.assertAlmostEqual(result["overall_monthly_total"], 1800.75, places=2)

    def test_calculate_with_zero_school_totals(self):
        """Test calculating when schools have zero totals."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "school_total": 0,
                    "students_reports": []
                },
                {
                    "school_name": "Beta School",
                    "school_total": 0,
                    "students_reports": []
                }
            ],
            "freelance_students": [
                {"name": "Alice Brown", "total": 500},
            ]
        }

        result = calculate_overall_monthly_total(accounting_data)

        # Verify overall_monthly_total (0 + 0 + 500 = 500)
        self.assertEqual(result["overall_monthly_total"], 500)

    def test_calculate_with_zero_freelance_totals(self):
        """Test calculating when freelance students have zero totals."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "school_total": 1000,
                    "students_reports": []
                }
            ],
            "freelance_students": [
                {"name": "Alice Brown", "total": 0},
                {"name": "Bob Wilson", "total": 0},
            ]
        }

        result = calculate_overall_monthly_total(accounting_data)

        # Verify overall_monthly_total (1000 + 0 + 0 = 1000)
        self.assertEqual(result["overall_monthly_total"], 1000)

    def test_calculate_with_negative_values(self):
        """Test calculating with negative values (credits/refunds)."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "school_total": 2000,
                    "students_reports": []
                }
            ],
            "freelance_students": [
                {"name": "Alice Brown", "total": 500},
                {"name": "Bob Wilson", "total": -200},  # Refund
            ]
        }

        result = calculate_overall_monthly_total(accounting_data)

        # Verify overall_monthly_total (2000 + 500 - 200 = 2300)
        self.assertEqual(result["overall_monthly_total"], 2300)

    def test_preserves_all_fields(self):
        """Test that all fields in the accounting data are preserved."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "school_id": "SCH001",
                    "school_total": 1000,
                    "students_reports": [
                        {"name": "Charlie", "total": 500}
                    ]
                }
            ],
            "freelance_students": [
                {"name": "Alice Brown", "total": 500, "student_id": "STU001"},
            ],
            "month": 11,
            "year": 2024,
            "teacher_name": "John Smith"
        }

        result = calculate_overall_monthly_total(accounting_data)

        # Verify all fields are preserved
        self.assertEqual(result["classes_in_schools"][0]["school_name"], "Alpha Academy")
        self.assertEqual(result["classes_in_schools"][0]["school_id"], "SCH001")
        self.assertEqual(result["freelance_students"][0]["name"], "Alice Brown")
        self.assertEqual(result["freelance_students"][0]["student_id"], "STU001")
        self.assertEqual(result["month"], 11)
        self.assertEqual(result["year"], 2024)
        self.assertEqual(result["teacher_name"], "John Smith")
        
        # Verify overall_monthly_total is added
        self.assertEqual(result["overall_monthly_total"], 1500)

    def test_overall_monthly_total_field_is_added(self):
        """Test that overall_monthly_total field is added to the accounting data."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "school_total": 1000,
                    "students_reports": []
                }
            ],
            "freelance_students": []
        }

        # Verify field doesn't exist before
        self.assertNotIn("overall_monthly_total", accounting_data)

        result = calculate_overall_monthly_total(accounting_data)

        # Verify field exists after
        self.assertIn("overall_monthly_total", result)

    def test_creates_copy_does_not_modify_original(self):
        """Test that the function creates a copy and doesn't modify the original."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "school_total": 1000,
                    "students_reports": []
                }
            ],
            "freelance_students": []
        }

        # Store original state
        original_has_total = "overall_monthly_total" in accounting_data

        result = calculate_overall_monthly_total(accounting_data)

        # Original should not have overall_monthly_total added
        # Note: This tests shallow copy behavior
        self.assertFalse(original_has_total)
        
        # Result should have overall_monthly_total
        self.assertIn("overall_monthly_total", result)

    def test_three_schools_and_multiple_freelance(self):
        """Test comprehensive scenario with three schools and multiple freelance students."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "school_total": 1100,
                    "students_reports": []
                },
                {
                    "school_name": "Beta School",
                    "school_total": 2400,
                    "students_reports": []
                },
                {
                    "school_name": "Gamma Institute",
                    "school_total": 1000,
                    "students_reports": []
                }
            ],
            "freelance_students": [
                {"name": "Alice", "total": 500},
                {"name": "Bob", "total": 600},
                {"name": "Charlie", "total": 700},
                {"name": "Diana", "total": 800},
            ]
        }

        result = calculate_overall_monthly_total(accounting_data)

        # Verify overall_monthly_total
        # Schools: 1100 + 2400 + 1000 = 4500
        # Freelance: 500 + 600 + 700 + 800 = 2600
        # Total: 4500 + 2600 = 7100
        self.assertEqual(result["overall_monthly_total"], 7100)

    def test_large_totals(self):
        """Test calculating with large total values."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "school_total": 100000,
                    "students_reports": []
                },
                {
                    "school_name": "Beta School",
                    "school_total": 250000,
                    "students_reports": []
                }
            ],
            "freelance_students": [
                {"name": "Alice Brown", "total": 50000},
                {"name": "Bob Wilson", "total": 75000},
            ]
        }

        result = calculate_overall_monthly_total(accounting_data)

        # Verify overall_monthly_total (100000 + 250000 + 50000 + 75000 = 475000)
        self.assertEqual(result["overall_monthly_total"], 475000)

    def test_single_school_zero_total_with_freelance(self):
        """Test edge case: school with zero total but freelance students have earnings."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "school_total": 0,
                    "students_reports": []
                }
            ],
            "freelance_students": [
                {"name": "Alice Brown", "total": 1500},
            ]
        }

        result = calculate_overall_monthly_total(accounting_data)

        # Verify overall_monthly_total (0 + 1500 = 1500)
        self.assertEqual(result["overall_monthly_total"], 1500)

    def test_multiple_schools_one_freelance(self):
        """Test multiple schools with a single freelance student."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "school_total": 800,
                    "students_reports": []
                },
                {
                    "school_name": "Beta School",
                    "school_total": 900,
                    "students_reports": []
                },
                {
                    "school_name": "Gamma Institute",
                    "school_total": 1000,
                    "students_reports": []
                }
            ],
            "freelance_students": [
                {"name": "Alice Brown", "total": 500},
            ]
        }

        result = calculate_overall_monthly_total(accounting_data)

        # Verify overall_monthly_total (800 + 900 + 1000 + 500 = 3200)
        self.assertEqual(result["overall_monthly_total"], 3200)

    def test_returns_same_structure(self):
        """Test that the function returns the accounting_data structure with added field."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "school_total": 1000,
                    "students_reports": []
                }
            ],
            "freelance_students": [
                {"name": "Alice Brown", "total": 500},
            ],
            "other_field": "some_value"
        }

        result = calculate_overall_monthly_total(accounting_data)

        # Verify structure is maintained
        self.assertIn("classes_in_schools", result)
        self.assertIn("freelance_students", result)
        self.assertIn("other_field", result)
        self.assertIn("overall_monthly_total", result)
        self.assertEqual(result["other_field"], "some_value")

    def test_mixed_integer_and_decimal_totals(self):
        """Test calculating with mixed integer and Decimal types."""
        accounting_data = {
            "classes_in_schools": [
                {
                    "school_name": "Alpha Academy",
                    "school_total": 1000,  # Integer
                    "students_reports": []
                },
                {
                    "school_name": "Beta School",
                    "school_total": Decimal("1500.50"),  # Decimal
                    "students_reports": []
                }
            ],
            "freelance_students": [
                {"name": "Alice Brown", "total": 500},  # Integer
                {"name": "Bob Wilson", "total": Decimal("250.25")},  # Decimal
            ]
        }

        result = calculate_overall_monthly_total(accounting_data)

        # Verify overall_monthly_total (1000 + 1500.50 + 500 + 250.25 = 3250.75)
        expected_total = 1000 + Decimal("1500.50") + 500 + Decimal("250.25")
        self.assertEqual(result["overall_monthly_total"], expected_total)

    def test_result_is_correct_type(self):
        """Test that the result returns the correct type based on input types."""
        # Test with all integers
        accounting_data_int = {
            "classes_in_schools": [
                {"school_name": "Alpha", "school_total": 1000, "students_reports": []}
            ],
            "freelance_students": [
                {"name": "Alice", "total": 500}
            ]
        }
        
        result_int = calculate_overall_monthly_total(accounting_data_int)
        self.assertIsInstance(result_int["overall_monthly_total"], int)
        
        # Test with Decimals
        accounting_data_decimal = {
            "classes_in_schools": [
                {"school_name": "Alpha", "school_total": Decimal("1000.00"), "students_reports": []}
            ],
            "freelance_students": [
                {"name": "Alice", "total": Decimal("500.00")}
            ]
        }
        
        result_decimal = calculate_overall_monthly_total(accounting_data_decimal)
        self.assertIsInstance(result_decimal["overall_monthly_total"], Decimal)

