import {
    createEntityAdapter, EntityAdapter, 
    EntityState, Update
} from '@ngrx/entity';


import { 
    getFirstDateofMonthStr, getLastDateOfMonthStr 
} from 'src/app/shared-utils/date-time.util';
import { 
    ScheduledClassesActions, ScheduledClassesActionTypes 
} from './scheduled-classes.actions';
import { ScheduledClassModel } from 'src/app/models/scheduled-class.model';
import { 
    StudentOrClassConfirmationModificationResponse 
} from 'src/app/models/student-or-class.model';


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
    unconfirmedScheduledClassesLoaded: boolean,
    updatedPurchasedHours: StudentOrClassConfirmationModificationResponse | undefined;
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
        successMessage: undefined,
        unconfirmedScheduledClassesLoaded: false,
        updatedPurchasedHours: undefined
    });

export function scheduledClassesReducer(
        state = initialScheduledClassesState,
        action: ScheduledClassesActions
    ): ScheduledClassesState {
        switch(action.type) {

            case ScheduledClassesActionTypes.ClassStatusUpdateCancelled:
                let statusEditErrMessage: string = "Error! Class Status Update Failed!";
                if (action.payload.err.error.Error) {
                    //console.log(action.payload.err.error.Error)
                    statusEditErrMessage = action.payload.err.error.Error;
                }
                return {
                    ...state,  successMessage: undefined,
                    errorMessage: statusEditErrMessage
                } 

            case ScheduledClassesActionTypes.ClassStatusUpdateSaved:
                let updatedScheduledClass: ScheduledClassModel = action.payload.scheduledClassUpdateResponse.scheduled_class;

                return adapter.updateOne(
                    { id: updatedScheduledClass.id, changes: updatedScheduledClass }, 
                    {
                        ...state, errMsg:undefined,
                        successMessage: 'You have successfully edited the class status!',
                        updatedPurchasedHours: action.payload.scheduledClassUpdateResponse.student_or_class_update
                    }
                ); 

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

            case ScheduledClassesActionTypes.MonthlyClassesRequested:
                let month:number = +action.payload.month;
                let year:number = +action.payload.year;
                let firstDate = getFirstDateofMonthStr(month, year);
                let lastDate = getLastDateOfMonthStr(month, year);
                return {
                    ...state,  dateRange: [firstDate, lastDate],
                    fetchingClassesInProgress: true
                }
        
            case ScheduledClassesActionTypes.MonthlyClassesRequestCancelled:
                let monthlyPageErrorMessage: string = "Error fetching monthly schedule!";
                if (action.payload.err.error.message) {
                    monthlyPageErrorMessage = action.payload.err.error.message;
                }
                return {
                    ...state,  successMessage: undefined,
                    errorMessage: monthlyPageErrorMessage,
                    fetchingClassesInProgress: false
                }

            case ScheduledClassesActionTypes.MonthlyClassesLoaded:
                return adapter.upsertMany(action.payload.scheduledClasses, {...state,
                    errorMessage: undefined,
                    monthlyScheduledClassesLoaded: true,
                    fetchingClassesInProgress: false
                });
        
            case ScheduledClassesActionTypes.RescheduleClassCancelled:
                let rescheduleErrMessage: string = "Error! Rescheduling Failed!";
                if (action.payload.err.error.Error) {
                    //console.log(action.payload.err.error.Error)
                    rescheduleErrMessage = action.payload.err.error.Error;
                }
                return {
                    ...state,  successMessage: undefined,
                    errorMessage: rescheduleErrMessage
                }
    
            case ScheduledClassesActionTypes.RescheduledClassUpdatedWithDailyBatchAdded:
                return adapter.upsertMany(action.payload.scheduledClasses, 
                    {
                        ...state, errorMessage: undefined,
                        successMessage: 'You have successfully rescheduled the class!'
                    }
                );
                                         
            case ScheduledClassesActionTypes.ScheduleSingleClassCancelled:
                console.log(action.payload);
                let userErrorMessage: string = "Error scheduling class!";
                if (action.payload.err.error.message) {
                    userErrorMessage = action.payload.err.error.message;
                }
                return {
                    ...state,  successMessage: undefined,
                    errorMessage: userErrorMessage
                }
                            

            case ScheduledClassesActionTypes.ScheduledSingleClassWithDailyBatchAdded:
                return adapter.upsertMany(action.payload.scheduledClasses, {...state,
                    errorMessage: undefined,
                    successMessage: 'Class scheduling successfully submitted!'
                });

            case ScheduledClassesActionTypes.ScheduledClassesCleared:
                    return initialScheduledClassesState;
        
            case ScheduledClassesActionTypes.ScheduledClassDeletionCancelled:
                let deletionErrMsg: string = "Error! Scheduled Class Deletion Failed!";
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
        
            case ScheduledClassesActionTypes.ScheduledClassesBatchDeletionCancelled:
                    let batchDeletionErrMsg: string = "Error! Batch Deletion Failed!";
                    if (action.payload.err.error.Error) {
                        batchDeletionErrMsg = action.payload.err.error.Error;
                    }
                    return {
                        ...state,  successMessage: undefined,
                        errorMessage: batchDeletionErrMsg
                    }
                                    
            case ScheduledClassesActionTypes.ScheduledClassesBatchDeletionSaved:
                return adapter.removeMany(action.payload.ids,  
                    { 
                        ...state,
                        errorMessage: undefined,
                        successMessage: action.payload.message
                    }
                );
     
            case ScheduledClassesActionTypes.ScheduledClassesMessagesCleared:
                return {
                    ...state,  successMessage: undefined,
                    errorMessage: undefined
            }

            case ScheduledClassesActionTypes.UpdatedPurchasedHoursCleared:
                return {
                    ...state, updatedPurchasedHours: undefined
                }   
                

            case ScheduledClassesActionTypes.UnconfirmedScheduledClassesLoaded:
                return adapter.upsertMany(action.payload.scheduledClasses, 
                    {
                        ...state,
                        errorMessage: undefined,
                        unconfirmedScheduledClassesLoaded: true
                    }
                );
            
            case ScheduledClassesActionTypes.UnconfirmedScheduledClassesRequestCancelled:
                let unconfirmedClassesErrorMessage: string = "Error fetching unconfirmed past scheduled classes!";
                if (action.payload.err.error.message) {
                    landingPageErrorMessage = action.payload.err.error.Error;
                }
                return {
                    ...state,  successMessage: undefined,
                    errorMessage: unconfirmedClassesErrorMessage
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
