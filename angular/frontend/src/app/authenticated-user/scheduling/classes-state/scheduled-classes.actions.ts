import { Action} from "@ngrx/store";
//import { Update } from "@ngrx/entity";

import { 
    CreateScheduledClassModel, ModifyClassStatusModel, 
    ModifyClassStatusResponse, RescheduleClassModel, 
    ScheduledClassModel, ScheduledClassBatchDeletionDataModel
} from "src/app/models/scheduled-class.model";

export enum ScheduledClassesActionTypes {
    ClassStatusUpdateCancelled= '[Edit Class Status Form Page] Update Class Status Cancelled',
    ClassStatusUpdateSaved = '[Scheduled Class Detail Page] Single Class Status Updated',    
    ClassStatusUpdateSubmitted = '[Edit Class Status Form Page] Updated Class Status Submitted',
    DailyClassesLoaded = '[Daily Classes API] Daily Batch Loaded',
    DailyClassesRequestCancelled= '[Daily Classes Page] Daily Batch Request Cancelled',
    DailyClassesRequested = '[Daily Classes Page] Daily Batch Requested',
    LandingPageScheduleLoaded = '[User Landing Page] Landing Page Daily Scheduled Classes Loaded',
    LandingPageScheduleRequestCancelled = '[User Landing Page] Landing Page Scheduled Classes Request Cancelled',    
    LandingPageScheduleRequested = '[User Landing Page] Landing Daily Scheduled Classes Requested',
    MonthlyClassesRequested = '[Monthly Classes Select Page] Monthly Batch Requested',
    MonthlyClassesRequestCancelled= '[Monthly Classes Page] Monthly Batch Request Cancelled',
    MonthlyClassesLoaded = '[Monthly Classes API] Monthly Batch Loaded',     
    RescheduleClassCancelled= '[Reschedule Class Form Page] Reschedule Class Cancelled',
    RescheduleClassSubmitted = '[Reschedule Class Form Page] Rescheduled Class Submitted',
    RescheduledClassUpdatedWithDailyBatchAdded = '[Single Class Detail Page] Rescheduled Single Class Updated',    
    ScheduleSingleClassSubmitted = '[Schedule Single Class Page] Single Class Submitted',
    ScheduleSingleClassCancelled = '[Schedule Single Class Page] Schedule Single Class Cancelled',        
    ScheduledSingleClassWithDailyBatchAdded = '[Schedule Single Class Page] Newly Scheduled Class with Daily Batch Added',
    ScheduledClassesBatchDeletionCancelled = '[Recurring Classes Applied Monthly Page] Monthly Batch Deletion of Scheduled Class Cancelled',
    ScheduledClassesBatchDeletionSubmitted = '[Recurring Classes Applied Monthly Page] Monthy Batch Deletion of Scheduled Class Submitted',
    ScheduledClassesBatchDeletionSaved = '[Recurring Classes Applied Monthly Page] Monthly Batch Deletion of Scheduled Class Saved',
    ScheduledClassesCleared = '[View User Logout] All Scheduled Classes Removed',
    ScheduledClassDeletionCancelled = '[Scheduled Classes API] Removal of Scheduled Class Cancelled',
    ScheduledClassDeletionRequested = '[Scheduled Classes Daily Page/Landing Page]  Removal of Scheduled Class Requested',
    ScheduledClassDeletionSaved = '[Scheduled Classes Daily Page/Landing Page] Scheduled Class Removed',
    ScheduledClassesMessagesCleared = '[Scheduled Class Edit Status, Reschedule and Schedule Pages] Scheduled Classes Messages Cleared',
    UpdatedPurchasedHoursCleared = '[Scheduled Class Detail Page (Edit Class Status Child)] Updated Purchased Hours Data Removed'
}

export class ClassStatusUpdateCancelled implements Action {
    readonly type = ScheduledClassesActionTypes.ClassStatusUpdateCancelled;
  
    constructor(public payload: {  err: any }) {}
}

export class ClassStatusUpdateSaved implements Action {
    readonly type = ScheduledClassesActionTypes.ClassStatusUpdateSaved;
  
    constructor(
        public payload: { 
            scheduledClassUpdateResponse: ModifyClassStatusResponse 
        }
    ) {}
}

export class ClassStatusUpdateSubmitted implements Action {
    readonly type = ScheduledClassesActionTypes.ClassStatusUpdateSubmitted;
  
    constructor(
        public payload: { scheduledClass: ModifyClassStatusModel }
    ) {}
}

export class DailyClassesLoaded implements Action {
    readonly type = ScheduledClassesActionTypes.DailyClassesLoaded;
  
    constructor(
        public payload: { scheduledClasses: ScheduledClassModel[] }
    ) {}
}

export class DailyClassesRequestCancelled implements Action {
    readonly type = ScheduledClassesActionTypes.DailyClassesRequestCancelled;
  
    constructor(public payload: {  err: any }) {}
}

export class DailyClassesRequested implements Action {
    readonly type = ScheduledClassesActionTypes.DailyClassesRequested;
  
    constructor(public payload: { date: string }) {}
}


export class LandingPageScheduleLoaded implements Action {
    readonly type = ScheduledClassesActionTypes.LandingPageScheduleLoaded;
  
    constructor(
        public payload: { scheduledClasses: ScheduledClassModel[] }
    ) {}
}

