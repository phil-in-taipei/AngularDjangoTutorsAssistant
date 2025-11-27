import { 
    StudentsOrClassesState 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.reducers';
import { 
    studentsOrClassesData,
    deletionResponseSuccess, 
    studentOrClassConfirmationModificationResponse 
} from './student-or-class-data';
import { StudentOrClassModel } from 'src/app/models/student-or-class.model';


export const statePriorToStudentsOrClassesLoadRequest: StudentsOrClassesState = {
  ids: [],
  entities: {},
  deletionModeActivated: false,
  errorMessage: undefined,
  fetchingStudentsOrClassesInProgress: false,
  studentsOrClassesLoaded: false,
  successMessage: undefined
};

export const stateAfterStudentsOrClassesLoadRequest: StudentsOrClassesState = {
  ...statePriorToStudentsOrClassesLoadRequest,
  fetchingStudentsOrClassesInProgress: true
};

export const stateAfterStudentsOrClassesLoadSuccess: StudentsOrClassesState = {
  ids: studentsOrClassesData.map(s => s.id),
  entities: studentsOrClassesData.reduce((acc, studentOrClass) => {
    acc[studentOrClass.id] = studentOrClass;
    return acc;
  }, {} as { [id: number]: any }),
  deletionModeActivated: false,
  errorMessage: undefined,
  fetchingStudentsOrClassesInProgress: false,
  studentsOrClassesLoaded: true,
  successMessage: undefined
};

export const stateAfterStudentsOrClassesLoadFailure: StudentsOrClassesState = {
  ...statePriorToStudentsOrClassesLoadRequest,
  errorMessage: 'Error fetching students or classes!',
  fetchingStudentsOrClassesInProgress: false
};

export const stateAfterStudentOrClassCreatedAdded: StudentsOrClassesState = {
  ...stateAfterStudentsOrClassesLoadSuccess,
  ids: [...(stateAfterStudentsOrClassesLoadSuccess.ids as number[]), 4] as number[],
  entities: {
    ...stateAfterStudentsOrClassesLoadSuccess.entities,
    4: {
      id: 4,
      student_or_class_name: 'The New Student',
      account_type: 'individual',
      school: 2,
      comments: 'Newly added student record',
      purchased_class_hours: 5,
      tuition_per_hour: 30.0,
      account_id: 'STU003',
      slug: 'new-student',
      template_str: 'New Student - Individual Student'
    }
  },
  successMessage: 'New Student Or Class successfully submitted!',
  errorMessage: undefined
};


export const stateAfterStudentOrClassEditUpdated: StudentsOrClassesState = {
  ...stateAfterStudentsOrClassesLoadSuccess,
  entities: {
    ...stateAfterStudentsOrClassesLoadSuccess.entities,
    1: {
      ...(stateAfterStudentsOrClassesLoadSuccess.entities[1]!),
      student_or_class_name: 'John Updated Doe',
      comments: 'Updated student comments',
      tuition_per_hour: 35.0
    } as StudentOrClassModel
  },
  successMessage: 'Student Or Class information edited!',
  errorMessage: undefined
};

export const stateAfterStudentOrClassDeletionSaved: StudentsOrClassesState = {
  ...stateAfterStudentsOrClassesLoadSuccess,
  ids: (stateAfterStudentsOrClassesLoadSuccess.ids as number[]).filter(
    (id: number) => id !== deletionResponseSuccess.id
  ),
  entities: Object.keys(stateAfterStudentsOrClassesLoadSuccess.entities)
    .filter((id) => Number(id) !== deletionResponseSuccess.id)
    .reduce((acc, id) => {
      acc[Number(id)] = stateAfterStudentsOrClassesLoadSuccess.entities[Number(id)]!;
      return acc;
    }, {} as { [id: number]: any }),
  successMessage: deletionResponseSuccess.message,
  errorMessage: undefined
};


export const stateAfterStudentOrClassDeletionFailure: StudentsOrClassesState = {
  ...stateAfterStudentsOrClassesLoadSuccess,
  successMessage: undefined,
  errorMessage: 'Error! Student Or Class Deletion Failed!'
};

export const stateAfterFreelanceAccountPurchasedHoursSaved: StudentsOrClassesState = {
  ...stateAfterStudentsOrClassesLoadSuccess,
  entities: {
    ...stateAfterStudentsOrClassesLoadSuccess.entities,
    [studentOrClassConfirmationModificationResponse.id]: {
      ...stateAfterStudentsOrClassesLoadSuccess.entities[studentOrClassConfirmationModificationResponse.id],
      purchased_class_hours: studentOrClassConfirmationModificationResponse.changes.purchased_class_hours
    }
  },
  successMessage: `Total purchased hours: ${studentOrClassConfirmationModificationResponse.changes.purchased_class_hours}`,
  errorMessage: undefined
};

export const stateAfterFreelanceAccountRefundedHoursSaved: StudentsOrClassesState = {
  ...stateAfterStudentsOrClassesLoadSuccess,
  entities: {
    ...stateAfterStudentsOrClassesLoadSuccess.entities,
    [studentOrClassConfirmationModificationResponse.id]: {
      ...stateAfterStudentsOrClassesLoadSuccess.entities[studentOrClassConfirmationModificationResponse.id],
      purchased_class_hours: 0
    }
  },
  successMessage: 'Total purchased hours: 0',
  errorMessage: undefined
};

export const stateAfterMessagesCleared: StudentsOrClassesState = {
  ...stateAfterStudentsOrClassesLoadSuccess,
  errorMessage: undefined,
  successMessage: undefined
};

export const stateAfterStudentsOrClassesCleared: StudentsOrClassesState = {
  ids: [],
  entities: {},
  deletionModeActivated: false,
  errorMessage: undefined,
  fetchingStudentsOrClassesInProgress: false,
  studentsOrClassesLoaded: false,
  successMessage: undefined
};
