from datetime import date, datetime, timedelta
from django.db.models import Case, When, Value, IntegerField
from django.utils.timezone import make_aware, get_current_timezone

from class_scheduling.models import ScheduledClass
from class_scheduling.utils import determine_duration_of_class_time
from student_account.models import StudentOrClass
from .models import PurchasedHoursModificationRecord
 
from pprint import pprint


def format_date_range_same_month(dates):
    if not dates:
        return ""
    
    # Convert to date objects and sort
    date_objects = []
    for date in dates:
        if hasattr(date, 'date'):
            date_objects.append(date.date())
        else:
            date_objects.append(date)
    
    date_objects.sort()
    
    # Assuming all dates are in the same month
    first_date = date_objects[0]
    month = first_date.month
    
    # Get all days
    days = [date.day for date in date_objects]
    
    # Format: first day with month, rest just days
    if len(days) == 1:
        return f"{month}/{days[0]}"
    else:
        return f"{month}/{days[0]}, " + ", ".join(str(day) for day in days[1:])


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


def get_scheduled_classes_at_school_during_date_range(
        teacher, school, start_date, finish_date
):
    queryset = ScheduledClass.objects.filter(
                date__gte=start_date,
                date__lt=finish_date,
                teacher=teacher,
                student_or_class__school=school
        )
    return queryset.order_by(
        'student_or_class__school__school_name'
    )


def get_scheduled_classes_at_school_during_month_period(
        teacher, school, month, year
):
    start_date = date(int(year), int(month), 1)
    if int(month) == 12:
        finish_date = date(int(year) + 1, 1, 1)
    else:
        finish_date = date(int(year), int(month) + 1, 1)

    queryset = ScheduledClass.objects.filter(
                date__gte=start_date,
                date__lt=finish_date,
                teacher=teacher,
                student_or_class__school=school
        )
    return queryset.order_by(
        'student_or_class__school__school_name'
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


def organize_scheduled_classes(classes):
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


# this will prepare data for a school report in which 
# each student or classes' recorded classes will be sub-sorted by 
# duration of class time. This is to match the format of the accouning report
# at my current school
def organize_scheduled_classes_by_duration_for_emailed_report(organized_classes):
    print('inside next function')
    school_data = organized_classes['classes_in_schools'][0]
    reorganized_school_report = {
        "school_name": school_data['school_name'],
        "students_classes": []
    }
    students_classes = school_data['students_classes']
    for batch_of_classes in students_classes:
        reorganized_batch = {
            'student_or_class_name': batch_of_classes['student_or_class_name'],
            'scheduled_classes': {}
        }
        scheduled_classes = batch_of_classes['scheduled_classes']
        scheduled_classes_sorted_by_duration = {}
        for scheduled_class in scheduled_classes:
            duration_of_class_time = determine_duration_of_class_time(
                scheduled_class.start_time, scheduled_class.finish_time
            )
            if duration_of_class_time not in scheduled_classes_sorted_by_duration:
                scheduled_classes_sorted_by_duration[duration_of_class_time] = [scheduled_class]
            else: scheduled_classes_sorted_by_duration[duration_of_class_time].append(scheduled_class)
        reorganized_batch["scheduled_classes"] = scheduled_classes_sorted_by_duration
        reorganized_school_report['students_classes'].append(reorganized_batch)
    return reorganized_school_report


def organize_sorted_classes_by_durations_into_list_of_dicts_for_excel_sheet(
        classes_data_sorted_by_duration
    ):
    print("inside next function")
    print("this is the data:")
    #pprint(classes_data_sorted_by_duration)
    new_list_of_dicts = []
    for student_or_class_data in classes_data_sorted_by_duration['students_classes']:
        #print("iteration")
        
        #print(student_or_class_data)
        for k, v in student_or_class_data['scheduled_classes'].items():
            print(k, v)
            classes_with_payments = [
                scheduled_class 
                for scheduled_class in v
                if scheduled_class.class_status in ['same_day_cancellation', 'completed']
            ]
            print(classes_with_payments)

            if len(classes_with_payments) > 0:
                print(":::::These are the classes with payments::::::")
                pprint(classes_with_payments)
                print("This is the pay rate")
                print(classes_with_payments[0])
                pay_rate = classes_with_payments[0].student_or_class.tuition_per_hour
                print(pay_rate)
                #pay_per_class = pay_rate * k
                number_of_classes = len(classes_with_payments)
                total_hours = number_of_classes * k
                class_dates = [
                    scheduled_class.date 
                    for scheduled_class in classes_with_payments
                ]
                student_duration_data = {
                    "student_or_class_name": student_or_class_data['student_or_class_name'],
                    "scheduled_classes": format_date_range_same_month(class_dates),#classes_with_payments,
                    "pay rate": pay_rate,
                    "class_duration": k,
                    "total_hours": total_hours,
                    #"pay per class": pay_per_class,
                    "number_of_classes": number_of_classes,
                    "payment": total_hours * pay_rate
                }
                new_list_of_dicts.append(student_duration_data)
    return new_list_of_dicts


def process_school_classes(accounting_data, organized_classes_data):
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
                    "name": student_or_class.student_or_class_name,
                    "account_id": student_or_class.id,
                    "rate": student_or_class.tuition_per_hour,
                    "hours": hours,
                    "total": student_or_class.tuition_per_hour * hours
                }

                school_report["students_reports"].append(accounting_report)
        accounting_data["classes_in_schools"].append(school_report)
    return accounting_data


