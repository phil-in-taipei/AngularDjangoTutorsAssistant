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
}  
  
export interface RecurringClassAppliedMonthlyDeletionResponse {
    message: string;
    obsolete_class_strings: string;
    obsolete_class_ids: number[];
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
