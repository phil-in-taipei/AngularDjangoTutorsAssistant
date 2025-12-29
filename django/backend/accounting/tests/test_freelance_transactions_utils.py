from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal

from accounting.models import (
    FreelanceTuitionTransactionRecord,
    PurchasedHoursModificationRecord
)
from accounting.utils import create_purchased_hours_modification_record_for_tuition_transaction
from student_account.models import StudentOrClass
from user_profiles.models import UserProfile

User = get_user_model()


class CreatePurchasedHoursModificationRecordTestCase(TestCase):
    """
    Test suite for the create_purchased_hours_modification_record_for_tuition_transaction function.
    """

    def setUp(self):
        """
        Set up test data that will be used across multiple test methods.
        """
        # Create a test user
        self.user = User.objects.create_user(
            username='testteacher',
            email='teacher@test.com',
            password='testpass123'
        )

        # Create a user profile for the teacher
        self.teacher_profile = UserProfile.objects.create(
            user=self.user,
            contact_email='teacher@test.com',
            surname='Smith',
            given_name='John'
        )

        # Create a freelance student account
        self.student = StudentOrClass.objects.create(
            student_or_class_name='Alice Johnson',
            account_type='freelance',
            teacher=self.teacher_profile,
            purchased_class_hours=Decimal('10.00'),
            tuition_per_hour=1000,
            comments='Test student'
        )

    def test_creates_modification_record_for_payment_transaction(self):
        """
        Test that a PurchasedHoursModificationRecord is created correctly
        when a payment transaction is made.
        """
        # Store the initial hours
        previous_hours = self.student.purchased_class_hours

        # Create a payment transaction
        transaction = FreelanceTuitionTransactionRecord.objects.create(
            student_or_class=self.student,
            transaction_type='payment',
            class_hours_purchased_or_refunded=5
        )

        # Call the function under test
        create_purchased_hours_modification_record_for_tuition_transaction(
            previous_hours_purchased=previous_hours,
            freelance_tuition_transaction_record=transaction
        )

        # Verify the modification record was created
        modification_record = PurchasedHoursModificationRecord.objects.get(
            tuition_transaction=transaction
        )

        # Assert all fields are set correctly
        self.assertEqual(modification_record.student_or_class, self.student)
        self.assertEqual(modification_record.tuition_transaction, transaction)
        self.assertEqual(modification_record.modification_type, 'tuition_payment_add')
        self.assertEqual(modification_record.previous_purchased_class_hours, previous_hours)
        self.assertEqual(modification_record.updated_purchased_class_hours, Decimal('15.00'))
        self.assertIsNone(modification_record.modified_scheduled_class)

    def test_creates_modification_record_for_refund_transaction(self):
        """
        Test that a PurchasedHoursModificationRecord is created correctly
        when a refund transaction is made.
        """
        # Store the initial hours
        previous_hours = self.student.purchased_class_hours

        # Create a refund transaction
        transaction = FreelanceTuitionTransactionRecord.objects.create(
            student_or_class=self.student,
            transaction_type='refund',
            class_hours_purchased_or_refunded=3
        )

        # Call the function under test
        create_purchased_hours_modification_record_for_tuition_transaction(
            previous_hours_purchased=previous_hours,
            freelance_tuition_transaction_record=transaction
        )

        # Verify the modification record was created
        modification_record = PurchasedHoursModificationRecord.objects.get(
            tuition_transaction=transaction
        )

        # Assert all fields are set correctly
        self.assertEqual(modification_record.student_or_class, self.student)
        self.assertEqual(modification_record.tuition_transaction, transaction)
        self.assertEqual(modification_record.modification_type, 'tuition_refund_deduct')
        self.assertEqual(modification_record.previous_purchased_class_hours, previous_hours)
        self.assertEqual(modification_record.updated_purchased_class_hours, Decimal('7.00'))
        self.assertIsNone(modification_record.modified_scheduled_class)

    def test_modification_record_count_after_payment(self):
        """
        Test that exactly one PurchasedHoursModificationRecord is created
        for a payment transaction.
        """
        initial_count = PurchasedHoursModificationRecord.objects.count()

        previous_hours = self.student.purchased_class_hours
        transaction = FreelanceTuitionTransactionRecord.objects.create(
            student_or_class=self.student,
            transaction_type='payment',
            class_hours_purchased_or_refunded=2
        )

        create_purchased_hours_modification_record_for_tuition_transaction(
            previous_hours_purchased=previous_hours,
            freelance_tuition_transaction_record=transaction
        )

        final_count = PurchasedHoursModificationRecord.objects.count()
        self.assertEqual(final_count, initial_count + 1)

    def test_modification_record_reflects_correct_hours_calculation_for_payment(self):
        """
        Test that the updated_purchased_class_hours in the modification record
        correctly reflects the hours after a payment is added.
        """
        self.student.purchased_class_hours = Decimal('5.50')
        self.student.save()

        previous_hours = self.student.purchased_class_hours

        transaction = FreelanceTuitionTransactionRecord.objects.create(
            student_or_class=self.student,
            transaction_type='payment',
            class_hours_purchased_or_refunded=4
        )

        create_purchased_hours_modification_record_for_tuition_transaction(
            previous_hours_purchased=previous_hours,
            freelance_tuition_transaction_record=transaction
        )

        modification_record = PurchasedHoursModificationRecord.objects.get(
            tuition_transaction=transaction
        )

        # Updated hours should be 5.50 + 4.00 = 9.50
        self.assertEqual(modification_record.previous_purchased_class_hours, Decimal('5.50'))
        self.assertEqual(modification_record.updated_purchased_class_hours, Decimal('9.50'))

    def test_modification_record_reflects_correct_hours_calculation_for_refund(self):
        """
        Test that the updated_purchased_class_hours in the modification record
        correctly reflects the hours after a refund is deducted.
        """
        self.student.purchased_class_hours = Decimal('12.00')
        self.student.save()

        previous_hours = self.student.purchased_class_hours

        transaction = FreelanceTuitionTransactionRecord.objects.create(
            student_or_class=self.student,
            transaction_type='refund',
            class_hours_purchased_or_refunded=5
        )

        create_purchased_hours_modification_record_for_tuition_transaction(
            previous_hours_purchased=previous_hours,
            freelance_tuition_transaction_record=transaction
        )

        modification_record = PurchasedHoursModificationRecord.objects.get(
            tuition_transaction=transaction
        )

        # Updated hours should be 12.00 - 5.00 = 7.00
        self.assertEqual(modification_record.previous_purchased_class_hours, Decimal('12.00'))
        self.assertEqual(modification_record.updated_purchased_class_hours, Decimal('7.00'))

    def test_multiple_transactions_create_separate_modification_records(self):
        """
        Test that multiple transactions for the same student create
        separate modification records.
        """
        # First transaction
        previous_hours_1 = self.student.purchased_class_hours
        transaction_1 = FreelanceTuitionTransactionRecord.objects.create(
            student_or_class=self.student,
            transaction_type='payment',
            class_hours_purchased_or_refunded=3
        )
        create_purchased_hours_modification_record_for_tuition_transaction(
            previous_hours_purchased=previous_hours_1,
            freelance_tuition_transaction_record=transaction_1
        )

        # Refresh student object to get updated hours
        self.student.refresh_from_db()

        # Second transaction
        previous_hours_2 = self.student.purchased_class_hours
        transaction_2 = FreelanceTuitionTransactionRecord.objects.create(
            student_or_class=self.student,
            transaction_type='payment',
            class_hours_purchased_or_refunded=2
        )
        create_purchased_hours_modification_record_for_tuition_transaction(
            previous_hours_purchased=previous_hours_2,
            freelance_tuition_transaction_record=transaction_2
        )

        # Verify two modification records exist
        modification_records = PurchasedHoursModificationRecord.objects.filter(
            student_or_class=self.student
        )
        self.assertEqual(modification_records.count(), 2)

        # Verify the records have the correct previous/updated hours
        record_1 = modification_records.get(tuition_transaction=transaction_1)
        self.assertEqual(record_1.previous_purchased_class_hours, Decimal('10.00'))
        self.assertEqual(record_1.updated_purchased_class_hours, Decimal('13.00'))

        record_2 = modification_records.get(tuition_transaction=transaction_2)
        self.assertEqual(record_2.previous_purchased_class_hours, Decimal('13.00'))
        self.assertEqual(record_2.updated_purchased_class_hours, Decimal('15.00'))

    def test_modification_record_has_correct_student_reference(self):
        """
        Test that the modification record correctly references the student
        from the transaction, even when retrieved fresh from the database.
        """
        previous_hours = self.student.purchased_class_hours

        transaction = FreelanceTuitionTransactionRecord.objects.create(
            student_or_class=self.student,
            transaction_type='payment',
            class_hours_purchased_or_refunded=1
        )

        create_purchased_hours_modification_record_for_tuition_transaction(
            previous_hours_purchased=previous_hours,
            freelance_tuition_transaction_record=transaction
        )

        modification_record = PurchasedHoursModificationRecord.objects.get(
            tuition_transaction=transaction
        )

        # Verify the student_or_class reference matches
        self.assertEqual(modification_record.student_or_class.id, self.student.id)
        self.assertEqual(
            modification_record.student_or_class.student_or_class_name,
            'Alice Johnson'
        )

    def test_timestamp_is_auto_generated(self):
        """
        Test that the modification record has a timestamp that is
        automatically generated.
        """
        previous_hours = self.student.purchased_class_hours

        transaction = FreelanceTuitionTransactionRecord.objects.create(
            student_or_class=self.student,
            transaction_type='payment',
            class_hours_purchased_or_refunded=2
        )

        create_purchased_hours_modification_record_for_tuition_transaction(
            previous_hours_purchased=previous_hours,
            freelance_tuition_transaction_record=transaction
        )

        modification_record = PurchasedHoursModificationRecord.objects.get(
            tuition_transaction=transaction
        )

        # Verify timestamp exists and is not None
        self.assertIsNotNone(modification_record.time_stamp)

    def test_payment_with_zero_initial_hours(self):
        """
        Test creating a modification record when the student starts with
        zero purchased hours (edge case).
        """
        # Create a student with zero hours
        student_zero_hours = StudentOrClass.objects.create(
            student_or_class_name='Bob Zero',
            account_type='freelance',
            teacher=self.teacher_profile,
            purchased_class_hours=Decimal('0.00'),
            tuition_per_hour=1000
        )

        previous_hours = student_zero_hours.purchased_class_hours

        transaction = FreelanceTuitionTransactionRecord.objects.create(
            student_or_class=student_zero_hours,
            transaction_type='payment',
            class_hours_purchased_or_refunded=5
        )

        create_purchased_hours_modification_record_for_tuition_transaction(
            previous_hours_purchased=previous_hours,
            freelance_tuition_transaction_record=transaction
        )

        modification_record = PurchasedHoursModificationRecord.objects.get(
            tuition_transaction=transaction
        )

        self.assertEqual(modification_record.previous_purchased_class_hours, Decimal('0.00'))
        self.assertEqual(modification_record.updated_purchased_class_hours, Decimal('5.00'))

    def test_modification_type_matches_transaction_type(self):
        """
        Test that the modification_type field is correctly set based on
        the transaction_type.
        """
        # Test payment
        previous_hours = self.student.purchased_class_hours
        payment_transaction = FreelanceTuitionTransactionRecord.objects.create(
            student_or_class=self.student,
            transaction_type='payment',
            class_hours_purchased_or_refunded=3
        )

        create_purchased_hours_modification_record_for_tuition_transaction(
            previous_hours_purchased=previous_hours,
            freelance_tuition_transaction_record=payment_transaction
        )

        payment_record = PurchasedHoursModificationRecord.objects.get(
            tuition_transaction=payment_transaction
        )
        self.assertEqual(payment_record.modification_type, 'tuition_payment_add')

        # Refresh student
        self.student.refresh_from_db()
        previous_hours = self.student.purchased_class_hours

        # Test refund
        refund_transaction = FreelanceTuitionTransactionRecord.objects.create(
            student_or_class=self.student,
            transaction_type='refund',
            class_hours_purchased_or_refunded=2
        )

        create_purchased_hours_modification_record_for_tuition_transaction(
            previous_hours_purchased=previous_hours,
            freelance_tuition_transaction_record=refund_transaction
        )

        refund_record = PurchasedHoursModificationRecord.objects.get(
            tuition_transaction=refund_transaction
        )
        self.assertEqual(refund_record.modification_type, 'tuition_refund_deduct')
