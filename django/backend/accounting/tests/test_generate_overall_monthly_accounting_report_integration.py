from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date, time
from copy import deepcopy
from decimal import Decimal
from unittest.mock import patch, call, MagicMock

from user_profiles.models import UserProfile
from student_account.models import StudentOrClass
from school.models import School
from class_scheduling.models import ScheduledClass
from accounting.utils import (
    calculate_school_totals,
    calculate_overall_monthly_total,
    generate_estimated_earnings_report,
    generate_estimated_monthly_earnings_report_for_single_school,
    generate_estimated_earnings_report_for_single_school_within_date_range,
    get_scheduled_classes_at_school_during_date_range,
    get_estimated_number_of_worked_hours,
    get_scheduled_classes_during_month_period,
    get_scheduled_classes_at_school_during_month_period,
    organize_scheduled_classes, process_school_classes,
    process_freelance_students,
    generate_accounting_reports_for_classes_in_schools,
    generate_accounting_reports_for_classes_in_schools_and_freelance_teachers,
    sort_accounting_reports_by_name,
    sort_school_reports_alphabetically,
    sort_school_and_freelance_reports_alphabetically,
)


User = get_user_model()


class TestGenerateEstimatedEarningsReport(TestCase):
    """
    Integration test suite for generate_estimated_earnings_report function.
    This function orchestrates the entire pipeline to generate a monthly accounting report.
    """

    def setUp(self):
        """
        Set up comprehensive test data including:
        - Teacher profile
        - 2 Schools (Alpha Academy and Beta School)
        - 2 Freelance students
        - School-affiliated students
        - Scheduled classes for November 2024
        """
        # Create teacher user and profile
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

        # Create school-affiliated students
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
            student_or_class=self.freelance_student_2,
            date=date(2024, 11, 15),
            start_time=time(14, 0),
            finish_time=time(15, 30),
            class_status='completed'
        )

        # School classes
        self.nov_school_alpha_class = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.school_alpha_student,
            date=date(2024, 11, 12),
            start_time=time(13, 0),
            finish_time=time(14, 0),
            class_status='completed'
        )
        self.nov_school_beta_class = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.school_beta_student,
            date=date(2024, 11, 18),
            start_time=time(9, 0),
            finish_time=time(10, 30),
            class_status='completed'
        )

    def test_generate_complete_report_structure(self):
        """Test that the complete report has the expected structure."""
        report = generate_estimated_earnings_report(
            teacher=self.teacher_profile,
            month=11,
            year=2024
        )

        # Verify top-level structure
        self.assertIn('classes_in_schools', report)
        self.assertIn('freelance_students', report)
        self.assertIn('overall_monthly_total', report)

        # Verify classes_in_schools is a list
        self.assertIsInstance(report['classes_in_schools'], list)

        # Verify freelance_students is a list
        self.assertIsInstance(report['freelance_students'], list)

        # Verify overall_monthly_total exists
        self.assertIsNotNone(report['overall_monthly_total'])

    def test_generate_report_includes_all_schools(self):
        """Test that report includes all schools with classes."""
        report = generate_estimated_earnings_report(
            teacher=self.teacher_profile,
            month=11,
            year=2024
        )

        # Should have 2 schools in the report
        self.assertEqual(len(report['classes_in_schools']), 2)

        school_names = [school['school_name'] for school in report['classes_in_schools']]
        self.assertIn('Alpha Academy', school_names)
        self.assertIn('Beta School', school_names)

    def test_generate_report_includes_freelance_students(self):
        """Test that report includes all freelance students with classes."""
        report = generate_estimated_earnings_report(
            teacher=self.teacher_profile,
            month=11,
            year=2024
        )

        # Should have 2 freelance students in the report
        self.assertEqual(len(report['freelance_students']), 2)

        freelance_names = [student['name'] for student in report['freelance_students']]
        self.assertIn('Alice Brown', freelance_names)
        self.assertIn('Bob Wilson', freelance_names)

    def test_generate_report_schools_have_totals(self):
        """Test that each school has a school_total field calculated."""
        report = generate_estimated_earnings_report(
            teacher=self.teacher_profile,
            month=11,
            year=2024
        )

        # Each school should have a school_total field
        for school in report['classes_in_schools']:
            self.assertIn('school_total', school)
            self.assertIsNotNone(school['school_total'])

    def test_generate_report_students_sorted_alphabetically(self):
        """Test that students within schools are sorted alphabetically."""
        # Add another student to Alpha Academy to test sorting
        another_alpha_student = StudentOrClass.objects.create(
            student_or_class_name='Amy Anderson',
            account_type='school',
            school=self.school_alpha,
            teacher=self.teacher_profile,
            purchased_class_hours=None,
            tuition_per_hour=900
        )

        ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=another_alpha_student,
            date=date(2024, 11, 10),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='completed'
        )

        report = generate_estimated_earnings_report(
            teacher=self.teacher_profile,
            month=11,
            year=2024
        )

        # Find Alpha Academy in the report
        alpha_school = next(
            (school for school in report['classes_in_schools']
             if school['school_name'] == 'Alpha Academy'),
            None
        )

        self.assertIsNotNone(alpha_school)
        students = alpha_school['students_reports']

        # Students should be sorted: Amy Anderson before Charlie Davis
        if len(students) > 1:
            self.assertEqual(students[0]['name'], 'Amy Anderson')
            self.assertEqual(students[1]['name'], 'Charlie Davis')

    def test_generate_report_freelance_sorted_alphabetically(self):
        """Test that freelance students are sorted alphabetically."""
        report = generate_estimated_earnings_report(
            teacher=self.teacher_profile,
            month=11,
            year=2024
        )

        freelance_names = [student['name'] for student in report['freelance_students']]

        # Should be sorted: Alice Brown before Bob Wilson
        self.assertEqual(freelance_names, sorted(freelance_names))

    def test_generate_report_overall_total_is_correct(self):
        """Test that overall_monthly_total is calculated correctly."""
        report = generate_estimated_earnings_report(
            teacher=self.teacher_profile,
            month=11,
            year=2024
        )

        # Calculate expected total manually
        school_totals_sum = sum(
            school['school_total'] for school in report['classes_in_schools']
        )
        freelance_totals_sum = sum(
            student['total'] for student in report['freelance_students']
        )
        expected_total = school_totals_sum + freelance_totals_sum

        self.assertEqual(report['overall_monthly_total'], expected_total)

    def test_generate_report_for_different_month(self):
        """Test generating report for a different month with no classes."""
        report = generate_estimated_earnings_report(
            teacher=self.teacher_profile,
            month=10,  # October - no classes
            year=2024
        )

        # Should have empty lists
        self.assertEqual(len(report['classes_in_schools']), 0)
        self.assertEqual(len(report['freelance_students']), 0)
        self.assertEqual(report['overall_monthly_total'], 0)

    def test_generate_report_with_string_month_year(self):
        """Test that function handles string parameters for month and year."""
        report = generate_estimated_earnings_report(
            teacher=self.teacher_profile,
            month="11",
            year="2024"
        )

        # Should work the same as with integers
        self.assertGreater(len(report['classes_in_schools']), 0)
        self.assertGreater(len(report['freelance_students']), 0)

    def test_generate_report_multiple_classes_same_student(self):
        """Test report when a student has multiple classes in the month."""
        # Add another class for Alice Brown
        ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.freelance_student_1,
            date=date(2024, 11, 20),
            start_time=time(14, 0),
            finish_time=time(15, 0),
            class_status='completed'
        )

        report = generate_estimated_earnings_report(
            teacher=self.teacher_profile,
            month=11,
            year=2024
        )

        # Find Alice Brown in freelance students
        alice_report = next(
            (student for student in report['freelance_students']
             if student['name'] == 'Alice Brown'),
            None
        )

        self.assertIsNotNone(alice_report)
        # Total should reflect both classes
        self.assertGreater(alice_report['total'], 0)

    def test_generate_report_filters_by_teacher(self):
        """Test that report only includes classes for the specified teacher."""
        # Create another teacher with classes
        other_teacher_user = User.objects.create_user(
            username='teacher2',
            password='testpass123'
        )
        other_teacher_profile = UserProfile.objects.create(
            user=other_teacher_user,
            contact_email='teacher2@example.com',
            surname='Jones',
            given_name='Mary'
        )

        # Create class for other teacher
        ScheduledClass.objects.create(
            teacher=other_teacher_profile,
            student_or_class=self.freelance_student_1,
            date=date(2024, 11, 25),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='completed'
        )

        # Generate report for first teacher
        report = generate_estimated_earnings_report(
            teacher=self.teacher_profile,
            month=11,
            year=2024
        )

        # Should only include first teacher's classes (2 freelance)
        # Not the class taught by other_teacher
        self.assertEqual(len(report['freelance_students']), 2)

    def test_generate_report_december_edge_case(self):
        """Test generating report for December (year boundary)."""
        # Create classes in December 2024
        ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.freelance_student_1,
            date=date(2024, 12, 15),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='completed'
        )

        report = generate_estimated_earnings_report(
            teacher=self.teacher_profile,
            month=12,
            year=2024
        )

        # Should include December classes
        self.assertGreater(len(report['freelance_students']), 0)

    def test_generate_report_includes_various_class_statuses(self):
        """Test that report includes classes with different statuses."""
        # Add classes with different statuses
        ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.freelance_student_1,
            date=date(2024, 11, 22),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='scheduled'
        )

        ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.freelance_student_2,
            date=date(2024, 11, 25),
            start_time=time(14, 0),
            finish_time=time(15, 0),
            class_status='cancelled'
        )

        report = generate_estimated_earnings_report(
            teacher=self.teacher_profile,
            month=11,
            year=2024
        )

        # Report should include classes regardless of status
        self.assertEqual(len(report['freelance_students']), 2)

    def test_generate_report_with_only_schools(self):
        """Test generating report when there are only school classes, no freelance."""
        # Delete freelance classes
        ScheduledClass.objects.filter(
            student_or_class__school__isnull=True
        ).delete()

        report = generate_estimated_earnings_report(
            teacher=self.teacher_profile,
            month=11,
            year=2024
        )

        # Should have schools but no freelance
        self.assertGreater(len(report['classes_in_schools']), 0)
        self.assertEqual(len(report['freelance_students']), 0)

        # Overall total should equal school totals only
        school_totals_sum = sum(
            school['school_total'] for school in report['classes_in_schools']
        )
        self.assertEqual(report['overall_monthly_total'], school_totals_sum)

    def test_generate_report_with_only_freelance(self):
        """Test generating report when there are only freelance classes, no schools."""
        # Delete school classes
        ScheduledClass.objects.filter(
            student_or_class__school__isnull=False
        ).delete()

        report = generate_estimated_earnings_report(
            teacher=self.teacher_profile,
            month=11,
            year=2024
        )

        # Should have freelance but no schools
        self.assertEqual(len(report['classes_in_schools']), 0)
        self.assertGreater(len(report['freelance_students']), 0)

        # Overall total should equal freelance totals only
        freelance_totals_sum = sum(
            student['total'] for student in report['freelance_students']
        )
        self.assertEqual(report['overall_monthly_total'], freelance_totals_sum)

    @patch('accounting.utils.organize_scheduled_classes')
    def test_pipeline_calls_organize_scheduled_classes(self, mock_organize):
        """Test that the pipeline calls organize_scheduled_classes."""
        # Setup mock to return expected structure
        mock_organize.return_value = {
            'classes_in_schools': [],
            'freelance_students': []
        }

        with patch(
                'accounting.utils.generate_accounting_reports_for_classes_in_schools_and_freelance_teachers') as mock_generate:
            mock_generate.return_value = {
                'classes_in_schools': [],
                'freelance_students': []
            }

            report = generate_estimated_earnings_report(
                teacher=self.teacher_profile,
                month=11,
                year=2024
            )

        # Verify organize_scheduled_classes was called
        mock_organize.assert_called_once()

    @patch('accounting.utils.generate_accounting_reports_for_classes_in_schools_and_freelance_teachers')
    def test_pipeline_calls_generate_accounting_reports(self, mock_generate):
        """Test that the pipeline calls generate_accounting_reports_for_classes_in_schools_and_freelance_teachers."""
        # Setup mock to return expected structure
        mock_generate.return_value = {
            'classes_in_schools': [],
            'freelance_students': []
        }

        report = generate_estimated_earnings_report(
            teacher=self.teacher_profile,
            month=11,
            year=2024
        )

        # Verify function was called
        mock_generate.assert_called_once()

    def test_comprehensive_report_integration(self):
        """
        Comprehensive integration test with:
        - Multiple schools
        - Multiple students per school
        - Multiple freelance students
        - Multiple classes per student
        - Verify entire pipeline works end-to-end
        """
        # Add more students and classes for comprehensive test
        alpha_student_2 = StudentOrClass.objects.create(
            student_or_class_name='Emily Evans',
            account_type='school',
            school=self.school_alpha,
            teacher=self.teacher_profile,
            purchased_class_hours=None,
            tuition_per_hour=900
        )

        # Add more classes
        ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=alpha_student_2,
            date=date(2024, 11, 8),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='completed'
        )

        ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.school_alpha_student,
            date=date(2024, 11, 14),
            start_time=time(14, 0),
            finish_time=time(15, 0),
            class_status='completed'
        )

        report = generate_estimated_earnings_report(
            teacher=self.teacher_profile,
            month=11,
            year=2024
        )

        # Verify comprehensive structure
        self.assertEqual(len(report['classes_in_schools']), 2)
        self.assertEqual(len(report['freelance_students']), 2)

        # Verify Alpha Academy has 2 students
        alpha_school = next(
            (school for school in report['classes_in_schools']
             if school['school_name'] == 'Alpha Academy'),
            None
        )
        self.assertEqual(len(alpha_school['students_reports']), 2)

        # Verify students are sorted
        student_names = [s['name'] for s in alpha_school['students_reports']]
        self.assertEqual(student_names, sorted(student_names))

        # Verify overall total is positive
        self.assertGreater(report['overall_monthly_total'], 0)

        # Verify school totals are calculated
        self.assertIn('school_total', alpha_school)
        self.assertGreater(alpha_school['school_total'], 0)

