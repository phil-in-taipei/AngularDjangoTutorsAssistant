import { DeletionResponse } from 'src/app/models/deletion-response';
import { 
  RecurringClassAppliedMonthlyCreateModel,
  RecurringClassAppliedMonthlyModel,
  RecurringClassAppliedMonthlyDeletionResponse,
  RecurringClassCreateModel,
  RecurringClassModel
} from 'src/app/models/recurring-schedule.model';
import { ScheduledClassBatchDeletionDataModel } from 'src/app/models/scheduled-class.model';

export const recurringClassData: RecurringClassModel = {
  id: 1,
  recurring_start_time: '14:00:00',
  recurring_finish_time: '15:00:00',
  recurring_day_of_week: 1,
  student_or_class: 1,
  teacher: 1,
  day_of_week_string: 'Monday'
};

export const recurringClassesData: RecurringClassModel[] = [
  {
    id: 1,
    recurring_start_time: '14:00:00',
    recurring_finish_time: '15:00:00',
    recurring_day_of_week: 1,
    student_or_class: 1,
    teacher: 1,
    day_of_week_string: 'Monday'
  },
  {
    id: 2,
    recurring_start_time: '15:30:00',
    recurring_finish_time: '16:30:00',
    recurring_day_of_week: 3,
    student_or_class: 2,
    teacher: 1,
    day_of_week_string: 'Wednesday'
  },
  {
    id: 3,
    recurring_start_time: '10:00:00',
    recurring_finish_time: '11:00:00',
    recurring_day_of_week: 5,
    student_or_class: 3,
    teacher: 1,
    day_of_week_string: 'Friday'
  }
];

export const recurringClassCreateData: RecurringClassCreateModel = {
  recurring_start_time: '17:00:00',
  recurring_finish_time: '18:00:00',
  recurring_day_of_week: 6,
  student_or_class: 1,
  teacher: 1
};

export const recurringClassCreatedResponseData: RecurringClassModel = {
  id: 4,
  recurring_start_time: '17:00:00',
  recurring_finish_time: '18:00:00',
  recurring_day_of_week: 6,
  student_or_class: 1,
  teacher: 1,
  day_of_week_string: 'Saturday'
};

export const recurringClassAppliedMonthlyData: RecurringClassAppliedMonthlyModel = {
  id: 1,
  scheduling_month: 3,
  scheduling_year: 2025,
  recurring_class: 1,
  recurring_day_of_week: 1,
  recurring_start_time: '14:00:00'
};

export const recurringClassAppliedMonthliesData: RecurringClassAppliedMonthlyModel[] = [
  {
    id: 1,
    scheduling_month: 3,
    scheduling_year: 2025,
    recurring_class: 1,
    recurring_day_of_week: 1,
    recurring_start_time: '14:00:00'
  },
  {
    id: 2,
    scheduling_month: 3,
    scheduling_year: 2025,
    recurring_class: 2,
    recurring_day_of_week: 3,
    recurring_start_time: '15:30:00'
  },
  {
    id: 3,
    scheduling_month: 3,
    scheduling_year: 2025,
    recurring_class: 3,
    recurring_day_of_week: 5,
    recurring_start_time: '10:00:00'
  }
];

export const recurringClassAppliedMonthlyCreateData: RecurringClassAppliedMonthlyCreateModel = {
  scheduling_month: 3,
  scheduling_year: 2025,
  recurring_class: 1
};

export const newlyCreatedRecurringClassAppliedMonthlyData: RecurringClassAppliedMonthlyModel = {
  id: 4,
  scheduling_month: 3,
  scheduling_year: 2025,
  recurring_class: 1,
  recurring_start_time: '14:00:00',
  recurring_day_of_week: 1,
};

export const scheduledClassBatchDeletionData: ScheduledClassBatchDeletionDataModel = {
  obsolete_class_strings: 'Class 1, Class 2, Class 3, Class 4',
  obsolete_class_ids: [10, 11, 12, 13]
};

export const recurringClassAppliedMonthlyDeletionResponse: RecurringClassAppliedMonthlyDeletionResponse = {
  id: 3,
  message: 'Recurring Class Applied Monthly successfully deleted!',
  scheduled_class_batch_deletion_data: scheduledClassBatchDeletionData
};

export const deletionResponseSuccess: DeletionResponse = {
  id: 1,
  message: 'Recurring class deleted successfully'
};

export const httpRecurringClassCreateError1 = {
  recurring_start_time: ['Enter a valid time.'],
  recurring_finish_time: ['Finish time must be after start time.'],
  recurring_day_of_week: ['Select a valid choice. 7 is not one of the available choices.'],
  student_or_class: ['This field is required.']
};

export const httpRecurringClassAppliedMonthlyCreateError1 = {
  scheduling_month: ['Ensure this value is less than or equal to 12.'],
  scheduling_year: ['Enter a valid year.'],
  recurring_class: ['Invalid pk "999" - object does not exist.']
};

export const httpRecurringClassDeleteError1 = {
  detail: 'You do not have permission to perform this action.'
};

export const httpRecurringClassAppliedMonthlyDeleteError1 = {
  detail: 'You do not have permission to perform this action.'
};
