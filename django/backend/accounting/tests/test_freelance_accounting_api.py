import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from decimal import Decimal

from accounting.models import (
    FreelanceTuitionTransactionRecord,
    PurchasedHoursModificationRecord
)
from accounting.serializers import FreelanceTuitionTransactionRecordSerializer
from student_account.models import StudentOrClass
from user_profiles.models import UserProfile

User = get_user_model()

TUITION_TRANSACTION_URL = '/api/accounting/tuition-transactions/'


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


class FreelanceTuitionTransactionPublicApiTests(TestCase):
    """Test the publicly available tuition transaction API"""

    def setUp(self):
        self.client = APIClient()
        self.test_user = get_test_user()
        self.teacher_profile = create_test_teacher_profile(self.test_user)
        self.student = create_test_student(self.teacher_profile)

    def test_login_required_for_create(self):
        """Test that login is required for creating a tuition transaction"""
        print("Test that login is required for creating a tuition transaction")
        
        payload = {
            'student_or_class': self.student.id,
            'transaction_type': 'payment',
            'class_hours_purchased_or_refunded': 5
        }
        
        res = self.client.post(
            TUITION_TRANSACTION_URL,
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_required_for_list(self):
        """Test that login is required for retrieving tuition transactions list"""
        print("Test that login is required for retrieving tuition transactions list")
        
        res = self.client.get(TUITION_TRANSACTION_URL)
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class FreelanceTuitionTransactionPrivateApiTests(TestCase):
    """Test the authenticated tuition transaction API"""

    def setUp(self):
        self.client = APIClient()
        self.test_user = get_test_user()
        self.teacher_profile = create_test_teacher_profile(self.test_user)
        self.student = create_test_student(self.teacher_profile)
        self.client.force_authenticate(self.test_user)

    def test_create_payment_transaction_success(self):
        """Test successfully creating a payment transaction"""
        print("Test successfully creating a payment transaction")
        
        initial_hours = self.student.purchased_class_hours
        
        payload = {
            'student_or_class': self.student.id,
            'transaction_type': 'payment',
            'class_hours_purchased_or_refunded': 5
        }
        
        res = self.client.post(
            TUITION_TRANSACTION_URL,
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        # Verify transaction was created
        transaction = FreelanceTuitionTransactionRecord.objects.get(id=res.data['id'])
        self.assertEqual(transaction.student_or_class.id, self.student.id)
        self.assertEqual(transaction.transaction_type, 'payment')
        self.assertEqual(transaction.class_hours_purchased_or_refunded, 5)
        self.assertEqual(transaction.transaction_amount, 5000)  # 5 hours * 1000/hour
        
        # Verify student hours were updated
        self.student.refresh_from_db()
        self.assertEqual(self.student.purchased_class_hours, initial_hours + Decimal('5.00'))

    def test_create_refund_transaction_success(self):
        """Test successfully creating a refund transaction"""
        print("Test successfully creating a refund transaction")
        
        initial_hours = self.student.purchased_class_hours
        
        payload = {
            'student_or_class': self.student.id,
            'transaction_type': 'refund',
            'class_hours_purchased_or_refunded': 3
        }
        
        res = self.client.post(
            TUITION_TRANSACTION_URL,
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        # Verify transaction was created
        transaction = FreelanceTuitionTransactionRecord.objects.get(id=res.data['id'])
        self.assertEqual(transaction.student_or_class.id, self.student.id)
        self.assertEqual(transaction.transaction_type, 'refund')
        self.assertEqual(transaction.class_hours_purchased_or_refunded, 3)
        self.assertEqual(transaction.transaction_amount, 3000)  # 3 hours * 1000/hour
        
        # Verify student hours were updated
        self.student.refresh_from_db()
        self.assertEqual(self.student.purchased_class_hours, initial_hours - Decimal('3.00'))

    def test_create_transaction_creates_modification_record(self):
        """Test that creating a transaction also creates a modification record"""
        print("Test that creating a transaction also creates a modification record")
        
        initial_modification_count = PurchasedHoursModificationRecord.objects.count()
        initial_hours = self.student.purchased_class_hours
        
        payload = {
            'student_or_class': self.student.id,
            'transaction_type': 'payment',
            'class_hours_purchased_or_refunded': 4
        }
        
        res = self.client.post(
            TUITION_TRANSACTION_URL,
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        # Verify modification record was created
        final_modification_count = PurchasedHoursModificationRecord.objects.count()
        self.assertEqual(final_modification_count, initial_modification_count + 1)
        
        # Verify modification record details
        transaction = FreelanceTuitionTransactionRecord.objects.get(id=res.data['id'])
        modification_record = PurchasedHoursModificationRecord.objects.get(
            tuition_transaction=transaction
        )
        
        self.assertEqual(modification_record.student_or_class, self.student)
        self.assertEqual(modification_record.modification_type, 'tuition_payment_add')
        self.assertEqual(modification_record.previous_purchased_class_hours, initial_hours)
        self.assertEqual(
            modification_record.updated_purchased_class_hours,
            initial_hours + Decimal('4.00')
        )

    def test_create_payment_with_different_tuition_rate(self):
        """Test creating a payment transaction for a student with different tuition rate"""
        print("Test creating a payment transaction for a student with different tuition rate")
        
        # Create a student with a different tuition rate
        expensive_student = create_test_student(
            self.teacher_profile,
            name='Bob Expensive',
            initial_hours='5.00',
            tuition_rate=1500
        )
        
        payload = {
            'student_or_class': expensive_student.id,
            'transaction_type': 'payment',
            'class_hours_purchased_or_refunded': 2
        }
        
        res = self.client.post(
            TUITION_TRANSACTION_URL,
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        transaction = FreelanceTuitionTransactionRecord.objects.get(id=res.data['id'])
        self.assertEqual(transaction.transaction_amount, 3000)  # 2 hours * 1500/hour

    def test_create_transaction_with_missing_fields(self):
        """Test that creating a transaction with missing required fields fails"""
        print("Test that creating a transaction with missing required fields fails")
        
        # Missing class_hours_purchased_or_refunded
        payload = {
            'student_or_class': self.student.id,
            'transaction_type': 'payment',
        }
        
        res = self.client.post(
            TUITION_TRANSACTION_URL,
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_transaction_with_invalid_student(self):
        """Test that creating a transaction with invalid student ID fails"""
        print("Test that creating a transaction with invalid student ID fails")
        
        payload = {
            'student_or_class': 99999,  # Non-existent ID
            'transaction_type': 'payment',
            'class_hours_purchased_or_refunded': 5
        }
        
        res = self.client.post(
            TUITION_TRANSACTION_URL,
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_multiple_transactions_for_same_student(self):
        """Test creating multiple transactions for the same student"""
        print("Test creating multiple transactions for the same student")
        
        # First transaction
        payload_1 = {
            'student_or_class': self.student.id,
            'transaction_type': 'payment',
            'class_hours_purchased_or_refunded': 3
        }
        
        res_1 = self.client.post(
            TUITION_TRANSACTION_URL,
            data=json.dumps(payload_1),
            content_type='application/json'
        )
        
        self.assertEqual(res_1.status_code, status.HTTP_201_CREATED)
        self.student.refresh_from_db()
        hours_after_first = self.student.purchased_class_hours
        
        # Second transaction
        payload_2 = {
            'student_or_class': self.student.id,
            'transaction_type': 'payment',
            'class_hours_purchased_or_refunded': 2
        }
        
        res_2 = self.client.post(
            TUITION_TRANSACTION_URL,
            data=json.dumps(payload_2),
            content_type='application/json'
        )
        
        self.assertEqual(res_2.status_code, status.HTTP_201_CREATED)
        
        # Verify both transactions exist
        transactions = FreelanceTuitionTransactionRecord.objects.filter(
            student_or_class=self.student
        )
        self.assertEqual(transactions.count(), 2)
        
        # Verify final hours
        self.student.refresh_from_db()
        self.assertEqual(
            self.student.purchased_class_hours,
            Decimal('10.00') + Decimal('3.00') + Decimal('2.00')
        )

    def test_create_payment_then_refund(self):
        """Test creating a payment followed by a refund"""
        print("Test creating a payment followed by a refund")
        
        initial_hours = self.student.purchased_class_hours
        
        # Create payment
        payment_payload = {
            'student_or_class': self.student.id,
            'transaction_type': 'payment',
            'class_hours_purchased_or_refunded': 5
        }
        
        res_payment = self.client.post(
            TUITION_TRANSACTION_URL,
            data=json.dumps(payment_payload),
            content_type='application/json'
        )
        
        self.assertEqual(res_payment.status_code, status.HTTP_201_CREATED)
        
        # Create refund
        refund_payload = {
            'student_or_class': self.student.id,
            'transaction_type': 'refund',
            'class_hours_purchased_or_refunded': 2
        }
        
        res_refund = self.client.post(
            TUITION_TRANSACTION_URL,
            data=json.dumps(refund_payload),
            content_type='application/json'
        )
        
        self.assertEqual(res_refund.status_code, status.HTTP_201_CREATED)
        
        # Verify final hours (10 + 5 - 2 = 13)
        self.student.refresh_from_db()
        self.assertEqual(
            self.student.purchased_class_hours,
            initial_hours + Decimal('5.00') - Decimal('2.00')
        )

    def test_retrieve_transaction_list(self):
        """Test retrieving list of transactions"""
        print("Test retrieving list of transactions")
        
        # Create some transactions
        FreelanceTuitionTransactionRecord.objects.create(
            student_or_class=self.student,
            transaction_type='payment',
            class_hours_purchased_or_refunded=3
        )
        
        FreelanceTuitionTransactionRecord.objects.create(
            student_or_class=self.student,
            transaction_type='payment',
            class_hours_purchased_or_refunded=2
        )
        
        res = self.client.get(TUITION_TRANSACTION_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_retrieve_single_transaction(self):
        """Test retrieving a single transaction by ID"""
        print("Test retrieving a single transaction by ID")
        
        transaction = FreelanceTuitionTransactionRecord.objects.create(
            student_or_class=self.student,
            transaction_type='payment',
            class_hours_purchased_or_refunded=4
        )
        
        url = f'{TUITION_TRANSACTION_URL}{transaction.id}/'
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        serializer = FreelanceTuitionTransactionRecordSerializer(transaction)
        self.assertEqual(res.data, serializer.data)

    def test_transaction_amount_calculated_correctly(self):
        """Test that transaction_amount is calculated correctly on save"""
        print("Test that transaction_amount is calculated correctly on save")
        
        payload = {
            'student_or_class': self.student.id,
            'transaction_type': 'payment',
            'class_hours_purchased_or_refunded': 7
        }
        
        res = self.client.post(
            TUITION_TRANSACTION_URL,
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        # Verify the transaction_amount was calculated (not editable in payload)
        self.assertEqual(res.data['transaction_amount'], 7000)  # 7 * 1000

    def test_create_transaction_for_different_teachers_students(self):
        """Test that different teachers can create transactions for their own students"""
        print("Test that different teachers can create transactions for their own students")
        
        # Create a second teacher and student
        second_user = get_test_user(username='teacher2', password='pass2')
        second_teacher = create_test_teacher_profile(
            second_user,
            surname='Jones',
            given_name='Mary'
        )
        second_student = create_test_student(
            second_teacher,
            name='Charlie Brown',
            initial_hours='8.00'
        )
        
        # Authenticate as second teacher
        self.client.force_authenticate(second_user)
        
        payload = {
            'student_or_class': second_student.id,
            'transaction_type': 'payment',
            'class_hours_purchased_or_refunded': 4
        }
        
        res = self.client.post(
            TUITION_TRANSACTION_URL,
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        transaction = FreelanceTuitionTransactionRecord.objects.get(id=res.data['id'])
        self.assertEqual(transaction.student_or_class, second_student)
        self.assertEqual(transaction.student_or_class.teacher, second_teacher)

    def test_timestamp_auto_generated_on_create(self):
        """Test that timestamp is automatically generated when creating transaction"""
        print("Test that timestamp is automatically generated when creating transaction")
        
        payload = {
            'student_or_class': self.student.id,
            'transaction_type': 'payment',
            'class_hours_purchased_or_refunded': 2
        }
        
        res = self.client.post(
            TUITION_TRANSACTION_URL,
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        transaction = FreelanceTuitionTransactionRecord.objects.get(id=res.data['id'])
        self.assertIsNotNone(transaction.time_stamp)
        self.assertIn('time_stamp', res.data)
