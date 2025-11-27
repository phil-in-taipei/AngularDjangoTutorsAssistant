import { 
    initialStudentsOrClassesState, 
    studentsOrClassesReducer 
} from "./student-or-class.reducers";

import { 
    studentsOrClassesData,
    studentOrClassEditData,
    deletionResponseSuccess,
    studentOrClassConfirmationModificationResponse
} from "src/app/test-data/authenticated-user-module-tests/student-or-class-related-tests/student-or-class-data";

import { 
    statePriorToStudentsOrClassesLoadRequest,
    stateAfterStudentsOrClassesLoadRequest,
    stateAfterStudentsOrClassesLoadSuccess,
    stateAfterStudentsOrClassesLoadFailure,
    stateAfterStudentOrClassCreatedAdded,
    stateAfterStudentOrClassEditUpdated,
    stateAfterStudentOrClassDeletionSaved,
    stateAfterStudentOrClassDeletionFailure,
    stateAfterFreelanceAccountPurchasedHoursSaved,
    stateAfterFreelanceAccountRefundedHoursSaved,
    stateAfterMessagesCleared,
    stateAfterStudentsOrClassesCleared
} from "src/app/test-data/authenticated-user-module-tests/student-or-class-related-tests/student-or-class-state";

import { 
    StudentsOrClassesCleared,
    StudentsOrClassesRequested,
    StudentsOrClassesLoaded,
    StudentsOrClassesRequestCancelled,
    StudentOrClassCreatedAdded,
    StudentOrClassCreationCancelled,
    StudentOrClassEditUpdated,
    StudentOrClassEditCancelled,
    StudentOrClassDeletionModeActivated,
    StudentOrClassDeletionModeDeactivated,
    StudentOrClassDeletionSaved,
    StudentOrClassDeletionCancelled,
    StudentsOrClassesMessagesCleared,
    StudentOrClassPurchasedHoursUpdated,
    FreelanceAccountPurchasedHoursSaved,
    FreelanceAccountRefundedHoursSaved
} from "./student-or-class.actions";


