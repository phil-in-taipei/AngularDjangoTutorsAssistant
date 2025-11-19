import { Dictionary } from "@ngrx/entity";
import { 
  recurringClassData, 
  recurringClassesData,
  recurringClassCreatedResponseData 
} from "./recurring-schedule-data"; // <-- Your existing mock data file
import { RecurringClassModel } from "src/app/models/recurring-schedule.model";

// --- Define the ID arrays for before and after POST operations ---

const recurringClassIdsPriorToSubmission: number[] = [
  recurringClassesData[0].id,
  recurringClassesData[1].id,
  recurringClassesData[2].id
];

const recurringClassIdsAfterPost: number[] = [
  ...recurringClassIdsPriorToSubmission,
  recurringClassCreatedResponseData.id // Assuming this is the new one created in the test
];

// --- Define entity dictionaries (keyed by ID as strings) ---

const entitiesPriorToSubmission: Dictionary<RecurringClassModel> = {
  [recurringClassesData[0].id]: recurringClassesData[0],
  [recurringClassesData[1].id]: recurringClassesData[1],
  [recurringClassesData[2].id]: recurringClassesData[2],
};

const entitiesAfterPost: Dictionary<RecurringClassModel> = {
  [recurringClassesData[0].id]: recurringClassesData[0],
  [recurringClassesData[1].id]: recurringClassesData[1],
  [recurringClassesData[2].id]: recurringClassesData[2],
  [recurringClassCreatedResponseData.id]: recurringClassCreatedResponseData,
};

// --- Define success & error messages for test assertions ---

const deletionFailureMessage: string = "Error! Recurring Class Deletion Failed!";
const deletionSuccessMessage: string = "Recurring Class successfully deleted!";
const fetchFailureMessage: string = "Error fetching recurring classes!";
const submissionFailureMessage: string = "Error submitting recurring class!";
const submissionSuccessMessage: string = "Recurring Class successfully submitted!";

// --- Define ngrx/entity state snapshots for different test conditions ---

export const statePriorToNewRecurringClassSubmission = {
  recurringClasses: {
    ids: recurringClassIdsPriorToSubmission,
    entities: entitiesPriorToSubmission,
    deletionModeActivated: false,
    errorMessage: undefined,
    recurringClassesLoaded: true,
    successMessage: undefined
  }
};

export const stateAfterNewRecurringClassSubmission = {
  recurringClasses: {
    ids: recurringClassIdsAfterPost,
    entities: entitiesAfterPost,
    deletionModeActivated: false,
    errorMessage: undefined,
    recurringClassesLoaded: true,
    successMessage: submissionSuccessMessage
  }
};

export const stateAfterNewRecurringClassSubmissionFailure = {
  recurringClasses: {
    ids: recurringClassIdsPriorToSubmission,
    entities: entitiesPriorToSubmission,
    deletionModeActivated: false,
    errorMessage: submissionFailureMessage,
    recurringClassesLoaded: true,
    successMessage: undefined
  }
};

export const stateFollowingRecurringClassDeletion = {
  recurringClasses: {
    ids: recurringClassIdsPriorToSubmission.slice(0, 2), // e.g. one deleted
    entities: {
      [recurringClassesData[0].id]: recurringClassesData[0],
      [recurringClassesData[1].id]: recurringClassesData[1],
    },
    deletionModeActivated: false,
    errorMessage: undefined,
    recurringClassesLoaded: true,
    successMessage: deletionSuccessMessage
  }
};

export const stateFollowingRecurringClassDeletionFailure = {
  recurringClasses: {
    ids: recurringClassIdsPriorToSubmission,
    entities: entitiesPriorToSubmission,
    deletionModeActivated: false,
    errorMessage: deletionFailureMessage,
    recurringClassesLoaded: true,
    successMessage: undefined
  }
};

export const stateFollowingRecurringClassFetchFailure = {
  recurringClasses: {
    ids: [],
    entities: {},
    deletionModeActivated: false,
    errorMessage: fetchFailureMessage,
    recurringClassesLoaded: false,
    successMessage: undefined
  }
};
