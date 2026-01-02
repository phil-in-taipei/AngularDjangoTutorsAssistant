import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from decimal import Decimal
from django.utils.timezone import make_aware, get_current_timezone
from datetime import datetime, timedelta

from accounting.models import (
    FreelanceTuitionTransactionRecord,
    PurchasedHoursModificationRecord
)
from accounting.serializers import PurchasedHoursModificationRecordSerializer
from accounting.utils import create_purchased_hours_modification_record_for_tuition_transaction
from student_account.models import StudentOrClass
from user_profiles.models import UserProfile
from class_scheduling.models import ScheduledClass

User = get_user_model()

PURCHASED_HOURS_MODIFICATIONS_BY_MONTH_ACCOUNT_URL = '/api/accounting/purchased-hours-modifications/by-month-and-account/{month}/{year}/{account_id}/'


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


def create_modification_record_with_timestamp(
        student, transaction, modification_type, prev_hours, updated_hours, timestamp
):
    """Helper function to create a modification record with a specific timestamp"""
    modification = PurchasedHoursModificationRecord(
        student_or_class=student,
        tuition_transaction=transaction,
        modification_type=modification_type,
        previous_purchased_class_hours=prev_hours,
        updated_purchased_class_hours=updated_hours
    )
    modification.save()
    # Manually set the timestamp after creation
    modification.time_stamp = timestamp
    modification.save(update_fields=['time_stamp'])
    return modification


def create_class_modification_record_with_timestamp(
        student, scheduled_class, modification_type, prev_hours, updated_hours, timestamp
):
    """Helper function to create a class status modification record with a specific timestamp"""
    modification = PurchasedHoursModificationRecord(
        student_or_class=student,
        modified_scheduled_class=scheduled_class,
        modification_type=modification_type,
        previous_purchased_class_hours=prev_hours,
        updated_purchased_class_hours=updated_hours
    )
    modification.save()
    # Manually set the timestamp after creation
    modification.time_stamp = timestamp
    modification.save(update_fields=['time_stamp'])
    return modification


