from datetime import date, datetime, timedelta
from django.db.models import Case, When, Value, IntegerField
from django.utils.timezone import make_aware, get_current_timezone

from class_scheduling.models import ScheduledClass
from class_scheduling.utils import determine_duration_of_class_time
from student_account.models import StudentOrClass
from .models import PurchasedHoursModificationRecord
 
from pprint import pprint


def create_purchased_hours_modification_record_for_tuition_transaction(
        previous_hours_purchased, freelance_tuition_transaction_record,
):
    if freelance_tuition_transaction_record.transaction_type == "payment":
        modification_type = "tuition_payment_add"
    else:
        modification_type = "tuition_refund_deduct"
    student_or_class=StudentOrClass.objects.get(
        id=freelance_tuition_transaction_record.student_or_class.id
    )
    PurchasedHoursModificationRecord.objects.create(
        student_or_class=student_or_class,
        tuition_transaction=freelance_tuition_transaction_record,
        modification_type=modification_type,
        previous_purchased_class_hours=previous_hours_purchased,
        updated_purchased_class_hours=student_or_class.purchased_class_hours
    )
    print("----------------------------------------------------------------------")
    print(F"These are the previous hours purchased: {previous_hours_purchased}")
    print("----------------------------------------------------------------------")
    print(F"These are the updated hours purchased: {student_or_class.purchased_class_hours}")
    print("----------------------------------------------------------------------")


def create_timestamps_for_beginning_and_end_of_month_and_year(month: int, year: int) -> dict:
    """
    Generate timestamps for the beginning and end of a specific month and year.
    
    Args:
        month (int): The month (1-12)
        year (int): The year
    
    Returns:
        dict: A dictionary with 'start' and 'end' keys containing timestamps
    
    Note: 
    - Uses Django's make_aware to ensure timezone-aware timestamps
    - Assumes the current system timezone (can be modified if needed)
    """
    start_of_month = datetime(year, month, 1, 0, 0, 0)
    
    if month == 12:
        # For December, next month is January of the next year
        end_of_month = datetime(year, month, 31, 23, 59, 59)
    else:
        # For other months, use the day before the first day of the next month
        next_month_first_day = datetime(year, month + 1, 1)
        end_of_month = next_month_first_day - timedelta(seconds=1)
    
    # Make timestamps timezone-aware
    start_timestamp = make_aware(start_of_month, get_current_timezone())
    end_timestamp = make_aware(end_of_month, get_current_timezone())
    
    return {
        'start': start_timestamp,
        'end': end_timestamp
    }


def get_scheduled_classes_during_month_period(
        teacher, month, year
):
    start_date = date(int(year), int(month), 1)
    if int(month) == 12:
        finish_date = date(int(year) + 1, 1, 1)
    else:
        finish_date = date(int(year), int(month) + 1, 1)

    queryset = ScheduledClass.objects.filter(
                date__gte=start_date,
                date__lt=finish_date,
                teacher=teacher
        )
    return queryset.order_by(
        Case(
            When(student_or_class__school__isnull=True, then=Value(1)),
            default=Value(0),
            output_field=IntegerField()
        ),
        'student_or_class__school__school_name'  # Then by school name
    )


def get_estimated_number_of_worked_hours(scheduled_classes):
    number_of_worked_hours = 0
    for scheduled_class in scheduled_classes:
        if (
                scheduled_class.class_status == "completed"
                or scheduled_class.class_status == "same_day_cancellation"
        ):
            number_of_worked_hours += determine_duration_of_class_time(
                scheduled_class.start_time, scheduled_class.finish_time
            )
    return number_of_worked_hours


def organize_scheduled_classes(teacher, month, year):
    # Get all classes for the specified month and year
    classes = get_scheduled_classes_during_month_period(teacher, month, year)
    
    # Initialize the main dictionary structure
    organized_data = {
        "classes_in_schools": [],
        "freelance_students": []
    }
    
    # Group classes by school/freelance first
    school_classes = {}
    freelance_classes = {}
    
    for scheduled_class in classes:
        student_class = scheduled_class.student_or_class
        
        # Check if this is a school class or freelance student
        if student_class.school:
            # This is a school class
            school_name = student_class.school.school_name
            
            # Initialize school if not already in dictionary
            if school_name not in school_classes:
                school_classes[school_name] = {}
                
            # Initialize student/class if not already in this school
            student_name = student_class.student_or_class_name
            if student_name not in school_classes[school_name]:
                school_classes[school_name][student_name] = []
                
            # Add class to this student's list
            school_classes[school_name][student_name].append(scheduled_class)
        else:
            # This is a freelance student
            student_name = student_class.student_or_class_name
            
            # Initialize student if not already in dictionary
            if student_name not in freelance_classes:
                freelance_classes[student_name] = []
                
            # Add class to this student's list
            freelance_classes[student_name].append(scheduled_class)
    
    # Convert school data to the required format
    for school_name, students in school_classes.items():
        school_data = {
            "school_name": school_name,
            "students_classes": []
        }
        
        for student_name, scheduled_classes in students.items():
            school_data["students_classes"].append({
                "student_or_class_name": student_name,
                "scheduled_classes": scheduled_classes
            })
        
        organized_data["classes_in_schools"].append(school_data)
    
    # Convert freelance data to the required format
    for student_name, scheduled_classes in freelance_classes.items():
        organized_data["freelance_students"].append({
            "student_or_class_name": student_name,
            "scheduled_classes": scheduled_classes
        })
    
    return organized_data


def generate_accounting_reports(organized_classes_data):
    # Create a copy of the structure to avoid modifying the original
    accounting_data = {
        "classes_in_schools": [],
        "freelance_students": []
    }
    
    # Process school classes
    for school_data in organized_classes_data["classes_in_schools"]:
        school_report = {
            "school_name": school_data["school_name"],
            "students_reports": []
        }
        
        for student_classes in school_data["students_classes"]:
            scheduled_classes = student_classes["scheduled_classes"]
            
            # Get the student_or_class object (assuming the first class has it)
            if scheduled_classes:
                student_or_class = scheduled_classes[0].student_or_class
                hours = get_estimated_number_of_worked_hours(scheduled_classes)
                
                accounting_report = {
                    "Name": student_or_class.student_or_class_name,
                    "Rate": student_or_class.tuition_per_hour,
                    "Hours": hours,
                    "Total": student_or_class.tuition_per_hour * hours
                }
                
                school_report["students_reports"].append(accounting_report)
        
        accounting_data["classes_in_schools"].append(school_report)
    
    # Process freelance students
    for student_classes in organized_classes_data["freelance_students"]:
        scheduled_classes = student_classes["scheduled_classes"]
        
        # Get the student_or_class object
        if scheduled_classes:
            student_or_class = scheduled_classes[0].student_or_class
            hours = get_estimated_number_of_worked_hours(scheduled_classes)
            
            accounting_report = {
                "Name": student_or_class.student_or_class_name,
                "Rate": student_or_class.tuition_per_hour,
                "Hours": hours,
                "Total": student_or_class.tuition_per_hour * hours
            }
            
            accounting_data["freelance_students"].append(accounting_report)
    
    return accounting_data


def generate_estimated_earnings_report(
        teacher, month, year
):
    #sorted_classes = get_scheduled_classes_during_month_period(
    #    teacher, month, year
    #)
    sorted_classes = organize_scheduled_classes(teacher, month, year)
    print("************This is the query result************")
    pprint(sorted_classes)
    generate_accounting_reports(sorted_classes)
    return generate_accounting_reports(sorted_classes)


