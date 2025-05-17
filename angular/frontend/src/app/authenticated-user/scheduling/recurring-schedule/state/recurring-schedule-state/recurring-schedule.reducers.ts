import { createEntityAdapter, EntityAdapter, EntityState } from '@ngrx/entity';

import { 
    RecurringClassActions, RecurringClassesActionTypes 
} from './recurring-schedule.actions';
import { RecurringClassModel } from "src/app/models/recurring-schedule.model";

function compareRecurringClasses(
    a: RecurringClassModel, 
    b: RecurringClassModel
  ): number {
    // First compare by day of week
    const dayComparison = a.recurring_day_of_week - b.recurring_day_of_week;
    
    // If days are different, return that comparison
    if (dayComparison !== 0) {
      return dayComparison;
    }
    
    // If days are the same, compare start times
    const timeA = new Date('1970-01-01T' + a.recurring_start_time);
    const timeB = new Date('1970-01-01T' + b.recurring_start_time);
    
    return timeA.getTime() - timeB.getTime();
  }

  export interface RecurringClassesState extends EntityState<RecurringClassModel> {
    deletionModeActivated: boolean;
    errorMessage: string | undefined,
    recurringClassesLoaded: boolean,
    successMessage: string | undefined,
  };
  
  export const adapter: EntityAdapter<RecurringClassModel> =
    createEntityAdapter<RecurringClassModel>(
      { sortComparer: compareRecurringClasses }
    );
  
  export const initialRecurringClassesState: RecurringClassesState = adapter
    .getInitialState(
        {
          deletionModeActivated: false,
          errorMessage: undefined,
          recurringClassesLoaded: false,
          successMessage: undefined
        }
    );
  
  export function recurringClassesReducer(
    state = initialRecurringClassesState,
    action: RecurringClassActions
  ): RecurringClassesState {
    switch (action.type) {
  
      case RecurringClassesActionTypes.RecurringClassAdded:
        return adapter.addOne(action.payload.recurringClass, { ...state,
          errorMessage: undefined,
          successMessage: 'Recurring Class successfully submitted!'
        });
  
      case RecurringClassesActionTypes.RecurringClassCreationCancelled:
        console.log(action.payload);
        let creationErrorMessage: string = "Error submitting recurring class!";
        if (action.payload.err.error.message) {
          creationErrorMessage = action.payload.err.error.message;
        }
        return {
          ...state, successMessage: undefined,
          errorMessage: creationErrorMessage
        }
  
      case RecurringClassesActionTypes.RecurringClassesCleared:
        return initialRecurringClassesState;
  
      case RecurringClassesActionTypes.RecurringClassesRequestCancelled:
        console.log("******ERROR***********")
        console.log(action.payload.err);
        let recurringClassesErrorMessage: string = "Error fetching recurring classes!";
        if (action.payload.err.error.message) {
          recurringClassesErrorMessage = action.payload.err.error.message;
        }
        return {
          ...state, successMessage: undefined,
          errorMessage: recurringClassesErrorMessage
        }
  
      case RecurringClassesActionTypes.RecurringClassDeletionCancelled:
        let errMsg: string = "Error! Recurring Class Deletion Failed!";
        if (action.payload.err.error.Error) {
          errMsg = action.payload.err.error.Error;
        }
        return {
          ...state, successMessage: undefined,
          errorMessage: errMsg
        }


      case RecurringClassesActionTypes.RecurringClassDeletionModeActivated:
        return {
              ...state, 
              deletionModeActivated: true
              }
                    
      case RecurringClassesActionTypes.RecurringClassDeletionModeDeactivated:
        return {
            ...state, 
            deletionModeActivated: false                    
          }    
                
      case RecurringClassesActionTypes.RecurringClassDeletionSaved:
        return adapter.removeOne(action.payload.id,
          {
            ...state,
            errorMessage: undefined,
            successMessage: action.payload.message
          }
        );
  
      case RecurringClassesActionTypes.RecurringClassesLoaded:
        return adapter.upsertMany(action.payload.recurringClasses, { ...state,
          errorMessage: undefined,
          recurringClassesLoaded: true
        });
  
      case RecurringClassesActionTypes.RecurringClassesMessagesCleared:
        return {
          ...state, successMessage: undefined,
          errorMessage: undefined
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