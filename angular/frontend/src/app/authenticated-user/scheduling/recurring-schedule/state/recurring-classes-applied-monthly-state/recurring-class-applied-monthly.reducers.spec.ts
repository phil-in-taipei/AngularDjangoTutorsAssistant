import { 
    initialRecurringClassAppliedMonthlysState, 
    recurringClassAppliedMonthlysReducer 
} from "./recurring-class-applied-monthly.reducers";

import { 
    recurringClassAppliedMonthliesData,
    recurringClassAppliedMonthlyData,
    recurringClassAppliedMonthlyDeletionResponse,
    newlyCreatedRecurringClassAppliedMonthlyData
} from "src/app/test-data/authenticated-user-module-tests/scheduling-module-tests/scheduled-classes-related-tests/recurring-schedule-module-tests/recurring-schedule-related-tests/recurring-schedule-data";
import { 
    statePriorToNewRecurringClassAppliedMonthlySubmission,
    stateAfterNewRecurringClassAppliedMonthlySubmissionFailure, 
    stateAfterNewRecurringClassAppliedMonthlySubmission, 
    stateFollowingRecurringClassAppliedMonthlyDeletion, 
    stateFollowingRecurringClassAppliedMonthlyDeletionFailure,
    stateFollowingRecurringClassAppliedMonthlyFetchFailure
} from "src/app/test-data/authenticated-user-module-tests/scheduling-module-tests/scheduled-classes-related-tests/recurring-schedule-module-tests/recurring-schedule-related-tests/recurring-schedule-applied-monthly-state";

import { 
    RecurringClassAppliedMonthlysCleared, 
    RecurringClassAppliedMonthlyAdded, 
    RecurringClassAppliedMonthlyCreationCancelled, 
    RecurringClassAppliedMonthlyDeletionCancelled, 
    RecurringClassAppliedMonthlyDeletionSaved, 
    RecurringClassAppliedMonthlysLoaded,
    RecurringClassAppliedMonthlysRequestCancelled,
    RecurringClassesAppliedMonthlyMessagesCleared,
    RecurringClassAppliedMonthlyDeletionModeActivated,
    RecurringClassAppliedMonthlyDeletionModeDeactivated
} from "./recurring-class-applied-monthly.actions";

