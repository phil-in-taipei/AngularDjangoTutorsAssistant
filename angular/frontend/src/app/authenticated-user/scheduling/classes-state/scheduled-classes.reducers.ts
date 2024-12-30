import {createEntityAdapter, EntityAdapter, EntityState} from '@ngrx/entity';

import { 
    getFirstDateofMonthStr, getLastDateOfMonthStr 
} from 'src/app/shared-utils/date-time.util';
import { 
    ScheduledClassesActions, ScheduledClassesActionTypes 
} from './scheduled-classes.actions';
import { ScheduledClassModel } from 'src/app/models/scheduled-class.model';


function compareByDateAndTime(
        a: ScheduledClassModel,
        b: ScheduledClassModel
    ) {
    const monthlyDayA = a.date;
    const monthlyDayB = b.date;
    const startTimeA = a.start_time;
    const startTimeB = b.start_time;

    let comparison = 0;
    if (monthlyDayA > monthlyDayB) {
        comparison = 1;
    } else if (monthlyDayA < monthlyDayB) {
        comparison = -1;
    } else {
        if (startTimeA > startTimeB) {
            comparison = 1;
        } else if (startTimeA < startTimeB) {
            comparison = -1;
        }
    }
    return comparison;
}

export interface ScheduledClassesState extends EntityState<ScheduledClassModel> {
    dateRange: [string, string] | undefined;
    fetchingClassesInProgress: boolean;
    errorMessage: string | undefined,
    monthlyScheduledClassesLoaded: boolean,
    landingPageScheduledClassesLoaded: boolean,
    successMessage: string | undefined,
};


export const adapter: EntityAdapter<ScheduledClassModel> = 
    createEntityAdapter<ScheduledClassModel>(
        { sortComparer: compareByDateAndTime }
    );

export const initialScheduledClassesState: ScheduledClassesState = 
    adapter.getInitialState({
        dateRange: undefined,
        errorMessage: undefined,
        fetchingClassesInProgress: false,
        monthlyScheduledClassesLoaded: false,
        landingPageScheduledClassesLoaded: false,
        successMessage: undefined
    });


export function scheduledClassesReducer(
        state = initialScheduledClassesState,
        action: ScheduledClassesActions
    ): ScheduledClassesState {
        switch(action.type) {

            case ScheduledClassesActionTypes.DailyClassesRequested:
                return {
                    ...state, 
                    fetchingClassesInProgress: true
                }
    
    
            case ScheduledClassesActionTypes.DailyClassesLoaded:
                return adapter.upsertMany(action.payload.scheduledClasses, 
                    {...state,
                        errorMessage: undefined,
                        fetchingClassesInProgress: false
                    }
                );
    
            case ScheduledClassesActionTypes.DailyClassesRequestCancelled:
                let dailyScheduleErrorMessage: string = "Error fetching daily classes!";
                if (action.payload.err.error.message) {
                    dailyScheduleErrorMessage = action.payload.err.error.Error;
                }
                return {
                    ...state,  successMessage: undefined,
                    errorMessage: dailyScheduleErrorMessage
                }

            case ScheduledClassesActionTypes.LandingPageScheduleLoaded:
                return adapter.upsertMany(action.payload.scheduledClasses, 
                    {
                        ...state,
                        errorMessage: undefined,
                        landingPageScheduledClassesLoaded: true
                    }
                );
        
            case ScheduledClassesActionTypes.LandingPageScheduleRequestCancelled:
                let landingPageErrorMessage: string = "Error fetching daily schedule!";
                if (action.payload.err.error.message) {
                    landingPageErrorMessage = action.payload.err.error.Error;
                }
                return {
                    ...state,  successMessage: undefined,
                    errorMessage: landingPageErrorMessage
                }

            case ScheduledClassesActionTypes.ScheduledClassesCleared:
                    return initialScheduledClassesState;
        
            case ScheduledClassesActionTypes.ScheduledClassDeletionCancelled:
                let deletionErrMsg: string = "Error! Task Deletion Failed!";
                if (action.payload.err.error.Error) {
                    deletionErrMsg = action.payload.err.error.Error;
                }
                return {
                    ...state,  successMessage: undefined,
                    errorMessage: deletionErrMsg
                }
                
            case ScheduledClassesActionTypes.ScheduledClassDeletionSaved:
                return adapter.removeOne(action.payload.id, 
                    { 
                        ...state,
                        errorMessage: undefined,
                        successMessage: action.payload.message
                    }
                );
            
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
