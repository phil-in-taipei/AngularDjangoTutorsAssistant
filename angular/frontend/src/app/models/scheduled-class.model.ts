import { StudentOrClassConfirmationModificationResponse } from "./student-or-class.model";

export interface CreateScheduledClassModel {
    date: string;
    start_time: string;
    finish_time: string;
    student_or_class: number;
    teacher: number;
}

export interface ModifyClassStatusModel {
    id: number;
    class_status: string;
    teacher_notes: string;
    class_content: string;
}

export interface ModifyClassStatusResponse {
    scheduled_class: ScheduledClassModel;
    student_or_class_update: StudentOrClassConfirmationModificationResponse;
}

export interface RescheduleClassModel {
    id: number;
    date: string;
    start_time: string;
    finish_time: string;
    student_or_class: number;
    teacher: number;
}

export interface ScheduledClassModel {
    id: number;
    date: string;
    start_time: string;
    finish_time: string;
    student_or_class: number;
    teacher: number;
    class_status: string;
    teacher_notes: string;
    class_content: string;
  }

