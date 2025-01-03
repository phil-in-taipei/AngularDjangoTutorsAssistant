import {createEntityAdapter, EntityAdapter, EntityState} from '@ngrx/entity';

import { StudentOrClassModel } from 'src/app/models/student-or-class.model';
import { 
    StudentOrClassActions, StudentOrClassActionTypes 
} from './student-or-class.actions';


function compareStudentsOrClassesByName(
    a: StudentOrClassModel, b: StudentOrClassModel) {
    const studentOrClassA = a.student_or_class_name;
    const studentOrClassB = b.student_or_class_name;

    let comparison = 0;
    if (studentOrClassA > studentOrClassB) {
      comparison = 1;
    } else if (studentOrClassA < studentOrClassB) {
      comparison = -1;
    }
    return comparison;
};

export interface StudentsOrClassesState extends EntityState<StudentOrClassModel> {
    fetchingStudentsOrClassesInProgress: boolean;
    errorMessage: string | undefined,
    studentsOrClassesLoaded: boolean,
    successMessage: string | undefined,
};

export const adapter: EntityAdapter<StudentOrClassModel> =
    createEntityAdapter<StudentOrClassModel>(
        { sortComparer: compareStudentsOrClassesByName }
    );

export const initialStudentsOrClassesState: StudentsOrClassesState = adapter.getInitialState({
    errorMessage: undefined,
    fetchingStudentsOrClassesInProgress: false,
    studentsOrClassesLoaded: false,
    successMessage: undefined
});

export function studentsOrClassesReducer(
    state = initialStudentsOrClassesState,
    action: StudentOrClassActions): StudentsOrClassesState {

    let reducerErrorMessage: string | undefined = undefined;
    let reducerSuccessMessage: string | undefined = undefined;

    switch(action.type) {

        case StudentOrClassActionTypes.StudentOrClassCreatedAdded:
            reducerErrorMessage = undefined;
            reducerSuccessMessage = 'New Student Or Class successfully submitted!';
            return adapter.addOne(action.payload.studentOrClass, {...state,
                errorMessage: reducerErrorMessage,
                successMessage: reducerSuccessMessage
            });

        case StudentOrClassActionTypes.StudentOrClassCreationCancelled:
            reducerErrorMessage = "Error submitting new Student Or Class!";
            reducerSuccessMessage = undefined;
            if (action.payload.err.error.message) {
                reducerErrorMessage = action.payload.err.error.message;
            }
            return {
                ...state,  successMessage: reducerSuccessMessage,
                errorMessage: reducerErrorMessage
            }

        case StudentOrClassActionTypes.StudentOrClassDeletionCancelled:
            reducerErrorMessage = "Error! Student Or Class Deletion Failed!";
            reducerSuccessMessage = undefined;
            if (action.payload.err.error.Error) {
                reducerErrorMessage = action.payload.err.error.Error;
            }
            return {
                ...state,  successMessage: reducerSuccessMessage,
                errorMessage: reducerErrorMessage
            }

        case StudentOrClassActionTypes.StudentOrClassDeletionSaved:
            reducerErrorMessage = undefined;
            reducerSuccessMessage = action.payload.message;
            return adapter.removeOne(action.payload.id,
                {
                    ...state,
                    errorMessage: undefined,
                    successMessage: reducerSuccessMessage
                }
            );

        case StudentOrClassActionTypes.StudentOrClassEditCancelled:
            reducerErrorMessage = "Error! Editing Student Or Class Failed!";
            reducerSuccessMessage = undefined;

            if (action.payload.err.error.Error) {
                reducerErrorMessage = action.payload.err.error.Error;
            }
            return {
                ...state,  successMessage: reducerSuccessMessage,
                errorMessage: reducerErrorMessage
            }

        case StudentOrClassActionTypes.StudentOrClassEditUpdated:
            reducerErrorMessage = undefined;
            reducerSuccessMessage = 'Student Or Class information edited!';
            return adapter.updateOne(action.payload.studentOrClass,
                {
                    ...state,
                    errorMessage: reducerErrorMessage,
                    successMessage: reducerSuccessMessage
                }
            );

        case StudentOrClassActionTypes.StudentsOrClassesMessagesCleared:
            reducerErrorMessage = undefined;
            reducerSuccessMessage = undefined;
            return {
                ...state,  successMessage: reducerSuccessMessage,
                errorMessage: reducerErrorMessage
            }

        case StudentOrClassActionTypes.StudentsOrClassesCleared:
            return initialStudentsOrClassesState;

        case StudentOrClassActionTypes.StudentsOrClassesLoaded:
            reducerErrorMessage = undefined;
            reducerSuccessMessage = undefined;

            return adapter.upsertMany(action.payload.studentsOrClasses, {...state,
                errorMessage: reducerErrorMessage,
                fetchingStudentsOrClassesInProgress: false,
                studentsOrClassesLoaded: true,
                successMessage: reducerSuccessMessage
            });

        case StudentOrClassActionTypes.StudentsOrClassesRequestCancelled:
            reducerErrorMessage = "Error fetching students or classes!";
            reducerSuccessMessage = undefined;

            if (action.payload.err.error.message) {
                reducerErrorMessage = action.payload.err.error.message;
            }
            return {
                 ...state,  errorMessage: reducerErrorMessage,
                 successMessage: reducerSuccessMessage,
            }

        case StudentOrClassActionTypes.StudentsOrClassesRequested:
            return {
                ...state,
                fetchingStudentsOrClassesInProgress: true
            }

        default: {
            return state
        }
    }

}

export const {
    selectAll,
    selectEntities,
    selectIds,
  } = adapter.getSelectors();
