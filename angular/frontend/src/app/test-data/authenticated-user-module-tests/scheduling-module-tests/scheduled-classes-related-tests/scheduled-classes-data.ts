import { BatchDeletionResponse, DeletionResponse } from 'src/app/models/deletion-response';
import { 
  CreateScheduledClassModel,
  ModifyClassStatusModel,
  ModifyClassStatusResponse,
  RescheduleClassModel,
  ScheduledClassModel,
  ScheduledClassBatchDeletionDataModel
} from 'src/app/models/scheduled-class.model';
import { StudentOrClassConfirmationModificationResponse } from 'src/app/models/student-or-class.model';

export const scheduledClassData: ScheduledClassModel = {
  id: 1,
  date: '2025-03-15',
  start_time: '14:00:00',
  finish_time: '15:00:00',
  student_or_class: 1,
  teacher: 1,
  class_status: 'scheduled',
  teacher_notes: '',
  class_content: ''
};

export const scheduledClassesData: ScheduledClassModel[] = [
  {
    id: 1,
    date: '2025-03-15',
    start_time: '14:00:00',
    finish_time: '15:00:00',
    student_or_class: 1,
    teacher: 1,
    class_status: 'scheduled',
    teacher_notes: '',
    class_content: ''
  },
  {
    id: 2,
    date: '2025-03-15',
    start_time: '15:30:00',
    finish_time: '16:30:00',
    student_or_class: 2,
    teacher: 1,
    class_status: 'scheduled',
    teacher_notes: '',
    class_content: ''
  },
  {
    id: 3,
    date: '2025-03-15',
    start_time: '17:00:00',
    finish_time: '18:00:00',
    student_or_class: 3,
    teacher: 1,
    class_status: 'confirmed',
    teacher_notes: 'Great progress today',
    class_content: 'Algebra review'
  }
];

export const scheduledClassesByDateData: ScheduledClassModel[] = [
  {
    id: 1,
    date: '2025-03-15',
    start_time: '14:00:00',
    finish_time: '15:00:00',
    student_or_class: 1,
    teacher: 1,
    class_status: 'scheduled',
    teacher_notes: '',
    class_content: ''
  },
  {
    id: 2,
    date: '2025-03-15',
    start_time: '15:30:00',
    finish_time: '16:30:00',
    student_or_class: 2,
    teacher: 1,
    class_status: 'scheduled',
    teacher_notes: '',
    class_content: ''
  }
];

export const scheduledClassesByMonthData: ScheduledClassModel[] = [
  {
    id: 1,
    date: '2025-03-15',
    start_time: '14:00:00',
    finish_time: '15:00:00',
    student_or_class: 1,
    teacher: 1,
    class_status: 'scheduled',
    teacher_notes: '',
    class_content: ''
  },
  {
    id: 2,
    date: '2025-03-15',
    start_time: '15:30:00',
    finish_time: '16:30:00',
    student_or_class: 2,
    teacher: 1,
    class_status: 'scheduled',
    teacher_notes: '',
    class_content: ''
  },
  {
    id: 4,
    date: '2025-03-22',
    start_time: '14:00:00',
    finish_time: '15:00:00',
    student_or_class: 1,
    teacher: 1,
    class_status: 'scheduled',
    teacher_notes: '',
    class_content: ''
  },
  {
    id: 5,
    date: '2025-03-29',
    start_time: '14:00:00',
    finish_time: '15:00:00',
    student_or_class: 1,
    teacher: 1,
    class_status: 'scheduled',
    teacher_notes: '',
    class_content: ''
  }
];

export const unconfirmedStatusClassesData: ScheduledClassModel[] = [
  {
    id: 10,
    date: '2025-03-01',
    start_time: '14:00:00',
    finish_time: '15:00:00',
    student_or_class: 1,
    teacher: 1,
    class_status: 'scheduled',
    teacher_notes: '',
    class_content: ''
  },
  {
    id: 11,
    date: '2025-03-05',
    start_time: '15:30:00',
    finish_time: '16:30:00',
    student_or_class: 2,
    teacher: 1,
    class_status: 'scheduled',
    teacher_notes: '',
    class_content: ''
  }
];

export const createScheduledClassData: CreateScheduledClassModel = {
  date: '2025-03-20',
  start_time: '14:00:00',
  finish_time: '15:00:00',
  student_or_class: 1,
  teacher: 1
};

export const rescheduleClassData: RescheduleClassModel = {
  id: 1,
  date: '2025-03-21',
  start_time: '15:00:00',
  finish_time: '16:00:00',
  student_or_class: 1,
  teacher: 1
};

export const modifyClassStatusData: ModifyClassStatusModel = {
  id: 1,
  class_status: 'confirmed',
  teacher_notes: 'Excellent progress on multiplication',
  class_content: 'Multiplication tables 1-10'
};

export const studentOrClassConfirmationModification: StudentOrClassConfirmationModificationResponse = {
  id: 1,
  changes: {
    purchased_class_hours: 9
  }
};

export const modifyClassStatusResponse: ModifyClassStatusResponse = {
  scheduled_class: {
    id: 1,
    date: '2025-03-15',
    start_time: '14:00:00',
    finish_time: '15:00:00',
    student_or_class: 1,
    teacher: 1,
    class_status: 'confirmed',
    teacher_notes: 'Excellent progress on multiplication',
    class_content: 'Multiplication tables 1-10'
  },
  student_or_class_update: studentOrClassConfirmationModification
};

export const scheduledClassBatchDeletionData: ScheduledClassBatchDeletionDataModel = {
  obsolete_class_strings: 'Class 1, Class 2, Class 3',
  obsolete_class_ids: [1, 2, 3]
};

export const batchDeletionResponseSuccess: BatchDeletionResponse = {
  ids: [1, 2, 3],
  message: 'Successfully deleted 3 scheduled classes'
};

export const deletionResponseSuccess: DeletionResponse = {
  id: 1,
  message: 'Scheduled class deleted successfully'
};

export const httpScheduledClassCreateError1 = {
  date: ['This field is required.'],
  start_time: ['Enter a valid time.'],
  student_or_class: ['This field is required.']
};

export const httpScheduledClassRescheduleError1 = {
  date: ['Date cannot be in the past.'],
  start_time: ['Start time must be before finish time.']
};

export const httpModifyClassStatusError1 = {
  class_status: ['Select a valid choice. That choice is not one of the available choices.'],
  id: ['This field is required.']
};

export const httpBatchDeleteError1 = {
  obsolete_class_ids: ['This field is required.']
};

export const httpSingleDeleteError1 = {
  detail: 'You do not have permission to perform this action.'
};