class PurchasedHoursModificationsByMonthAccountPublicApiTests(TestCase):
    """Test the publicly available purchased hours modifications by month/account API"""

    def setUp(self):
        self.client = APIClient()
        self.test_user = get_test_user()
        self.teacher_profile = create_test_teacher_profile(self.test_user)
        self.student = create_test_student(self.teacher_profile)

    def test_login_required_for_list_by_month_account(self):
        """Test that login is required for retrieving modification records"""
        print("Test that login is required for retrieving modification records")

        url = PURCHASED_HOURS_MODIFICATIONS_BY_MONTH_ACCOUNT_URL.format(
            month=6, year=2024, account_id=self.student.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PurchasedHoursModificationsByMonthAccountPrivateApiTests(TestCase):
    """Test the authenticated purchased hours modifications by month/account API"""

    def setUp(self):
        self.client = APIClient()
        self.test_user = get_test_user()
        self.teacher_profile = create_test_teacher_profile(self.test_user)
        self.student = create_test_student(self.teacher_profile)
        self.client.force_authenticate(self.test_user)

    def test_retrieve_modification_records_for_specific_month_year_and_account(self):
        """Test retrieving modification records for a specific month, year, and account"""
        print("Test retrieving modification records for a specific month, year, and account")

        # Create transactions and their modification records in June 2024
        june_timestamp_1 = make_aware(datetime(2024, 6, 5, 10, 30), get_current_timezone())
        june_timestamp_2 = make_aware(datetime(2024, 6, 15, 14, 20), get_current_timezone())

        transaction_1 = create_transaction_with_specific_timestamp(
            self.student, 'payment', 5, june_timestamp_1
        )
        modification_1 = create_modification_record_with_timestamp(
            self.student, transaction_1, 'tuition_payment_add',
            Decimal('10.00'), Decimal('15.00'), june_timestamp_1
        )

        transaction_2 = create_transaction_with_specific_timestamp(
            self.student, 'payment', 3, june_timestamp_2
        )
        modification_2 = create_modification_record_with_timestamp(
            self.student, transaction_2, 'tuition_payment_add',
            Decimal('15.00'), Decimal('18.00'), june_timestamp_2
        )

        # Create a modification record in a different month (should not be included)
        july_timestamp = make_aware(datetime(2024, 7, 10, 10, 30), get_current_timezone())
        transaction_3 = create_transaction_with_specific_timestamp(
            self.student, 'payment', 2, july_timestamp
        )
        create_modification_record_with_timestamp(
            self.student, transaction_3, 'tuition_payment_add',
            Decimal('18.00'), Decimal('20.00'), july_timestamp
        )

        url = PURCHASED_HOURS_MODIFICATIONS_BY_MONTH_ACCOUNT_URL.format(
            month=6, year=2024, account_id=self.student.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

        # Verify the correct modifications are returned
        modification_ids = [m['id'] for m in res.data]
        self.assertIn(modification_1.id, modification_ids)
        self.assertIn(modification_2.id, modification_ids)

    def test_empty_result_for_month_with_no_modifications(self):
        """Test that an empty list is returned for a month with no modification records"""
        print("Test that an empty list is returned for a month with no modification records")

        # Create modification in June
        june_timestamp = make_aware(datetime(2024, 6, 15, 10, 30), get_current_timezone())
        transaction = create_transaction_with_specific_timestamp(
            self.student, 'payment', 5, june_timestamp
        )
        create_modification_record_with_timestamp(
            self.student, transaction, 'tuition_payment_add',
            Decimal('10.00'), Decimal('15.00'), june_timestamp
        )

        # Query for July (no modifications)
        url = PURCHASED_HOURS_MODIFICATIONS_BY_MONTH_ACCOUNT_URL.format(
            month=7, year=2024, account_id=self.student.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 0)

    def test_modifications_filtered_by_account_id(self):
        """Test that only modifications for the specified account are returned"""
        print("Test that only modifications for the specified account are returned")

        # Create second student for same teacher
        student_2 = create_test_student(
            self.teacher_profile,
            name='Bob Smith',
            initial_hours='8.00'
        )

        # Create modifications for both students in June 2024
        june_timestamp_1 = make_aware(datetime(2024, 6, 5, 10, 30), get_current_timezone())
        june_timestamp_2 = make_aware(datetime(2024, 6, 10, 14, 20), get_current_timezone())

        transaction_1 = create_transaction_with_specific_timestamp(
            self.student, 'payment', 5, june_timestamp_1
        )
        student_1_modification = create_modification_record_with_timestamp(
            self.student, transaction_1, 'tuition_payment_add',
            Decimal('10.00'), Decimal('15.00'), june_timestamp_1
        )

        transaction_2 = create_transaction_with_specific_timestamp(
            student_2, 'payment', 3, june_timestamp_2
        )
        student_2_modification = create_modification_record_with_timestamp(
            student_2, transaction_2, 'tuition_payment_add',
            Decimal('8.00'), Decimal('11.00'), june_timestamp_2
        )

        # Query for first student
        url_student_1 = PURCHASED_HOURS_MODIFICATIONS_BY_MONTH_ACCOUNT_URL.format(
            month=6, year=2024, account_id=self.student.id
        )
        res_student_1 = self.client.get(url_student_1)

        self.assertEqual(res_student_1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_student_1.data), 1)
        self.assertEqual(res_student_1.data[0]['id'], student_1_modification.id)

        # Query for second student
        url_student_2 = PURCHASED_HOURS_MODIFICATIONS_BY_MONTH_ACCOUNT_URL.format(
            month=6, year=2024, account_id=student_2.id
        )
        res_student_2 = self.client.get(url_student_2)

        self.assertEqual(res_student_2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_student_2.data), 1)
        self.assertEqual(res_student_2.data[0]['id'], student_2_modification.id)

    def test_modifications_ordered_by_timestamp(self):
        """Test that modification records are returned ordered by timestamp"""
        print("Test that modification records are returned ordered by timestamp")

        # Create modifications with different timestamps (out of order)
        june_timestamp_3 = make_aware(datetime(2024, 6, 20, 10, 30), get_current_timezone())
        june_timestamp_1 = make_aware(datetime(2024, 6, 5, 10, 30), get_current_timezone())
        june_timestamp_2 = make_aware(datetime(2024, 6, 15, 14, 20), get_current_timezone())

        transaction_3 = create_transaction_with_specific_timestamp(
            self.student, 'payment', 5, june_timestamp_3
        )
        modification_3 = create_modification_record_with_timestamp(
            self.student, transaction_3, 'tuition_payment_add',
            Decimal('18.00'), Decimal('23.00'), june_timestamp_3
        )

        transaction_1 = create_transaction_with_specific_timestamp(
            self.student, 'payment', 3, june_timestamp_1
        )
        modification_1 = create_modification_record_with_timestamp(
            self.student, transaction_1, 'tuition_payment_add',
            Decimal('10.00'), Decimal('13.00'), june_timestamp_1
        )

        transaction_2 = create_transaction_with_specific_timestamp(
            self.student, 'payment', 2, june_timestamp_2
        )
        modification_2 = create_modification_record_with_timestamp(
            self.student, transaction_2, 'tuition_payment_add',
            Decimal('13.00'), Decimal('15.00'), june_timestamp_2
        )

        url = PURCHASED_HOURS_MODIFICATIONS_BY_MONTH_ACCOUNT_URL.format(
            month=6, year=2024, account_id=self.student.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

        # Verify ordering (earliest first)
        self.assertEqual(res.data[0]['id'], modification_1.id)
        self.assertEqual(res.data[1]['id'], modification_2.id)
        self.assertEqual(res.data[2]['id'], modification_3.id)

    def test_modifications_at_month_boundaries(self):
        """Test that modifications at the beginning and end of month are included"""
        print("Test that modifications at the beginning and end of month are included")

        # Modification at start of month (June 1, 00:00:01)
        start_timestamp = make_aware(datetime(2024, 6, 1, 0, 0, 1), get_current_timezone())
        start_transaction = create_transaction_with_specific_timestamp(
            self.student, 'payment', 2, start_timestamp
        )
        start_modification = create_modification_record_with_timestamp(
            self.student, start_transaction, 'tuition_payment_add',
            Decimal('10.00'), Decimal('12.00'), start_timestamp
        )

        # Modification at end of month (June 30, 23:59:58)
        end_timestamp = make_aware(datetime(2024, 6, 30, 23, 59, 58), get_current_timezone())
        end_transaction = create_transaction_with_specific_timestamp(
            self.student, 'payment', 3, end_timestamp
        )
        end_modification = create_modification_record_with_timestamp(
            self.student, end_transaction, 'tuition_payment_add',
            Decimal('12.00'), Decimal('15.00'), end_timestamp
        )

        url = PURCHASED_HOURS_MODIFICATIONS_BY_MONTH_ACCOUNT_URL.format(
            month=6, year=2024, account_id=self.student.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

        modification_ids = [m['id'] for m in res.data]
        self.assertIn(start_modification.id, modification_ids)
        self.assertIn(end_modification.id, modification_ids)

    def test_modifications_just_outside_month_not_included(self):
        """Test that modifications just outside the month range are not included"""
        print("Test that modifications just outside the month range are not included")

        # Modification just before month starts (May 31, 23:59:59)
        before_timestamp = make_aware(datetime(2024, 5, 31, 23, 59, 59), get_current_timezone())
        before_transaction = create_transaction_with_specific_timestamp(
            self.student, 'payment', 2, before_timestamp
        )
        create_modification_record_with_timestamp(
            self.student, before_transaction, 'tuition_payment_add',
            Decimal('10.00'), Decimal('12.00'), before_timestamp
        )

        # Modification in the middle of June
        june_timestamp = make_aware(datetime(2024, 6, 15, 12, 0, 0), get_current_timezone())
        june_transaction = create_transaction_with_specific_timestamp(
            self.student, 'payment', 3, june_timestamp
        )
        june_modification = create_modification_record_with_timestamp(
            self.student, june_transaction, 'tuition_payment_add',
            Decimal('12.00'), Decimal('15.00'), june_timestamp
        )

        # Modification just after month ends (July 1, 00:00:00)
        after_timestamp = make_aware(datetime(2024, 7, 1, 0, 0, 0), get_current_timezone())
        after_transaction = create_transaction_with_specific_timestamp(
            self.student, 'payment', 2, after_timestamp
        )
        create_modification_record_with_timestamp(
            self.student, after_transaction, 'tuition_payment_add',
            Decimal('15.00'), Decimal('17.00'), after_timestamp
        )

        url = PURCHASED_HOURS_MODIFICATIONS_BY_MONTH_ACCOUNT_URL.format(
            month=6, year=2024, account_id=self.student.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['id'], june_modification.id)

    def test_different_years_are_separate(self):
        """Test that modifications from different years are kept separate"""
        print("Test that modifications from different years are kept separate")

        # Create modifications in June 2024
        june_2024_timestamp = make_aware(datetime(2024, 6, 15, 10, 30), get_current_timezone())
        transaction_2024 = create_transaction_with_specific_timestamp(
            self.student, 'payment', 5, june_2024_timestamp
        )
        modification_2024 = create_modification_record_with_timestamp(
            self.student, transaction_2024, 'tuition_payment_add',
            Decimal('10.00'), Decimal('15.00'), june_2024_timestamp
        )

        # Create modifications in June 2023
        june_2023_timestamp = make_aware(datetime(2023, 6, 15, 10, 30), get_current_timezone())
        transaction_2023 = create_transaction_with_specific_timestamp(
            self.student, 'payment', 3, june_2023_timestamp
        )
        modification_2023 = create_modification_record_with_timestamp(
            self.student, transaction_2023, 'tuition_payment_add',
            Decimal('7.00'), Decimal('10.00'), june_2023_timestamp
        )

        # Query June 2024
        url_2024 = PURCHASED_HOURS_MODIFICATIONS_BY_MONTH_ACCOUNT_URL.format(
            month=6, year=2024, account_id=self.student.id
        )
        res_2024 = self.client.get(url_2024)

        self.assertEqual(res_2024.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_2024.data), 1)
        self.assertEqual(res_2024.data[0]['id'], modification_2024.id)

        # Query June 2023
        url_2023 = PURCHASED_HOURS_MODIFICATIONS_BY_MONTH_ACCOUNT_URL.format(
            month=6, year=2023, account_id=self.student.id
        )
        res_2023 = self.client.get(url_2023)

        self.assertEqual(res_2023.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_2023.data), 1)
        self.assertEqual(res_2023.data[0]['id'], modification_2023.id)

    def test_payment_and_refund_modifications_both_included(self):
        """Test that both payment and refund modification records are included"""
        print("Test that both payment and refund modification records are included")

        june_timestamp_1 = make_aware(datetime(2024, 6, 5, 10, 30), get_current_timezone())
        june_timestamp_2 = make_aware(datetime(2024, 6, 15, 14, 20), get_current_timezone())

        payment_transaction = create_transaction_with_specific_timestamp(
            self.student, 'payment', 5, june_timestamp_1
        )
        payment_modification = create_modification_record_with_timestamp(
            self.student, payment_transaction, 'tuition_payment_add',
            Decimal('10.00'), Decimal('15.00'), june_timestamp_1
        )

        refund_transaction = create_transaction_with_specific_timestamp(
            self.student, 'refund', 2, june_timestamp_2
        )
        refund_modification = create_modification_record_with_timestamp(
            self.student, refund_transaction, 'tuition_refund_deduct',
            Decimal('15.00'), Decimal('13.00'), june_timestamp_2
        )

        url = PURCHASED_HOURS_MODIFICATIONS_BY_MONTH_ACCOUNT_URL.format(
            month=6, year=2024, account_id=self.student.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

        # Verify both types are present
        modification_types = [m['modification_type'] for m in res.data]
        self.assertIn('tuition_payment_add', modification_types)
        self.assertIn('tuition_refund_deduct', modification_types)

    def test_class_status_modification_records_included(self):
        """Test that class status modification records are included in results"""
        print("Test that class status modification records are included in results")

        # Create a scheduled class
        june_class_date = datetime(2024, 6, 10).date()
        scheduled_class = ScheduledClass.objects.create(
            student_or_class=self.student,
            teacher=self.teacher_profile,
            date=june_class_date,
            start_time=datetime.strptime('10:00', '%H:%M').time(),
            finish_time=datetime.strptime('11:00', '%H:%M').time(),
            class_status='completed'
        )

        # Create a class status modification record
        june_timestamp = make_aware(datetime(2024, 6, 10, 11, 30), get_current_timezone())
        class_modification = create_class_modification_record_with_timestamp(
            self.student, scheduled_class, 'class_status_modification_deduct',
            Decimal('10.00'), Decimal('9.00'), june_timestamp
        )

        url = PURCHASED_HOURS_MODIFICATIONS_BY_MONTH_ACCOUNT_URL.format(
            month=6, year=2024, account_id=self.student.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['id'], class_modification.id)
        self.assertEqual(res.data[0]['modification_type'], 'class_status_modification_deduct')

    def test_mixed_tuition_and_class_modifications(self):
        """Test retrieving both tuition and class status modifications together"""
        print("Test retrieving both tuition and class status modifications together")

        # Create tuition modification
        june_timestamp_1 = make_aware(datetime(2024, 6, 5, 10, 30), get_current_timezone())
        transaction = create_transaction_with_specific_timestamp(
            self.student, 'payment', 5, june_timestamp_1
        )
        tuition_modification = create_modification_record_with_timestamp(
            self.student, transaction, 'tuition_payment_add',
            Decimal('10.00'), Decimal('15.00'), june_timestamp_1
        )

        # Create class status modification
        june_class_date = datetime(2024, 6, 10).date()
        scheduled_class = ScheduledClass.objects.create(
            student_or_class=self.student,
            teacher=self.teacher_profile,
            date=june_class_date,
            start_time=datetime.strptime('10:00', '%H:%M').time(),
            finish_time=datetime.strptime('11:00', '%H:%M').time(),
            class_status='completed'
        )

        june_timestamp_2 = make_aware(datetime(2024, 6, 10, 11, 30), get_current_timezone())
        class_modification = create_class_modification_record_with_timestamp(
            self.student, scheduled_class, 'class_status_modification_deduct',
            Decimal('15.00'), Decimal('14.00'), june_timestamp_2
        )

        url = PURCHASED_HOURS_MODIFICATIONS_BY_MONTH_ACCOUNT_URL.format(
            month=6, year=2024, account_id=self.student.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

        # Verify both types are present
        modification_ids = [m['id'] for m in res.data]
        self.assertIn(tuition_modification.id, modification_ids)
        self.assertIn(class_modification.id, modification_ids)

    def test_serializer_fields_in_response(self):
        """Test that the response contains all expected serializer fields"""
        print("Test that the response contains all expected serializer fields")

        june_timestamp = make_aware(datetime(2024, 6, 15, 10, 30), get_current_timezone())
        transaction = create_transaction_with_specific_timestamp(
            self.student, 'payment', 5, june_timestamp
        )
        create_modification_record_with_timestamp(
            self.student, transaction, 'tuition_payment_add',
            Decimal('10.00'), Decimal('15.00'), june_timestamp
        )

        url = PURCHASED_HOURS_MODIFICATIONS_BY_MONTH_ACCOUNT_URL.format(
            month=6, year=2024, account_id=self.student.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

        # Verify expected fields are present
        modification_data = res.data[0]
        expected_fields = [
            'id', 'student_or_class', 'tuition_transaction', 'modified_scheduled_class',
            'modification_type', 'previous_purchased_class_hours',
            'updated_purchased_class_hours', 'time_stamp'
        ]

        for field in expected_fields:
            self.assertIn(field, modification_data)

    def test_nested_serializer_data_for_tuition_transaction(self):
        """Test that nested tuition_transaction data is included (read_only)"""
        print("Test that nested tuition_transaction data is included")

        june_timestamp = make_aware(datetime(2024, 6, 15, 10, 30), get_current_timezone())
        transaction = create_transaction_with_specific_timestamp(
            self.student, 'payment', 5, june_timestamp
        )
        create_modification_record_with_timestamp(
            self.student, transaction, 'tuition_payment_add',
            Decimal('10.00'), Decimal('15.00'), june_timestamp
        )

        url = PURCHASED_HOURS_MODIFICATIONS_BY_MONTH_ACCOUNT_URL.format(
            month=6, year=2024, account_id=self.student.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

        # Verify nested transaction data is present
        modification_data = res.data[0]
        self.assertIsNotNone(modification_data['tuition_transaction'])
        self.assertIn('id', modification_data['tuition_transaction'])
        self.assertIn('transaction_amount', modification_data['tuition_transaction'])

    def test_nested_serializer_data_for_scheduled_class(self):
        """Test that nested modified_scheduled_class data is included (read_only)"""
        print("Test that nested modified_scheduled_class data is included")

        # Create a scheduled class
        june_class_date = datetime(2024, 6, 10).date()
        scheduled_class = ScheduledClass.objects.create(
            student_or_class=self.student,
            teacher=self.teacher_profile,
            date=june_class_date,
            start_time=datetime.strptime('10:00', '%H:%M').time(),
            finish_time=datetime.strptime('11:00', '%H:%M').time(),
            class_status='completed'
        )

        june_timestamp = make_aware(datetime(2024, 6, 10, 11, 30), get_current_timezone())
        create_class_modification_record_with_timestamp(
            self.student, scheduled_class, 'class_status_modification_deduct',
            Decimal('10.00'), Decimal('9.00'), june_timestamp
        )

        url = PURCHASED_HOURS_MODIFICATIONS_BY_MONTH_ACCOUNT_URL.format(
            month=6, year=2024, account_id=self.student.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

        # Verify nested class data is present
        modification_data = res.data[0]
        self.assertIsNotNone(modification_data['modified_scheduled_class'])
        self.assertIn('id', modification_data['modified_scheduled_class'])
        self.assertIn('date', modification_data['modified_scheduled_class'])
        self.assertIn('class_status', modification_data['modified_scheduled_class'])

    def test_february_leap_year_modifications(self):
        """Test retrieving modifications for February in a leap year"""
        print("Test retrieving modifications for February in a leap year")

        # Create modification on Feb 29, 2024 (leap year)
        feb_29_timestamp = make_aware(datetime(2024, 2, 29, 12, 0), get_current_timezone())
        transaction = create_transaction_with_specific_timestamp(
            self.student, 'payment', 5, feb_29_timestamp
        )
        feb_modification = create_modification_record_with_timestamp(
            self.student, transaction, 'tuition_payment_add',
            Decimal('10.00'), Decimal('15.00'), feb_29_timestamp
        )

        url = PURCHASED_HOURS_MODIFICATIONS_BY_MONTH_ACCOUNT_URL.format(
            month=2, year=2024, account_id=self.student.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['id'], feb_modification.id)

    def test_december_modifications(self):
        """Test retrieving modifications for December (edge case month)"""
        print("Test retrieving modifications for December")

        dec_timestamp_1 = make_aware(datetime(2024, 12, 1, 10, 0), get_current_timezone())
        dec_timestamp_2 = make_aware(datetime(2024, 12, 31, 23, 59, 0), get_current_timezone())

        transaction_1 = create_transaction_with_specific_timestamp(
            self.student, 'payment', 3, dec_timestamp_1
        )
        dec_modification_1 = create_modification_record_with_timestamp(
            self.student, transaction_1, 'tuition_payment_add',
            Decimal('10.00'), Decimal('13.00'), dec_timestamp_1
        )

        transaction_2 = create_transaction_with_specific_timestamp(
            self.student, 'payment', 2, dec_timestamp_2
        )
        dec_modification_2 = create_modification_record_with_timestamp(
            self.student, transaction_2, 'tuition_payment_add',
            Decimal('13.00'), Decimal('15.00'), dec_timestamp_2
        )

        url = PURCHASED_HOURS_MODIFICATIONS_BY_MONTH_ACCOUNT_URL.format(
            month=12, year=2024, account_id=self.student.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_nonexistent_account_id_returns_empty(self):
        """Test that querying with a non-existent account ID returns empty list"""
        print("Test that querying with a non-existent account ID returns empty list")

        # Create modification for existing student
        june_timestamp = make_aware(datetime(2024, 6, 15, 10, 30), get_current_timezone())
        transaction = create_transaction_with_specific_timestamp(
            self.student, 'payment', 5, june_timestamp
        )
        create_modification_record_with_timestamp(
            self.student, transaction, 'tuition_payment_add',
            Decimal('10.00'), Decimal('15.00'), june_timestamp
        )

        # Query with non-existent account ID
        url = PURCHASED_HOURS_MODIFICATIONS_BY_MONTH_ACCOUNT_URL.format(
            month=6, year=2024, account_id=99999
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 0)

    def test_large_number_of_modifications_in_month(self):
        """Test retrieving a large number of modification records for a single month"""
        print("Test retrieving a large number of modification records for a single month")

        # Create 10 modifications in June
        for day in range(1, 11):
            timestamp = make_aware(datetime(2024, 6, day, 10, 30), get_current_timezone())
            transaction = create_transaction_with_specific_timestamp(
                self.student, 'payment', 2, timestamp
            )
            create_modification_record_with_timestamp(
                self.student, transaction, 'tuition_payment_add',
                Decimal(f'{10 + (day - 1) * 2}.00'), Decimal(f'{12 + (day - 1) * 2}.00'), timestamp
            )

        url = PURCHASED_HOURS_MODIFICATIONS_BY_MONTH_ACCOUNT_URL.format(
            month=6, year=2024, account_id=self.student.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 10)

    def test_different_teacher_can_access_their_students_modifications(self):
        """Test that different teachers can access their own students' modifications"""
        print("Test that different teachers can access their own students' modifications")

        # Create second teacher with student
        second_user = get_test_user(username='teacher2', password='pass2')
        second_teacher = create_test_teacher_profile(
            second_user, surname='Jones', given_name='Mary'
        )
        second_student = create_test_student(
            second_teacher, name='Charlie Brown', initial_hours='8.00'
        )

        # Create modifications for second teacher's student
        june_timestamp = make_aware(datetime(2024, 6, 15, 10, 30), get_current_timezone())
        transaction = create_transaction_with_specific_timestamp(
            second_student, 'payment', 5, june_timestamp
        )
        second_modification = create_modification_record_with_timestamp(
            second_student, transaction, 'tuition_payment_add',
            Decimal('8.00'), Decimal('13.00'), june_timestamp
        )

        # Authenticate as second teacher and query
        self.client.force_authenticate(second_user)

        url = PURCHASED_HOURS_MODIFICATIONS_BY_MONTH_ACCOUNT_URL.format(
            month=6, year=2024, account_id=second_student.id
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['id'], second_modification.id)
