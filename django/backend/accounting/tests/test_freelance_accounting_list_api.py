import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from decimal import Decimal
from django.utils.timezone import make_aware, get_current_timezone
from datetime import datetime, timedelta

from accounting.models import FreelanceTuitionTransactionRecord
from accounting.serializers import FreelanceTuitionTransactionRecordSerializer
from student_account.models import StudentOrClass
from user_profiles.models import UserProfile

User = get_user_model()

TUITION_TRANSACTIONS_BY_MONTH_YEAR_URL = '/api/accounting/received-tuition-transactions-by-month-year/{month}/{year}/'


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


def create_test_student(teacher_profile, name='Alice Johnson', initial_hours='10.00', tuition_rate=1000):
    """Helper function to create a freelance student"""
    return StudentOrClass.objects.create(
        student_or_class_name=name,
        account_type='freelance',
        teacher=teacher_profile,
        purchased_class_hours=Decimal(initial_hours),
        tuition_per_hour=tuition_rate,
        comments='Test student'
    )


def create_transaction_with_specific_timestamp(student, transaction_type, hours, timestamp):
    """Helper function to create a transaction with a specific timestamp"""
    transaction = FreelanceTuitionTransactionRecord(
        student_or_class=student,
        transaction_type=transaction_type,
        class_hours_purchased_or_refunded=hours
    )
    transaction.save()
    # Manually set the timestamp after creation
    transaction.time_stamp = timestamp
    transaction.save(update_fields=['time_stamp'])
    return transaction


