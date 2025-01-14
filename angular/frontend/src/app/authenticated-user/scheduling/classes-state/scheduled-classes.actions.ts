import { Action} from "@ngrx/store";
import { Update } from "@ngrx/entity";

import { 
    CreateScheduledClassModel, RescheduleClassModel, ScheduledClassModel 
} from "src/app/models/scheduled-class.model";

export enum ScheduledClassesActionTypes {
    DailyClassesLoaded = '[Daily Classes API] Daily Batch Loaded',
    DailyClassesRequestCancelled= '[Daily Classes Page] Daily Batch Request Cancelled',
    DailyClassesRequested = '[Daily Classes Page] Daily Batch Requested',
    LandingPageScheduleLoaded = '[User Landing Page] Landing Page Daily Scheduled Classes Loaded',
    LandingPageScheduleRequestCancelled = '[User Landing Page] Landing Page Scheduled Classes Request Cancelled',    
    LandingPageScheduleRequested = '[User Landing Page] Landing Daily Scheduled Classes Requested',
    RescheduleClassCancelled= '[Reschedule Class Form Page] Reschedule Class Cancelled',
    RescheduleClassSubmitted = '[Reschedule Class Form Page] Rescheduled Class Submitted',
    RescheduledClassUpdatedWithDailyBatchAdded = '[Single Class Detail Page] Rescheduled Single Class Updated',    
    ScheduleSingleClassSubmitted = '[Schedule Single Class Page] Single Class Submitted',
    ScheduleSingleClassCancelled = '[Schedule Single Class Page] Schedule Single Class Cancelled',        
    ScheduledSingleClassWithDailyBatchAdded = '[Schedule Single Class Page] Newly Scheduled Class with Daily Batch Added',
    ScheduledClassesCleared = '[View User Logout] All Scheduled Classes Removed',
    ScheduledClassDeletionCancelled = '[Scheduled Classes API] Removal of Scheduled Class Cancelled',
    ScheduledClassDeletionRequested = '[Scheduled Classes Daily Page/Landing Page]  Removal of Scheduled Class Requested',
    ScheduledClassDeletionSaved = '[Scheduled Classes Daily Page/Landing Page] Scheduled Class Removed',
    ScheduledClassesMessagesCleared = '[Scheduled Class Edit Status, Reschedule and Schedule Pages] Scheduled Classes Messages Cleared',
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

export type ScheduledClassesActions = 
    DailyClassesLoaded | DailyClassesRequestCancelled | 
    DailyClassesRequested | LandingPageScheduleLoaded | 
    LandingPageScheduleRequestCancelled | LandingPageScheduleRequested | 
    RescheduleClassCancelled | RescheduleClassSubmitted |
    RescheduledClassUpdatedWithDailyBatchAdded | ScheduleSingleClassSubmitted |
    ScheduleSingleClassCancelled | ScheduledSingleClassWithDailyBatchAdded |
    ScheduledClassesCleared | ScheduledClassDeletionCancelled |
    ScheduledClassDeletionRequested | ScheduledClassDeletionSaved | 
    ScheduledClassesMessagesCleared;