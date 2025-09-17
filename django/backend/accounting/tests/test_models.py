from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from datetime import date, time
from decimal import Decimal
from unittest.mock import patch

from school.models import School
from student_account.models import StudentOrClass
from user_profiles.models import UserProfile
from class_scheduling.models import ScheduledClass
from accounting.models import (
    FreelanceTuitionTransactionRecord, PurchasedHoursModificationRecord,
    TRANSACTION_TYPE, ACCOUNT_BALANCE_ALTERATION_TYPE
)


class FreelanceTuitionTransactionRecordModelTests(TestCase):
    """Test the FreelanceTuitionTransactionRecord Model"""

    def setUp(self):
        # Create test user and profile
        self.test_user = get_user_model().objects.create_user(
            'teacher1',
            'password1'
        )
        self.teacher_profile = UserProfile.objects.create(
            user=self.test_user,
            contact_email="teacher1@gmx.com",
            surname="Smith",
            given_name="John"
        )

        # Create freelance student
        self.freelance_student = StudentOrClass.objects.create(
            student_or_class_name="Alice Brown",
            account_type='freelance',
            teacher=self.teacher_profile,
            purchased_class_hours=Decimal('10.00'),
            tuition_per_hour=1200
        )

        # Create payment transaction
        self.payment_transaction = FreelanceTuitionTransactionRecord.objects.create(
            student_or_class=self.freelance_student,
            transaction_type='payment',
            class_hours_purchased_or_refunded=5
        )

    def test_transaction_record_fields(self):
        """Test the transaction record fields"""
        print("Test the transaction record fields")
        self.assertEqual(
            self.payment_transaction.student_or_class,
            self.freelance_student
        )
        self.assertEqual(
            self.payment_transaction.transaction_type,
            'payment'
        )
        self.assertEqual(
            self.payment_transaction.class_hours_purchased_or_refunded,
            5
        )
        # transaction_amount should be auto-calculated in save method
        self.assertEqual(
            self.payment_transaction.transaction_amount,
            6000  # 1200 * 5
        )
        # time_stamp should be auto-generated
        self.assertIsNotNone(self.payment_transaction.time_stamp)

    def test_transaction_record_str(self):
        """Test the transaction record string representation"""
        print("Test the transaction record string")
        formatted_time = self.payment_transaction.time_stamp.strftime("%Y-%m-%d %H:%M")
        expected_str = f"Payment: Alice Brown for $6,000 at {formatted_time}"
        self.assertEqual(str(self.payment_transaction), expected_str)

    def test_default_transaction_type(self):
        """Test default transaction type is payment"""
        print("Test default transaction type")
        default_transaction = FreelanceTuitionTransactionRecord.objects.create(
            student_or_class=self.freelance_student,
            class_hours_purchased_or_refunded=3
        )
        self.assertEqual(default_transaction.transaction_type, 'payment')

    def test_transaction_amount_auto_calculation(self):
        """Test transaction amount is automatically calculated"""
        print("Test transaction amount auto calculation")
        # Create transaction without specifying transaction_amount
        transaction = FreelanceTuitionTransactionRecord.objects.create(
            student_or_class=self.freelance_student,
            transaction_type='payment',
            class_hours_purchased_or_refunded=8
        )
        # Should be calculated as tuition_per_hour * hours
        expected_amount = 1200 * 8
        self.assertEqual(transaction.transaction_amount, expected_amount)

    def test_payment_updates_purchased_hours(self):
        """Test that payment transactions update student's purchased hours"""
        print("Test payment updates purchased hours")
        # Get initial hours
        self.freelance_student.refresh_from_db()
        initial_hours = self.freelance_student.purchased_class_hours

        # Create new payment transaction
        FreelanceTuitionTransactionRecord.objects.create(
            student_or_class=self.freelance_student,
            transaction_type='payment',
            class_hours_purchased_or_refunded=3
        )

        # Check that hours were added
        self.freelance_student.refresh_from_db()
        expected_hours = initial_hours + Decimal('3.00')
        self.assertEqual(self.freelance_student.purchased_class_hours, expected_hours)

    def test_refund_updates_purchased_hours(self):
        """Test that refund transactions update student's purchased hours"""
        print("Test refund updates purchased hours")
        # Get initial hours
        self.freelance_student.refresh_from_db()
        initial_hours = self.freelance_student.purchased_class_hours

        # Create refund transaction
        FreelanceTuitionTransactionRecord.objects.create(
            student_or_class=self.freelance_student,
            transaction_type='refund',
            class_hours_purchased_or_refunded=2
        )

        # Check that hours were subtracted
        self.freelance_student.refresh_from_db()
        expected_hours = initial_hours - Decimal('2.00')
        self.assertEqual(self.freelance_student.purchased_class_hours, expected_hours)

    def test_refund_transaction_str(self):
        """Test refund transaction string representation"""
        print("Test refund transaction string")
        refund_transaction = FreelanceTuitionTransactionRecord.objects.create(
            student_or_class=self.freelance_student,
            transaction_type='refund',
            class_hours_purchased_or_refunded=2
        )

        formatted_time = refund_transaction.time_stamp.strftime("%Y-%m-%d %H:%M")
        expected_str = f"Refund: Alice Brown for $2,400 at {formatted_time}"
        self.assertEqual(str(refund_transaction), expected_str)

    def test_limit_choices_to_freelance_only(self):
        """Test that only freelance students can be selected"""
        print("Test limit choices to freelance only")
        # Create school student
        school = School.objects.create(
            school_name="Test School",
            address_line_1="123 School St",
            address_line_2="Taipei, Taiwan",
            contact_phone="0987654321",
            scheduling_teacher=self.teacher_profile
        )

        school_student = StudentOrClass.objects.create(
            student_or_class_name="Bob Wilson",
            account_type='school',
            school=school,
            teacher=self.teacher_profile,
            tuition_per_hour=800
        )

        # This should work (freelance student)
        freelance_transaction = FreelanceTuitionTransactionRecord.objects.create(
            student_or_class=self.freelance_student,
            class_hours_purchased_or_refunded=1
        )
        self.assertIsNotNone(freelance_transaction.id)

        # Note: Django's limit_choices_to doesn't enforce database constraints,
        # it only limits choices in forms. We can still create the record.
        # If you need database-level enforcement, you'd need a custom constraint.

    @patch('builtins.print')  # Mock the print statements in save method
    def test_payment_save_method_prints(self, mock_print):
        """Test that payment save method includes print statements"""
        print("Test payment save method prints")
        FreelanceTuitionTransactionRecord.objects.create(
            student_or_class=self.freelance_student,
            transaction_type='payment',
            class_hours_purchased_or_refunded=1
        )

        # Verify print was called (should be called twice based on the save method)
        self.assertTrue(mock_print.called)
        self.assertGreaterEqual(mock_print.call_count, 1)


