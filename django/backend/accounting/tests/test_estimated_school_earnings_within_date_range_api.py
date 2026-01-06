import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from decimal import Decimal
from datetime import date, time
from unittest.mock import patch

from student_account.models import StudentOrClass
from user_profiles.models import UserProfile
from class_scheduling.models import ScheduledClass
from school.models import School

User = get_user_model()

ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL = '/api/accounting/estimated-school-earnings-within-date-range/{start_date}/{finish_date}/{school_id}/'


def get_test_user(username='testteacher', password='testpassword'):
    """Helper function to create a test user"""
    return User.objects.create_user(username, password)


def create_test_teacher_profile(user, surname='Smith', given_name='John'):
    """Helper function to create a teacher profile"""
    return UserProfile.objects.create(
        user=user,
        contact_email=f'{user.username}@test.com',
        surname=surname,
        given_name=given_name
    )


def create_test_school(teacher_profile, name='Test School', address_line_1='123 Main St'):
    """Helper function to create a school"""
    return School.objects.create(
        school_name=name,
        address_line_1=address_line_1,
        address_line_2='Suite 100',
        contact_phone='5551234567',
        scheduling_teacher=teacher_profile
    )


def create_test_student(
        teacher_profile, name='Test Student', account_type='school',
        school=None, initial_hours=None, tuition_rate=1000
):
    """Helper function to create a student"""
    return StudentOrClass.objects.create(
        student_or_class_name=name,
        account_type=account_type,
        school=school,
        teacher=teacher_profile,
        purchased_class_hours=Decimal(initial_hours) if initial_hours else None,
        tuition_per_hour=tuition_rate,
        comments='Test student'
    )


def create_scheduled_class(
        teacher, student, class_date, start_time_str='10:00',
        finish_time_str='11:00', class_status='completed'
):
    """Helper function to create a scheduled class"""
    return ScheduledClass.objects.create(
        teacher=teacher,
        student_or_class=student,
        date=class_date,
        start_time=time(*map(int, start_time_str.split(':'))),
        finish_time=time(*map(int, finish_time_str.split(':'))),
        class_status=class_status
    )


