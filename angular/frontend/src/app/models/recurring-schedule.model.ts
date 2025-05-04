import { ScheduledClassBatchDeletionDataModel } from "./scheduled-class.model";

export interface RecurringClassAppliedMonthlyCreateModel {
    scheduling_month: number;
    scheduling_year: number;
    recurring_class: number;
} 

export interface RecurringClassAppliedMonthlyModel {
    id: number;
    scheduling_month: number;
    scheduling_year: number;
    recurring_class: number;
    recurring_day_of_week: number;
    recurring_start_time: string;
}  
  
export interface RecurringClassAppliedMonthlyDeletionResponse {
    id: number;
    message: string;
    scheduled_class_batch_deletion_data: ScheduledClassBatchDeletionDataModel;
}

export interface RecurringClassCreateModel {
    recurring_start_time: string;
    recurring_finish_time: string;
    recurring_day_of_week: number;
    student_or_class: number;
    teacher: number;
}

export interface RecurringClassModel {
    id: number;
    recurring_start_time: string;
    recurring_finish_time: string;
    recurring_day_of_week: number;
    student_or_class: number;
    teacher: number;
    day_of_week_string: string;
}
