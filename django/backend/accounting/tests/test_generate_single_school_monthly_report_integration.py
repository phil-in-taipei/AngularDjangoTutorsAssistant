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


class TestGenerateEstimatedMonthlyEarningsReportForSingleSchool(TestCase):
    """
    Integration test suite for generate_estimated_monthly_earnings_report_for_single_school function.
    This function orchestrates the pipeline to generate a monthly accounting report for a single school.
    """

    def setUp(self):
        """
        Set up comprehensive test data including:
        - Teacher profile
        - 2 Schools (Alpha Academy and Beta School)
        - Students at each school
        - Freelance students (should be excluded)
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

        # Create another teacher for filtering tests
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

        # Create students at Alpha Academy
        self.alpha_student_1 = StudentOrClass.objects.create(
            student_or_class_name='Charlie Davis',
            account_type='school',
            school=self.school_alpha,
            teacher=self.teacher_profile,
            purchased_class_hours=None,
            tuition_per_hour=900
        )
        self.alpha_student_2 = StudentOrClass.objects.create(
            student_or_class_name='Amy Anderson',
            account_type='school',
            school=self.school_alpha,
            teacher=self.teacher_profile,
            purchased_class_hours=None,
            tuition_per_hour=900
        )

        # Create student at Beta School
        self.beta_student = StudentOrClass.objects.create(
            student_or_class_name='Diana Miller',
            account_type='school',
            school=self.school_beta,
            teacher=self.teacher_profile,
            purchased_class_hours=None,
            tuition_per_hour=950
        )

        # Create freelance student (should be excluded)
        self.freelance_student = StudentOrClass.objects.create(
            student_or_class_name='Alice Brown',
            account_type='freelance',
            school=None,
            teacher=self.teacher_profile,
            purchased_class_hours=Decimal('10.00'),
            tuition_per_hour=1000
        )

        # Create scheduled classes for Alpha Academy in November 2024
        self.nov_alpha_class_1 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.alpha_student_1,
            date=date(2024, 11, 5),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='completed'
        )
        self.nov_alpha_class_2 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.alpha_student_1,
            date=date(2024, 11, 12),
            start_time=time(14, 0),
            finish_time=time(15, 0),
            class_status='completed'
        )
        self.nov_alpha_class_3 = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.alpha_student_2,
            date=date(2024, 11, 18),
            start_time=time(13, 0),
            finish_time=time(14, 0),
            class_status='completed'
        )

        # Create scheduled class for Beta School in November 2024
        self.nov_beta_class = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.beta_student,
            date=date(2024, 11, 10),
            start_time=time(9, 0),
            finish_time=time(10, 0),
            class_status='completed'
        )

        # Create freelance class (should be excluded)
        self.nov_freelance_class = ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.freelance_student,
            date=date(2024, 11, 15),
            start_time=time(14, 0),
            finish_time=time(15, 30),
            class_status='completed'
        )

    def test_generate_report_structure(self):
        """Test that the report has the expected structure for a single school."""
        report = generate_estimated_monthly_earnings_report_for_single_school(
            teacher=self.teacher_profile,
            school=self.school_alpha,
            month=11,
            year=2024
        )

        # Verify structure
        self.assertIn('school_name', report)
        self.assertIn('students_reports', report)
        self.assertIn('school_total', report)

        # Should NOT be a list, should be a dict
        self.assertIsInstance(report, dict)

    def test_generate_report_for_alpha_academy(self):
        """Test generating report for Alpha Academy."""
        report = generate_estimated_monthly_earnings_report_for_single_school(
            teacher=self.teacher_profile,
            school=self.school_alpha,
            month=11,
            year=2024
        )

        # Verify school name
        self.assertEqual(report['school_name'], 'Alpha Academy')

        # Should have 2 students
        self.assertEqual(len(report['students_reports']), 2)

        # Verify school_total is calculated
        self.assertIn('school_total', report)
        self.assertGreater(report['school_total'], 0)

    def test_generate_report_for_beta_school(self):
        """Test generating report for Beta School."""
        report = generate_estimated_monthly_earnings_report_for_single_school(
            teacher=self.teacher_profile,
            school=self.school_beta,
            month=11,
            year=2024
        )

        # Verify school name
        self.assertEqual(report['school_name'], 'Beta School')

        # Should have 1 student
        self.assertEqual(len(report['students_reports']), 1)

        # Verify school_total is calculated
        self.assertGreater(report['school_total'], 0)

    def test_students_sorted_alphabetically(self):
        """Test that students are sorted alphabetically."""
        report = generate_estimated_monthly_earnings_report_for_single_school(
            teacher=self.teacher_profile,
            school=self.school_alpha,
            month=11,
            year=2024
        )

        student_names = [student['name'] for student in report['students_reports']]

        # Should be sorted: Amy Anderson before Charlie Davis
        self.assertEqual(student_names, sorted(student_names))
        self.assertEqual(student_names[0], 'Amy Anderson')
        self.assertEqual(student_names[1], 'Charlie Davis')

    def test_excludes_other_schools(self):
        """Test that report only includes classes from the specified school."""
        report = generate_estimated_monthly_earnings_report_for_single_school(
            teacher=self.teacher_profile,
            school=self.school_alpha,
            month=11,
            year=2024
        )

        # Should only have Alpha Academy students
        student_names = [student['name'] for student in report['students_reports']]
        self.assertIn('Amy Anderson', student_names)
        self.assertIn('Charlie Davis', student_names)
        self.assertNotIn('Diana Miller', student_names)  # Beta School student

    def test_excludes_freelance_students(self):
        """Test that freelance students are not included in the report."""
        report = generate_estimated_monthly_earnings_report_for_single_school(
            teacher=self.teacher_profile,
            school=self.school_alpha,
            month=11,
            year=2024
        )

        student_names = [student['name'] for student in report['students_reports']]
        self.assertNotIn('Alice Brown', student_names)  # Freelance student

    def test_filters_by_teacher(self):
        """Test that report only includes classes for the specified teacher."""
        # Create class for other teacher at Alpha Academy
        ScheduledClass.objects.create(
            teacher=self.other_teacher_profile,
            student_or_class=self.alpha_student_1,
            date=date(2024, 11, 8),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='completed'
        )

        report = generate_estimated_monthly_earnings_report_for_single_school(
            teacher=self.teacher_profile,
            school=self.school_alpha,
            month=11,
            year=2024
        )

        # Should only include first teacher's classes
        # This is reflected in the totals and student reports
        self.assertEqual(report['school_name'], 'Alpha Academy')
        self.assertEqual(len(report['students_reports']), 2)

    def test_school_total_is_correct(self):
        """Test that school_total is calculated correctly."""
        report = generate_estimated_monthly_earnings_report_for_single_school(
            teacher=self.teacher_profile,
            school=self.school_alpha,
            month=11,
            year=2024
        )

        # Calculate expected total manually
        calculated_total = sum(
            student['total'] for student in report['students_reports']
        )

        self.assertEqual(report['school_total'], calculated_total)

    def test_empty_month_returns_empty_report(self):
        """Test that a month with no classes returns an empty report with correct structure."""
        report = generate_estimated_monthly_earnings_report_for_single_school(
            teacher=self.teacher_profile,
            school=self.school_alpha,
            month=10,  # October - no classes
            year=2024
        )

        # Should return empty report structure
        self.assertEqual(report['school_name'], 'Alpha Academy')
        self.assertEqual(len(report['student_reports']), 0)
        self.assertEqual(report['school_total'], 0.0)

    def test_school_with_no_classes_returns_empty_report(self):
        """Test that a school with no classes returns the correct empty structure."""
        # Create a third school with no classes
        school_gamma = School.objects.create(
            school_name='Gamma Institute',
            address_line_1='789 Pine St',
            address_line_2='Floor 3',
            contact_phone='5551111111',
            scheduling_teacher=self.teacher_profile
        )

        report = generate_estimated_monthly_earnings_report_for_single_school(
            teacher=self.teacher_profile,
            school=school_gamma,
            month=11,
            year=2024
        )

        # Should return empty report with school name
        self.assertEqual(report['school_name'], 'Gamma Institute')
        self.assertEqual(report['student_reports'], [])
        self.assertEqual(report['school_total'], 0.0)

    def test_empty_report_has_float_zero(self):
        """Test that empty reports have school_total as float(0)."""
        school_gamma = School.objects.create(
            school_name='Gamma Institute',
            address_line_1='789 Pine St',
            address_line_2='Floor 3',
            contact_phone='5551111111',
            scheduling_teacher=self.teacher_profile
        )

        report = generate_estimated_monthly_earnings_report_for_single_school(
            teacher=self.teacher_profile,
            school=school_gamma,
            month=11,
            year=2024
        )

        # Verify it's specifically a float type
        self.assertIsInstance(report['school_total'], float)
        self.assertEqual(report['school_total'], 0.0)

    def test_string_month_and_year_parameters(self):
        """Test that function handles string parameters for month and year."""
        report = generate_estimated_monthly_earnings_report_for_single_school(
            teacher=self.teacher_profile,
            school=self.school_alpha,
            month="11",  # String instead of int
            year="2024"  # String instead of int
        )

        # Should work the same as with integers
        self.assertEqual(report['school_name'], 'Alpha Academy')
        self.assertGreater(len(report['students_reports']), 0)

    def test_december_edge_case(self):
        """Test generating report for December (year boundary)."""
        # Create classes in December 2024
        ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.alpha_student_1,
            date=date(2024, 12, 15),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='completed'
        )

        report = generate_estimated_monthly_earnings_report_for_single_school(
            teacher=self.teacher_profile,
            school=self.school_alpha,
            month=12,
            year=2024
        )

        # Should include December classes
        self.assertGreater(len(report['students_reports']), 0)

    def test_multiple_classes_same_student(self):
        """Test report when a student has multiple classes in the month."""
        # alpha_student_1 already has 2 classes in November
        report = generate_estimated_monthly_earnings_report_for_single_school(
            teacher=self.teacher_profile,
            school=self.school_alpha,
            month=11,
            year=2024
        )

        # Find Charlie Davis in the report
        charlie_report = next(
            (student for student in report['students_reports']
             if student['name'] == 'Charlie Davis'),
            None
        )

        self.assertIsNotNone(charlie_report)
        # Should have aggregated hours/total from both classes
        self.assertGreater(charlie_report['hours'], 1)
        self.assertGreater(charlie_report['total'], 0)

    def test_includes_various_class_statuses(self):
        """Test that report includes classes with different statuses."""
        # Add classes with different statuses
        ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.alpha_student_1,
            date=date(2024, 11, 22),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='scheduled'
        )

        ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.alpha_student_2,
            date=date(2024, 11, 25),
            start_time=time(14, 0),
            finish_time=time(15, 0),
            class_status='cancelled'
        )

        report = generate_estimated_monthly_earnings_report_for_single_school(
            teacher=self.teacher_profile,
            school=self.school_alpha,
            month=11,
            year=2024
        )

        # Report should include classes regardless of status
        self.assertEqual(len(report['students_reports']), 2)

    def test_returns_first_school_from_list(self):
        """Test that function returns the first (and only) school from the processed list."""
        report = generate_estimated_monthly_earnings_report_for_single_school(
            teacher=self.teacher_profile,
            school=self.school_alpha,
            month=11,
            year=2024
        )

        # Should be a dict, not a list
        self.assertIsInstance(report, dict)
        # Should not have a list structure
        self.assertNotIsInstance(report, list)

    def test_preserves_student_report_fields(self):
        """Test that all student report fields are preserved."""
        report = generate_estimated_monthly_earnings_report_for_single_school(
            teacher=self.teacher_profile,
            school=self.school_alpha,
            month=11,
            year=2024
        )

        # Check first student report has expected fields
        if len(report['students_reports']) > 0:
            student = report['students_reports'][0]
            self.assertIn('name', student)
            self.assertIn('hours', student)
            self.assertIn('total', student)

    @patch('accounting.utils.organize_scheduled_classes')
    def test_pipeline_calls_organize_scheduled_classes(self, mock_organize):
        """Test that the pipeline calls organize_scheduled_classes."""
        # Setup mock to return expected structure
        mock_organize.return_value = {
            'classes_in_schools': [
                {
                    'school_name': 'Alpha Academy',
                    'classes': []
                }
            ],
            'freelance_students': []
        }

        with patch('accounting.utils.generate_accounting_reports_for_classes_in_schools') as mock_generate:
            mock_generate.return_value = {
                'classes_in_schools': [
                    {
                        'school_name': 'Alpha Academy',
                        'students_reports': [],
                        'school_total': 0
                    }
                ]
            }

            report = generate_estimated_monthly_earnings_report_for_single_school(
                teacher=self.teacher_profile,
                school=self.school_alpha,
                month=11,
                year=2024
            )

        # Verify organize_scheduled_classes was called
        mock_organize.assert_called_once()

    @patch('accounting.utils.generate_accounting_reports_for_classes_in_schools')
    def test_pipeline_calls_generate_accounting_reports(self, mock_generate):
        """Test that the pipeline calls generate_accounting_reports_for_classes_in_schools."""
        # Setup mock to return expected structure
        mock_generate.return_value = {
            'classes_in_schools': [
                {
                    'school_name': 'Alpha Academy',
                    'students_reports': [],
                    'school_total': 0
                }
            ]
        }

        report = generate_estimated_monthly_earnings_report_for_single_school(
            teacher=self.teacher_profile,
            school=self.school_alpha,
            month=11,
            year=2024
        )

        # Verify function was called
        mock_generate.assert_called_once()

    def test_comprehensive_report_integration(self):
        """
        Comprehensive integration test with:
        - Multiple students at one school
        - Multiple classes per student
        - Verify entire pipeline works end-to-end
        """
        # Add more classes for comprehensive test
        ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.alpha_student_2,
            date=date(2024, 11, 8),
            start_time=time(10, 0),
            finish_time=time(11, 0),
            class_status='completed'
        )

        ScheduledClass.objects.create(
            teacher=self.teacher_profile,
            student_or_class=self.alpha_student_1,
            date=date(2024, 11, 14),
            start_time=time(14, 0),
            finish_time=time(15, 0),
            class_status='completed'
        )

        report = generate_estimated_monthly_earnings_report_for_single_school(
            teacher=self.teacher_profile,
            school=self.school_alpha,
            month=11,
            year=2024
        )

        # Verify comprehensive structure
        self.assertEqual(report['school_name'], 'Alpha Academy')
        self.assertEqual(len(report['students_reports']), 2)

        # Verify students are sorted
        student_names = [s['name'] for s in report['students_reports']]
        self.assertEqual(student_names, sorted(student_names))

        # Verify school total is positive
        self.assertGreater(report['school_total'], 0)

        # Verify each student has multiple classes aggregated
        for student in report['students_reports']:
            self.assertGreater(student['hours'], 1)
            self.assertGreater(student['total'], 0)

    def test_different_schools_produce_different_reports(self):
        """Test that reports for different schools are independent."""
        alpha_report = generate_estimated_monthly_earnings_report_for_single_school(
            teacher=self.teacher_profile,
            school=self.school_alpha,
            month=11,
            year=2024
        )

        beta_report = generate_estimated_monthly_earnings_report_for_single_school(
            teacher=self.teacher_profile,
            school=self.school_beta,
            month=11,
            year=2024
        )

        # Should have different school names
        self.assertEqual(alpha_report['school_name'], 'Alpha Academy')
        self.assertEqual(beta_report['school_name'], 'Beta School')

        # Should have different students
        self.assertNotEqual(
            len(alpha_report['students_reports']),
            len(beta_report['students_reports'])
        )

        # Should have different totals
        self.assertNotEqual(
            alpha_report['school_total'],
            beta_report['school_total']
        )

    def test_report_does_not_include_classes_in_schools_key(self):
        """Test that the returned report is a single school dict, not wrapped in classes_in_schools."""
        report = generate_estimated_monthly_earnings_report_for_single_school(
            teacher=self.teacher_profile,
            school=self.school_alpha,
            month=11,
            year=2024
        )

        # Should NOT have classes_in_schools key
        self.assertNotIn('classes_in_schools', report)

        # Should directly have school_name, students_reports, school_total
        self.assertIn('school_name', report)
        self.assertIn('students_reports', report)
        self.assertIn('school_total', report)
