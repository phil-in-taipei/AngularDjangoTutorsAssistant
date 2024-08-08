import {createEntityAdapter, EntityAdapter, EntityState} from '@ngrx/entity';

import { SchoolActions, SchoolActionTypes } from './school.actions';
import { SchoolModel } from 'src/app/models/school.model';



function compareSchoolsByName(
    a:SchoolModel, b:SchoolModel) {
    const schoolA = a.school_name;
    const schoolB = b.school_name;
  
    let comparison = 0;
    if (schoolA > schoolB) {
      comparison = 1;
    } else if (schoolA < schoolB) {
      comparison = -1;
    }
    return comparison;
};

export interface SchoolsState extends EntityState<SchoolModel> {
    fetchingSchoolsInProgress: boolean;
    errorMessage: string | undefined,
    schoolsLoaded: boolean,
    successMessage: string | undefined,
};

export const adapter: EntityAdapter<SchoolModel> = 
    createEntityAdapter<SchoolModel>(
        { sortComparer: compareSchoolsByName }
    );

export const initialSchoolsState: SchoolsState = adapter.getInitialState({
    errorMessage: undefined,
    fetchingSchoolsInProgress: false,
    schoolsLoaded: false,
    successMessage: undefined
});

export function schoolsReducer(
    state = initialSchoolsState,
    action: SchoolActions): SchoolsState {

    let reducerErrorMessage: string | undefined = undefined;
    let reducerSuccessMessage: string | undefined = undefined;

    switch(action.type) {

        case SchoolActionTypes.SchoolCreatedAdded:
            reducerErrorMessage = undefined;
            reducerSuccessMessage = 'Task successfully submitted!';
            return adapter.addOne(action.payload.school, {...state,
                errorMessage: reducerErrorMessage,
                successMessage: reducerSuccessMessage
            });

        case SchoolActionTypes.SchoolCreationCancelled:
            reducerErrorMessage = "Error submitting weekly task scheduler!";
            reducerSuccessMessage = undefined;
            if (action.payload.err.error.message) {
                reducerErrorMessage = action.payload.err.error.message;
            }
            return {
                ...state,  successMessage: reducerSuccessMessage,
                errorMessage: reducerErrorMessage
            }

        case SchoolActionTypes.SchoolDeletionCancelled:
            reducerErrorMessage = "Error! School Deletion Failed!";
            reducerSuccessMessage = undefined;
            if (action.payload.err.error.Error) {
                reducerErrorMessage = action.payload.err.error.Error;
            }
            return {
                ...state,  successMessage: reducerSuccessMessage,
                errorMessage: reducerErrorMessage
            }
        
        case SchoolActionTypes.SchoolDeletionSaved:
            reducerErrorMessage = undefined;
            reducerSuccessMessage = action.payload.message;
            return adapter.removeOne(action.payload.id, 
                { 
                    ...state,
                    errorMessage: undefined,
                    successMessage: reducerSuccessMessage
                }
            );


        case SchoolActionTypes.SchoolEditCancelled:
            reducerErrorMessage = "Error! Editing School Failed!";
            reducerSuccessMessage = undefined;

            if (action.payload.err.error.Error) {
                reducerErrorMessage = action.payload.err.error.Error;
            }
            return {
                ...state,  successMessage: reducerSuccessMessage,
                errorMessage: reducerErrorMessage
            }
        
        case SchoolActionTypes.SchoolEditUpdated:
            reducerErrorMessage = undefined;
            reducerSuccessMessage = 'School information edtied!';
            return adapter.updateOne(action.payload.school, 
                {
                    ...state,
                    errorMessage: reducerErrorMessage,
                    successMessage: reducerSuccessMessage
                }
            );
   
        case SchoolActionTypes.SchoolsMessagesCleared:
            reducerErrorMessage = undefined;
            reducerSuccessMessage = undefined;
            return {
                ...state,  successMessage: reducerSuccessMessage,
                errorMessage: reducerErrorMessage
            }

        case SchoolActionTypes.SchoolsCleared:
            return initialSchoolsState;
    
        case SchoolActionTypes.SchoolsLoaded:
            reducerErrorMessage = undefined;
            reducerSuccessMessage = undefined;
    
            return adapter.upsertMany(action.payload.schools, {...state,
                errorMessage: reducerErrorMessage,
                fetchingSchoolsInProgress: false,
                schoolsLoaded: false,
                successMessage: reducerSuccessMessage
            });   

        case SchoolActionTypes.SchoolsRequestCancelled:
            reducerErrorMessage = "Error fetching schools!";
            reducerSuccessMessage = undefined;

            if (action.payload.err.error.message) {
                reducerErrorMessage = action.payload.err.error.message;
            }
            return {
                 ...state,  errorMessage: reducerErrorMessage, 
                 successMessage: reducerSuccessMessage,
            }

        case SchoolActionTypes.SchoolsRequested:
            return {
                ...state, 
                fetchingSchoolsInProgress: true
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
