import { 
  ScheduledClassModel,
  StudentOrClassAttendanceRecordResponse 
} from 'src/app/models/scheduled-class.model';

export const pastClassesArray: ScheduledClassModel[] = [
  {
    id: 1,
    date: '2025-02-15',
    start_time: '14:00:00',
    finish_time: '15:00:00',
    student_or_class: 1,
    teacher: 1,
    class_status: 'confirmed',
    teacher_notes: 'Excellent progress on multiplication',
    class_content: 'Multiplication tables 1-10'
  },
  {
    id: 2,
    date: '2025-02-22',
    start_time: '14:00:00',
    finish_time: '15:00:00',
    student_or_class: 1,
    teacher: 1,
    class_status: 'confirmed',
    teacher_notes: 'Good work on division',
    class_content: 'Division basics'
  },
  {
    id: 3,
    date: '2025-03-01',
    start_time: '14:00:00',
    finish_time: '15:00:00',
    student_or_class: 1,
    teacher: 1,
    class_status: 'confirmed',
    teacher_notes: 'Reviewed fractions',
    class_content: 'Introduction to fractions'
  }
];

export const pastClassesArrayPage2: ScheduledClassModel[] = [
  {
    id: 4,
    date: '2025-03-08',
    start_time: '14:00:00',
    finish_time: '15:00:00',
    student_or_class: 1,
    teacher: 1,
    class_status: 'confirmed',
    teacher_notes: 'Practiced adding fractions',
    class_content: 'Adding and subtracting fractions'
  },
  {
    id: 5,
    date: '2025-03-15',
    start_time: '14:00:00',
    finish_time: '15:00:00',
    student_or_class: 1,
    teacher: 1,
    class_status: 'confirmed',
    teacher_notes: 'Quiz on fractions',
    class_content: 'Fractions review and assessment'
  },
  {
    id: 6,
    date: '2025-03-22',
    start_time: '14:00:00',
    finish_time: '15:00:00',
    student_or_class: 1,
    teacher: 1,
    class_status: 'confirmed',
    teacher_notes: 'Started decimals',
    class_content: 'Introduction to decimals'
  }
];

export const pastClassesArrayLastPage: ScheduledClassModel[] = [
  {
    id: 7,
    date: '2025-03-29',
    start_time: '14:00:00',
    finish_time: '15:00:00',
    student_or_class: 1,
    teacher: 1,
    class_status: 'confirmed',
    teacher_notes: 'Converting fractions to decimals',
    class_content: 'Decimal and fraction conversions'
  },
  {
    id: 8,
    date: '2025-04-05',
    start_time: '14:00:00',
    finish_time: '15:00:00',
    student_or_class: 1,
    teacher: 1,
    class_status: 'confirmed',
    teacher_notes: 'Great understanding of concepts',
    class_content: 'Percentages introduction'
  }
];

export const studentOrClassAttendanceRecordResponse: StudentOrClassAttendanceRecordResponse = {
  count: 8,
  next: 'http://example.com/api/scheduling/classes/student-or-class-attendance/1/?page=2',
  previous: null,
  results: pastClassesArray
};

export const studentOrClassAttendanceRecordResponsePage2: StudentOrClassAttendanceRecordResponse = {
  count: 8,
  next: 'http://example.com/api/scheduling/classes/student-or-class-attendance/1/?page=3',
  previous: 'http://example.com/api/scheduling/classes/student-or-class-attendance/1/?page=1',
  results: pastClassesArrayPage2
};

export const studentOrClassAttendanceRecordResponseLastPage: StudentOrClassAttendanceRecordResponse = {
  count: 8,
  next: null,
  previous: 'http://example.com/api/scheduling/classes/student-or-class-attendance/1/?page=2',
  results: pastClassesArrayLastPage
};

export const httpAttendanceRecordError1 = {
  detail: 'Invalid page.'
};