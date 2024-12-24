import {createFeatureSelector, createSelector} from '@ngrx/store';

import { ScheduledClassesState } from "./scheduled-classes.reducers";
import * as fromScheduledClasses from "./scheduled-classes.reducers";

export const selectScheduledClassesState = 
            createFeatureSelector<ScheduledClassesState>("scheduledClasses");

export const selectAllScheduledClasses = createSelector(
    selectScheduledClassesState,
    fromScheduledClasses.selectAll
);

export const selectScheduledClassById = (id:number) => createSelector(
    selectScheduledClassesState,
    scheduledClassesState => scheduledClassesState.entities[id]
);
  
export const selectScheduledClassesByDate = (date: string) => createSelector(
    selectAllScheduledClasses,
    scheduledClassesState => {
        return scheduledClassesState.filter(
            scheduledClass => scheduledClass.date == date
        );
    }
);

export const fetchingClassesInProgress = createSelector(
    selectScheduledClassesState,
    scheduledClassesState => scheduledClassesState.fetchingClassesInProgress
);
              
export const landingPageScheduleLoaded = createSelector(
    selectScheduledClassesState,
    scheduledClassesState => scheduledClassesState.landingPageScheduledClassesLoaded
);