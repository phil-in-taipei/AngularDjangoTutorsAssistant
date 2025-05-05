import { Action} from "@ngrx/store";
import { Update } from "@ngrx/entity";

import { 
    StudentOrClassCreateAndEditModel, StudentOrClassEditModel,
    StudentOrClassModel 
} from "src/app/models/student-or-class.model";


export enum StudentOrClassActionTypes {
    FreelanceAccountPurchasedHoursSaved = '[Make Purchase Page] Amount of Purchased Hours Updated Following Purchase Transaction',
    FreelanceAccountRefundedHoursSaved = '[Make Refund Page] Amount of Purchased Hours Updated Following Refund Transaction',
    StudentOrClassCreateSubmitted = '[Create Student Or Class Page] Student Or Class Submitted',
    StudentOrClassCreatedAdded = '[Create Student Or Class Page] Newly Created Student Or Class Added',
    StudentOrClassCreationCancelled = '[Create Student Or Class Page] Student Or Class Creation Cancelled',
    StudentOrClassDeletionCancelled = '[Students Or Classes List Page] Removal of Student Or Class Cancelled',
    StudentOrClassDeletionModeActivated = '[Students Or Classes List Page] Students Or Classes Deletion Mode Activated',
    StudentOrClassDeletionModeDeactivated = '[Students Or Classes List Page] Students Or Classes Deletion Mode Deactivated',    
    StudentOrClassDeletionRequested = '[Students Or Classes List Page]  Removal of Student Or Class Requested',
    StudentOrClassDeletionSaved = '[Students Or Classes List Page] Student Or Class Removed',
    StudentOrClassEditCancelled= '[Student Or Class Detail Page] Edit Student Or Class Cancelled',
    StudentOrClassEditSubmitted = '[Student Or Class Detail Page] Edited Student Or Class Submitted',
    StudentOrClassEditUpdated = '[Student Or Class Detail Page] Edited Student Or Class Updated',
    StudentOrClassPurchasedHoursUpdated = '[Scheduled Class Detail Page] Freelance Student Purchased Hours Updated',
    StudentsOrClassesMessagesCleared = '[Students Or Classes List, Detail, and Submission Pages] Students Or Classes Messages Cleared',
    StudentsOrClassesCleared = '[View User Logout] All Students Or Classes Removed',
    StudentsOrClassesLoaded = '[StudentOrClasses API] Students Or Classes Loaded',
    StudentsOrClassesRequested = '[Authenicated User Component View] Users Students Or Classes Requested',
    StudentsOrClassesRequestCancelled= '[Authenticated User Component View] Users Students Or Classes Request Cancelled',
};

export class FreelanceAccountPurchasedHoursSaved implements Action {
    readonly type = StudentOrClassActionTypes.FreelanceAccountPurchasedHoursSaved;
  
    constructor(
        public payload: { 
            class_hours_purchased_or_refunded: number, 
            studentOrClass: StudentOrClassModel
        }
    ) {}
}

export class FreelanceAccountRefundedHoursSaved implements Action {
    readonly type = StudentOrClassActionTypes.FreelanceAccountRefundedHoursSaved;
  
    constructor(
        public payload: { 
            class_hours_purchased_or_refunded: number, 
            studentOrClass: StudentOrClassModel
        }
    ) {}
}

export class StudentOrClassCreatedAdded implements Action {
    readonly type = StudentOrClassActionTypes.StudentOrClassCreatedAdded;

    constructor(
        public payload: { studentOrClass: StudentOrClassModel }
    ) {}
}

export class StudentOrClassCreateSubmitted implements Action {
    readonly type = StudentOrClassActionTypes.StudentOrClassCreateSubmitted;

    constructor(
        public payload: { studentOrClass: StudentOrClassCreateAndEditModel }
    ){}
};

export class StudentOrClassCreationCancelled implements Action {
    readonly type = StudentOrClassActionTypes.StudentOrClassCreationCancelled;

    constructor(public payload: {  err: any }) {}
}

export class StudentOrClassDeletionCancelled implements Action {
    readonly type = StudentOrClassActionTypes.StudentOrClassDeletionCancelled;

    constructor(public payload: {  err: any }) {}
}

export class StudentOrClassDeletionModeActivated implements Action {
    readonly type = StudentOrClassActionTypes.StudentOrClassDeletionModeActivated;
}

export class StudentOrClassDeletionModeDeactivated implements Action {
    readonly type = StudentOrClassActionTypes.StudentOrClassDeletionModeDeactivated;
}

export class StudentOrClassDeletionRequested implements Action {
    readonly type = StudentOrClassActionTypes.StudentOrClassDeletionRequested;

    constructor(public payload: { id: number }) {}
}

export class StudentOrClassDeletionSaved implements Action {
    readonly type = StudentOrClassActionTypes.StudentOrClassDeletionSaved;

    constructor(public payload: { id: number, message: string }) {}
}

export class StudentOrClassEditCancelled implements Action {
    readonly type = StudentOrClassActionTypes.StudentOrClassEditCancelled;

    constructor(public payload: {  err: any }) {}
}

export class StudentOrClassEditSubmitted implements Action {
    readonly type = StudentOrClassActionTypes.StudentOrClassEditSubmitted;

    constructor(
        public payload:
            {
                id: number, studentOrClass: StudentOrClassEditModel
            }
    ) {}
}

export class StudentOrClassEditUpdated implements Action {
    readonly type = StudentOrClassActionTypes.StudentOrClassEditUpdated;

    constructor(public payload: {  studentOrClass: Update<StudentOrClassModel> }) {
    }
}

export class StudentOrClassPurchasedHoursUpdated implements Action {
    readonly type = StudentOrClassActionTypes.StudentOrClassPurchasedHoursUpdated;

    constructor(public payload: {  studentOrClass: Update<StudentOrClassModel> }) {
    }
}

export class StudentsOrClassesCleared implements Action {
    readonly type = StudentOrClassActionTypes.StudentsOrClassesCleared;
}

export class StudentsOrClassesLoaded implements Action {
    readonly type = StudentOrClassActionTypes.StudentsOrClassesLoaded;

    constructor(
      public payload: { studentsOrClasses: StudentOrClassModel[] }
    ) {}
  }

export class StudentsOrClassesMessagesCleared implements Action {
    readonly type = StudentOrClassActionTypes.StudentsOrClassesMessagesCleared;
}

export class StudentsOrClassesRequestCancelled implements Action {
    readonly type = StudentOrClassActionTypes.StudentsOrClassesRequestCancelled;

    constructor(public payload: {  err: any }) {}
  }

export class StudentsOrClassesRequested implements Action {
    readonly type = StudentOrClassActionTypes.StudentsOrClassesRequested;
  }

export type StudentOrClassActions = FreelanceAccountPurchasedHoursSaved |
    FreelanceAccountRefundedHoursSaved | StudentOrClassCreatedAdded | 
    StudentOrClassCreateSubmitted | StudentOrClassCreationCancelled | 
    StudentOrClassDeletionCancelled | StudentOrClassDeletionModeActivated |
    StudentOrClassDeletionModeDeactivated |StudentOrClassDeletionRequested | 
    StudentOrClassDeletionSaved | StudentOrClassEditCancelled |
    StudentOrClassEditSubmitted | StudentOrClassEditUpdated |
    StudentsOrClassesCleared |  StudentsOrClassesLoaded | 
    StudentsOrClassesMessagesCleared | StudentsOrClassesRequestCancelled | 
    StudentsOrClassesRequested  | StudentOrClassPurchasedHoursUpdated;