class FreelanceTuitionTransactionsByMonthYearPublicApiTests(TestCase):
    """Test the publicly available tuition transactions by month/year API"""

    def setUp(self):
        self.client = APIClient()
        self.test_user = get_test_user()
        self.teacher_profile = create_test_teacher_profile(self.test_user)
        self.student = create_test_student(self.teacher_profile)

    def test_login_required_for_list_by_month_year(self):
        """Test that login is required for retrieving transactions by month and year"""
        print("Test that login is required for retrieving transactions by month and year")
        
        url = TUITION_TRANSACTIONS_BY_MONTH_YEAR_URL.format(month=6, year=2024)
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class FreelanceTuitionTransactionsByMonthYearPrivateApiTests(TestCase):
    """Test the authenticated tuition transactions by month/year API"""

    def setUp(self):
        self.client = APIClient()
        self.test_user = get_test_user()
        self.teacher_profile = create_test_teacher_profile(self.test_user)
        self.student = create_test_student(self.teacher_profile)
        self.client.force_authenticate(self.test_user)

    def test_retrieve_transactions_for_specific_month_and_year(self):
        """Test retrieving transactions for a specific month and year"""
        print("Test retrieving transactions for a specific month and year")
        
        # Create transactions in June 2024
        june_timestamp_1 = make_aware(datetime(2024, 6, 5, 10, 30), get_current_timezone())
        june_timestamp_2 = make_aware(datetime(2024, 6, 15, 14, 20), get_current_timezone())
        
        transaction_1 = create_transaction_with_specific_timestamp(
            self.student, 'payment', 5, june_timestamp_1
        )
        transaction_2 = create_transaction_with_specific_timestamp(
            self.student, 'payment', 3, june_timestamp_2
        )
        
        # Create a transaction in a different month (should not be included)
        july_timestamp = make_aware(datetime(2024, 7, 10, 10, 30), get_current_timezone())
        create_transaction_with_specific_timestamp(
            self.student, 'payment', 2, july_timestamp
        )
        
        url = TUITION_TRANSACTIONS_BY_MONTH_YEAR_URL.format(month=6, year=2024)
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        
        # Verify the correct transactions are returned
        transaction_ids = [t['id'] for t in res.data]
        self.assertIn(transaction_1.id, transaction_ids)
        self.assertIn(transaction_2.id, transaction_ids)

    def test_empty_result_for_month_with_no_transactions(self):
        """Test that an empty list is returned for a month with no transactions"""
        print("Test that an empty list is returned for a month with no transactions")
        
        # Create transaction in June
        june_timestamp = make_aware(datetime(2024, 6, 15, 10, 30), get_current_timezone())
        create_transaction_with_specific_timestamp(
            self.student, 'payment', 5, june_timestamp
        )
        
        # Query for July (no transactions)
        url = TUITION_TRANSACTIONS_BY_MONTH_YEAR_URL.format(month=7, year=2024)
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 0)

    def test_transactions_filtered_by_authenticated_user(self):
        """Test that only transactions for the authenticated user's students are returned"""
        print("Test that only transactions for the authenticated user's students are returned")
        
        # Create second teacher with student
        second_user = get_test_user(username='teacher2', password='pass2')
        second_teacher = create_test_teacher_profile(
            second_user, surname='Jones', given_name='Mary'
        )
        second_student = create_test_student(second_teacher, name='Bob Smith')
        
        # Create transactions for both teachers in June 2024
        june_timestamp_1 = make_aware(datetime(2024, 6, 5, 10, 30), get_current_timezone())
        june_timestamp_2 = make_aware(datetime(2024, 6, 10, 14, 20), get_current_timezone())
        
        first_teacher_transaction = create_transaction_with_specific_timestamp(
            self.student, 'payment', 5, june_timestamp_1
        )
        second_teacher_transaction = create_transaction_with_specific_timestamp(
            second_student, 'payment', 3, june_timestamp_2
        )
        
        # Query as first teacher
        url = TUITION_TRANSACTIONS_BY_MONTH_YEAR_URL.format(month=6, year=2024)
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['id'], first_teacher_transaction.id)
        
        # Authenticate as second teacher and verify their transactions
        self.client.force_authenticate(second_user)
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['id'], second_teacher_transaction.id)

    def test_transactions_ordered_by_timestamp(self):
        """Test that transactions are returned ordered by timestamp"""
        print("Test that transactions are returned ordered by timestamp")
        
        # Create transactions with different timestamps (out of order)
        june_timestamp_3 = make_aware(datetime(2024, 6, 20, 10, 30), get_current_timezone())
        june_timestamp_1 = make_aware(datetime(2024, 6, 5, 10, 30), get_current_timezone())
        june_timestamp_2 = make_aware(datetime(2024, 6, 15, 14, 20), get_current_timezone())
        
        transaction_3 = create_transaction_with_specific_timestamp(
            self.student, 'payment', 5, june_timestamp_3
        )
        transaction_1 = create_transaction_with_specific_timestamp(
            self.student, 'payment', 3, june_timestamp_1
        )
        transaction_2 = create_transaction_with_specific_timestamp(
            self.student, 'payment', 2, june_timestamp_2
        )
        
        url = TUITION_TRANSACTIONS_BY_MONTH_YEAR_URL.format(month=6, year=2024)
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)
        
        # Verify ordering (earliest first)
        self.assertEqual(res.data[0]['id'], transaction_1.id)
        self.assertEqual(res.data[1]['id'], transaction_2.id)
        self.assertEqual(res.data[2]['id'], transaction_3.id)

    def test_transactions_at_month_boundaries(self):
        """Test that transactions at the beginning and end of month are included"""
        print("Test that transactions at the beginning and end of month are included")
        
        # Transaction at start of month (June 1, 00:00:01)
        start_timestamp = make_aware(datetime(2024, 6, 1, 0, 0, 1), get_current_timezone())
        start_transaction = create_transaction_with_specific_timestamp(
            self.student, 'payment', 2, start_timestamp
        )
        
        # Transaction at end of month (June 30, 23:59:58)
        end_timestamp = make_aware(datetime(2024, 6, 30, 23, 59, 58), get_current_timezone())
        end_transaction = create_transaction_with_specific_timestamp(
            self.student, 'payment', 3, end_timestamp
        )
        
        url = TUITION_TRANSACTIONS_BY_MONTH_YEAR_URL.format(month=6, year=2024)
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        
        transaction_ids = [t['id'] for t in res.data]
        self.assertIn(start_transaction.id, transaction_ids)
        self.assertIn(end_transaction.id, transaction_ids)

    def test_transactions_just_outside_month_not_included(self):
        """Test that transactions just outside the month range are not included"""
        print("Test that transactions just outside the month range are not included")
        
        # Transaction just before month starts (May 31, 23:59:59)
        before_timestamp = make_aware(datetime(2024, 5, 31, 23, 59, 59), get_current_timezone())
        create_transaction_with_specific_timestamp(
            self.student, 'payment', 2, before_timestamp
        )
        
        # Transaction in the middle of June
        june_timestamp = make_aware(datetime(2024, 6, 15, 12, 0, 0), get_current_timezone())
        june_transaction = create_transaction_with_specific_timestamp(
            self.student, 'payment', 3, june_timestamp
        )
        
        # Transaction just after month ends (July 1, 00:00:00)
        after_timestamp = make_aware(datetime(2024, 7, 1, 0, 0, 0), get_current_timezone())
        create_transaction_with_specific_timestamp(
            self.student, 'payment', 2, after_timestamp
        )
        
        url = TUITION_TRANSACTIONS_BY_MONTH_YEAR_URL.format(month=6, year=2024)
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['id'], june_transaction.id)

    def test_february_leap_year_transactions(self):
        """Test retrieving transactions for February in a leap year"""
        print("Test retrieving transactions for February in a leap year")
        
        # Create transaction on Feb 29, 2024 (leap year)
        feb_29_timestamp = make_aware(datetime(2024, 2, 29, 12, 0), get_current_timezone())
        feb_transaction = create_transaction_with_specific_timestamp(
            self.student, 'payment', 5, feb_29_timestamp
        )
        
        url = TUITION_TRANSACTIONS_BY_MONTH_YEAR_URL.format(month=2, year=2024)
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['id'], feb_transaction.id)

    def test_december_transactions(self):
        """Test retrieving transactions for December (edge case month)"""
        print("Test retrieving transactions for December")
        
        # Create transactions in December
        dec_timestamp_1 = make_aware(datetime(2024, 12, 1, 10, 0), get_current_timezone())
        dec_timestamp_2 = make_aware(datetime(2024, 12, 31, 23, 59, 0), get_current_timezone())
        
        dec_transaction_1 = create_transaction_with_specific_timestamp(
            self.student, 'payment', 3, dec_timestamp_1
        )
        dec_transaction_2 = create_transaction_with_specific_timestamp(
            self.student, 'payment', 2, dec_timestamp_2
        )
        
        url = TUITION_TRANSACTIONS_BY_MONTH_YEAR_URL.format(month=12, year=2024)
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_different_years_are_separate(self):
        """Test that transactions from different years are kept separate"""
        print("Test that transactions from different years are kept separate")
        
        # Create transactions in June 2024
        june_2024_timestamp = make_aware(datetime(2024, 6, 15, 10, 30), get_current_timezone())
        transaction_2024 = create_transaction_with_specific_timestamp(
            self.student, 'payment', 5, june_2024_timestamp
        )
        
        # Create transactions in June 2023
        june_2023_timestamp = make_aware(datetime(2023, 6, 15, 10, 30), get_current_timezone())
        transaction_2023 = create_transaction_with_specific_timestamp(
            self.student, 'payment', 3, june_2023_timestamp
        )
        
        # Query June 2024
        url_2024 = TUITION_TRANSACTIONS_BY_MONTH_YEAR_URL.format(month=6, year=2024)
        res_2024 = self.client.get(url_2024)
        
        self.assertEqual(res_2024.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_2024.data), 1)
        self.assertEqual(res_2024.data[0]['id'], transaction_2024.id)
        
        # Query June 2023
        url_2023 = TUITION_TRANSACTIONS_BY_MONTH_YEAR_URL.format(month=6, year=2023)
        res_2023 = self.client.get(url_2023)
        
        self.assertEqual(res_2023.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_2023.data), 1)
        self.assertEqual(res_2023.data[0]['id'], transaction_2023.id)

    def test_multiple_students_same_month(self):
        """Test retrieving transactions for multiple students in the same month"""
        print("Test retrieving transactions for multiple students in the same month")
        
        # Create second student for same teacher
        student_2 = create_test_student(
            self.teacher_profile,
            name='Charlie Brown',
            initial_hours='15.00'
        )
        
        # Create transactions for both students in June
        june_timestamp_1 = make_aware(datetime(2024, 6, 5, 10, 30), get_current_timezone())
        june_timestamp_2 = make_aware(datetime(2024, 6, 15, 14, 20), get_current_timezone())
        
        transaction_1 = create_transaction_with_specific_timestamp(
            self.student, 'payment', 5, june_timestamp_1
        )
        transaction_2 = create_transaction_with_specific_timestamp(
            student_2, 'payment', 3, june_timestamp_2
        )
        
        url = TUITION_TRANSACTIONS_BY_MONTH_YEAR_URL.format(month=6, year=2024)
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        
        transaction_ids = [t['id'] for t in res.data]
        self.assertIn(transaction_1.id, transaction_ids)
        self.assertIn(transaction_2.id, transaction_ids)

    def test_payment_and_refund_transactions_both_included(self):
        """Test that both payment and refund transactions are included"""
        print("Test that both payment and refund transactions are included")
        
        june_timestamp_1 = make_aware(datetime(2024, 6, 5, 10, 30), get_current_timezone())
        june_timestamp_2 = make_aware(datetime(2024, 6, 15, 14, 20), get_current_timezone())
        
        payment_transaction = create_transaction_with_specific_timestamp(
            self.student, 'payment', 5, june_timestamp_1
        )
        refund_transaction = create_transaction_with_specific_timestamp(
            self.student, 'refund', 2, june_timestamp_2
        )
        
        url = TUITION_TRANSACTIONS_BY_MONTH_YEAR_URL.format(month=6, year=2024)
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        
        # Verify both types are present
        transaction_types = [t['transaction_type'] for t in res.data]
        self.assertIn('payment', transaction_types)
        self.assertIn('refund', transaction_types)

    def test_serializer_fields_in_response(self):
        """Test that the response contains all expected serializer fields"""
        print("Test that the response contains all expected serializer fields")
        
        june_timestamp = make_aware(datetime(2024, 6, 15, 10, 30), get_current_timezone())
        transaction = create_transaction_with_specific_timestamp(
            self.student, 'payment', 5, june_timestamp
        )
        
        url = TUITION_TRANSACTIONS_BY_MONTH_YEAR_URL.format(month=6, year=2024)
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        
        # Verify expected fields are present
        transaction_data = res.data[0]
        expected_fields = [
            'id', 'student_or_class', 'transaction_amount',
            'transaction_type', 'class_hours_purchased_or_refunded', 'time_stamp'
        ]
        
        for field in expected_fields:
            self.assertIn(field, transaction_data)

    def test_january_transactions(self):
        """Test retrieving transactions for January (first month)"""
        print("Test retrieving transactions for January")
        
        jan_timestamp = make_aware(datetime(2024, 1, 15, 10, 30), get_current_timezone())
        jan_transaction = create_transaction_with_specific_timestamp(
            self.student, 'payment', 4, jan_timestamp
        )
        
        url = TUITION_TRANSACTIONS_BY_MONTH_YEAR_URL.format(month=1, year=2024)
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['id'], jan_transaction.id)

    def test_large_number_of_transactions_in_month(self):
        """Test retrieving a large number of transactions for a single month"""
        print("Test retrieving a large number of transactions for a single month")
        
        # Create 10 transactions in June
        for day in range(1, 11):
            timestamp = make_aware(datetime(2024, 6, day, 10, 30), get_current_timezone())
            create_transaction_with_specific_timestamp(
                self.student, 'payment', 2, timestamp
            )
        
        url = TUITION_TRANSACTIONS_BY_MONTH_YEAR_URL.format(month=6, year=2024)
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 10)
