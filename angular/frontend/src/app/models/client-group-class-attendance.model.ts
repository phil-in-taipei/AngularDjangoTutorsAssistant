export interface GroupClassStudentAttendanceRecordModel {
  id: number;
  student_account: number;
  student_name: string;
  attendance_status: string;
  time_stamp: string;
}

export interface GroupClassMeetingRecordModel {
  id: number;
  scheduled_class: number;
  group_class: number;
  group_class_name: string;
  teacher_name: string;
  class_date: string;
  class_duration: number;
  time_stamp: string;
  student_attendance_records: GroupClassStudentAttendanceRecordModel[];
}

export interface GroupClassAttendanceSubmitModel {
  attendance_records: GroupClassStudentAttendanceRecordModel[];
}
