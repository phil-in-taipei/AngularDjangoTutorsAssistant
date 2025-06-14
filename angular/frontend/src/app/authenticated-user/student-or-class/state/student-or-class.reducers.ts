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
    deletionModeActivated: boolean;
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
    deletionModeActivated: false,
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

    switch(action.type) { //FreelanceAccountPurchasedHoursSaved

        case StudentOrClassActionTypes.FreelanceAccountPurchasedHoursSaved:
            // clone with spead operator and add the new value before saving the clone
            let studentOrClass:StudentOrClassModel = { ...action.payload.studentOrClass }
            if (
                studentOrClass.purchased_class_hours !== null && 
                studentOrClass.purchased_class_hours !== undefined
            ) {
                let newBalance:number = +studentOrClass.purchased_class_hours + +action.payload.class_hours_purchased_or_refunded;
                studentOrClass.purchased_class_hours = newBalance;    
            }
    
            return adapter.updateOne(
                {
                    id: action.payload.studentOrClass.id,
                    changes: studentOrClass
                },
                {
                    ...state, errorMessage:undefined,
                    successMessage: `Total purchased hours: ${studentOrClass.purchased_class_hours}`
                }
            );


        case StudentOrClassActionTypes.FreelanceAccountRefundedHoursSaved:
            // clone with spead operator and add the new value before saving the clone
            let freelanceAccount:StudentOrClassModel = { ...action.payload.studentOrClass }
            
            if (
                freelanceAccount.purchased_class_hours !== null && 
                freelanceAccount.purchased_class_hours !== undefined
            ) {
                let updatedBalance:number = +freelanceAccount.purchased_class_hours - +action.payload.class_hours_purchased_or_refunded;
                freelanceAccount.purchased_class_hours = updatedBalance;    
            }
            
            return adapter.updateOne(
                {
                    id: action.payload.studentOrClass.id,
                    changes: freelanceAccount
                },
                {
                    ...state, errorMessage:undefined,
                    successMessage: `Total purchased hours: ${freelanceAccount.purchased_class_hours}`
                }
            );  

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

        case StudentOrClassActionTypes.StudentOrClassDeletionModeActivated:
            return {
                ...state, 
                deletionModeActivated: true
            }
            
        case StudentOrClassActionTypes.StudentOrClassDeletionModeDeactivated:
            return {
                ...state, 
                deletionModeActivated: false
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

        case StudentOrClassActionTypes.StudentOrClassPurchasedHoursUpdated:
            
            return adapter.updateOne(
                action.payload.studentOrClass,
                {
                    ...state, errorMessage:undefined,
                    successMessage: `Updated Purchased Hours: ${action.payload.studentOrClass.changes.purchased_class_hours}`
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
