import { 
    initialRecurringClassesState, 
    recurringClassesReducer 
} from "./recurring-schedule.reducers";
import { 
    recurringClassData, recurringClassesData, recurringClassCreatedResponseData 
} from "src/app/test-data/authenticated-user-module-tests/scheduling-module-tests/scheduled-classes-related-tests/recurring-schedule-module-tests/recurring-schedule-related-tests/recurring-schedule-data";

import { 
    statePriorToNewRecurringClassSubmission, 
    stateAfterNewRecurringClassSubmission, 
    stateAfterNewRecurringClassSubmissionFailure, 
    stateFollowingRecurringClassDeletion, 
    stateFollowingRecurringClassDeletionFailure,
    stateFollowingRecurringClassFetchFailure
 } from "src/app/test-data/authenticated-user-module-tests/scheduling-module-tests/scheduled-classes-related-tests/recurring-schedule-module-tests/recurring-schedule-related-tests/recurring-schedule-state";
import { 
    RecurringClassesCleared, 
    RecurringClassAdded,
    RecurringClassCreationCancelled, 
    RecurringClassDeletionCancelled, 
    RecurringClassDeletionSaved, 
    RecurringClassesLoaded,
    RecurringClassesRequestCancelled,
    RecurringClassesMessagesCleared,
    RecurringClassDeletionModeActivated,
    RecurringClassDeletionModeDeactivated
} from "./recurring-schedule.actions";

fdescribe('recurringClassesReducer', () => {

    it('returns an initial state when cleared', () => {
        const state = recurringClassesReducer(
            initialRecurringClassesState, 
            new RecurringClassesCleared()
        );
        expect(state).toEqual(initialRecurringClassesState);
    });

    it('returns the state with recurring classes entities and indicates that ' 
        + 'the classes have been loaded', () => {
        const state = recurringClassesReducer(
            initialRecurringClassesState, 
            new RecurringClassesLoaded({ recurringClasses: recurringClassesData })
        );
        expect(state).toEqual(statePriorToNewRecurringClassSubmission.recurringClasses);
    });

    it('returns the state with one less recurring class entity and indicates that ' 
       + 'the third recurring class has been successfully deleted', () => {
        const state = recurringClassesReducer(
            statePriorToNewRecurringClassSubmission.recurringClasses, 
            new RecurringClassDeletionSaved({ 
                id: recurringClassesData[2].id, 
                message: stateFollowingRecurringClassDeletion.recurringClasses.successMessage 
            })
        );
        expect(state).toEqual(stateFollowingRecurringClassDeletion.recurringClasses);
    });

    it('returns the state with all recurring class entities and indicates that ' 
        + 'the deletion of a recurring class failed', () => {
        const state = recurringClassesReducer(
            statePriorToNewRecurringClassSubmission.recurringClasses, 
            new RecurringClassDeletionCancelled({ 
                err: {
                    error: {
                        Error: "Error! Recurring Class Deletion Failed!"
                    }
                } 
            })
        );
        expect(state).toEqual(
            stateFollowingRecurringClassDeletionFailure.recurringClasses
        );
    });

    it('returns the state with new recurring class entity and indicates that ' 
        + 'the recurring class has been successfully submitted', () => {
        const state = recurringClassesReducer(
            statePriorToNewRecurringClassSubmission.recurringClasses, 
            new RecurringClassAdded({ recurringClass: recurringClassCreatedResponseData })
        );
        expect(state).toEqual(
            stateAfterNewRecurringClassSubmission.recurringClasses
        );
    });

    it('returns the state with originally loaded recurring classes entity and indicates that '
        + 'submission of a new recurring class has been unsuccessful', () => {
        const state = recurringClassesReducer(
            statePriorToNewRecurringClassSubmission.recurringClasses, 
            new RecurringClassCreationCancelled({ 
                err: {
                    error: {
                        message: "Error submitting recurring class!"
                    } 
                } 
            })
        );
        expect(state).toEqual(
            stateAfterNewRecurringClassSubmissionFailure.recurringClasses
        );
    });

    it('returns the initial state with error message when fetching recurring classes fails', () => {
        const state = recurringClassesReducer(
            initialRecurringClassesState, 
            new RecurringClassesRequestCancelled({ 
                err: {
                    error: {
                        message: "Error fetching recurring classes!"
                    } 
                } 
            })
        );
        expect(state).toEqual(
            stateFollowingRecurringClassFetchFailure.recurringClasses
        );
    });

    it('clears success and error messages when messages cleared action is dispatched', () => {
        const stateWithMessages = {
            ...statePriorToNewRecurringClassSubmission.recurringClasses,
            successMessage: 'Some success message',
            errorMessage: 'Some error message'
        };
        
        const state = recurringClassesReducer(
            stateWithMessages, 
            new RecurringClassesMessagesCleared()
        );
        
        expect(state.successMessage).toBeUndefined();
        expect(state.errorMessage).toBeUndefined();
        expect(state.ids).toEqual(stateWithMessages.ids);
        expect(state.entities).toEqual(stateWithMessages.entities);
    });

    it('sets deletionModeActivated to true when deletion mode is activated', () => {
        const state = recurringClassesReducer(
            statePriorToNewRecurringClassSubmission.recurringClasses,
            new RecurringClassDeletionModeActivated()
        );
        
        expect(state.deletionModeActivated).toBe(true);
        expect(state.ids).toEqual(statePriorToNewRecurringClassSubmission.recurringClasses.ids);
        expect(state.entities).toEqual(statePriorToNewRecurringClassSubmission.recurringClasses.entities);
    });

    it('sets deletionModeActivated to false when deletion mode is deactivated', () => {
        const stateWithDeletionMode = {
            ...statePriorToNewRecurringClassSubmission.recurringClasses,
            deletionModeActivated: true
        };
        
        const state = recurringClassesReducer(
            stateWithDeletionMode,
            new RecurringClassDeletionModeDeactivated()
        );
        
        expect(state.deletionModeActivated).toBe(false);
        expect(state.ids).toEqual(statePriorToNewRecurringClassSubmission.recurringClasses.ids);
        expect(state.entities).toEqual(statePriorToNewRecurringClassSubmission.recurringClasses.entities);
    });

});