export class LandingPageScheduleRequestCancelled implements Action {
    readonly type = ScheduledClassesActionTypes.LandingPageScheduleRequestCancelled;
  
    constructor(public payload: {  err: any }) {}
}

export class LandingPageScheduleRequested implements Action {
    readonly type = ScheduledClassesActionTypes.LandingPageScheduleRequested;
}

export class MonthlyClassesRequested implements Action {
    readonly type = ScheduledClassesActionTypes.MonthlyClassesRequested;
  
    constructor(
        public payload: { month: number, year: number 
    }) {}
}

export class MonthlyClassesRequestCancelled implements Action {
    readonly type = ScheduledClassesActionTypes.MonthlyClassesRequestCancelled;
  
    constructor(public payload: {  err: any }) {}
}

export class MonthlyClassesLoaded implements Action {
    readonly type = ScheduledClassesActionTypes.MonthlyClassesLoaded;
  
    constructor(
        public payload: { scheduledClasses: ScheduledClassModel[] }
    ) {}
}

export class RescheduleClassCancelled implements Action {
    readonly type = ScheduledClassesActionTypes.RescheduleClassCancelled;
  
    constructor(public payload: {  err: any }) {}
}

export class RescheduleClassSubmitted implements Action {
    readonly type = ScheduledClassesActionTypes.RescheduleClassSubmitted;

    constructor(public payload: 
        {  id: number, scheduledClass: RescheduleClassModel }) {}
}

export class RescheduledClassUpdatedWithDailyBatchAdded implements Action {
    readonly type = ScheduledClassesActionTypes.RescheduledClassUpdatedWithDailyBatchAdded;
  
    constructor(public payload: {  scheduledClasses: ScheduledClassModel[] }) {
    }
}

export class ScheduleSingleClassSubmitted implements Action {
    readonly type = ScheduledClassesActionTypes.ScheduleSingleClassSubmitted;
  
    constructor(
        public payload: { scheduledClass: CreateScheduledClassModel }
    ){}
};

export class ScheduleSingleClassCancelled implements Action {
    readonly type = ScheduledClassesActionTypes.ScheduleSingleClassCancelled;
  
    constructor(public payload: {  err: any }) {}
}

export class ScheduledSingleClassWithDailyBatchAdded implements Action {
    readonly type = ScheduledClassesActionTypes.ScheduledSingleClassWithDailyBatchAdded;
  
    constructor(
        public payload: { scheduledClasses: ScheduledClassModel[] }
    ) {}
}

export class ScheduledClassesCleared implements Action {
    readonly type = ScheduledClassesActionTypes.ScheduledClassesCleared;
}

export class ScheduledClassesBatchDeletionCancelled implements Action {
    readonly type = ScheduledClassesActionTypes.ScheduledClassesBatchDeletionCancelled;
  
    constructor(public payload: {  err: any }) {}
}

export class ScheduledClassesBatchDeletionSubmitted implements Action {
    readonly type = ScheduledClassesActionTypes.ScheduledClassesBatchDeletionSubmitted;
    constructor(public payload: { 
        obsolete_class_data: ScheduledClassBatchDeletionDataModel 
    }) {}
}

export class ScheduledClassesBatchDeletionSaved implements Action {
    readonly type = ScheduledClassesActionTypes.ScheduledClassesBatchDeletionSaved;
  
    constructor(public payload: { ids: number[], message: string }) {}
}

export class ScheduledClassDeletionCancelled implements Action {
    readonly type = ScheduledClassesActionTypes.ScheduledClassDeletionCancelled;
  
    constructor(public payload: {  err: any }) {}
}

export class ScheduledClassDeletionRequested implements Action {
    readonly type = ScheduledClassesActionTypes.ScheduledClassDeletionRequested;
  
    constructor(public payload: { id: number }) {}
}

export class ScheduledClassDeletionSaved implements Action {
    readonly type = ScheduledClassesActionTypes.ScheduledClassDeletionSaved;
  
    constructor(public payload: { id: number, message: string }) {}
}

export class ScheduledClassesMessagesCleared implements Action {
    readonly type = ScheduledClassesActionTypes.ScheduledClassesMessagesCleared;
}

export class UpdatedPurchasedHoursCleared implements Action {
    readonly type = ScheduledClassesActionTypes.UpdatedPurchasedHoursCleared;
}

export type ScheduledClassesActions = ClassStatusUpdateCancelled |
    ClassStatusUpdateSaved | ClassStatusUpdateSubmitted |
    DailyClassesLoaded | DailyClassesRequestCancelled | 
    DailyClassesRequested | LandingPageScheduleLoaded | 
    LandingPageScheduleRequestCancelled | LandingPageScheduleRequested | 
    MonthlyClassesRequested | MonthlyClassesRequestCancelled |
    MonthlyClassesLoaded | RescheduleClassCancelled | 
    RescheduleClassSubmitted | RescheduledClassUpdatedWithDailyBatchAdded | 
    ScheduleSingleClassSubmitted | ScheduleSingleClassCancelled | 
    ScheduledSingleClassWithDailyBatchAdded | ScheduledClassesCleared | 
    ScheduledClassDeletionCancelled | ScheduledClassesBatchDeletionCancelled | 
    ScheduledClassesBatchDeletionSubmitted | ScheduledClassesBatchDeletionSaved |
    ScheduledClassDeletionRequested | ScheduledClassDeletionSaved | 
    ScheduledClassesMessagesCleared | UpdatedPurchasedHoursCleared;