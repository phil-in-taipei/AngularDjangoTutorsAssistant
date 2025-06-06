import { createEntityAdapter, EntityAdapter, EntityState } from '@ngrx/entity';

import { RecurringClassAppliedMonthlyModel } from 'src/app/models/recurring-schedule.model';
import { 
    RecurringClassAppliedMonthlyActionTypes, RecurringClassAppliedMonthlyActions 
} from './recurring-class-applied-monthly.actions';
import { 
  RecurringClassAppliedMonthlyDeletionResponse 
} from 'src/app/models/recurring-schedule.model';
import { 
  ScheduledClassBatchDeletionDataModel 
} from 'src/app/models/scheduled-class.model';

function compareRecurringClassesAppliedMonthly(
  a: RecurringClassAppliedMonthlyModel, 
  b: RecurringClassAppliedMonthlyModel
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

export interface RecurringClassAppliedMonthlysState 
    extends EntityState<RecurringClassAppliedMonthlyModel> {
      deletionModeActivated: boolean;
      errorMessage: string | undefined,
      recurringClassAppliedMonthlysLoaded: boolean,
      successMessage: string | undefined,
      optionalBatchDeletionData: ScheduledClassBatchDeletionDataModel | undefined
    };
    
export const adapter: EntityAdapter<RecurringClassAppliedMonthlyModel> =
    
createEntityAdapter<RecurringClassAppliedMonthlyModel>(
  { sortComparer: compareRecurringClassesAppliedMonthly }
);
    
export const initialRecurringClassAppliedMonthlysState: 
    RecurringClassAppliedMonthlysState = adapter.getInitialState({

    deletionModeActivated: false,

    errorMessage: undefined,
    
    recurringClassAppliedMonthlysLoaded: false,
    
    successMessage: undefined,

    optionalBatchDeletionData: undefined

});

export function recurringClassAppliedMonthlysReducer(
    state = initialRecurringClassAppliedMonthlysState,
    action: RecurringClassAppliedMonthlyActions
    ): RecurringClassAppliedMonthlysState {
    switch (action.type) {
        case RecurringClassAppliedMonthlyActionTypes.RecurringClassAppliedMonthlyAdded:
            return adapter.addOne(action.payload.recurringClassAppliedMonthly, {
              ...state,
              errorMessage: undefined,
              successMessage: 'Recurring Class Applied Monthly successfully submitted!'
            });
       
        case RecurringClassAppliedMonthlyActionTypes.RecurringClassAppliedMonthlyCreationCancelled:
            console.log(action.payload);
            let creationErrorMessage: string = "Error submitting recurring class applied monthly!";
            if (action.payload.err.error.message) {
              creationErrorMessage = action.payload.err.error.message;
            }
            return {
              ...state,
              successMessage: undefined,
              errorMessage: creationErrorMessage
            }
       
        case RecurringClassAppliedMonthlyActionTypes.RecurringClassAppliedMonthlysCleared:
            return initialRecurringClassAppliedMonthlysState;
       
        case RecurringClassAppliedMonthlyActionTypes.RecurringClassAppliedMonthlysRequestCancelled:
            let recurringClassesErrorMessage: string = "Error fetching recurring classes applied monthly!";
            if (action.payload.err.error.message) {
              recurringClassesErrorMessage = action.payload.err.error.message;
            }
            return {
              ...state,
              successMessage: undefined,
              errorMessage: recurringClassesErrorMessage
            }
       
        case RecurringClassAppliedMonthlyActionTypes.RecurringClassAppliedMonthlyDeletionCancelled:
            let errMsg: string = "Error! Recurring Class Applied Monthly Deletion Failed!";
            if (action.payload.err.error.Error) {
              errMsg = action.payload.err.error.Error;
            }
            return {
              ...state,
              successMessage: undefined,
              errorMessage: errMsg
            }

        case RecurringClassAppliedMonthlyActionTypes.RecurringClassAppliedMonthlyDeletionModeActivated:
          return {
                ...state, 
                deletionModeActivated: true
                }
                    
        case RecurringClassAppliedMonthlyActionTypes.RecurringClassAppliedMonthlyDeletionModeDeactivated:
          return {
              ...state, 
              deletionModeActivated: false                    
            }    
                  
        case RecurringClassAppliedMonthlyActionTypes.RecurringClassAppliedMonthlyDeletionSaved:
          let deletionResponseData: RecurringClassAppliedMonthlyDeletionResponse = 
            action.payload.recurringClassAppliedMonthlyDeletionResponse
            return adapter.removeOne(
              deletionResponseData.id,
              {
                ...state,
                errorMessage: undefined,
                successMessage: deletionResponseData.message,
                optionalBatchDeletionData: deletionResponseData.scheduled_class_batch_deletion_data
              }
            );
       
        case RecurringClassAppliedMonthlyActionTypes.RecurringClassAppliedMonthlysLoaded:
            return adapter.upsertMany(
              action.payload.recurringClassesAppliedMonthly,
              {
                ...state,
                errorMessage: undefined,
                recurringClassAppliedMonthlysLoaded: true
              }
            );
       
        case RecurringClassAppliedMonthlyActionTypes.RecurringClassesAppliedMonthlyMessagesCleared:
            return {
              ...state,
              successMessage: undefined,
              errorMessage: undefined,
              optionalBatchDeletionData: undefined
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