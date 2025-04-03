import { ScheduledClassModel } from "./scheduled-class.model";

export interface FreelanceTuitionTransactionRecordModel {
    id: number;
    transaction_amount: number;
    transaction_type: string;
    class_hours_purchased_or_refunded: number;
    student_or_class: number;
    time_stamp: string;
}


export interface PurchasedHoursModificationRecordModel {
    id: number;
    student_or_class: number;
    tuition_transaction: FreelanceTuitionTransactionRecordModel | undefined;
    modified_scheduled_class: ScheduledClassModel | undefined;
    modification_type: string;
    previous_purchased_class_hours: number;
    updated_purchased_class_hours: number;
    time_stamp: string;
}

export interface StudentOrClassAccountingReportModel {
    Name: string;
    Rate: number;
    Hours: number;
    Total: number; 
}

export interface SchoolAccountingReportModel {
    school_name: string;
    student_reports : StudentOrClassAccountingReportModel[]
    school_total: number;
}

export interface SchoolsAndFreelanceStudentsAccountingReport {
    classes_in_schools: SchoolAccountingReportModel[]
    freelance_students: StudentOrClassAccountingReportModel[]
}
