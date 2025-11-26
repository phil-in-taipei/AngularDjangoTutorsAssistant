import { 
    initialSchoolsState, 
    schoolsReducer 
} from "./school.reducers";
import { 
    newlyCreatedSchoolData,
    schoolData,
    schoolsData,
    schoolCreateAndEditData,
    deletionResponseSuccess
} from "src/app/test-data/authenticated-user-module-tests/school-related-tests/school-data";

import { 
    statePriorToSchoolsLoadRequest,
    stateAfterSchoolsRequested,
    stateAfterSchoolsLoadedSuccess,
    stateAfterSchoolsLoadFailure,
    stateAfterSchoolCreatedAdded,
    stateAfterSchoolCreationCancelled,
    stateAfterSchoolEditUpdated,
    stateAfterSchoolEditCancelled,
    stateAfterSchoolDeletionModeActivated,
    stateAfterSchoolDeletionModeDeactivated,
    stateAfterSchoolDeletionSaved,
    stateAfterSchoolDeletionCancelled,
    stateAfterSchoolsMessagesCleared,
    stateAfterSchoolsCleared
} from "src/app/test-data/authenticated-user-module-tests/school-related-tests/school-state";

import { 
    SchoolsCleared,
    SchoolsRequested,
    SchoolsLoaded,
    SchoolsRequestCancelled,
    SchoolCreatedAdded,
    SchoolCreationCancelled,
    SchoolEditUpdated,
    SchoolEditCancelled,
    SchoolDeletionModeActivated,
    SchoolDeletionModeDeactivated,
    SchoolDeletionSaved,
    SchoolDeletionCancelled,
    SchoolsMessagesCleared
} from "./school.actions";

fdescribe('schoolsReducer', () => {

    it('returns an initial state when cleared', () => {
        const state = schoolsReducer(
            initialSchoolsState, 
            new SchoolsCleared()
        );
        expect(state).toEqual(initialSchoolsState);
    });

    it('sets fetchingSchoolsInProgress to true when schools are requested', () => {
        const state = schoolsReducer(
            statePriorToSchoolsLoadRequest,
            new SchoolsRequested()
        );
        expect(state).toEqual(stateAfterSchoolsRequested);
    });

    it('returns the state with school entities and indicates that ' 
        + 'the schools have been loaded', () => {
        const state = schoolsReducer(
            stateAfterSchoolsRequested, 
            new SchoolsLoaded({ schools: schoolsData })
        );
        expect(state).toEqual(stateAfterSchoolsLoadedSuccess);
    });

    it('returns the initial state with error message when fetching schools fails', () => {
        const state = schoolsReducer(
            statePriorToSchoolsLoadRequest, 
            new SchoolsRequestCancelled({ 
                err: {
                    error: {
                        message: "Error fetching schools!"
                    } 
                } 
            })
        );
        expect(state).toEqual(stateAfterSchoolsLoadFailure);
    });

    it('returns the state with new school entity and indicates that ' 
        + 'the school has been successfully submitted', () => {
        const state = schoolsReducer(
            stateAfterSchoolsLoadedSuccess, 
            new SchoolCreatedAdded({ school: newlyCreatedSchoolData })
        );
        expect(state).toEqual(stateAfterSchoolCreatedAdded);
    });

    it('returns the state with originally loaded schools and indicates that '
        + 'submission of a new school has been unsuccessful', () => {
        const state = schoolsReducer(
            stateAfterSchoolsLoadedSuccess, 
            new SchoolCreationCancelled({ 
                err: {
                    error: {
                        message: "Error submitting new school!"
                    } 
                } 
            })
        );
        expect(state).toEqual(stateAfterSchoolCreationCancelled);
    });

    it('returns the state with updated school entity and indicates that ' 
        + 'the school has been successfully edited', () => {
        const updatedSchool = {
            id: schoolData.id,
            changes: {
                school_name: schoolCreateAndEditData.school_name,
                address_line_1: schoolCreateAndEditData.address_line_1,
                address_line_2: schoolCreateAndEditData.address_line_2,
                contact_phone: schoolCreateAndEditData.contact_phone,
                other_information: schoolCreateAndEditData.other_information
            }
        };
        
        const state = schoolsReducer(
            stateAfterSchoolsLoadedSuccess, 
            new SchoolEditUpdated({ school: updatedSchool })
        );
        expect(state).toEqual(stateAfterSchoolEditUpdated);
    });

    it('returns the state with originally loaded schools and indicates that '
        + 'editing a school has been unsuccessful', () => {
        const state = schoolsReducer(
            stateAfterSchoolsLoadedSuccess, 
            new SchoolEditCancelled({ 
                err: {
                    error: {
                        Error: "Error! Editing School Failed!"
                    } 
                } 
            })
        );
        expect(state).toEqual(stateAfterSchoolEditCancelled);
    });

    it('sets deletionModeActivated to true when deletion mode is activated', () => {
        const state = schoolsReducer(
            stateAfterSchoolsLoadedSuccess,
            new SchoolDeletionModeActivated()
        );
        expect(state).toEqual(stateAfterSchoolDeletionModeActivated);
    });

    it('sets deletionModeActivated to false when deletion mode is deactivated', () => {
        const state = schoolsReducer(
            stateAfterSchoolDeletionModeActivated,
            new SchoolDeletionModeDeactivated()
        );
        expect(state).toEqual(stateAfterSchoolDeletionModeDeactivated);
    });

    it('returns the state with one less school entity and indicates that ' 
       + 'the school has been successfully deleted', () => {
        const state = schoolsReducer(
            stateAfterSchoolsLoadedSuccess, 
            new SchoolDeletionSaved({ 
                id: deletionResponseSuccess.id, 
                message: deletionResponseSuccess.message
            })
        );
        expect(state).toEqual(stateAfterSchoolDeletionSaved);
    });

    it('returns the state with all school entities and indicates that ' 
        + 'the deletion of a school failed', () => {
        const state = schoolsReducer(
            stateAfterSchoolsLoadedSuccess, 
            new SchoolDeletionCancelled({ 
                err: {
                    error: {
                        Error: "Error! School Deletion Failed!"
                    }
                } 
            })
        );
        expect(state).toEqual(stateAfterSchoolDeletionCancelled);
    });

    it('clears success and error messages when messages cleared action is dispatched', () => {
        const stateWithMessages = {
            ...stateAfterSchoolsLoadedSuccess,
            successMessage: 'Some success message',
            errorMessage: 'Some error message'
        };
        
        const state = schoolsReducer(
            stateWithMessages, 
            new SchoolsMessagesCleared()
        );
        
        expect(state.successMessage).toBeUndefined();
        expect(state.errorMessage).toBeUndefined();
        expect(state.ids).toEqual(stateAfterSchoolsLoadedSuccess.ids);
        expect(state.entities).toEqual(stateAfterSchoolsLoadedSuccess.entities);
    });

});
