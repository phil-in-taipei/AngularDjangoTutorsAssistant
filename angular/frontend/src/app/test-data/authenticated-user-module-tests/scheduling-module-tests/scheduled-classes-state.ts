// scheduled-classes-state-mock.ts
import { Dictionary } from "@ngrx/entity";
import { 
    initialScheduledClassesState 
} from "src/app/authenticated-user/scheduling/classes-state/scheduled-classes.reducers";
import { 
    scheduledClassesByDateData,
    scheduledClassesByMonthData,
  unconfirmedStatusClassesData,
  modifyClassStatusResponse,
  scheduledClassBatchDeletionData,
  batchDeletionResponseSuccess,
  deletionResponseSuccess,
  createScheduledClassData,
  rescheduleClassData,
  scheduledClassesData,
} from "./scheduled-classes-related-tests/scheduled-classes-data";

import { ScheduledClassModel } from "src/app/models/scheduled-class.model";

const march15IDs: number[] = [
  scheduledClassesByDateData[0].id,
  scheduledClassesByDateData[1].id,
];
const marchIDs: number[] = [
  scheduledClassesByMonthData[0].id,
  scheduledClassesByMonthData[1].id,
  scheduledClassesByMonthData[2].id,
  scheduledClassesByMonthData[3].id,
];
const marchEntities: Dictionary<ScheduledClassModel> = {
  "1": scheduledClassesByMonthData[0],
  "2": scheduledClassesByMonthData[1],
  "4": scheduledClassesByMonthData[2],
  "5": scheduledClassesByMonthData[3],
};
const march15Entities: Dictionary<ScheduledClassModel> = {
  "1": scheduledClassesByDateData[0],
  "2": scheduledClassesByDateData[1],
};
const unconfirmedIDs: number[] = [
  unconfirmedStatusClassesData[0].id,
  unconfirmedStatusClassesData[1].id,
];
const unconfirmedEntities: Dictionary<ScheduledClassModel> = {
  "10": unconfirmedStatusClassesData[0],
  "11": unconfirmedStatusClassesData[1],
};
const march21IDs: number[] = [rescheduleClassData.id];
const march21Entities: Dictionary<ScheduledClassModel> = {
  "1": {
    ...scheduledClassesByDateData[0],
    date: rescheduleClassData.date,
    start_time: rescheduleClassData.start_time,
    finish_time: rescheduleClassData.finish_time,
  },
};
const march20IDs: number[] = [createScheduledClassData.student_or_class];
const march20Entities: Dictionary<ScheduledClassModel> = {
  "6": {
    id: 6,
    date: createScheduledClassData.date,
    start_time: createScheduledClassData.start_time,
    finish_time: createScheduledClassData.finish_time,
    student_or_class: createScheduledClassData.student_or_class,
    teacher: createScheduledClassData.teacher,
    class_status: "scheduled",
    teacher_notes: "",
    class_content: "",
  },
};
const marchIDsPostDeletion: number[] = [scheduledClassesByMonthData[2].id, scheduledClassesByMonthData[3].id];
const marchEntitiesPostDeletion: Dictionary<ScheduledClassModel> = {
  "4": scheduledClassesByMonthData[2],
  "5": scheduledClassesByMonthData[3],
};
const marchIDsPostBatchDeletion: number[] = [scheduledClassesByMonthData[3].id];
const marchEntitiesPostBatchDeletion: Dictionary<ScheduledClassModel> = {
  "5": scheduledClassesByMonthData[3],
};
const confirmationFailureMessage: string = "Error! Class Status Update Failed!";
const deletionSuccessMessage: string = "Scheduled class deleted successfully";
const deletionFailureMessage: string = "Error! Scheduled Class Deletion Failed!";
const newScheduledClassFailureMessage: string = "Error scheduling class!";
const newScheduledClassSuccessMessage: string = "Class scheduling successfully submitted!";
const rescheduleFailureMessage: string = "Error! Rescheduling Failed!";
const rescheduleSuccessMessage: string = "You have successfully rescheduled the class!";
const batchDeletionSuccessMessage: string = "Successfully deleted 3 scheduled classes";
const batchDeletionFailureMessage: string = "Error! Batch Deletion Failed!";

export const statePriorToNewScheduledClassSubmitted = {
  scheduledClasses: {
    ids: marchIDs,
    entities: marchEntities,
    dateRange: undefined,
    deletionModeActivated: false,
    errorMessage: undefined,
    fetchingClassesInProgress: false,
    monthlyScheduledClassesLoaded: true,
    landingPageScheduledClassesLoaded: true,
    successMessage: undefined,
    unconfirmedScheduledClassesLoaded: false,
    updatedPurchasedHours: undefined,
  },
};

export const stateAfterNewScheduledClassSubmitted = {
  scheduledClasses: {
    ids: [...marchIDs, ...march20IDs],
    entities: { ...marchEntities, ...march20Entities },
    dateRange: undefined,
    deletionModeActivated: false,
    errorMessage: undefined,
    fetchingClassesInProgress: false,
    monthlyScheduledClassesLoaded: true,
    landingPageScheduledClassesLoaded: true,
    successMessage: newScheduledClassSuccessMessage,
    unconfirmedScheduledClassesLoaded: false,
    updatedPurchasedHours: undefined,
  },
};