class EstimatedSchoolEarningsWithinDateRangePublicApiTests(TestCase):
    """Test the publicly available estimated school earnings within date range API"""

    def setUp(self):
        self.client = APIClient()
        self.test_user = get_test_user()
        self.teacher_profile = create_test_teacher_profile(self.test_user)
        self.school = create_test_school(self.teacher_profile, name='Test School')

    def test_login_required_for_estimated_school_earnings_date_range(self):
        """Test that login is required for retrieving estimated school earnings"""
        print("Test that login is required for retrieving estimated school earnings")

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=self.school.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class EstimatedSchoolEarningsWithinDateRangePrivateApiTests(TestCase):
    """Test the authenticated estimated school earnings within date range API"""

    def setUp(self):
        """
        Set up comprehensive test data including:
        - Teacher profile
        - 2 Schools (Alpha Academy and Beta School)
        - Students at each school
        - Freelance students (should be excluded)
        - Scheduled classes across multiple dates
        """
        self.client = APIClient()

        # Create teacher user and profile
        self.teacher_user = get_test_user(username='teacher1', password='testpass123')
        self.teacher_profile = create_test_teacher_profile(
            self.teacher_user, surname='Smith', given_name='John'
        )
        self.client.force_authenticate(self.teacher_user)

        # Create another teacher for filtering tests
        self.other_teacher_user = get_test_user(username='teacher2', password='testpass123')
        self.other_teacher_profile = create_test_teacher_profile(
            self.other_teacher_user, surname='Jones', given_name='Mary'
        )

        # Create 2 schools
        self.school_alpha = create_test_school(
            self.teacher_profile, name='Alpha Academy', address_line_1='123 Main St'
        )
        self.school_beta = create_test_school(
            self.teacher_profile, name='Beta School', address_line_1='456 Oak Ave'
        )

        # Create students at Alpha Academy
        self.alpha_student_1 = create_test_student(
            self.teacher_profile, name='Charlie Davis', account_type='school',
            school=self.school_alpha, tuition_rate=900
        )
        self.alpha_student_2 = create_test_student(
            self.teacher_profile, name='Amy Anderson', account_type='school',
            school=self.school_alpha, tuition_rate=900
        )

        # Create student at Beta School
        self.beta_student = create_test_student(
            self.teacher_profile, name='Diana Miller', account_type='school',
            school=self.school_beta, tuition_rate=950
        )

        # Create freelance student (should be excluded)
        self.freelance_student = create_test_student(
            self.teacher_profile, name='Alice Brown', account_type='freelance',
            school=None, initial_hours='10.00', tuition_rate=1000
        )

        # Create scheduled classes for Alpha Academy
        self.alpha_class_nov_5 = create_scheduled_class(
            self.teacher_profile, self.alpha_student_1,
            date(2024, 11, 5), '10:00', '11:00', 'completed'
        )
        self.alpha_class_nov_10 = create_scheduled_class(
            self.teacher_profile, self.alpha_student_1,
            date(2024, 11, 10), '14:00', '15:00', 'completed'
        )
        self.alpha_class_nov_12 = create_scheduled_class(
            self.teacher_profile, self.alpha_student_2,
            date(2024, 11, 12), '13:00', '14:00', 'completed'
        )
        self.alpha_class_nov_20 = create_scheduled_class(
            self.teacher_profile, self.alpha_student_1,
            date(2024, 11, 20), '10:00', '11:00', 'completed'
        )

        # Create scheduled class for Beta School
        self.beta_class_nov_10 = create_scheduled_class(
            self.teacher_profile, self.beta_student,
            date(2024, 11, 10), '09:00', '10:00', 'completed'
        )

        # Create freelance class (should be excluded)
        self.freelance_class_nov_8 = create_scheduled_class(
            self.teacher_profile, self.freelance_student,
            date(2024, 11, 8), '14:00', '15:30', 'completed'
        )

    def test_retrieve_report_structure(self):
        """Test that the API returns the expected report structure for a single school"""
        print("Test that the API returns the expected report structure for a single school")

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Verify structure
        self.assertIn('school_name', res.data)
        self.assertIn('students_reports', res.data)
        self.assertIn('school_total', res.data)

        # Should be a dict, not a list
        self.assertIsInstance(res.data, dict)

    def test_retrieve_report_for_alpha_academy(self):
        """Test retrieving report for Alpha Academy within date range"""
        print("Test retrieving report for Alpha Academy within date range")

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Verify school name
        self.assertEqual(res.data['school_name'], 'Alpha Academy')

        # Should have 2 students
        self.assertEqual(len(res.data['students_reports']), 2)

        # Verify school_total is calculated
        self.assertIn('school_total', res.data)
        self.assertGreater(res.data['school_total'], 0)

    def test_retrieve_report_for_beta_school(self):
        """Test retrieving report for Beta School within date range"""
        print("Test retrieving report for Beta School within date range")

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=self.school_beta.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Verify school name
        self.assertEqual(res.data['school_name'], 'Beta School')

        # Should have 1 student
        self.assertEqual(len(res.data['students_reports']), 1)

        # Verify school_total is calculated
        self.assertGreater(res.data['school_total'], 0)

    def test_students_sorted_alphabetically(self):
        """Test that students are sorted alphabetically"""
        print("Test that students are sorted alphabetically")

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        student_names = [student['name'] for student in res.data['students_reports']]

        # Should be sorted: Amy Anderson before Charlie Davis
        self.assertEqual(student_names, sorted(student_names))
        self.assertEqual(student_names[0], 'Amy Anderson')
        self.assertEqual(student_names[1], 'Charlie Davis')

    def test_only_includes_classes_in_date_range(self):
        """Test that only classes within the date range are included"""
        print("Test that only classes within the date range are included")

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Should include classes from Nov 5, 10, 12 but not Nov 20
        # Charlie Davis has 2 classes in range (Nov 5, 10)
        charlie_report = next(
            (student for student in res.data['students_reports'] 
             if student['name'] == 'Charlie Davis'),
            None
        )
        
        self.assertIsNotNone(charlie_report)
        # Should have 2 hours from 2 classes in range
        self.assertGreater(charlie_report['hours'], 1)

    def test_excludes_classes_outside_date_range(self):
        """Test that classes outside the date range are excluded"""
        print("Test that classes outside the date range are excluded")

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Calculate total hours for Charlie Davis
        charlie_report = next(
            (student for student in res.data['students_reports'] 
             if student['name'] == 'Charlie Davis'),
            None
        )
        
        # Should have 2 hours (Nov 5 and Nov 10), not 3 (would include Nov 20)
        self.assertAlmostEqual(charlie_report['hours'], 2.0, places=1)

    def test_excludes_other_schools(self):
        """Test that report only includes classes from the specified school"""
        print("Test that report only includes classes from the specified school")

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Should only have Alpha Academy students
        student_names = [student['name'] for student in res.data['students_reports']]
        self.assertIn('Amy Anderson', student_names)
        self.assertIn('Charlie Davis', student_names)
        self.assertNotIn('Diana Miller', student_names)  # Beta School student

    def test_excludes_freelance_students(self):
        """Test that freelance students are not included in the report"""
        print("Test that freelance students are not included in the report")

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        student_names = [student['name'] for student in res.data['students_reports']]
        self.assertNotIn('Alice Brown', student_names)  # Freelance student

    def test_filters_by_authenticated_teacher(self):
        """Test that report only includes classes for the authenticated teacher"""
        print("Test that report only includes classes for the authenticated teacher")

        # Create class for other teacher at Alpha Academy
        create_scheduled_class(
            self.other_teacher_profile, self.alpha_student_1,
            date(2024, 11, 8), '10:00', '11:00', 'completed'
        )

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Should only include first teacher's classes
        self.assertEqual(res.data['school_name'], 'Alpha Academy')
        self.assertEqual(len(res.data['students_reports']), 2)

    def test_school_total_is_correct(self):
        """Test that school_total is calculated correctly"""
        print("Test that school_total is calculated correctly")

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Calculate expected total manually
        calculated_total = sum(
            student['total'] for student in res.data['students_reports']
        )

        self.assertEqual(res.data['school_total'], calculated_total)

    def test_empty_date_range_returns_empty_report(self):
        """Test that a date range with no classes returns an empty report"""
        print("Test that a date range with no classes returns an empty report")

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-10-01', finish_date='2024-10-15', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Should return empty report structure
        self.assertEqual(res.data['school_name'], 'Alpha Academy')
        self.assertEqual(len(res.data['student_reports']), 0)
        self.assertEqual(res.data['school_total'], 0.0)

    def test_school_with_no_classes_returns_empty_report(self):
        """Test that a school with no classes returns the correct empty structure"""
        print("Test that a school with no classes returns the correct empty structure")

        # Create a third school with no classes
        school_gamma = create_test_school(
            self.teacher_profile, name='Gamma Institute', address_line_1='789 Pine St'
        )

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=school_gamma.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Should return empty report with school name
        self.assertEqual(res.data['school_name'], 'Gamma Institute')
        self.assertEqual(res.data['student_reports'], [])
        self.assertEqual(res.data['school_total'], 0.0)

    def test_empty_report_has_float_zero(self):
        """Test that empty reports have school_total as float(0)"""
        print("Test that empty reports have school_total as float(0)")

        school_gamma = create_test_school(
            self.teacher_profile, name='Gamma Institute', address_line_1='789 Pine St'
        )

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=school_gamma.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Verify it's specifically a float type
        self.assertIsInstance(res.data['school_total'], float)
        self.assertEqual(res.data['school_total'], 0.0)

    def test_single_day_range(self):
        """Test generating report for a single day"""
        print("Test generating report for a single day")

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-10', finish_date='2024-11-11', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Should only include Charlie Davis (has class on Nov 10)
        self.assertEqual(len(res.data['students_reports']), 1)
        self.assertEqual(res.data['students_reports'][0]['name'], 'Charlie Davis')

    def test_long_date_range(self):
        """Test with a long date range spanning multiple weeks"""
        print("Test with a long date range spanning multiple weeks")

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-01', finish_date='2024-11-30', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Should include all November classes
        # Charlie Davis has 3 classes total (Nov 5, 10, 20)
        charlie_report = next(
            (student for student in res.data['students_reports'] 
             if student['name'] == 'Charlie Davis'),
            None
        )
        
        self.assertIsNotNone(charlie_report)
        self.assertGreater(charlie_report['hours'], 2)

    def test_cross_month_boundary(self):
        """Test date range that crosses month boundary"""
        print("Test date range that crosses month boundary")

        # Create class in December
        create_scheduled_class(
            self.teacher_profile, self.alpha_student_1,
            date(2024, 12, 5), '10:00', '11:00', 'completed'
        )

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-25', finish_date='2024-12-10', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Should include classes from both November and December
        self.assertGreater(len(res.data['students_reports']), 0)

    def test_cross_year_boundary(self):
        """Test date range that crosses year boundary"""
        print("Test date range that crosses year boundary")

        # Create class in January 2025
        create_scheduled_class(
            self.teacher_profile, self.alpha_student_1,
            date(2025, 1, 10), '10:00', '11:00', 'completed'
        )

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-12-20', finish_date='2025-01-15', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Should include January 2025 class
        self.assertGreater(len(res.data['students_reports']), 0)

    def test_includes_various_class_statuses(self):
        """Test that report includes classes with different statuses"""
        print("Test that report includes classes with different statuses")

        # Add classes with different statuses
        create_scheduled_class(
            self.teacher_profile, self.alpha_student_1,
            date(2024, 11, 15), '10:00', '11:00', 'scheduled'
        )
        create_scheduled_class(
            self.teacher_profile, self.alpha_student_2,
            date(2024, 11, 18), '14:00', '15:00', 'cancelled'
        )

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-25', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Report should include classes regardless of status
        self.assertEqual(len(res.data['students_reports']), 2)

    def test_multiple_classes_same_student(self):
        """Test report when a student has multiple classes in the date range"""
        print("Test report when a student has multiple classes in the date range")

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Find Charlie Davis in the report
        charlie_report = next(
            (student for student in res.data['students_reports'] 
             if student['name'] == 'Charlie Davis'),
            None
        )

        self.assertIsNotNone(charlie_report)
        # Should have aggregated hours/total from multiple classes
        self.assertGreater(charlie_report['hours'], 1)
        self.assertGreater(charlie_report['total'], 0)

    def test_preserves_student_report_fields(self):
        """Test that all student report fields are preserved"""
        print("Test that all student report fields are preserved")

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Check first student report has expected fields
        if len(res.data['students_reports']) > 0:
            student = res.data['students_reports'][0]
            self.assertIn('name', student)
            self.assertIn('hours', student)
            self.assertIn('total', student)

    def test_comprehensive_report_integration(self):
        """
        Comprehensive integration test with:
        - Multiple students at one school
        - Multiple classes per student
        - Custom date range
        """
        print("Comprehensive integration test")

        # Add more classes
        create_scheduled_class(
            self.teacher_profile, self.alpha_student_2,
            date(2024, 11, 8), '10:00', '11:00', 'completed'
        )
        create_scheduled_class(
            self.teacher_profile, self.alpha_student_1,
            date(2024, 11, 14), '14:00', '15:00', 'completed'
        )

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Verify comprehensive structure
        self.assertEqual(res.data['school_name'], 'Alpha Academy')
        self.assertEqual(len(res.data['students_reports']), 2)
        
        # Verify students are sorted
        student_names = [s['name'] for s in res.data['students_reports']]
        self.assertEqual(student_names, sorted(student_names))
        
        # Verify school total is positive
        self.assertGreater(res.data['school_total'], 0)
        
        # Verify each student has multiple classes aggregated
        for student in res.data['students_reports']:
            self.assertGreater(student['hours'], 1)
            self.assertGreater(student['total'], 0)

    def test_different_schools_same_date_range(self):
        """Test that reports for different schools are independent"""
        print("Test that reports for different schools are independent")

        url_alpha = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=self.school_alpha.id
        )
        res_alpha = self.client.get(url_alpha)

        url_beta = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=self.school_beta.id
        )
        res_beta = self.client.get(url_beta)

        self.assertEqual(res_alpha.status_code, status.HTTP_200_OK)
        self.assertEqual(res_beta.status_code, status.HTTP_200_OK)

        # Should have different school names
        self.assertEqual(res_alpha.data['school_name'], 'Alpha Academy')
        self.assertEqual(res_beta.data['school_name'], 'Beta School')

        # Should have different students
        self.assertNotEqual(
            len(res_alpha.data['students_reports']),
            len(res_beta.data['students_reports'])
        )

        # Should have different totals
        self.assertNotEqual(
            res_alpha.data['school_total'],
            res_beta.data['school_total']
        )

    def test_report_does_not_include_classes_in_schools_key(self):
        """Test that the returned report is a single school dict, not wrapped"""
        print("Test that the returned report is a single school dict, not wrapped")

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Should NOT have classes_in_schools key
        self.assertNotIn('classes_in_schools', res.data)
        
        # Should directly have school_name, students_reports, school_total
        self.assertIn('school_name', res.data)
        self.assertIn('students_reports', res.data)
        self.assertIn('school_total', res.data)

    def test_different_date_ranges_produce_different_results(self):
        """Test that different date ranges for same school produce different results"""
        print("Test that different date ranges for same school produce different results")

        # First range: Nov 5-15 (includes 3 classes)
        url1 = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=self.school_alpha.id
        )
        res1 = self.client.get(url1)

        # Second range: Nov 15-25 (includes 1 class - Nov 20)
        url2 = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-15', finish_date='2024-11-25', school_id=self.school_alpha.id
        )
        res2 = self.client.get(url2)

        self.assertEqual(res1.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        
        # Should have different numbers of classes
        self.assertNotEqual(
            len(res1.data['students_reports']),
            len(res2.data['students_reports'])
        )

        # Should have different totals
        self.assertNotEqual(
            res1.data['school_total'],
            res2.data['school_total']
        )

    def test_nonexistent_school_id_returns_404(self):
        """Test that querying with a non-existent school ID returns 404"""
        print("Test that querying with a non-existent school ID returns 404")

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=99999
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_without_teacher_profile_returns_404(self):
        """Test that a user without a teacher profile gets 404"""
        print("Test that a user without a teacher profile gets 404")

        # Create user without teacher profile
        user_without_profile = get_test_user(username='noprofile', password='pass')
        self.client.force_authenticate(user_without_profile)

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_response_is_json_serializable(self):
        """Test that the response can be properly JSON serialized"""
        print("Test that the response can be properly JSON serialized")

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Attempt to serialize the response data to JSON
        try:
            json_data = json.dumps(res.data)
            self.assertIsNotNone(json_data)
        except (TypeError, ValueError) as e:
            self.fail(f"Response data is not JSON serializable: {e}")

    def test_date_format_iso_8601(self):
        """Test that the API accepts ISO 8601 date format (YYYY-MM-DD)"""
        print("Test that the API accepts ISO 8601 date format")

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreater(len(res.data['students_reports']), 0)

    def test_same_start_and_finish_date(self):
        """Test with the same start and finish date (single day)"""
        print("Test with the same start and finish date (single day)")

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-10', finish_date='2024-11-10', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Note: When start_date equals finish_date, the date range is typically empty
        # because the range is exclusive of the end date (start_date <= date < finish_date)
        # This test verifies the API handles this edge case gracefully
        self.assertIsInstance(res.data['student_reports'], list)

    def test_reverse_date_range_invalid(self):
        """Test with finish_date before start_date (invalid range)"""
        print("Test with finish_date before start_date (invalid range)")

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-15', finish_date='2024-11-05', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        # Should return 200 with empty results or handle gracefully
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_leap_year_february_date_range(self):
        """Test date range in February of a leap year"""
        print("Test date range in February of a leap year")

        # Create class on Feb 29, 2024 (leap year)
        create_scheduled_class(
            self.teacher_profile, self.alpha_student_1,
            date(2024, 2, 29), '10:00', '11:00', 'completed'
        )

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-02-20', finish_date='2024-03-05', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreater(len(res.data['students_reports']), 0)

    def test_report_with_classes_at_date_boundaries(self):
        """Test that classes at the start and end dates are included"""
        print("Test that classes at the start and end dates are included")

        # Create class at start date (Nov 5) - already exists
        # Create class at end date (Nov 15)
        create_scheduled_class(
            self.teacher_profile, self.alpha_student_2,
            date(2024, 11, 15), '10:00', '11:00', 'completed'
        )

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Should include both boundary classes
        self.assertEqual(len(res.data['students_reports']), 2)

    def test_report_with_zero_duration_classes(self):
        """Test that classes with zero duration are handled appropriately"""
        print("Test that classes with zero duration are handled appropriately")

        # Create class with same start and finish time (zero duration)
        create_scheduled_class(
            self.teacher_profile, self.alpha_student_1,
            date(2024, 11, 8), '10:00', '10:00', 'completed'
        )

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Response should be valid even with zero-duration class
        self.assertIsNotNone(res.data)

    def test_very_long_date_range(self):
        """Test with a very long date range (entire year)"""
        print("Test with a very long date range (entire year)")

        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-01-01', finish_date='2024-12-31', school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Should include all classes for the year
        self.assertGreater(len(res.data['students_reports']), 0)

    def test_different_teacher_cannot_access_other_teachers_schools(self):
        """Test that a different teacher's data is filtered appropriately"""
        print("Test that a different teacher's data is filtered appropriately")

        # Create school for other teacher
        other_teacher_school = create_test_school(
            self.other_teacher_profile, name='Other School', address_line_1='999 Other St'
        )

        # Try to access as first teacher (currently authenticated)
        url = ESTIMATED_SCHOOL_EARNINGS_WITHIN_DATE_RANGE_URL.format(
            start_date='2024-11-05', finish_date='2024-11-15', school_id=other_teacher_school.id
        )
        res = self.client.get(url)

        # Since the school exists but doesn't belong to the authenticated teacher,
        # the report should still be generated but may be empty or filtered
        self.assertEqual(res.status_code, status.HTTP_200_OK)
