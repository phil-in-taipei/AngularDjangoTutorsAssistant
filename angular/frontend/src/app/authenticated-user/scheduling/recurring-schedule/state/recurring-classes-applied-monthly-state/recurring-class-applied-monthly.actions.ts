import { Action } from '@ngrx/store';

import { 
    RecurringClassAppliedMonthlyCreateModel, 
    RecurringClassAppliedMonthlyDeletionResponse,
    RecurringClassAppliedMonthlyModel 
} from "src/app/models/recurring-schedule.model";

export enum RecurringClassAppliedMonthlyActionTypes {
    RecurringClassAppliedMonthlysCleared = '[View User Logout] All Recurring Classes Applied Monthly Removed',
    RecurringClassAppliedMonthlysRequested = '[Recurring Classes Applied Monthly Component View] Recurring Classes Applied Monthly Requested',
    RecurringClassAppliedMonthlysRequestCancelled= '[Recurring Classes Applied Monthly Component View] Recurring Classes Applied Monthly Request Cancelled',
    RecurringClassAppliedMonthlysLoaded = '[Recurring Class Applied Monthly API] Recurring Classes Applied Monthly Loaded',
    RecurringClassAppliedMonthlyCreateSubmitted = '[Create Recurring Class Page] Recurring Class Applied Monthly Submitted',
    RecurringClassAppliedMonthlyAdded = '[Create Recurring Class Applied Monthly Page] Newly Created Monthly Applied Monthly Added',
    RecurringClassAppliedMonthlyCreationCancelled = '[Create Recurring Class Applied Monthly Page] Recurring Class Applied Monthly Creation Cancelled',
    RecurringClassAppliedMonthlyDeletionCancelled = '[Recurring Class Applied Monthlys Page] Removal of Recurring Class Applied Monthly Cancelled',
    RecurringClassAppliedMonthlyDeletionModeActivated = '[Recurring Classes Applied Monthly List Page] Recurring Class Applied Monthly Deletion Mode Activated',
    RecurringClassAppliedMonthlyDeletionModeDeactivated = '[Recurring Classes Applied Monthly List Page] Recurring Class Applied Monthly Deletion Mode Deactivated',
    RecurringClassAppliedMonthlyDeletionRequested = '[Recurring Class Applied Monthlys Page]  Removal of Recurring Class Applied Monthly Requested',
    RecurringClassAppliedMonthlyDeletionSaved = '[Recurring Class Applied Monthlys Page] Recurring Class Applied Monthly Removed',
    RecurringClassesAppliedMonthlyMessagesCleared = '[Recurring Class Applied Monthly List, and Submission Pages] Recurring Classes Applied Monthly Messages Cleared',
}

export class RecurringClassAppliedMonthlysCleared implements Action {
    readonly type = RecurringClassAppliedMonthlyActionTypes.RecurringClassAppliedMonthlysCleared;
}

export class RecurringClassAppliedMonthlysLoaded implements Action {
    readonly type = RecurringClassAppliedMonthlyActionTypes.RecurringClassAppliedMonthlysLoaded;

    constructor(
        public payload: { recurringClassesAppliedMonthly: RecurringClassAppliedMonthlyModel[] }
    ) {}
}

export class RecurringClassAppliedMonthlysRequestCancelled implements Action {
    readonly type = RecurringClassAppliedMonthlyActionTypes.RecurringClassAppliedMonthlysRequestCancelled;

    constructor(public payload: { err: any }) {}
}

export class RecurringClassAppliedMonthlysRequested implements Action {
    readonly type = RecurringClassAppliedMonthlyActionTypes.RecurringClassAppliedMonthlysRequested;

    constructor(
        public payload: { month: number, year: number }
    ) {}
}

export class RecurringClassAppliedMonthlyCreateSubmitted implements Action {
    readonly type = RecurringClassAppliedMonthlyActionTypes.RecurringClassAppliedMonthlyCreateSubmitted;

    constructor(
        public payload: { recurringClassAppliedMonthly: RecurringClassAppliedMonthlyCreateModel }
    ){}
}

export class RecurringClassAppliedMonthlyAdded implements Action {
    readonly type = RecurringClassAppliedMonthlyActionTypes.RecurringClassAppliedMonthlyAdded;

    constructor(
        public payload: { recurringClassAppliedMonthly: RecurringClassAppliedMonthlyModel }
    ) {}
}

export class RecurringClassAppliedMonthlyCreationCancelled implements Action {
    readonly type = RecurringClassAppliedMonthlyActionTypes.RecurringClassAppliedMonthlyCreationCancelled;

    constructor(public payload: { err: any }) {}
}

export class RecurringClassAppliedMonthlyDeletionCancelled implements Action {
    readonly type = RecurringClassAppliedMonthlyActionTypes.RecurringClassAppliedMonthlyDeletionCancelled;

    constructor(public payload: { err: any }) {}
}

export class RecurringClassAppliedMonthlyDeletionModeActivated implements Action {
    readonly type = RecurringClassAppliedMonthlyActionTypes.RecurringClassAppliedMonthlyDeletionModeActivated;
}

export class RecurringClassAppliedMonthlyDeletionModeDeactivated implements Action {
    readonly type = RecurringClassAppliedMonthlyActionTypes.RecurringClassAppliedMonthlyDeletionModeDeactivated;
}

export class RecurringClassAppliedMonthlyDeletionRequested implements Action {
    readonly type = RecurringClassAppliedMonthlyActionTypes.RecurringClassAppliedMonthlyDeletionRequested;

    constructor(public payload: { id: number }) {}
}

export class RecurringClassAppliedMonthlyDeletionSaved implements Action {
    readonly type = RecurringClassAppliedMonthlyActionTypes.RecurringClassAppliedMonthlyDeletionSaved;
    constructor(public payload: {
        recurringClassAppliedMonthlyDeletionResponse:  RecurringClassAppliedMonthlyDeletionResponse
    }) {}
}

export class RecurringClassesAppliedMonthlyMessagesCleared implements Action {
    readonly type = RecurringClassAppliedMonthlyActionTypes.RecurringClassesAppliedMonthlyMessagesCleared;
}

export type RecurringClassAppliedMonthlyActions = RecurringClassAppliedMonthlysCleared |
    RecurringClassAppliedMonthlysLoaded | RecurringClassAppliedMonthlysRequestCancelled |
    RecurringClassAppliedMonthlysRequested | RecurringClassAppliedMonthlyCreateSubmitted |
    RecurringClassAppliedMonthlyAdded | RecurringClassAppliedMonthlyCreationCancelled |
    RecurringClassAppliedMonthlyDeletionCancelled | RecurringClassAppliedMonthlyDeletionRequested |
    RecurringClassAppliedMonthlyDeletionModeActivated | RecurringClassAppliedMonthlyDeletionModeDeactivated | 
    RecurringClassAppliedMonthlyDeletionSaved | RecurringClassesAppliedMonthlyMessagesCleared;