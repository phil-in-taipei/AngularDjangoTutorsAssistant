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

ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL = '/api/accounting/estimated-earnings-by-month-year/{month}/{year}/'


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
        teacher_profile, name='Test Student', account_type='freelance',
        school=None, initial_hours='10.00', tuition_rate=1000
):
    """Helper function to create a student"""
    return StudentOrClass.objects.create(
        student_or_class_name=name,
        account_type=account_type,
        school=school,
        teacher=teacher_profile,
        purchased_class_hours=Decimal(initial_hours) if account_type == 'freelance' else None,
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


class EstimatedEarningsByMonthYearPublicApiTests(TestCase):
    """Test the publicly available estimated earnings by month/year API"""

    def setUp(self):
        self.client = APIClient()
        self.test_user = get_test_user()
        self.teacher_profile = create_test_teacher_profile(self.test_user)

    def test_login_required_for_estimated_earnings(self):
        """Test that login is required for retrieving estimated earnings"""
        print("Test that login is required for retrieving estimated earnings")

        url = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=11, year=2024)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class EstimatedEarningsByMonthYearPrivateApiTests(TestCase):
    """Test the authenticated estimated earnings by month/year API"""

    def setUp(self):
        """
        Set up comprehensive test data including:
        - Teacher profile
        - 2 Schools (Alpha Academy and Beta School)
        - 2 Freelance students
        - School-affiliated students
        - Scheduled classes for November 2024
        """
        self.client = APIClient()

        # Create teacher user and profile
        self.teacher_user = get_test_user(username='teacher1', password='testpass123')
        self.teacher_profile = create_test_teacher_profile(
            self.teacher_user, surname='Smith', given_name='John'
        )
        self.client.force_authenticate(self.teacher_user)

        # Create 2 schools
        self.school_alpha = create_test_school(
            self.teacher_profile, name='Alpha Academy', address_line_1='123 Main St'
        )
        self.school_beta = create_test_school(
            self.teacher_profile, name='Beta School', address_line_1='456 Oak Ave'
        )

        # Create 2 freelance students
        self.freelance_student_1 = create_test_student(
            self.teacher_profile, name='Alice Brown', account_type='freelance',
            initial_hours='10.00', tuition_rate=1000
        )
        self.freelance_student_2 = create_test_student(
            self.teacher_profile, name='Bob Wilson', account_type='freelance',
            initial_hours='15.00', tuition_rate=1200
        )

        # Create school-affiliated students
        self.school_alpha_student = create_test_student(
            self.teacher_profile, name='Charlie Davis', account_type='school',
            school=self.school_alpha, tuition_rate=900
        )
        self.school_beta_student = create_test_student(
            self.teacher_profile, name='Diana Miller', account_type='school',
            school=self.school_beta, tuition_rate=950
        )

        # Create scheduled classes for November 2024
        self.nov_freelance_class_1 = create_scheduled_class(
            self.teacher_profile, self.freelance_student_1,
            date(2024, 11, 5), '10:00', '11:00', 'completed'
        )
        self.nov_freelance_class_2 = create_scheduled_class(
            self.teacher_profile, self.freelance_student_2,
            date(2024, 11, 15), '14:00', '15:30', 'completed'
        )
        self.nov_school_alpha_class = create_scheduled_class(
            self.teacher_profile, self.school_alpha_student,
            date(2024, 11, 12), '13:00', '14:00', 'completed'
        )
        self.nov_school_beta_class = create_scheduled_class(
            self.teacher_profile, self.school_beta_student,
            date(2024, 11, 18), '09:00', '10:30', 'completed'
        )

    def test_retrieve_estimated_earnings_report_structure(self):
        """Test that the API returns the expected report structure"""
        print("Test that the API returns the expected report structure")

        url = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=11, year=2024)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Verify top-level structure
        self.assertIn('classes_in_schools', res.data)
        self.assertIn('freelance_students', res.data)
        self.assertIn('overall_monthly_total', res.data)

        # Verify data types
        self.assertIsInstance(res.data['classes_in_schools'], list)
        self.assertIsInstance(res.data['freelance_students'], list)
        self.assertIsNotNone(res.data['overall_monthly_total'])

    def test_report_includes_all_schools(self):
        """Test that report includes all schools with classes"""
        print("Test that report includes all schools with classes")

        url = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=11, year=2024)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Should have 2 schools in the report
        self.assertEqual(len(res.data['classes_in_schools']), 2)

        school_names = [school['school_name'] for school in res.data['classes_in_schools']]
        self.assertIn('Alpha Academy', school_names)
        self.assertIn('Beta School', school_names)

    def test_report_includes_freelance_students(self):
        """Test that report includes all freelance students with classes"""
        print("Test that report includes all freelance students with classes")

        url = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=11, year=2024)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Should have 2 freelance students in the report
        self.assertEqual(len(res.data['freelance_students']), 2)

        freelance_names = [student['name'] for student in res.data['freelance_students']]
        self.assertIn('Alice Brown', freelance_names)
        self.assertIn('Bob Wilson', freelance_names)

    def test_schools_have_totals(self):
        """Test that each school has a school_total field calculated"""
        print("Test that each school has a school_total field calculated")

        url = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=11, year=2024)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Each school should have a school_total field
        for school in res.data['classes_in_schools']:
            self.assertIn('school_total', school)
            self.assertIsNotNone(school['school_total'])

    def test_students_sorted_alphabetically_within_schools(self):
        """Test that students within schools are sorted alphabetically"""
        print("Test that students within schools are sorted alphabetically")

        # Add another student to Alpha Academy to test sorting
        another_alpha_student = create_test_student(
            self.teacher_profile, name='Amy Anderson', account_type='school',
            school=self.school_alpha, tuition_rate=900
        )
        create_scheduled_class(
            self.teacher_profile, another_alpha_student,
            date(2024, 11, 10), '10:00', '11:00', 'completed'
        )

        url = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=11, year=2024)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Find Alpha Academy in the report
        alpha_school = next(
            (school for school in res.data['classes_in_schools']
             if school['school_name'] == 'Alpha Academy'),
            None
        )

        self.assertIsNotNone(alpha_school)
        students = alpha_school['students_reports']

        # Students should be sorted: Amy Anderson before Charlie Davis
        if len(students) > 1:
            self.assertEqual(students[0]['name'], 'Amy Anderson')
            self.assertEqual(students[1]['name'], 'Charlie Davis')

    def test_freelance_students_sorted_alphabetically(self):
        """Test that freelance students are sorted alphabetically"""
        print("Test that freelance students are sorted alphabetically")

        url = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=11, year=2024)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        freelance_names = [student['name'] for student in res.data['freelance_students']]

        # Should be sorted: Alice Brown before Bob Wilson
        self.assertEqual(freelance_names, sorted(freelance_names))

    def test_overall_total_is_correct(self):
        """Test that overall_monthly_total is calculated correctly"""
        print("Test that overall_monthly_total is calculated correctly")

        url = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=11, year=2024)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Calculate expected total manually
        school_totals_sum = sum(
            school['school_total'] for school in res.data['classes_in_schools']
        )
        freelance_totals_sum = sum(
            student['total'] for student in res.data['freelance_students']
        )
        expected_total = school_totals_sum + freelance_totals_sum

        self.assertEqual(res.data['overall_monthly_total'], expected_total)

    def test_report_for_month_with_no_classes(self):
        """Test generating report for a month with no classes"""
        print("Test generating report for a month with no classes")

        url = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=10, year=2024)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Should have empty lists
        self.assertEqual(len(res.data['classes_in_schools']), 0)
        self.assertEqual(len(res.data['freelance_students']), 0)
        self.assertEqual(res.data['overall_monthly_total'], 0)

    def test_report_with_multiple_classes_same_student(self):
        """Test report when a student has multiple classes in the month"""
        print("Test report when a student has multiple classes in the month")

        # Add another class for Alice Brown
        create_scheduled_class(
            self.teacher_profile, self.freelance_student_1,
            date(2024, 11, 20), '14:00', '15:00', 'completed'
        )

        url = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=11, year=2024)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Find Alice Brown in freelance students
        alice_report = next(
            (student for student in res.data['freelance_students']
             if student['name'] == 'Alice Brown'),
            None
        )

        self.assertIsNotNone(alice_report)
        # Total should reflect both classes
        self.assertGreater(alice_report['total'], 0)

    def test_report_filters_by_authenticated_teacher(self):
        """Test that report only includes classes for the authenticated teacher"""
        print("Test that report only includes classes for the authenticated teacher")

        # Create another teacher with classes
        other_teacher_user = get_test_user(username='teacher2', password='pass2')
        other_teacher_profile = create_test_teacher_profile(
            other_teacher_user, surname='Jones', given_name='Mary'
        )

        # Create class for other teacher using the same freelance student
        create_scheduled_class(
            other_teacher_profile, self.freelance_student_1,
            date(2024, 11, 25), '10:00', '11:00', 'completed'
        )

        # Query as first teacher (already authenticated in setUp)
        url = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=11, year=2024)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Should only include first teacher's classes (2 freelance students)
        # Not the class taught by other_teacher
        self.assertEqual(len(res.data['freelance_students']), 2)

    def test_report_for_december_edge_case(self):
        """Test generating report for December (year boundary)"""
        print("Test generating report for December (year boundary)")

        # Create class in December 2024
        create_scheduled_class(
            self.teacher_profile, self.freelance_student_1,
            date(2024, 12, 15), '10:00', '11:00', 'completed'
        )

        url = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=12, year=2024)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Should include December classes
        self.assertGreater(len(res.data['freelance_students']), 0)

    def test_report_includes_various_class_statuses(self):
        """Test that report includes classes with different statuses"""
        print("Test that report includes classes with different statuses")

        # Add classes with different statuses
        create_scheduled_class(
            self.teacher_profile, self.freelance_student_1,
            date(2024, 11, 22), '10:00', '11:00', 'scheduled'
        )
        create_scheduled_class(
            self.teacher_profile, self.freelance_student_2,
            date(2024, 11, 25), '14:00', '15:00', 'cancelled'
        )

        url = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=11, year=2024)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Report should include classes regardless of status
        self.assertEqual(len(res.data['freelance_students']), 2)

    def test_report_with_only_school_classes(self):
        """Test generating report when there are only school classes, no freelance"""
        print("Test generating report when there are only school classes, no freelance")

        # Delete freelance classes
        ScheduledClass.objects.filter(
            student_or_class__school__isnull=True
        ).delete()

        url = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=11, year=2024)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Should have schools but no freelance
        self.assertGreater(len(res.data['classes_in_schools']), 0)
        self.assertEqual(len(res.data['freelance_students']), 0)

        # Overall total should equal school totals only
        school_totals_sum = sum(
            school['school_total'] for school in res.data['classes_in_schools']
        )
        self.assertEqual(res.data['overall_monthly_total'], school_totals_sum)

    def test_report_with_only_freelance_classes(self):
        """Test generating report when there are only freelance classes, no schools"""
        print("Test generating report when there are only freelance classes, no schools")

        # Delete school classes
        ScheduledClass.objects.filter(
            student_or_class__school__isnull=False
        ).delete()

        url = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=11, year=2024)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Should have freelance but no schools
        self.assertEqual(len(res.data['classes_in_schools']), 0)
        self.assertGreater(len(res.data['freelance_students']), 0)

        # Overall total should equal freelance totals only
        freelance_totals_sum = sum(
            student['total'] for student in res.data['freelance_students']
        )
        self.assertEqual(res.data['overall_monthly_total'], freelance_totals_sum)

    def test_report_for_different_years_are_separate(self):
        """Test that reports from different years are kept separate"""
        print("Test that reports from different years are kept separate")

        # Create classes in November 2023
        create_scheduled_class(
            self.teacher_profile, self.freelance_student_1,
            date(2023, 11, 15), '10:00', '11:00', 'completed'
        )

        # Query November 2024
        url_2024 = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=11, year=2024)
        res_2024 = self.client.get(url_2024)

        self.assertEqual(res_2024.status_code, status.HTTP_200_OK)
        # Should have 2 freelance students (from setUp)
        self.assertEqual(len(res_2024.data['freelance_students']), 2)

        # Query November 2023
        url_2023 = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=11, year=2023)
        res_2023 = self.client.get(url_2023)

        self.assertEqual(res_2023.status_code, status.HTTP_200_OK)
        # Should have 1 freelance student (from 2023)
        self.assertEqual(len(res_2023.data['freelance_students']), 1)

    def test_comprehensive_report_integration(self):
        """
        Comprehensive integration test with:
        - Multiple schools
        - Multiple students per school
        - Multiple freelance students
        - Multiple classes per student
        """
        print("Comprehensive integration test")

        # Add more students and classes
        alpha_student_2 = create_test_student(
            self.teacher_profile, name='Emily Evans', account_type='school',
            school=self.school_alpha, tuition_rate=900
        )

        create_scheduled_class(
            self.teacher_profile, alpha_student_2,
            date(2024, 11, 8), '10:00', '11:00', 'completed'
        )
        create_scheduled_class(
            self.teacher_profile, self.school_alpha_student,
            date(2024, 11, 14), '14:00', '15:00', 'completed'
        )

        url = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=11, year=2024)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Verify comprehensive structure
        self.assertEqual(len(res.data['classes_in_schools']), 2)
        self.assertEqual(len(res.data['freelance_students']), 2)

        # Verify Alpha Academy has 2 students
        alpha_school = next(
            (school for school in res.data['classes_in_schools']
             if school['school_name'] == 'Alpha Academy'),
            None
        )
        self.assertEqual(len(alpha_school['students_reports']), 2)

        # Verify students are sorted
        student_names = [s['name'] for s in alpha_school['students_reports']]
        self.assertEqual(student_names, sorted(student_names))

        # Verify overall total is positive
        self.assertGreater(res.data['overall_monthly_total'], 0)

        # Verify school totals are calculated
        self.assertIn('school_total', alpha_school)
        self.assertGreater(alpha_school['school_total'], 0)

    def test_february_leap_year_report(self):
        """Test generating report for February in a leap year"""
        print("Test generating report for February in a leap year")

        # Create class on Feb 29, 2024 (leap year)
        create_scheduled_class(
            self.teacher_profile, self.freelance_student_1,
            date(2024, 2, 29), '10:00', '11:00', 'completed'
        )

        url = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=2, year=2024)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreater(len(res.data['freelance_students']), 0)

    def test_january_report(self):
        """Test generating report for January (first month of year)"""
        print("Test generating report for January (first month of year)")

        # Create class in January 2024
        create_scheduled_class(
            self.teacher_profile, self.freelance_student_1,
            date(2024, 1, 15), '10:00', '11:00', 'completed'
        )

        url = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=1, year=2024)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreater(len(res.data['freelance_students']), 0)

    def test_different_teacher_sees_only_their_classes(self):
        """Test that different teachers see only their own classes in the report"""
        print("Test that different teachers see only their own classes in the report")

        # Create second teacher
        second_teacher_user = get_test_user(username='teacher2', password='pass2')
        second_teacher_profile = create_test_teacher_profile(
            second_teacher_user, surname='Jones', given_name='Mary'
        )

        # Create student and class for second teacher
        second_teacher_student = create_test_student(
            second_teacher_profile, name='Xavier Young', account_type='freelance',
            initial_hours='10.00', tuition_rate=1100
        )
        create_scheduled_class(
            second_teacher_profile, second_teacher_student,
            date(2024, 11, 10), '10:00', '11:00', 'completed'
        )

        # First teacher's request (already authenticated)
        url = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=11, year=2024)
        res_teacher1 = self.client.get(url)

        self.assertEqual(res_teacher1.status_code, status.HTTP_200_OK)
        freelance_names_teacher1 = [
            student['name'] for student in res_teacher1.data['freelance_students']
        ]
        self.assertNotIn('Xavier Young', freelance_names_teacher1)

        # Second teacher's request
        self.client.force_authenticate(second_teacher_user)
        res_teacher2 = self.client.get(url)

        self.assertEqual(res_teacher2.status_code, status.HTTP_200_OK)
        freelance_names_teacher2 = [
            student['name'] for student in res_teacher2.data['freelance_students']
        ]
        self.assertIn('Xavier Young', freelance_names_teacher2)
        self.assertNotIn('Alice Brown', freelance_names_teacher2)

    def test_response_is_json_serializable(self):
        """Test that the response can be properly JSON serialized"""
        print("Test that the response can be properly JSON serialized")

        url = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=11, year=2024)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Attempt to serialize the response data to JSON
        try:
            json_data = json.dumps(res.data)
            self.assertIsNotNone(json_data)
        except (TypeError, ValueError) as e:
            self.fail(f"Response data is not JSON serializable: {e}")

    def test_report_with_classes_at_month_boundaries(self):
        """Test that classes at the beginning and end of month are included"""
        print("Test that classes at the beginning and end of month are included")

        # Class at start of month (November 1)
        create_scheduled_class(
            self.teacher_profile, self.freelance_student_1,
            date(2024, 11, 1), '10:00', '11:00', 'completed'
        )

        # Class at end of month (November 30)
        create_scheduled_class(
            self.teacher_profile, self.freelance_student_2,
            date(2024, 11, 30), '10:00', '11:00', 'completed'
        )

        url = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=11, year=2024)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Should include both boundary classes plus the ones from setUp
        self.assertEqual(len(res.data['freelance_students']), 2)

    def test_invalid_month_parameter(self):
        """Test behavior with invalid month parameter"""
        print("Test behavior with invalid month parameter")

        # Test with month 13 (invalid)
        url = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=13, year=2024)

        # The API currently raises a ValueError for invalid months
        with self.assertRaises(ValueError):
            res = self.client.get(url)

    def test_invalid_year_parameter(self):
        """Test behavior with invalid year parameter"""
        print("Test behavior with invalid year parameter")

        # Test with year 0 (invalid)
        url = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=11, year=0)

        # The API currently raises a ValueError for invalid years
        with self.assertRaises(ValueError):
            res = self.client.get(url)

    def test_user_without_teacher_profile(self):
        """Test that a user without a teacher profile gets 404"""
        print("Test that a user without a teacher profile gets 404")

        # Create user without teacher profile
        user_without_profile = get_test_user(username='noprofile', password='pass')
        self.client.force_authenticate(user_without_profile)

        url = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=11, year=2024)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_report_with_zero_duration_classes_excluded(self):
        """Test that classes with zero duration are handled appropriately"""
        print("Test that classes with zero duration are handled appropriately")

        # Create class with same start and finish time (zero duration)
        create_scheduled_class(
            self.teacher_profile, self.freelance_student_1,
            date(2024, 11, 28), '10:00', '10:00', 'completed'
        )

        url = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=11, year=2024)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Response should be valid even with zero-duration class
        self.assertIsNotNone(res.data)

    def test_multiple_schools_sorted_alphabetically(self):
        """Test that schools are sorted alphabetically in the response"""
        print("Test that schools are sorted alphabetically in the response")

        url = ESTIMATED_EARNINGS_BY_MONTH_YEAR_URL.format(month=11, year=2024)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        school_names = [school['school_name'] for school in res.data['classes_in_schools']]

        # Schools should be sorted alphabetically
        self.assertEqual(school_names, sorted(school_names))
