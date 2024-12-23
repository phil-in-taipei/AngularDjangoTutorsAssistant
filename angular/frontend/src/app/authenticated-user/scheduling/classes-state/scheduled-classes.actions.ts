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

export type ScheduledClassesActions = 
    DailyClassesLoaded | DailyClassesRequestCancelled | 
    DailyClassesRequested | LandingPageScheduleLoaded | 
    LandingPageScheduleRequestCancelled | LandingPageScheduleRequested;