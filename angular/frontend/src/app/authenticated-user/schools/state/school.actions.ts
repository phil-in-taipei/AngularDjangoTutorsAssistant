import { Action} from "@ngrx/store";
import { Update } from "@ngrx/entity";

import { 
    SchoolCreateAndEditModel, SchoolModel 
} from "src/app/models/school.model";


export enum SchoolActionTypes {
    SchoolCreateSubmitted = '[Create School Page] School Submitted',
    SchoolCreatedAdded = '[Create School Page] Newly Created School Added',
    SchoolCreationCancelled = '[Create School Page] School Creation Cancelled',
    SchoolDeletionCancelled = '[Schools List Page] Removal of School Cancelled',
    SchoolDeletionRequested = '[Schools List Page]  Removal of School Requested',
    SchoolDeletionSaved = '[School List Page] School Removed',
    SchoolEditCancelled= '[School Detail Page] Edit School Cancelled',
    SchoolEditSubmitted = '[School Detail Page] Edited School Submitted',
    SchoolEditUpdated = '[School Detail Page] Edited School Updated',
    SchoolsMessagesCleared = '[School List, Detail, and Submission Pages] School Messages Cleared',
    SchoolsCleared = '[View User Logout] All Schools Removed',
    SchoolsLoaded = '[Schools API] Schools Loaded',
    SchoolsRequested = '[Authenicated User Component View] Users Schools Requested',
    SchoolsRequestCancelled= '[Authenticated User Component View] Users Schools Request Cancelled',
};

export class SchoolCreatedAdded implements Action {
    readonly type = SchoolActionTypes.SchoolCreatedAdded;
  
    constructor(
        public payload: { school: SchoolModel }
    ) {}
}

export class SchoolCreateSubmitted implements Action {
    readonly type = SchoolActionTypes.SchoolCreateSubmitted;
  
    constructor(
        public payload: { school: SchoolCreateAndEditModel }
    ){}
};

export class SchoolCreationCancelled implements Action {
    readonly type = SchoolActionTypes.SchoolCreationCancelled;
  
    constructor(public payload: {  err: any }) {}
}

export class SchoolDeletionCancelled implements Action {
    readonly type = SchoolActionTypes.SchoolDeletionCancelled;
  
    constructor(public payload: {  err: any }) {}
}

export class SchoolDeletionRequested implements Action {
    readonly type = SchoolActionTypes.SchoolDeletionRequested;
  
    constructor(public payload: { id: number }) {}
}

export class SchoolDeletionSaved implements Action {
    readonly type = SchoolActionTypes.SchoolDeletionSaved;
  
    constructor(public payload: { id: number, message: string }) {}
}

export class SchoolEditCancelled implements Action {
    readonly type = SchoolActionTypes.SchoolEditCancelled;
  
    constructor(public payload: {  err: any }) {}
}

export class SchoolEditSubmitted implements Action {
    readonly type = SchoolActionTypes.SchoolEditSubmitted;

    constructor(
        public payload: 
            {  
                id: number, school: SchoolCreateAndEditModel 
            }
    ) {}
}

export class SchoolEditUpdated implements Action {
    readonly type = SchoolActionTypes.SchoolEditUpdated;
  
    constructor(public payload: {  school: Update<SchoolModel> }) {
    }
}

export class SchoolsCleared implements Action {
    readonly type = SchoolActionTypes.SchoolsCleared;
}

export class SchoolsLoaded implements Action {
    readonly type = SchoolActionTypes.SchoolsLoaded;
  
    constructor(
      public payload: { schools: SchoolModel[] }
    ) {}
  }

export class SchoolsMessagesCleared implements Action {
    readonly type = SchoolActionTypes.SchoolsMessagesCleared;
}

export class SchoolsRequestCancelled implements Action {
    readonly type = SchoolActionTypes.SchoolsRequestCancelled;
  
    constructor(public payload: {  err: any }) {}
  }
  
export class SchoolsRequested implements Action {
    readonly type = SchoolActionTypes.SchoolsRequested;
  }

export type SchoolActions = SchoolCreatedAdded | SchoolCreateSubmitted |
    SchoolCreationCancelled | SchoolDeletionCancelled |
    SchoolDeletionRequested | SchoolDeletionSaved |
    SchoolEditCancelled |SchoolEditSubmitted | SchoolEditUpdated | 
    SchoolsCleared | SchoolsLoaded | SchoolsMessagesCleared |
    SchoolsRequestCancelled | SchoolsRequested;
