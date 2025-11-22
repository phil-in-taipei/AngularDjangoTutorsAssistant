import { Dictionary } from "@ngrx/entity";
import { 
  recurringClassAppliedMonthlyData,
  recurringClassAppliedMonthliesData,
  recurringClassAppliedMonthlyDeletionResponse,
  newlyCreatedRecurringClassAppliedMonthlyData,
  scheduledClassBatchDeletionData
} from "./recurring-schedule-data";
import { 
  RecurringClassAppliedMonthlyModel 
} from "src/app/models/recurring-schedule.model";
import { 
  ScheduledClassBatchDeletionDataModel 
} from "src/app/models/scheduled-class.model";

// -----------------------------------------------------------------------------
// Mock Entity Collections
// -----------------------------------------------------------------------------

// IDs before any new submission
const recurringClassAppliedMonthlyIdsPriorToSubmission: number[] = [
  recurringClassAppliedMonthliesData[0].id,
  recurringClassAppliedMonthliesData[1].id,
  recurringClassAppliedMonthliesData[2].id,
];

// IDs after new monthly application (added recurringClassAppliedMonthlyData)
const recurringClassAppliedMonthlyIdsAfterPost: number[] = [
  newlyCreatedRecurringClassAppliedMonthlyData.id,
  ...recurringClassAppliedMonthlyIdsPriorToSubmission,
];

// Entities dictionary before POST
const entitiesPriorToSubmission: Dictionary<RecurringClassAppliedMonthlyModel> = {
  [recurringClassAppliedMonthliesData[0].id]: recurringClassAppliedMonthliesData[0],
  [recurringClassAppliedMonthliesData[1].id]: recurringClassAppliedMonthliesData[1],
  [recurringClassAppliedMonthliesData[2].id]: recurringClassAppliedMonthliesData[2],
};

// Entities dictionary after POST (includes the new record)
const entitiesAfterPost: Dictionary<RecurringClassAppliedMonthlyModel> = {
  [newlyCreatedRecurringClassAppliedMonthlyData.id]: newlyCreatedRecurringClassAppliedMonthlyData,
  [recurringClassAppliedMonthliesData[0].id]: recurringClassAppliedMonthliesData[0],
  [recurringClassAppliedMonthliesData[1].id]: recurringClassAppliedMonthliesData[1],
  [recurringClassAppliedMonthliesData[2].id]: recurringClassAppliedMonthliesData[2],
};

// -----------------------------------------------------------------------------
// Mock messages for UI assertions
// -----------------------------------------------------------------------------

const deletionFailureMessage: string = "Error! Recurring Class Applied Monthly Deletion Failed!";
const deletionSuccessMessage: string = "Recurring Class Applied Monthly successfully deleted!";
const fetchFailureMessage: string = "Error fetching recurring classes applied monthly!";
const submissionFailureMessage: string = "Error submitting recurring class application!";
const submissionSuccessMessage: string = "Recurring Class Applied Monthly successfully submitted!";

// -----------------------------------------------------------------------------
// Mock optional batch deletion data
// -----------------------------------------------------------------------------

const optionalBatchDeletionData: ScheduledClassBatchDeletionDataModel = {
  ...scheduledClassBatchDeletionData
};

// -----------------------------------------------------------------------------
// Mock ngrx/entity state snapshots for unit testing
// -----------------------------------------------------------------------------

export const statePriorToNewRecurringClassAppliedMonthlySubmission = {
  recurringClassAppliedMonthlys: {
    ids: recurringClassAppliedMonthlyIdsPriorToSubmission,
    entities: entitiesPriorToSubmission,
    deletionModeActivated: false,
    errorMessage: undefined,
    recurringClassAppliedMonthlysLoaded: true,
    successMessage: undefined,
    optionalBatchDeletionData: undefined
  }
};

export const stateAfterNewRecurringClassAppliedMonthlySubmission = {
  recurringClassAppliedMonthlys: {
    ids: recurringClassAppliedMonthlyIdsAfterPost,
    entities: entitiesAfterPost,
    deletionModeActivated: false,
    errorMessage: undefined,
    recurringClassAppliedMonthlysLoaded: true,
    successMessage: submissionSuccessMessage,
    optionalBatchDeletionData: undefined
  }
};

export const stateAfterNewRecurringClassAppliedMonthlySubmissionFailure = {
  recurringClassAppliedMonthlys: {
    ids: recurringClassAppliedMonthlyIdsPriorToSubmission,
    entities: entitiesPriorToSubmission,
    deletionModeActivated: false,
    errorMessage: submissionFailureMessage,
    recurringClassAppliedMonthlysLoaded: true,
    successMessage: undefined,
    optionalBatchDeletionData: undefined
  }
};

export const stateFollowingRecurringClassAppliedMonthlyDeletion = {
  recurringClassAppliedMonthlys: {
    ids: recurringClassAppliedMonthlyIdsPriorToSubmission.slice(0, 2), // assuming last item deleted
    entities: {
      [recurringClassAppliedMonthliesData[0].id]: recurringClassAppliedMonthliesData[0],
      [recurringClassAppliedMonthliesData[1].id]: recurringClassAppliedMonthliesData[1],
    },
    deletionModeActivated: false,
    errorMessage: undefined,
    recurringClassAppliedMonthlysLoaded: true,
    successMessage: deletionSuccessMessage,
    optionalBatchDeletionData: optionalBatchDeletionData
  }
};

export const stateFollowingRecurringClassAppliedMonthlyDeletionFailure = {
  recurringClassAppliedMonthlys: {
    ids: recurringClassAppliedMonthlyIdsPriorToSubmission,
    entities: entitiesPriorToSubmission,
    deletionModeActivated: false,
    errorMessage: deletionFailureMessage,
    recurringClassAppliedMonthlysLoaded: true,
    successMessage: undefined,
    optionalBatchDeletionData: undefined
  }
};

export const stateFollowingRecurringClassAppliedMonthlyFetchFailure = {
  recurringClassAppliedMonthlys: {
    ids: [],
    entities: {},
    deletionModeActivated: false,
    errorMessage: fetchFailureMessage,
    recurringClassAppliedMonthlysLoaded: false,
    successMessage: undefined,
    optionalBatchDeletionData: undefined
  }
};
