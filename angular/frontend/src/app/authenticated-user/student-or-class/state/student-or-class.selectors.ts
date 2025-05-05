import {createFeatureSelector, createSelector} from '@ngrx/store';

import { StudentsOrClassesState } from './student-or-class.reducers';
import * as fromStudentsOrClasses from './student-or-class.reducers';


export const selectStudentsOrClassesState =
            createFeatureSelector<StudentsOrClassesState>("studentsOrClasses");


export const deletionModeForStudentsOrClassesActivated = createSelector(
    selectStudentsOrClassesState,
        state => state.deletionModeActivated
);
    
export const fetchingStudentsOrClassesInProgress = createSelector(
            selectStudentsOrClassesState,
            state => state.fetchingStudentsOrClassesInProgress
        );        

export const selectAllStudentsOrClasses = createSelector(
    selectStudentsOrClassesState,
        fromStudentsOrClasses.selectAll
    );

export const selectFreelanceStudentsOrClasses = createSelector(
    selectAllStudentsOrClasses,
    studentsOrClasses => studentsOrClasses.filter(
        item => item.account_type === 'freelance'
    )
);

export const selectStudentOrClassById = (id: number) => createSelector(
    selectStudentsOrClassesState,
    state => state.entities[id]
);

export const studentsOrClassesLoadedInState = createSelector(
        selectStudentsOrClassesState,
        state => state.studentsOrClassesLoaded
    );

export const studentsOrClassesErrorMsg = createSelector(
        selectStudentsOrClassesState,
        state => state.errorMessage
    );

export const studentsOrClassesSuccessMsg = createSelector(
        selectStudentsOrClassesState,
        state => state.successMessage
    );