fdescribe('studentsOrClassesReducer', () => {

    it('returns an initial state when cleared', () => {
        const state = studentsOrClassesReducer(
            initialStudentsOrClassesState, 
            new StudentsOrClassesCleared()
        );
        expect(state).toEqual(initialStudentsOrClassesState);
    });

    it('sets fetchingStudentsOrClassesInProgress to true when students or classes are requested', () => {
        const state = studentsOrClassesReducer(
            statePriorToStudentsOrClassesLoadRequest,
            new StudentsOrClassesRequested()
        );
        expect(state).toEqual(stateAfterStudentsOrClassesLoadRequest);
    });

    it('returns the state with student or class entities and indicates that ' 
        + 'the students or classes have been loaded', () => {
        const state = studentsOrClassesReducer(
            stateAfterStudentsOrClassesLoadRequest, 
            new StudentsOrClassesLoaded({ studentsOrClasses: studentsOrClassesData })
        );
        expect(state).toEqual(stateAfterStudentsOrClassesLoadSuccess);
    });

    it('returns the initial state with error message when fetching students or classes fails', () => {
        const state = studentsOrClassesReducer(
            statePriorToStudentsOrClassesLoadRequest, 
            new StudentsOrClassesRequestCancelled({ 
                err: {
                    error: {
                        message: "Error fetching students or classes!"
                    } 
                } 
            })
        );
        expect(state).toEqual(stateAfterStudentsOrClassesLoadFailure);
    });

    it('returns the state with new student or class entity and indicates that ' 
        + 'the student or class has been successfully submitted', () => {
        const newStudentOrClass = stateAfterStudentOrClassCreatedAdded.entities[4]!;
        
        const state = studentsOrClassesReducer(
            stateAfterStudentsOrClassesLoadSuccess, 
            new StudentOrClassCreatedAdded({ studentOrClass: newStudentOrClass })
        );
        expect(state).toEqual(stateAfterStudentOrClassCreatedAdded);
    });

    it('returns the state with originally loaded students or classes and indicates that '
        + 'submission of a new student or class has been unsuccessful', () => {
        const state = studentsOrClassesReducer(
            stateAfterStudentsOrClassesLoadSuccess, 
            new StudentOrClassCreationCancelled({ 
                err: {
                    error: {
                        message: "Error submitting new Student Or Class!"
                    } 
                } 
            })
        );
        expect(state.errorMessage).toBe('Error submitting new Student Or Class!');
        expect(state.successMessage).toBeUndefined();
        expect(state.ids).toEqual(stateAfterStudentsOrClassesLoadSuccess.ids);
    });

    it('returns the state with updated student or class entity and indicates that ' 
        + 'the student or class has been successfully edited', () => {
        const updatedStudentOrClass = {
            id: studentsOrClassesData[0].id,
            changes: {
                student_or_class_name: studentOrClassEditData.student_or_class_name,
                comments: studentOrClassEditData.comments,
                tuition_per_hour: studentOrClassEditData.tuition_per_hour
            }
        };
        
        const state = studentsOrClassesReducer(
            stateAfterStudentsOrClassesLoadSuccess, 
            new StudentOrClassEditUpdated({ studentOrClass: updatedStudentOrClass })
        );
        expect(state).toEqual(stateAfterStudentOrClassEditUpdated);
    });

    it('returns the state with originally loaded students or classes and indicates that '
        + 'editing a student or class has been unsuccessful', () => {
        const state = studentsOrClassesReducer(
            stateAfterStudentsOrClassesLoadSuccess, 
            new StudentOrClassEditCancelled({ 
                err: {
                    error: {
                        Error: "Error! Editing Student Or Class Failed!"
                    } 
                } 
            })
        );
        expect(state.errorMessage).toBe('Error! Editing Student Or Class Failed!');
        expect(state.successMessage).toBeUndefined();
        expect(state.ids).toEqual(stateAfterStudentsOrClassesLoadSuccess.ids);
    });

    it('sets deletionModeActivated to true when deletion mode is activated', () => {
        const state = studentsOrClassesReducer(
            stateAfterStudentsOrClassesLoadSuccess,
            new StudentOrClassDeletionModeActivated()
        );
        expect(state.deletionModeActivated).toBe(true);
        expect(state.ids).toEqual(stateAfterStudentsOrClassesLoadSuccess.ids);
    });

    it('sets deletionModeActivated to false when deletion mode is deactivated', () => {
        const stateWithDeletionMode = {
            ...stateAfterStudentsOrClassesLoadSuccess,
            deletionModeActivated: true
        };
        
        const state = studentsOrClassesReducer(
            stateWithDeletionMode,
            new StudentOrClassDeletionModeDeactivated()
        );
        expect(state.deletionModeActivated).toBe(false);
        expect(state.ids).toEqual(stateAfterStudentsOrClassesLoadSuccess.ids);
    });

    it('returns the state with one less student or class entity and indicates that ' 
       + 'the student or class has been successfully deleted', () => {
        const state = studentsOrClassesReducer(
            stateAfterStudentsOrClassesLoadSuccess, 
            new StudentOrClassDeletionSaved({ 
                id: deletionResponseSuccess.id, 
                message: deletionResponseSuccess.message
            })
        );
        expect(state).toEqual(stateAfterStudentOrClassDeletionSaved);
    });

    it('returns the state with all student or class entities and indicates that ' 
        + 'the deletion of a student or class failed', () => {
        const state = studentsOrClassesReducer(
            stateAfterStudentsOrClassesLoadSuccess, 
            new StudentOrClassDeletionCancelled({ 
                err: {
                    error: {
                        Error: "Error! Student Or Class Deletion Failed!"
                    }
                } 
            })
        );
        expect(state).toEqual(stateAfterStudentOrClassDeletionFailure);
    });

    it('updates purchased class hours and sets appropriate success message', () => {
        const updatedStudentOrClass = {
            id: studentOrClassConfirmationModificationResponse.id,
            changes: {
                purchased_class_hours: studentOrClassConfirmationModificationResponse.changes.purchased_class_hours
            }
        };
        
        const state = studentsOrClassesReducer(
            stateAfterStudentsOrClassesLoadSuccess, 
            new StudentOrClassPurchasedHoursUpdated({ studentOrClass: updatedStudentOrClass })
        );
        
        const updatedEntity = state.entities[updatedStudentOrClass.id]!;
        expect(updatedEntity.purchased_class_hours)
            .toBe(studentOrClassConfirmationModificationResponse.changes.purchased_class_hours);
        expect(state.successMessage).toBe(
            `Updated Purchased Hours: ${studentOrClassConfirmationModificationResponse.changes.purchased_class_hours}`
        );
        expect(state.errorMessage).toBeUndefined();
    });
    
    it('adds purchased hours to freelance account and updates total with success message', () => {
        const studentOrClass = studentsOrClassesData[0];
        const hoursToAdd = 5;
        
        const state = studentsOrClassesReducer(
            stateAfterStudentsOrClassesLoadSuccess, 
            new FreelanceAccountPurchasedHoursSaved({ 
                studentOrClass: studentOrClass,
                class_hours_purchased_or_refunded: hoursToAdd
            })
        );
        
        expect(state).toEqual(stateAfterFreelanceAccountPurchasedHoursSaved);
    });

    it('subtracts refunded hours from freelance account and updates total with success message', () => {
        const studentOrClass = studentsOrClassesData[0];
        const hoursToRefund = 10;
        
        const state = studentsOrClassesReducer(
            stateAfterStudentsOrClassesLoadSuccess, 
            new FreelanceAccountRefundedHoursSaved({ 
                studentOrClass: studentOrClass,
                class_hours_purchased_or_refunded: hoursToRefund
            })
        );
        
        expect(state).toEqual(stateAfterFreelanceAccountRefundedHoursSaved);
    });

    it('clears success and error messages when messages cleared action is dispatched', () => {
        const stateWithMessages = {
            ...stateAfterStudentsOrClassesLoadSuccess,
            successMessage: 'Some success message',
            errorMessage: 'Some error message'
        };
        
        const state = studentsOrClassesReducer(
            stateWithMessages, 
            new StudentsOrClassesMessagesCleared()
        );
        
        expect(state.successMessage).toBeUndefined();
        expect(state.errorMessage).toBeUndefined();
        expect(state.ids).toEqual(stateAfterStudentsOrClassesLoadSuccess.ids);
        expect(state.entities).toEqual(stateAfterStudentsOrClassesLoadSuccess.entities);
    });

});