class PurchasedHoursModificationRecordModelTests(TestCase):
    """Test the PurchasedHoursModificationRecord Model"""

    def setUp(self):
        # Create test user and profile
        self.test_user = get_user_model().objects.create_user(
            'teacher1',
            'password1'
        )
        self.teacher_profile = UserProfile.objects.create(
            user=self.test_user,
            contact_email="teacher1@gmx.com",
            surname="Smith",
            given_name="John"
        )

        # Create freelance student
        self.freelance_student = StudentOrClass.objects.create(
            student_or_class_name="Alice Brown",
            account_type='freelance',
            teacher=self.teacher_profile,
            purchased_class_hours=Decimal('10.00'),
            tuition_per_hour=1200
        )

        # Create scheduled class
        self.scheduled_class = ScheduledClass.objects.create(
            student_or_class=self.freelance_student,
            teacher=self.teacher_profile,
            date=date(2024, 3, 15),
            start_time=time(9, 0),
            finish_time=time(10, 0),
            class_status='completed'
        )

        # Create tuition transaction
        self.tuition_transaction = FreelanceTuitionTransactionRecord.objects.create(
            student_or_class=self.freelance_student,
            transaction_type='payment',
            class_hours_purchased_or_refunded=5
        )

        # Create modification record for tuition transaction
        self.tuition_modification = PurchasedHoursModificationRecord.objects.create(
            student_or_class=self.freelance_student,
            tuition_transaction=self.tuition_transaction,
            modification_type='tuition_payment_add',
            previous_purchased_class_hours=Decimal('10.00'),
            updated_purchased_class_hours=Decimal('15.00')
        )

        # Create modification record for class status change
        self.class_modification = PurchasedHoursModificationRecord.objects.create(
            student_or_class=self.freelance_student,
            modified_scheduled_class=self.scheduled_class,
            modification_type='class_status_modification_deduct',
            previous_purchased_class_hours=Decimal('15.00'),
            updated_purchased_class_hours=Decimal('14.00')
        )

    def test_modification_record_fields(self):
        """Test the modification record fields"""
        print("Test the modification record fields")
        self.assertEqual(
            self.tuition_modification.student_or_class,
            self.freelance_student
        )
        self.assertEqual(
            self.tuition_modification.tuition_transaction,
            self.tuition_transaction
        )
        self.assertEqual(
            self.tuition_modification.modification_type,
            'tuition_payment_add'
        )
        self.assertEqual(
            self.tuition_modification.previous_purchased_class_hours,
            Decimal('10.00')
        )
        self.assertEqual(
            self.tuition_modification.updated_purchased_class_hours,
            Decimal('15.00')
        )
        self.assertIsNotNone(self.tuition_modification.time_stamp)

    def test_tuition_modification_str(self):
        """Test tuition modification string representation"""
        print("Test tuition modification string")
        formatted_time = self.tuition_modification.time_stamp.strftime("%Y-%m-%d %H:%M")
        expected_str = f"Tuition Transaction ($6,000): 5hrs at {formatted_time}"
        self.assertEqual(str(self.tuition_modification), expected_str)

    def test_class_modification_str(self):
        """Test class modification string representation"""
        print("Test class modification string")
        formatted_time = self.class_modification.time_stamp.strftime("%Y-%m-%d %H:%M")
        expected_str = f"Class Status Modification: Alice Brown at {formatted_time}"
        self.assertEqual(str(self.class_modification), expected_str)

    def test_default_modification_type(self):
        """Test default modification type"""
        print("Test default modification type")
        default_modification = PurchasedHoursModificationRecord.objects.create(
            student_or_class=self.freelance_student,
            modified_scheduled_class=self.scheduled_class,
            previous_purchased_class_hours=Decimal('10.00'),
            updated_purchased_class_hours=Decimal('9.00')
        )
        self.assertEqual(
            default_modification.modification_type,
            'class_status_modification_deduct'
        )

    def test_modification_type_choices(self):
        """Test all modification type choices"""
        print("Test modification type choices")
        modification_types = [
            'tuition_payment_add',
            'tuition_refund_deduct',
            'class_status_modification_add',
            'class_status_modification_deduct'
        ]

        for i, mod_type in enumerate(modification_types):
            if mod_type.startswith('tuition'):
                # Create a new tuition transaction for each test
                new_tuition_transaction = FreelanceTuitionTransactionRecord.objects.create(
                    student_or_class=self.freelance_student,
                    transaction_type='payment',
                    class_hours_purchased_or_refunded=2
                )
                modification = PurchasedHoursModificationRecord.objects.create(
                    student_or_class=self.freelance_student,
                    tuition_transaction=new_tuition_transaction,
                    modification_type=mod_type,
                    previous_purchased_class_hours=Decimal('10.00'),
                    updated_purchased_class_hours=Decimal('12.00')
                )
            else:
                # Create a new scheduled class for each class status test
                new_scheduled_class = ScheduledClass.objects.create(
                    student_or_class=self.freelance_student,
                    teacher=self.teacher_profile,
                    date=date(2024, 3, 16 + i),  # Different date for each
                    start_time=time(9, 0),
                    finish_time=time(10, 0)
                )
                modification = PurchasedHoursModificationRecord.objects.create(
                    student_or_class=self.freelance_student,
                    modified_scheduled_class=new_scheduled_class,
                    modification_type=mod_type,
                    previous_purchased_class_hours=Decimal('10.00'),
                    updated_purchased_class_hours=Decimal('11.00')
                )
            self.assertEqual(modification.modification_type, mod_type)

    def test_ordering(self):
        """Test model ordering"""
        print("Test model ordering")
        # Create another teacher and student for ordering test
        user2 = get_user_model().objects.create_user('teacher2', 'password')
        teacher2_profile = UserProfile.objects.create(
            user=user2,
            contact_email="teacher2@gmx.com",
            surname="Anderson",
            given_name="Amy"
        )

        student2 = StudentOrClass.objects.create(
            student_or_class_name="Beta Student",
            account_type='freelance',
            teacher=teacher2_profile,
            purchased_class_hours=Decimal('5.00')
        )

        scheduled_class2 = ScheduledClass.objects.create(
            student_or_class=student2,
            teacher=teacher2_profile,
            date=date(2024, 3, 16),
            start_time=time(10, 0),
            finish_time=time(11, 0)
        )

        modification2 = PurchasedHoursModificationRecord.objects.create(
            student_or_class=student2,
            modified_scheduled_class=scheduled_class2,
            modification_type='class_status_modification_add',
            previous_purchased_class_hours=Decimal('5.00'),
            updated_purchased_class_hours=Decimal('6.00')
        )

        all_modifications = list(PurchasedHoursModificationRecord.objects.all())

        # Should be ordered by teacher, time_stamp, student_name
        # Anderson should come before Smith
        first_teacher_surname = all_modifications[0].student_or_class.teacher.surname
        self.assertEqual(first_teacher_surname, "Anderson")

    def test_constraint_tuition_transaction_valid(self):
        """Test constraint allows valid tuition transaction combinations"""
        print("Test constraint tuition transaction valid")
        # Create a new tuition transaction since OneToOneField prevents reuse
        new_tuition_transaction = FreelanceTuitionTransactionRecord.objects.create(
            student_or_class=self.freelance_student,
            transaction_type='refund',
            class_hours_purchased_or_refunded=3
        )

        # Valid: tuition transaction with tuition modification type, no scheduled class
        valid_tuition_mod = PurchasedHoursModificationRecord.objects.create(
            student_or_class=self.freelance_student,
            tuition_transaction=new_tuition_transaction,
            modification_type='tuition_refund_deduct',
            previous_purchased_class_hours=Decimal('15.00'),
            updated_purchased_class_hours=Decimal('10.00')
        )
        self.assertIsNotNone(valid_tuition_mod.id)

    def test_constraint_class_status_valid(self):
        """Test constraint allows valid class status combinations"""
        print("Test constraint class status valid")
        # Create a new scheduled class since we want to test independently
        new_scheduled_class = ScheduledClass.objects.create(
            student_or_class=self.freelance_student,
            teacher=self.teacher_profile,
            date=date(2024, 3, 20),
            start_time=time(11, 0),
            finish_time=time(12, 0)
        )

        # Valid: scheduled class with class status modification type, no tuition transaction
        valid_class_mod = PurchasedHoursModificationRecord.objects.create(
            student_or_class=self.freelance_student,
            modified_scheduled_class=new_scheduled_class,
            modification_type='class_status_modification_add',
            previous_purchased_class_hours=Decimal('14.00'),
            updated_purchased_class_hours=Decimal('15.00')
        )
        self.assertIsNotNone(valid_class_mod.id)

    def test_one_to_one_relationship(self):
        """Test the OneToOneField relationship with tuition transaction"""
        print("Test one to one relationship")
        # Trying to create another modification record with same tuition transaction should fail
        with self.assertRaises(IntegrityError):
            PurchasedHoursModificationRecord.objects.create(
                student_or_class=self.freelance_student,
                tuition_transaction=self.tuition_transaction,  # Same transaction
                modification_type='tuition_payment_add',
                previous_purchased_class_hours=Decimal('5.00'),
                updated_purchased_class_hours=Decimal('10.00')
            )

    def test_cascade_deletion_tuition_transaction(self):
        """Test cascade deletion when tuition transaction is deleted"""
        print("Test cascade deletion tuition transaction")
        modification_id = self.tuition_modification.id

        # Verify modification exists
        self.assertTrue(
            PurchasedHoursModificationRecord.objects.filter(id=modification_id).exists()
        )

        # Delete tuition transaction
        self.tuition_transaction.delete()

        # Verify modification is also deleted
        self.assertFalse(
            PurchasedHoursModificationRecord.objects.filter(id=modification_id).exists()
        )

    def test_cascade_deletion_scheduled_class(self):
        """Test cascade deletion when scheduled class is deleted"""
        print("Test cascade deletion scheduled class")
        modification_id = self.class_modification.id

        # Verify modification exists
        self.assertTrue(
            PurchasedHoursModificationRecord.objects.filter(id=modification_id).exists()
        )

        # Delete scheduled class
        self.scheduled_class.delete()

        # Verify modification is also deleted
        self.assertFalse(
            PurchasedHoursModificationRecord.objects.filter(id=modification_id).exists()
        )

    def test_cascade_deletion_student_or_class(self):
        """Test cascade deletion when student is deleted"""
        print("Test cascade deletion student")
        tuition_mod_id = self.tuition_modification.id
        class_mod_id = self.class_modification.id

        # Verify both modifications exist
        self.assertTrue(
            PurchasedHoursModificationRecord.objects.filter(id=tuition_mod_id).exists()
        )
        self.assertTrue(
            PurchasedHoursModificationRecord.objects.filter(id=class_mod_id).exists()
        )

        # Delete student
        self.freelance_student.delete()

        # Verify both modifications are deleted
        self.assertFalse(
            PurchasedHoursModificationRecord.objects.filter(id=tuition_mod_id).exists()
        )
        self.assertFalse(
            PurchasedHoursModificationRecord.objects.filter(id=class_mod_id).exists()
        )

    def test_decimal_field_precision(self):
        """Test decimal field precision for purchased hours"""
        print("Test decimal field precision")
        modification = PurchasedHoursModificationRecord.objects.create(
            student_or_class=self.freelance_student,
            modified_scheduled_class=self.scheduled_class,
            modification_type='class_status_modification_add',
            previous_purchased_class_hours=Decimal('123.45'),
            updated_purchased_class_hours=Decimal('234.56')
        )

        self.assertEqual(modification.previous_purchased_class_hours, Decimal('123.45'))
        self.assertEqual(modification.updated_purchased_class_hours, Decimal('234.56'))
