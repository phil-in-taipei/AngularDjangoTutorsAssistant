from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date, time
from decimal import Decimal

from school.models import School
from student_account.models import StudentOrClass
from user_profiles.models import UserProfile
from class_scheduling.models import ScheduledClass


class ScheduledClassModelTests(TestCase):
    """Test the ScheduledClass Model"""

    def setUp(self):
        # Create test users and profiles
        self.test_user1 = get_user_model().objects.create_user(
            'teacher1',
            'password1'
        )
        self.teacher1_profile = UserProfile.objects.create(
            user=self.test_user1,
            contact_email="teacher1@gmx.com",
            surname="Smith",
            given_name="John"
        )

        self.test_user2 = get_user_model().objects.create_user(
            'teacher2',
            'password2'
        )
        self.teacher2_profile = UserProfile.objects.create(
            user=self.test_user2,
            contact_email="teacher2@gmx.com",
            surname="Johnson",
            given_name="Jane"
        )

        # Create test school
        self.test_school = School.objects.create(
            school_name="Test School",
            address_line_1="123 School St",
            address_line_2="Taipei, Taiwan",
            contact_phone="0987654321",
            scheduling_teacher=self.teacher1_profile
        )

        # Create test students
        self.freelance_student = StudentOrClass.objects.create(
            student_or_class_name="Alice Brown",
            account_type='freelance',
            teacher=self.teacher1_profile,
            purchased_class_hours=Decimal('15.00'),
            tuition_per_hour=1000
        )

        self.school_student = StudentOrClass.objects.create(
            student_or_class_name="Bob Wilson",
            account_type='school',
            school=self.test_school,
            teacher=self.teacher1_profile,
            tuition_per_hour=800
        )

        # Create test scheduled classes
        self.test_date = date(2024, 3, 15)
        self.scheduled_class1 = ScheduledClass.objects.create(
            student_or_class=self.freelance_student,
            teacher=self.teacher1_profile,
            date=self.test_date,
            start_time=time(9, 0),
            finish_time=time(10, 0),
            class_status='scheduled',
            teacher_notes="First class notes",
            class_content="Grammar lesson"
        )

        self.scheduled_class2 = ScheduledClass.objects.create(
            student_or_class=self.school_student,
            teacher=self.teacher1_profile,
            date=self.test_date,
            start_time=time(14, 0),
            finish_time=time(15, 30),
            class_status='completed',
            teacher_notes="Second class notes",
            class_content="Conversation practice"
        )

    def test_scheduled_class_fields(self):
        """Test the scheduled class fields"""
        print("Test the scheduled class fields")
        self.assertEqual(
            self.scheduled_class1.student_or_class,
            self.freelance_student
        )
        self.assertEqual(
            self.scheduled_class1.teacher,
            self.teacher1_profile
        )
        self.assertEqual(
            self.scheduled_class1.date,
            self.test_date
        )
        self.assertEqual(
            self.scheduled_class1.start_time,
            time(9, 0)
        )
        self.assertEqual(
            self.scheduled_class1.finish_time,
            time(10, 0)
        )
        self.assertEqual(
            self.scheduled_class1.class_status,
            'scheduled'
        )
        self.assertEqual(
            self.scheduled_class1.teacher_notes,
            'First class notes'
        )
        self.assertEqual(
            self.scheduled_class1.class_content,
            'Grammar lesson'
        )

    def test_scheduled_class_str(self):
        """Test the scheduled class model string representation"""
        print("Test the scheduled class string")
        expected_str = "{} on {} at {}-{} with {}".format(
            str(self.scheduled_class1.teacher).title(), self.scheduled_class1.date,
            self.scheduled_class1.start_time, self.scheduled_class1.finish_time,
            str(self.scheduled_class1.student_or_class).title()
        )
        #expected_str = f"John Smith on {self.test_date} at 09:00:00-10:00:00 with Alice Brown"
        self.assertEqual(str(self.scheduled_class1), expected_str)

    def test_default_values(self):
        """Test model default values"""
        print("Test default values")
        class_with_defaults = ScheduledClass.objects.create(
            student_or_class=self.freelance_student,
            teacher=self.teacher1_profile,
            date=date(2024, 3, 20),
            start_time=time(11, 0),
            finish_time=time(12, 0)
        )
        self.assertEqual(class_with_defaults.class_status, 'scheduled')
        self.assertEqual(class_with_defaults.teacher_notes, '')
        self.assertEqual(class_with_defaults.class_content, '')

    def test_ordering(self):
        """Test model ordering"""
        print("Test model ordering")
        # Create another class on a different date
        future_class = ScheduledClass.objects.create(
            student_or_class=self.freelance_student,
            teacher=self.teacher2_profile,
            date=date(2024, 3, 20),  # Later date
            start_time=time(8, 0),
            finish_time=time(9, 0)
        )

        # Create another class on same date, different teacher
        same_date_class = ScheduledClass.objects.create(
            student_or_class=self.school_student,
            teacher=self.teacher2_profile,
            date=self.test_date,
            start_time=time(16, 0),
            finish_time=time(17, 0)
        )

        all_classes = list(ScheduledClass.objects.all())

        # Should be ordered by: -date (desc), teacher, start_time
        # Future date first, then test_date
        self.assertEqual(all_classes[0], future_class)
        # Then same date classes, ordered by teacher surname (Johnson before Smith)
        self.assertEqual(all_classes[1], same_date_class)

    def test_already_booked_classes_during_date_and_time_overlap_start(self):
        """Test finding classes that overlap at start time"""
        print("Test overlap at start time")
        # Query for 8:30-9:30 (overlaps with 9:00-10:00 class)
        overlapping_classes = ScheduledClass.custom_query.already_booked_classes_during_date_and_time(
            self.test_date, time(8, 30), time(9, 30)
        )
        self.assertIn(self.scheduled_class1, overlapping_classes)
        self.assertNotIn(self.scheduled_class2, overlapping_classes)

    def test_already_booked_classes_during_date_and_time_overlap_end(self):
        """Test finding classes that overlap at end time"""
        print("Test overlap at end time")
        # Query for 9:30-10:30 (overlaps with 9:00-10:00 class)
        overlapping_classes = ScheduledClass.custom_query.already_booked_classes_during_date_and_time(
            self.test_date, time(9, 30), time(10, 30)
        )
        self.assertIn(self.scheduled_class1, overlapping_classes)
        self.assertNotIn(self.scheduled_class2, overlapping_classes)

    def test_already_booked_classes_during_date_and_time_completely_within(self):
        """Test finding classes when query time is completely within existing class"""
        print("Test query time within existing class")
        # Query for 9:15-9:45 (completely within 9:00-10:00 class)
        overlapping_classes = ScheduledClass.custom_query.already_booked_classes_during_date_and_time(
            self.test_date, time(9, 15), time(9, 45)
        )
        self.assertIn(self.scheduled_class1, overlapping_classes)

    def test_already_booked_classes_during_date_and_time_no_overlap(self):
        """Test finding classes with no time overlap"""
        print("Test no time overlap")
        # Query for 11:00-12:00 (no overlap with existing classes)
        overlapping_classes = ScheduledClass.custom_query.already_booked_classes_during_date_and_time(
            self.test_date, time(11, 0), time(12, 0)
        )
        self.assertEqual(len(overlapping_classes), 0)

    def test_already_booked_classes_during_date_and_time_different_date(self):
        """Test finding classes on different date"""
        print("Test different date")
        different_date = date(2024, 3, 16)
        overlapping_classes = ScheduledClass.custom_query.already_booked_classes_during_date_and_time(
            different_date, time(9, 0), time(10, 0)
        )
        self.assertEqual(len(overlapping_classes), 0)

    def test_student_already_booked_during_date_and_time_true(self):
        """Test student conflict detection - conflict exists"""
        print("Test student conflict exists")
        # Check if freelance_student has conflict at 9:30-10:30 (should conflict with 9:00-10:00)
        has_conflict = ScheduledClass.custom_query.student_or_class_already_booked_classes_during_date_and_time(
            self.test_date, time(9, 30), time(10, 30), self.freelance_student.id
        )
        self.assertTrue(has_conflict)

    def test_student_already_booked_during_date_and_time_false(self):
        """Test student conflict detection - no conflict"""
        print("Test student no conflict")
        # Check if freelance_student has conflict at 11:00-12:00 (should be free)
        has_conflict = ScheduledClass.custom_query.student_or_class_already_booked_classes_during_date_and_time(
            self.test_date, time(11, 0), time(12, 0), self.freelance_student.id
        )
        self.assertFalse(has_conflict)

    def test_student_already_booked_different_student(self):
        """Test student conflict detection - different student"""
        print("Test different student no conflict")
        # Check if school_student has conflict at 9:00-10:00 (freelance_student's time)
        has_conflict = ScheduledClass.custom_query.student_or_class_already_booked_classes_during_date_and_time(
            self.test_date, time(9, 0), time(10, 0), self.school_student.id
        )
        self.assertFalse(has_conflict)

    def test_teacher_already_booked_during_date_and_time_true(self):
        """Test teacher conflict detection - conflict exists"""
        print("Test teacher conflict exists")
        # Check if teacher1 has conflict at 8:30-9:30 (should conflict with 9:00-10:00 class)
        has_conflict = ScheduledClass.custom_query.teacher_already_booked_classes_during_date_and_time(
            self.test_date, time(8, 30), time(9, 30), self.teacher1_profile.id
        )
        self.assertTrue(has_conflict)

    def test_teacher_already_booked_during_date_and_time_false(self):
        """Test teacher conflict detection - no conflict"""
        print("Test teacher no conflict")
        # Check if teacher1 has conflict at 11:00-12:00 (should be free)
        has_conflict = ScheduledClass.custom_query.teacher_already_booked_classes_during_date_and_time(
            self.test_date, time(11, 0), time(12, 0), self.teacher1_profile.id
        )
        self.assertFalse(has_conflict)

    def test_teacher_already_booked_different_teacher(self):
        """Test teacher conflict detection - different teacher"""
        print("Test different teacher no conflict")
        # Check if teacher2 has conflict at 9:00-10:00 (teacher1's time)
        has_conflict = ScheduledClass.custom_query.teacher_already_booked_classes_during_date_and_time(
            self.test_date, time(9, 0), time(10, 0), self.teacher2_profile.id
        )
        self.assertFalse(has_conflict)

    def test_teacher_already_booked_classes_on_date(self):
        """Test getting all teacher's classes on a specific date"""
        print("Test teacher classes on date")
        teacher_classes = ScheduledClass.custom_query.teacher_already_booked_classes_on_date(
            self.test_date, self.teacher1_profile.id
        )

        # Should return both classes for teacher1 on test_date
        self.assertEqual(len(teacher_classes), 2)
        self.assertIn(self.scheduled_class1, teacher_classes)
        self.assertIn(self.scheduled_class2, teacher_classes)

    def test_teacher_already_booked_classes_on_date_different_teacher(self):
        """Test getting classes for teacher with no classes on date"""
        print("Test teacher no classes on date")
        teacher_classes = ScheduledClass.custom_query.teacher_already_booked_classes_on_date(
            self.test_date, self.teacher2_profile.id
        )

        # Should return empty queryset
        self.assertEqual(len(teacher_classes), 0)

    def test_teacher_already_booked_classes_on_date_different_date(self):
        """Test getting teacher's classes on date with no classes"""
        print("Test no classes on different date")
        different_date = date(2024, 3, 16)
        teacher_classes = ScheduledClass.custom_query.teacher_already_booked_classes_on_date(
            different_date, self.teacher1_profile.id
        )

        # Should return empty queryset
        self.assertEqual(len(teacher_classes), 0)

    def test_class_status_choices(self):
        """Test that all class status choices work"""
        print("Test class status choices")
        status_choices = [
            'scheduled', 'cancellation_request', 'cancelled',
            'completed', 'same_day_cancellation'
        ]

        for status in status_choices:
            test_class = ScheduledClass.objects.create(
                student_or_class=self.freelance_student,
                teacher=self.teacher1_profile,
                date=date(2024, 3, 25),
                start_time=time(10, 0),
                finish_time=time(11, 0),
                class_status=status
            )
            self.assertEqual(test_class.class_status, status)

    def test_edge_case_exact_time_boundaries(self):
            """Test exact time boundary conditions - API adjusts finish times by -1 minute"""
            print("Test exact time boundaries with API adjustment")
            # Create class from 10:00-10:59 (simulating API's -1 minute adjustment)
            boundary_class = ScheduledClass.objects.create(
                student_or_class=self.freelance_student,
                teacher=self.teacher2_profile,  # Different teacher to avoid other conflicts
                date=self.test_date,
                start_time=time(10, 0),
                finish_time=time(10, 59)  # API subtracts 1 minute before saving
            )

            # Query for exactly 11:00-12:00 (should not conflict with 10:00-10:59)
            no_conflict = ScheduledClass.custom_query.already_booked_classes_during_date_and_time(
                self.test_date, time(11, 0), time(12, 0)
            )
            self.assertNotIn(boundary_class, no_conflict)

            # Query for exactly 9:00-10:00 (WILL conflict because 10:00 start time falls within range)
            # This is correct behavior - prevents back-to-back scheduling conflicts
            has_boundary_conflict = ScheduledClass.custom_query.already_booked_classes_during_date_and_time(
                self.test_date, time(9, 0), time(10, 0)
            )
            self.assertIn(boundary_class, has_boundary_conflict)

            # Query for 9:00-9:59 (should not conflict with 10:00-10:59)
            no_conflict3 = ScheduledClass.custom_query.already_booked_classes_during_date_and_time(
                self.test_date, time(9, 0), time(9, 59)
            )
            self.assertNotIn(boundary_class, no_conflict3)

            # Query for 10:30-11:30 (should conflict with 10:00-10:59)
            has_overlap_conflict = ScheduledClass.custom_query.already_booked_classes_during_date_and_time(
                self.test_date, time(10, 30), time(11, 30)
            )
            self.assertIn(boundary_class, has_overlap_conflict)