export const stateAfterNewScheduledClassSubmissionFailure = {
  scheduledClasses: {
    ids: marchIDs,
    entities: marchEntities,
    dateRange: undefined,
    deletionModeActivated: false,
    errorMessage: newScheduledClassFailureMessage,
    fetchingClassesInProgress: false,
    monthlyScheduledClassesLoaded: true,
    landingPageScheduledClassesLoaded: true,
    successMessage: undefined,
    unconfirmedScheduledClassesLoaded: false,
    updatedPurchasedHours: undefined,
  },
};

export const stateAfterClassStatusUpdate = {
  scheduledClasses: {
    ids: marchIDs,
    entities: {
      ...marchEntities,
      "1": modifyClassStatusResponse.scheduled_class,
    },
    dateRange: undefined,
    deletionModeActivated: false,
    errorMessage: undefined,
    fetchingClassesInProgress: false,
    monthlyScheduledClassesLoaded: true,
    landingPageScheduledClassesLoaded: true,
    successMessage: "You have successfully edited the class status!",
    unconfirmedScheduledClassesLoaded: false,
    updatedPurchasedHours: modifyClassStatusResponse.student_or_class_update,
  },
};

export const stateAfterClassStatusUpdateFailure = {
  scheduledClasses: {
    ids: marchIDs,
    entities: marchEntities,
    dateRange: undefined,
    deletionModeActivated: false,
    errorMessage: confirmationFailureMessage,
    fetchingClassesInProgress: false,
    monthlyScheduledClassesLoaded: true,
    landingPageScheduledClassesLoaded: true,
    successMessage: undefined,
    unconfirmedScheduledClassesLoaded: false,
    updatedPurchasedHours: undefined,
  },
};

export const stateAfterClassRescheduled = {
  scheduledClasses: {
    ids: [...marchIDs.filter((id) => id !== 1), ...march21IDs],
    entities: { ...marchEntities, ...march21Entities },
    dateRange: undefined,
    deletionModeActivated: false,
    errorMessage: undefined,
    fetchingClassesInProgress: false,
    monthlyScheduledClassesLoaded: true,
    landingPageScheduledClassesLoaded: true,
    successMessage: rescheduleSuccessMessage,
    unconfirmedScheduledClassesLoaded: false,
    updatedPurchasedHours: undefined,
  },
};

export const stateAfterClassRescheduleFailure = {
  scheduledClasses: {
    ids: marchIDs,
    entities: marchEntities,
    dateRange: undefined,
    deletionModeActivated: false,
    errorMessage: rescheduleFailureMessage,
    fetchingClassesInProgress: false,
    monthlyScheduledClassesLoaded: true,
    landingPageScheduledClassesLoaded: true,
    successMessage: undefined,
    unconfirmedScheduledClassesLoaded: false,
    updatedPurchasedHours: undefined,
  },
};

export const stateAfterClassDeleted = {
  scheduledClasses: {
    ids: marchIDsPostDeletion,
    entities: marchEntitiesPostDeletion,
    dateRange: undefined,
    deletionModeActivated: false,
    errorMessage: undefined,
    fetchingClassesInProgress: false,
    monthlyScheduledClassesLoaded: true,
    landingPageScheduledClassesLoaded: true,
    successMessage: deletionSuccessMessage,
    unconfirmedScheduledClassesLoaded: false,
    updatedPurchasedHours: undefined,
  },
};

export const stateAfterClassDeletionFailure = {
  scheduledClasses: {
    ids: marchIDs,
    entities: marchEntities,
    dateRange: undefined,
    deletionModeActivated: false,
    errorMessage: deletionFailureMessage,
    fetchingClassesInProgress: false,
    monthlyScheduledClassesLoaded: true,
    landingPageScheduledClassesLoaded: true,
    successMessage: undefined,
    unconfirmedScheduledClassesLoaded: false,
    updatedPurchasedHours: undefined,
  },
};

export const stateAfterBatchDeletion = {
  scheduledClasses: {
    ids: marchIDsPostBatchDeletion,
    entities: marchEntitiesPostBatchDeletion,
    dateRange: undefined,
    deletionModeActivated: false,
    errorMessage: undefined,
    fetchingClassesInProgress: false,
    monthlyScheduledClassesLoaded: true,
    landingPageScheduledClassesLoaded: true,
    successMessage: batchDeletionSuccessMessage,
    unconfirmedScheduledClassesLoaded: false,
    updatedPurchasedHours: undefined,
  },
};

export const stateAfterBatchDeletionFailure = {
  scheduledClasses: {
    ids: marchIDs,
    entities: marchEntities,
    dateRange: undefined,
    deletionModeActivated: false,
    errorMessage: batchDeletionFailureMessage,
    fetchingClassesInProgress: false,
    monthlyScheduledClassesLoaded: true,
    landingPageScheduledClassesLoaded: true,
    successMessage: undefined,
    unconfirmedScheduledClassesLoaded: false,
    updatedPurchasedHours: undefined,
  },
};