def process_freelance_students(accounting_data, organized_classes_data):
    for student_classes in organized_classes_data["freelance_students"]:
        scheduled_classes = student_classes["scheduled_classes"]

        # Get the student_or_class object
        if scheduled_classes:
            student_or_class = scheduled_classes[0].student_or_class
            hours = get_estimated_number_of_worked_hours(scheduled_classes)

            accounting_report = {
                "name": student_or_class.student_or_class_name,
                "account_id": student_or_class.id,
                "rate": student_or_class.tuition_per_hour,
                "hours": hours,
                "total": student_or_class.tuition_per_hour * hours
            }

            accounting_data["freelance_students"].append(accounting_report)
    return accounting_data


def generate_accounting_reports_for_classes_in_schools(
        organized_classes_data
):
    # Create a copy of the structure to avoid modifying the original
    accounting_data = {
        "classes_in_schools": [],
    }

    # Process school classes
    accounting_data_with_school_classes_reports = process_school_classes(
        accounting_data=accounting_data,
        organized_classes_data=organized_classes_data
    )
    return accounting_data_with_school_classes_reports


def generate_accounting_reports_for_classes_in_schools_and_freelance_teachers(
        organized_classes_data
):
    # Create a copy of the structure to avoid modifying the original
    accounting_data = {
        "classes_in_schools": [],
        "freelance_students": []
    }
    
    # Process school classes
    accounting_data_with_school_classes_reports = process_school_classes(
        accounting_data=accounting_data,
        organized_classes_data=organized_classes_data
    )

    # Process freelance students
    accounting_data_with_school_and_freelance_reports = process_freelance_students(
        accounting_data=accounting_data_with_school_classes_reports,
        organized_classes_data=organized_classes_data
    )
    
    return accounting_data_with_school_and_freelance_reports


def sort_accounting_reports_by_name(reports):
    """
    Sort a list of accounting report dictionaries by the 'name' field alphabetically.
    
    Args:
        reports (list): A list of accounting report dictionaries.
        
    Returns:
        list: The sorted list of accounting report dictionaries.
    """
    return sorted(reports, key=lambda report: report['name'])


def sort_school_reports_alphabetically(accounting_data):
    for school_report in accounting_data["classes_in_schools"]:
        # for each school, sort accounting reports for 
        # student/class alphabetically by name
        school_report['students_reports'] = sort_accounting_reports_by_name(
            reports=school_report["students_reports"]
        )
    return accounting_data


def sort_school_and_freelance_reports_alphabetically(accounting_data):
    #sort school accounting data alphabetically:
    accounting_data = sort_school_reports_alphabetically(
        accounting_data=accounting_data
    )
    #sort freelance reports alphabetically by name
    accounting_data["freelance_students"] = sort_accounting_reports_by_name(
        reports=accounting_data["freelance_students"]
    )
    return accounting_data


def calculate_school_totals(report):
    # Create a copy of the report to avoid modifying the original
    updated_report = report.copy()
    
    # Process each school in the classes_in_schools list
    for school_report in updated_report["classes_in_schools"]:
        # Initialize school_total
        school_total = 0
        
        # Sum up the Total values from all students in this school
        for student_report in school_report["students_reports"]:
            school_total += student_report["total"]
        
        # Add the school_total field to the school report
        school_report["school_total"] = school_total
    
    return updated_report


