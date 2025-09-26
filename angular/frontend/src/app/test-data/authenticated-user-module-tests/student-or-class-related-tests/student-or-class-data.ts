import { DeletionResponse } from 'src/app/models/deletion-response';
import { 
  StudentOrClassCreateAndEditModel, 
  StudentOrClassEditModel,
  StudentOrClassModel,
  StudentOrClassConfirmationModificationResponse
} from 'src/app/models/student-or-class.model';

export const studentOrClassData: StudentOrClassModel = {
  id: 1,
  student_or_class_name: 'John Doe',
  account_type: 'individual',
  school: 1,
  comments: 'Test student comments',
  purchased_class_hours: 10,
  tuition_per_hour: 25.00,
  account_id: 'STU001',
  slug: 'john-doe',
  template_str: 'John Doe - Individual Student'
};

export const studentsOrClassesData: StudentOrClassModel[] = [
  {
    id: 1,
    student_or_class_name: 'John Doe',
    account_type: 'individual',
    school: 1,
    comments: 'Test student comments',
    purchased_class_hours: 10,
    tuition_per_hour: 25.00,
    account_id: 'STU001',
    slug: 'john-doe',
    template_str: 'John Doe - Individual Student'
  },
  {
    id: 2,
    student_or_class_name: 'Math Class Grade 5',
    account_type: 'class',
    school: 1,
    comments: 'Weekly math class for grade 5 students',
    purchased_class_hours: 20,
    tuition_per_hour: 30.00,
    account_id: 'CLS001',
    slug: 'math-class-grade-5',
    template_str: 'Math Class Grade 5 - Group Class'
  },
  {
    id: 3,
    student_or_class_name: 'Jane Smith',
    account_type: 'individual',
    school: undefined,
    comments: 'Private tutoring student',
    purchased_class_hours: undefined,
    tuition_per_hour: 40.00,
    account_id: 'STU002',
    slug: 'jane-smith',
    template_str: 'Jane Smith - Individual Student'
  }
];

export const studentOrClassCreateAndEditData: StudentOrClassCreateAndEditModel = {
  student_or_class_name: 'Updated Student Name',
  account_type: 'individual',
  school: 2,
  comments: 'Updated student comments',
  purchased_class_hours: 15,
  tuition_per_hour: 35.00
};

export const studentOrClassEditData: StudentOrClassEditModel = {
  student_or_class_name: 'Updated Student Name',
  comments: 'Updated student comments',
  tuition_per_hour: 35.00
};

export const deletionResponseSuccess: DeletionResponse = {
  id: 1,
  message: 'Student or class deleted successfully'
};

export const studentOrClassConfirmationModificationResponse: StudentOrClassConfirmationModificationResponse = {
  id: 1,
  changes: {
    purchased_class_hours: 15
  }
};

export const httpStudentOrClassCreateError1 = {
  student_or_class_name: ['This field is required.'],
  account_type: ['Select a valid choice. That choice is not one of the available choices.'],
  tuition_per_hour: ['Ensure this value is greater than or equal to 0.']
};

export const httpStudentOrClassEditError1 = {
  student_or_class_name: ['This field is required.'],
  tuition_per_hour: ['Ensure this value is greater than or equal to 0.']
};

export const httpStudentOrClassDeleteError1 = {
  detail: 'You do not have permission to perform this action.'
};