fdescribe('recurringClassAppliedMonthlysReducer', () => {

    it('returns an initial state when cleared', () => {
        const state = recurringClassAppliedMonthlysReducer(
            initialRecurringClassAppliedMonthlysState, 
            new RecurringClassAppliedMonthlysCleared()
        );
        expect(state).toEqual(initialRecurringClassAppliedMonthlysState);
    });

    it('returns the state with recurring class applied monthly entities ' 
        + 'and indicates that the application objects have been loaded', () => {
        const state = recurringClassAppliedMonthlysReducer(
            initialRecurringClassAppliedMonthlysState, 
            new RecurringClassAppliedMonthlysLoaded({
                recurringClassesAppliedMonthly: recurringClassAppliedMonthliesData
            })
        );
        expect(state).toEqual(
            statePriorToNewRecurringClassAppliedMonthlySubmission.recurringClassAppliedMonthlys
        );
    });

    it('returns the original state with one less recurring class applied monthly ' 
        + 'entity and indicates that the third recurring class application '
        + 'has been successfully deleted', () => {
        const state = recurringClassAppliedMonthlysReducer(
            statePriorToNewRecurringClassAppliedMonthlySubmission.recurringClassAppliedMonthlys, 
            new RecurringClassAppliedMonthlyDeletionSaved({ 
                recurringClassAppliedMonthlyDeletionResponse: recurringClassAppliedMonthlyDeletionResponse
            })
        );
        expect(state).toEqual(
            stateFollowingRecurringClassAppliedMonthlyDeletion.recurringClassAppliedMonthlys
        );
    });

    it('returns the state after the recurring class applied monthly entity has been added ' 
        + 'and indicates that the deletion of the recurring class application failed', () => {
        const state = recurringClassAppliedMonthlysReducer(
            statePriorToNewRecurringClassAppliedMonthlySubmission.recurringClassAppliedMonthlys, 
            new RecurringClassAppliedMonthlyDeletionCancelled({ 
                err: {
                    error: {
                        Error: "Error! Recurring Class Applied Monthly Deletion Failed!"
                    }
                } 
            })
        );
        expect(state).toEqual(
            stateFollowingRecurringClassAppliedMonthlyDeletionFailure.recurringClassAppliedMonthlys
        );
    });

    it('returns the state with new recurring class applied monthly entity and indicates that ' 
        + 'the recurring class applied monthly has been successfully submitted', () => {
        const state = recurringClassAppliedMonthlysReducer(
            statePriorToNewRecurringClassAppliedMonthlySubmission.recurringClassAppliedMonthlys, 
            new RecurringClassAppliedMonthlyAdded({
                recurringClassAppliedMonthly: newlyCreatedRecurringClassAppliedMonthlyData
            })
        );
        expect(state).toEqual(
            stateAfterNewRecurringClassAppliedMonthlySubmission.recurringClassAppliedMonthlys
        );
    });

    it('returns the state with originally loaded recurring class applied monthly ' 
        + 'entities and indicates that submission of a new recurring class applied monthly ' 
        + 'has been unsuccessful', () => {
        const state = recurringClassAppliedMonthlysReducer(
            statePriorToNewRecurringClassAppliedMonthlySubmission.recurringClassAppliedMonthlys, 
            new RecurringClassAppliedMonthlyCreationCancelled({ 
                err: {
                    error: {
                        message: "Error submitting recurring class application!"
                    } 
                } 
            })
        );
        expect(state).toEqual(
            stateAfterNewRecurringClassAppliedMonthlySubmissionFailure.recurringClassAppliedMonthlys
        );
    });

    it('returns the initial state with error message when fetching recurring classes applied monthly fails', () => {
        const state = recurringClassAppliedMonthlysReducer(
            initialRecurringClassAppliedMonthlysState, 
            new RecurringClassAppliedMonthlysRequestCancelled({ 
                err: {
                    error: {
                        message: "Error fetching recurring classes applied monthly!"
                    } 
                } 
            })
        );
        expect(state).toEqual(
            stateFollowingRecurringClassAppliedMonthlyFetchFailure.recurringClassAppliedMonthlys
        );
    });

    it('clears success and error messages and optional batch deletion data when messages cleared action is dispatched', () => {
        const stateWithMessages = {
            ...statePriorToNewRecurringClassAppliedMonthlySubmission.recurringClassAppliedMonthlys,
            successMessage: 'Some success message',
            errorMessage: 'Some error message',
            optionalBatchDeletionData: {
                obsolete_class_strings: 'Class 1, Class 2',
                obsolete_class_ids: [1, 2]
            }
        };
        
        const state = recurringClassAppliedMonthlysReducer(
            stateWithMessages, 
            new RecurringClassesAppliedMonthlyMessagesCleared()
        );
        
        expect(state.successMessage).toBeUndefined();
        expect(state.errorMessage).toBeUndefined();
        expect(state.optionalBatchDeletionData).toBeUndefined();
        expect(state.ids).toEqual(stateWithMessages.ids);
        expect(state.entities).toEqual(stateWithMessages.entities);
    });

    it('sets deletionModeActivated to true when deletion mode is activated', () => {
        const state = recurringClassAppliedMonthlysReducer(
            statePriorToNewRecurringClassAppliedMonthlySubmission.recurringClassAppliedMonthlys,
            new RecurringClassAppliedMonthlyDeletionModeActivated()
        );
        
        expect(state.deletionModeActivated).toBe(true);
        expect(state.ids).toEqual(
            statePriorToNewRecurringClassAppliedMonthlySubmission.recurringClassAppliedMonthlys.ids
        );
        expect(state.entities).toEqual(
            statePriorToNewRecurringClassAppliedMonthlySubmission.recurringClassAppliedMonthlys.entities
        );
    });

    it('sets deletionModeActivated to false when deletion mode is deactivated', () => {
        const stateWithDeletionMode = {
            ...statePriorToNewRecurringClassAppliedMonthlySubmission.recurringClassAppliedMonthlys,
            deletionModeActivated: true
        };
        
        const state = recurringClassAppliedMonthlysReducer(
            stateWithDeletionMode,
            new RecurringClassAppliedMonthlyDeletionModeDeactivated()
        );
        
        expect(state.deletionModeActivated).toBe(false);
        expect(state.ids).toEqual(
            statePriorToNewRecurringClassAppliedMonthlySubmission.recurringClassAppliedMonthlys.ids
        );
        expect(state.entities).toEqual(
            statePriorToNewRecurringClassAppliedMonthlySubmission.recurringClassAppliedMonthlys.entities
        );
    });

});
