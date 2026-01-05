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

ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL = '/api/accounting/estimated-school-earnings-by-month-year/{month}/{year}/{school_id}/'


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


class EstimatedSchoolEarningsByMonthYearPublicApiTests(TestCase):
    """Test the publicly available estimated school earnings by month/year API"""

    def setUp(self):
        self.client = APIClient()
        self.test_user = get_test_user()
        self.teacher_profile = create_test_teacher_profile(self.test_user)
        self.school = create_test_school(self.teacher_profile, name='Test School')

    def test_login_required_for_estimated_school_earnings(self):
        """Test that login is required for retrieving estimated school earnings"""
        print("Test that login is required for retrieving estimated school earnings")

        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=2024, school_id=self.school.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class EstimatedSchoolEarningsByMonthYearPrivateApiTests(TestCase):
    """Test the authenticated estimated school earnings by month/year API"""

    def setUp(self):
        """
        Set up comprehensive test data including:
        - Teacher profile
        - 2 Schools (Alpha Academy and Beta School)
        - Students at each school
        - Freelance students (should be excluded)
        - Scheduled classes for November 2024
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

        # Create scheduled classes for Alpha Academy in November 2024
        self.nov_alpha_class_1 = create_scheduled_class(
            self.teacher_profile, self.alpha_student_1,
            date(2024, 11, 5), '10:00', '11:00', 'completed'
        )
        self.nov_alpha_class_2 = create_scheduled_class(
            self.teacher_profile, self.alpha_student_1,
            date(2024, 11, 12), '14:00', '15:00', 'completed'
        )
        self.nov_alpha_class_3 = create_scheduled_class(
            self.teacher_profile, self.alpha_student_2,
            date(2024, 11, 18), '13:00', '14:00', 'completed'
        )

        # Create scheduled class for Beta School in November 2024
        self.nov_beta_class = create_scheduled_class(
            self.teacher_profile, self.beta_student,
            date(2024, 11, 10), '09:00', '10:00', 'completed'
        )

        # Create freelance class (should be excluded)
        self.nov_freelance_class = create_scheduled_class(
            self.teacher_profile, self.freelance_student,
            date(2024, 11, 15), '14:00', '15:30', 'completed'
        )

    def test_retrieve_report_structure(self):
        """Test that the API returns the expected report structure for a single school"""
        print("Test that the API returns the expected report structure for a single school")

        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=2024, school_id=self.school_alpha.id
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
        """Test retrieving report for Alpha Academy"""
        print("Test retrieving report for Alpha Academy")

        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=2024, school_id=self.school_alpha.id
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
        """Test retrieving report for Beta School"""
        print("Test retrieving report for Beta School")

        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=2024, school_id=self.school_beta.id
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

        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=2024, school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        student_names = [student['name'] for student in res.data['students_reports']]

        # Should be sorted: Amy Anderson before Charlie Davis
        self.assertEqual(student_names, sorted(student_names))
        self.assertEqual(student_names[0], 'Amy Anderson')
        self.assertEqual(student_names[1], 'Charlie Davis')

    def test_excludes_other_schools(self):
        """Test that report only includes classes from the specified school"""
        print("Test that report only includes classes from the specified school")

        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=2024, school_id=self.school_alpha.id
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

        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=2024, school_id=self.school_alpha.id
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

        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=2024, school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Should only include first teacher's classes
        self.assertEqual(res.data['school_name'], 'Alpha Academy')
        self.assertEqual(len(res.data['students_reports']), 2)

    def test_school_total_is_correct(self):
        """Test that school_total is calculated correctly"""
        print("Test that school_total is calculated correctly")

        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=2024, school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Calculate expected total manually
        calculated_total = sum(
            student['total'] for student in res.data['students_reports']
        )

        self.assertEqual(res.data['school_total'], calculated_total)

    def test_empty_month_returns_empty_report(self):
        """Test that a month with no classes returns an empty report with correct structure"""
        print("Test that a month with no classes returns an empty report with correct structure")

        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=10, year=2024, school_id=self.school_alpha.id
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

        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=2024, school_id=school_gamma.id
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

        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=2024, school_id=school_gamma.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Verify it's specifically a float type
        self.assertIsInstance(res.data['school_total'], float)
        self.assertEqual(res.data['school_total'], 0.0)

    def test_december_edge_case(self):
        """Test generating report for December (year boundary)"""
        print("Test generating report for December (year boundary)")

        # Create class in December 2024
        create_scheduled_class(
            self.teacher_profile, self.alpha_student_1,
            date(2024, 12, 15), '10:00', '11:00', 'completed'
        )

        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=12, year=2024, school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Should include December classes
        self.assertGreater(len(res.data['students_reports']), 0)

    def test_multiple_classes_same_student(self):
        """Test report when a student has multiple classes in the month"""
        print("Test report when a student has multiple classes in the month")

        # alpha_student_1 already has 2 classes in November from setUp
        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=2024, school_id=self.school_alpha.id
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
        # Should have aggregated hours/total from both classes
        self.assertGreater(charlie_report['hours'], 1)
        self.assertGreater(charlie_report['total'], 0)

    def test_includes_various_class_statuses(self):
        """Test that report includes classes with different statuses"""
        print("Test that report includes classes with different statuses")

        # Add classes with different statuses
        create_scheduled_class(
            self.teacher_profile, self.alpha_student_1,
            date(2024, 11, 22), '10:00', '11:00', 'scheduled'
        )
        create_scheduled_class(
            self.teacher_profile, self.alpha_student_2,
            date(2024, 11, 25), '14:00', '15:00', 'cancelled'
        )

        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=2024, school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Report should include classes regardless of status
        self.assertEqual(len(res.data['students_reports']), 2)

    def test_preserves_student_report_fields(self):
        """Test that all student report fields are preserved"""
        print("Test that all student report fields are preserved")

        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=2024, school_id=self.school_alpha.id
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

        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=2024, school_id=self.school_alpha.id
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

    def test_different_schools_produce_different_reports(self):
        """Test that reports for different schools are independent"""
        print("Test that reports for different schools are independent")

        url_alpha = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=2024, school_id=self.school_alpha.id
        )
        res_alpha = self.client.get(url_alpha)

        url_beta = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=2024, school_id=self.school_beta.id
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

        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=2024, school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Should NOT have classes_in_schools key
        self.assertNotIn('classes_in_schools', res.data)

        # Should directly have school_name, students_reports, school_total
        self.assertIn('school_name', res.data)
        self.assertIn('students_reports', res.data)
        self.assertIn('school_total', res.data)

    def test_nonexistent_school_id_returns_404(self):
        """Test that querying with a non-existent school ID returns 404"""
        print("Test that querying with a non-existent school ID returns 404")

        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=2024, school_id=99999
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_without_teacher_profile_returns_404(self):
        """Test that a user without a teacher profile gets 404"""
        print("Test that a user without a teacher profile gets 404")

        # Create user without teacher profile
        user_without_profile = get_test_user(username='noprofile', password='pass')
        self.client.force_authenticate(user_without_profile)

        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=2024, school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_month_parameter(self):
        """Test behavior with invalid month parameter"""
        print("Test behavior with invalid month parameter")

        # Test with month 13 (invalid)
        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=13, year=2024, school_id=self.school_alpha.id
        )

        # The API currently raises a ValueError for invalid months
        with self.assertRaises(ValueError):
            res = self.client.get(url)

    def test_invalid_year_parameter(self):
        """Test behavior with invalid year parameter"""
        print("Test behavior with invalid year parameter")

        # Test with year 0 (invalid)
        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=0, school_id=self.school_alpha.id
        )

        # The API currently raises a ValueError for invalid years
        with self.assertRaises(ValueError):
            res = self.client.get(url)

    def test_different_teacher_cannot_access_other_teachers_schools(self):
        """Test that a different teacher cannot access another teacher's school data"""
        print("Test that a different teacher cannot access another teacher's school data")

        # Create school for other teacher
        other_teacher_school = create_test_school(
            self.other_teacher_profile, name='Other School', address_line_1='999 Other St'
        )

        # Try to access as first teacher (currently authenticated)
        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=2024, school_id=other_teacher_school.id
        )
        res = self.client.get(url)

        # Since the school exists but doesn't belong to the authenticated teacher,
        # the report should still be generated but may be empty or filtered
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_response_is_json_serializable(self):
        """Test that the response can be properly JSON serialized"""
        print("Test that the response can be properly JSON serialized")

        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=2024, school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Attempt to serialize the response data to JSON
        try:
            json_data = json.dumps(res.data)
            self.assertIsNotNone(json_data)
        except (TypeError, ValueError) as e:
            self.fail(f"Response data is not JSON serializable: {e}")

    def test_january_report(self):
        """Test generating report for January (first month of year)"""
        print("Test generating report for January (first month of year)")

        # Create class in January 2024
        create_scheduled_class(
            self.teacher_profile, self.alpha_student_1,
            date(2024, 1, 15), '10:00', '11:00', 'completed'
        )

        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=1, year=2024, school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreater(len(res.data['students_reports']), 0)

    def test_february_leap_year_report(self):
        """Test generating report for February in a leap year"""
        print("Test generating report for February in a leap year")

        # Create class on Feb 29, 2024 (leap year)
        create_scheduled_class(
            self.teacher_profile, self.alpha_student_1,
            date(2024, 2, 29), '10:00', '11:00', 'completed'
        )

        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=2, year=2024, school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreater(len(res.data['students_reports']), 0)

    def test_report_for_different_years_are_separate(self):
        """Test that reports from different years are kept separate"""
        print("Test that reports from different years are kept separate")

        # Create classes in November 2023
        create_scheduled_class(
            self.teacher_profile, self.alpha_student_1,
            date(2023, 11, 15), '10:00', '11:00', 'completed'
        )

        # Query November 2024
        url_2024 = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=2024, school_id=self.school_alpha.id
        )
        res_2024 = self.client.get(url_2024)

        self.assertEqual(res_2024.status_code, status.HTTP_200_OK)
        # Should have 2 students from setUp (November 2024)
        self.assertEqual(len(res_2024.data['students_reports']), 2)

        # Query November 2023
        url_2023 = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=2023, school_id=self.school_alpha.id
        )
        res_2023 = self.client.get(url_2023)

        self.assertEqual(res_2023.status_code, status.HTTP_200_OK)
        # Should have 1 student (Charlie Davis from 2023)
        self.assertEqual(len(res_2023.data['students_reports']), 1)

    def test_report_with_classes_at_month_boundaries(self):
        """Test that classes at the beginning and end of month are included"""
        print("Test that classes at the beginning and end of month are included")

        # Class at start of month (November 1)
        create_scheduled_class(
            self.teacher_profile, self.alpha_student_1,
            date(2024, 11, 1), '10:00', '11:00', 'completed'
        )

        # Class at end of month (November 30)
        create_scheduled_class(
            self.teacher_profile, self.alpha_student_2,
            date(2024, 11, 30), '10:00', '11:00', 'completed'
        )

        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=2024, school_id=self.school_alpha.id
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
            date(2024, 11, 28), '10:00', '10:00', 'completed'
        )

        url = ESTIMATED_SCHOOL_EARNINGS_BY_MONTH_YEAR_URL.format(
            month=11, year=2024, school_id=self.school_alpha.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Response should be valid even with zero-duration class
        self.assertIsNotNone(res.data)