def calculate_overall_monthly_total(accounting_data):
    # Create a copy of the data to avoid modifying the original
    monthly_accounting_data = accounting_data.copy()
    
    # Initialize the overall total
    overall_monthly_total = 0
    
    # Sum up all school totals
    for school_report in monthly_accounting_data["classes_in_schools"]:
        overall_monthly_total += school_report["school_total"]
    
    # Sum up all freelance student totals
    for student_report in monthly_accounting_data["freelance_students"]:
        overall_monthly_total += student_report["total"]
    
    # Add the overall monthly total to the accounting data
    monthly_accounting_data["overall_monthly_total"] = overall_monthly_total
    
    return monthly_accounting_data


def generate_estimated_earnings_report(
        teacher, month, year
):
    classes_during_period = get_scheduled_classes_during_month_period(teacher, month, year)
    organized_classes_data = organize_scheduled_classes(classes=classes_during_period)

    basic_report = generate_accounting_reports_for_classes_in_schools_and_freelance_teachers(
        organized_classes_data=organized_classes_data
    )
    basic_report_sorted_alphabetically = sort_school_and_freelance_reports_alphabetically(
        accounting_data=basic_report
    )
    report_with_school_totals = calculate_school_totals(
        report=basic_report_sorted_alphabetically
    )
    return calculate_overall_monthly_total(accounting_data=report_with_school_totals)


def generate_estimated_earnings_report_for_single_school_within_date_range(
        teacher, school, start_date, finish_date
):
    classes_during_period = get_scheduled_classes_at_school_during_date_range(
        teacher=teacher, school=school, 
        start_date=start_date, finish_date=finish_date
    )
    organized_classes_data = organize_scheduled_classes(classes=classes_during_period)

    basic_report = generate_accounting_reports_for_classes_in_schools(
        organized_classes_data=organized_classes_data
    )
    basic_report_sorted_alphabetically = sort_school_reports_alphabetically(
        accounting_data=basic_report
    )
    report_with_school_totals = calculate_school_totals(
        report=basic_report_sorted_alphabetically
    )
    if len(report_with_school_totals['classes_in_schools']) > 0:
        return report_with_school_totals['classes_in_schools'][0]
    else:
        return {
            "school_name": school.school_name,
            "student_reports": [],
            "school_total": float(0)
        }


def generate_estimated_monthly_earnings_report_for_single_school(
        teacher, school, month, year
):
    classes_during_period = get_scheduled_classes_at_school_during_month_period(
        teacher, school, month, year
    )
    organized_classes_data = organize_scheduled_classes(classes=classes_during_period)

    basic_report = generate_accounting_reports_for_classes_in_schools(
        organized_classes_data=organized_classes_data
    )
    basic_report_sorted_alphabetically = sort_school_reports_alphabetically(
        accounting_data=basic_report
    )
    report_with_school_totals = calculate_school_totals(
        report=basic_report_sorted_alphabetically
    )
    if len(report_with_school_totals['classes_in_schools']) > 0:
        return report_with_school_totals['classes_in_schools'][0]
    else:
        return {
            "school_name": school.school_name,
            "student_reports": [],
            "school_total": float(0)
        }

# this will send an excel file with the monthly report formated
# so that each students'/class' data will be sorted by duration
# to match the accounting report format used at my current job
def generate_and_email_school_monthly_earnings_report_file(
        teacher, school, month, year
    ):
    print("*****Generating School Report*****")
    classes_during_period = get_scheduled_classes_at_school_during_month_period(
        teacher, school, month, year
    )
    organized_classes_data = organize_scheduled_classes(classes=classes_during_period)
    #pprint(organized_classes_data)
    print('this is inside the utils function')
    print("**********************************************************")
    classes_data_sorted_by_duration = organize_scheduled_classes_by_duration_for_emailed_report(
        organized_classes_data
    )
    print('___________________This is the data after sorting by duration________________')
    #pprint(classes_data_sorted_by_duration)
    classes_sorted_into_list_of_dicts_for_excel_prep = organize_sorted_classes_by_durations_into_list_of_dicts_for_excel_sheet(
        classes_data_sorted_by_duration
    )
    print("*******************************************************************")
    print("sorted_again by duration")
    print("**************************************************************")
    pprint(classes_sorted_into_list_of_dicts_for_excel_prep)
    return classes_sorted_into_list_of_dicts_for_excel_prep



