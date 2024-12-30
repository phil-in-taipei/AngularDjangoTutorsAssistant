import { Action} from "@ngrx/store";
import { Update } from "@ngrx/entity";

import { ScheduledClassModel } from "src/app/models/scheduled-class.model";

export enum ScheduledClassesActionTypes {
    DailyClassesLoaded = '[Daily Classes API] Daily Batch Loaded',
    DailyClassesRequestCancelled= '[Daily Classes Page] Daily Batch Request Cancelled',
    DailyClassesRequested = '[Daily Classes Page] Daily Batch Requested',
    LandingPageScheduleLoaded = '[User Landing Page] Landing Page Daily Scheduled Classes Loaded',
    LandingPageScheduleRequestCancelled = '[User Landing Page] Landing Page Scheduled Classes Request Cancelled',    
    LandingPageScheduleRequested = '[User Landing Page] Landing Daily Scheduled Classes Requested',
    ScheduledClassesCleared = '[View User Logout] All Scheduled Classes Removed',
    ScheduledClassDeletionCancelled = '[Scheduled Classes API] Removal of Scheduled Class Cancelled',
    ScheduledClassDeletionRequested = '[Scheduled Classes Daily Page/Landing Page]  Removal of Scheduled Class Requested',
    ScheduledClassDeletionSaved = '[Scheduled Classes Daily Page/Landing Page] Scheduled Class Removed',
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

export type ScheduledClassesActions = 
    DailyClassesLoaded | DailyClassesRequestCancelled | 
    DailyClassesRequested | LandingPageScheduleLoaded | 
    LandingPageScheduleRequestCancelled | LandingPageScheduleRequested | 
    ScheduledClassesCleared | ScheduledClassDeletionCancelled |
    ScheduledClassDeletionRequested | ScheduledClassDeletionSaved;