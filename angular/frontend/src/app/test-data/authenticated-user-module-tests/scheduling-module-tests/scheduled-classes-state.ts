// scheduled-classes-state-mock.ts
import { Dictionary } from "@ngrx/entity";
import { 
    initialScheduledClassesState, compareByDateAndTime
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

const confirmationFailureMessage: string = "Error! Class Status Update Failed!";
const deletionSuccessMessage: string = "Scheduled class deleted successfully";
const deletionFailureMessage: string = "Error! Scheduled Class Deletion Failed!";
const newScheduledClassFailureMessage: string = "Error scheduling class!";
const newScheduledClassSuccessMessage: string = "Class scheduling successfully submitted!";
const rescheduleFailureMessage: string = "Error! Rescheduling Failed!";
const rescheduleSuccessMessage: string = "You have successfully rescheduled the class!";
const batchDeletionSuccessMessage: string = "Successfully deleted 3 scheduled classes";
const batchDeletionFailureMessage: string = "Error! Batch Deletion Failed!";

// scheduled-classes-state-mock.ts
// ... (previous imports and constants)


// Helper function to sort ScheduledClassModel arrays
function sortScheduledClasses(classes: ScheduledClassModel[]): ScheduledClassModel[] {
  return [...classes].sort(compareByDateAndTime);
}

// Helper function to create sorted ids and entities
function createSortedState(classes: ScheduledClassModel[]): { ids: number[]; entities: Dictionary<ScheduledClassModel> } {
  const sortedClasses = sortScheduledClasses(classes);
  const ids = sortedClasses.map((sc) => sc.id);
  const entities = sortedClasses.reduce((acc, sc) => ({ ...acc, [sc.id]: sc }), {});
  return { ids, entities };
}

// Update all mock state objects to use sorted data
const { ids: marchIDs, entities: marchEntities } = createSortedState(scheduledClassesByMonthData);
const { ids: march15IDs, entities: march15Entities } = createSortedState(scheduledClassesByDateData);
const { ids: unconfirmedIDs, entities: unconfirmedEntities } = createSortedState(unconfirmedStatusClassesData);
const { ids: march21IDs, entities: march21Entities } = createSortedState([
  {
    ...scheduledClassesByDateData[0],
    date: rescheduleClassData.date,
    start_time: rescheduleClassData.start_time,
    finish_time: rescheduleClassData.finish_time,
  },
]);
const { ids: march20IDs, entities: march20Entities } = createSortedState([
  {
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
]);
const { ids: marchIDsPostDeletion, entities: marchEntitiesPostDeletion } = createSortedState(
  scheduledClassesByMonthData.filter((sc) => sc.id !== 1)
);
const { ids: marchIDsPostBatchDeletion, entities: marchEntitiesPostBatchDeletion } = createSortedState(
  scheduledClassesByMonthData.filter((sc) => !scheduledClassBatchDeletionData.obsolete_class_ids.includes(sc.id))
);

// Update all state objects to use sorted ids and entities
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
    ids: [1,2,6,4,5], //[...marchIDs, ...march20IDs],
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

// ... (update all other state objects similarly)

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
    ids: [2, 1, 4, 5],//[...marchIDs.filter((id) => id !== 1), ...march21IDs],
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
