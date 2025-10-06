import { 
  FreelanceTuitionTransactionModel,
  FreelanceTuitionTransactionRecordModel,
  PurchasedHoursModificationRecordModel,
  SchoolAccountingReportModel,
  SchoolsAndFreelanceStudentsAccountingReportModel,
  StudentOrClassAccountingReportModel
} from 'src/app/models/accounting.model';
import { EmailSuccessModel } from 'src/app/models/email-status.model';
import { ScheduledClassModel } from 'src/app/models/scheduled-class.model';

export const freelanceTuitionTransactionData: FreelanceTuitionTransactionModel = {
  transaction_type: 'purchase',
  class_hours_purchased_or_refunded: 10,
  student_or_class: 3
};

export const freelanceTuitionTransactionRecordData: FreelanceTuitionTransactionRecordModel = {
  id: 1,
  transaction_amount: 250.00,
  transaction_type: 'purchase',
  class_hours_purchased_or_refunded: 10,
  student_or_class: 3,
  time_stamp: '2025-03-15T14:30:00Z'
};

export const freelanceTuitionTransactionRecordsData: FreelanceTuitionTransactionRecordModel[] = [
  {
    id: 1,
    transaction_amount: 250.00,
    transaction_type: 'purchase',
    class_hours_purchased_or_refunded: 10,
    student_or_class: 3,
    time_stamp: '2025-03-15T14:30:00Z'
  },
  {
    id: 2,
    transaction_amount: 400.00,
    transaction_type: 'purchase',
    class_hours_purchased_or_refunded: 10,
    student_or_class: 4,
    time_stamp: '2025-03-20T10:15:00Z'
  },
  {
    id: 3,
    transaction_amount: -50.00,
    transaction_type: 'refund',
    class_hours_purchased_or_refunded: 2,
    student_or_class: 3,
    time_stamp: '2025-03-25T16:45:00Z'
  }
];

export const scheduledClassForModification: ScheduledClassModel = {
  id: 10,
  date: '2025-03-15',
  start_time: '14:00:00',
  finish_time: '15:00:00',
  student_or_class: 1,
  teacher: 1,
  class_status: 'confirmed',
  teacher_notes: 'Great progress',
  class_content: 'Algebra review'
};

export const purchasedHoursModificationRecordsData: PurchasedHoursModificationRecordModel[] = [
  {
    id: 1,
    student_or_class: 1,
    tuition_transaction: {
      id: 5,
      transaction_amount: 500.00,
      transaction_type: 'purchase',
      class_hours_purchased_or_refunded: 20,
      student_or_class: 1,
      time_stamp: '2025-03-01T09:00:00Z'
    },
    modified_scheduled_class: undefined,
    modification_type: 'purchase',
    previous_purchased_class_hours: 0,
    updated_purchased_class_hours: 20,
    time_stamp: '2025-03-01T09:00:00Z'
  },
  {
    id: 2,
    student_or_class: 1,
    tuition_transaction: undefined,
    modified_scheduled_class: scheduledClassForModification,
    modification_type: 'class_confirmed',
    previous_purchased_class_hours: 20,
    updated_purchased_class_hours: 19,
    time_stamp: '2025-03-15T15:00:00Z'
  },
  {
    id: 3,
    student_or_class: 1,
    tuition_transaction: undefined,
    modified_scheduled_class: {
      id: 11,
      date: '2025-03-22',
      start_time: '14:00:00',
      finish_time: '15:00:00',
      student_or_class: 1,
      teacher: 1,
      class_status: 'confirmed',
      teacher_notes: 'Excellent work',
      class_content: 'Geometry basics'
    },
    modification_type: 'class_confirmed',
    previous_purchased_class_hours: 19,
    updated_purchased_class_hours: 18,
    time_stamp: '2025-03-22T15:00:00Z'
  },
  {
    id: 4,
    student_or_class: 1,
    tuition_transaction: {
      id: 6,
      transaction_amount: -25.00,
      transaction_type: 'refund',
      class_hours_purchased_or_refunded: 1,
      student_or_class: 1,
      time_stamp: '2025-03-28T11:30:00Z'
    },
    modified_scheduled_class: undefined,
    modification_type: 'refund',
    previous_purchased_class_hours: 18,
    updated_purchased_class_hours: 17,
    time_stamp: '2025-03-28T11:30:00Z'
  }
];

export const studentOrClassAccountingReport1: StudentOrClassAccountingReportModel = {
  name: 'John Doe',
  account_id: 1,
  rate: 25.00,
  hours: 4,
  total: 100.00
};

export const studentOrClassAccountingReport2: StudentOrClassAccountingReportModel = {
  name: 'Math Class Grade 5',
  account_id: 2,
  rate: 30.00,
  hours: 3,
  total: 90.00
};

export const studentOrClassAccountingReport3: StudentOrClassAccountingReportModel = {
  name: 'Jane Smith',
  account_id: 3,
  rate: 40.00,
  hours: 2.5,
  total: 100.00
};

export const studentOrClassAccountingReport4: StudentOrClassAccountingReportModel = {
  name: 'Science Tutoring Group',
  account_id: 4,
  rate: 35.00,
  hours: 3,
  total: 105.00
};

export const schoolAccountingReportData: SchoolAccountingReportModel = {
  school_name: 'Test Elementary School',
  students_reports: [
    studentOrClassAccountingReport1,
    studentOrClassAccountingReport2
  ],
  school_total: 190.00
};

export const schoolAccountingReportDateRangeData: SchoolAccountingReportModel = {
  school_name: 'Test Elementary School',
  students_reports: [
    {
      name: 'John Doe',
      account_id: 1,
      rate: 25.00,
      hours: 5,
      total: 125.00
    },
    {
      name: 'Math Class Grade 5',
      account_id: 2,
      rate: 30.00,
      hours: 4,
      total: 120.00
    }
  ],
  school_total: 245.00
};

export const schoolAccountingReportData2: SchoolAccountingReportModel = {
  school_name: 'Another Test School',
  students_reports: [
    {
      name: 'Alice Johnson',
      account_id: 5,
      rate: 30.00,
      hours: 3,
      total: 90.00
    },
    {
      name: 'Bob Williams',
      account_id: 6,
      rate: 28.00,
      hours: 2,
      total: 56.00
    }
  ],
  school_total: 146.00
};

export const schoolsAndFreelanceStudentsAccountingReportData: SchoolsAndFreelanceStudentsAccountingReportModel = {
  classes_in_schools: [
    schoolAccountingReportData,
    schoolAccountingReportData2
  ],
  freelance_students: [
    studentOrClassAccountingReport3,
    studentOrClassAccountingReport4
  ],
  overall_monthly_total: 541.00
};

export const emailSuccessResponse: EmailSuccessModel = {
  message: 'Accounting report email sent successfully'
};

export const httpFreelanceTuitionTransactionCreateError1 = {
  transaction_type: ['Select a valid choice. invalid_type is not one of the available choices.'],
  class_hours_purchased_or_refunded: ['Ensure this value is greater than 0.'],
  student_or_class: ['This field is required.']
};

export const httpFreelancePaymentsFetchError1 = {
  detail: 'Invalid month. Month must be between 1 and 12.'
};

export const httpSchoolAccountingReportError1 = {
  detail: 'Invalid month. Month must be between 1 and 12.'
};

export const httpEmailReportError1 = {
  detail: 'Failed to send email. Please try again later.'
};
