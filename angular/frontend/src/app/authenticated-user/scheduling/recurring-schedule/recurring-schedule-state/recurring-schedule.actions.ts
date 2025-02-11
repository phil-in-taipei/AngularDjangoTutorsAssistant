import { Action} from "@ngrx/store";

import { 
    RecurringClassCreateModel, RecurringClassModel 
} from "src/app/models/recurring-schedule.model";

export enum RecurringClassesActionTypes {
  RecurringClassesCleared = '[View User Logout] All Recurring Classes Removed',
  RecurringClassesRequested = '[Recurring Classes Component View] Recurring Classes Requested',
  RecurringClassesRequestCancelled= '[Recurring Classes Component View] Recurring Classes Request Cancelled',
  RecurringClassesLoaded = '[Recurring Classes API] Recurring Classes Loaded',
  RecurringClassCreateSubmitted = '[Create Recurring Class Page] Recurring Class Submitted',
  RecurringClassAdded = '[Create Recurring Class Page] Newly Created Task with Daily Batch Added',
  RecurringClassCreationCancelled = '[Create Recurring Class Page] Recurring Class Creation Cancelled',
  RecurringClassDeletionCancelled = '[Recurring Classes Page] Removal of Recurring Class Cancelled',
  RecurringClassDeletionRequested = '[Recurring Classes  Page]  Removal of Recurring Class Requested',
  RecurringClassDeletionSaved = '[Recurring Classes Page] Recurring Class Removed',
  RecurringClassesMessagesCleared = '[Recurring Class List, and Submission Pages] Recurring Class Messages Cleared',
}

export class RecurringClassesCleared implements Action {
  readonly type = RecurringClassesActionTypes.RecurringClassesCleared;
}

export class RecurringClassesLoaded implements Action {
  readonly type = RecurringClassesActionTypes.RecurringClassesLoaded;

  constructor(
    public payload: { monthlyTasks: RecurringClassModel[] }
  ) {}
}

export class RecurringClassesRequestCancelled implements Action {
  readonly type = RecurringClassesActionTypes.RecurringClassesRequestCancelled;

  constructor(public payload: {  err: any }) {}
}

export class RecurringClassesRequested implements Action {
  readonly type = RecurringClassesActionTypes.RecurringClassesRequested;
}

export class RecurringClassCreateSubmitted implements Action {
  readonly type = RecurringClassesActionTypes.RecurringClassCreateSubmitted;

  constructor(
    public payload: { monthlyTask: RecurringClassCreateModel }
  ){}
};

export class RecurringClassAdded implements Action {
  readonly type = RecurringClassesActionTypes.RecurringClassAdded;

  constructor(
    public payload: { recurringClass: RecurringClassModel }
  ) {}
}

export class RecurringClassCreationCancelled implements Action {
  readonly type = RecurringClassesActionTypes.RecurringClassCreationCancelled;

  constructor(public payload: {  err: any }) {}
}

export class RecurringClassDeletionCancelled implements Action {
  readonly type = RecurringClassesActionTypes.RecurringClassDeletionCancelled;

  constructor(public payload: {  err: any }) {}
}

export class RecurringClassDeletionRequested implements Action {
  readonly type = RecurringClassesActionTypes.RecurringClassDeletionRequested;

  constructor(public payload: { id: number }) {}
}

export class RecurringClassDeletionSaved implements Action {
  readonly type = RecurringClassesActionTypes.RecurringClassDeletionSaved;

  constructor(public payload: { id: number, message: string }) {}
}

export class RecurringClassesMessagesCleared implements Action {
  readonly type = RecurringClassesActionTypes.RecurringClassesMessagesCleared;
}

export type RecurringClassActions = RecurringClassesCleared |
  RecurringClassesLoaded | RecurringClassesRequestCancelled |
  RecurringClassesRequested | RecurringClassCreateSubmitted |
  RecurringClassAdded | RecurringClassCreationCancelled |
  RecurringClassDeletionCancelled | RecurringClassDeletionRequested |
  RecurringClassDeletionSaved | RecurringClassesMessagesCleared;
