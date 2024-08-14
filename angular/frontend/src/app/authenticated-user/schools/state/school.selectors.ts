import {createFeatureSelector, createSelector} from '@ngrx/store';

import { SchoolsState } from './school.reducers';
import * as fromSchools from './school.reducers';


export const selectSchoolsState = 
            createFeatureSelector<SchoolsState>("schools");


export const fetchingSchoolsInProgress = createSelector(
            selectSchoolsState,
            state => state.fetchingSchoolsInProgress
        );

export const selectAllSchools = createSelector(
    selectSchoolsState,
        fromSchools.selectAll
    );

export const selectSchoolById = (id:number) => createSelector(
    selectSchoolsState,
    state => state.entities[id]
);

export const schoolsLoadedInState = createSelector(
        selectSchoolsState,
        state => state.schoolsLoaded
    );

    
export const schoolsErrorMsg = createSelector(
        selectSchoolsState,
        state => state.errorMessage
    );
          
export const schoolsSuccessMsg = createSelector(
        selectSchoolsState,
        state => state.successMessage
    );
