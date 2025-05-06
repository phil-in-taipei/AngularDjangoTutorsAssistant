import {createFeatureSelector, createSelector} from '@ngrx/store';

import { ScheduledClassesState } from "./scheduled-classes.reducers";
import * as fromScheduledClasses from "./scheduled-classes.reducers";

export const selectScheduledClassesState = 
            createFeatureSelector<ScheduledClassesState>("scheduledClasses");


export const deletionModeForScheduledClassesActivated = createSelector(
    selectScheduledClassesState,
        state => state.deletionModeActivated
);           

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

export const selectMonthlyDateRange = createSelector(
    selectScheduledClassesState,
    scheduledClassesState => scheduledClassesState.dateRange
  );
 
 // check if selector below still necessary 
export const selectScheduledClassesByMonthLoaded = createSelector(
    selectScheduledClassesState,
    scheduledClassesState => scheduledClassesState.monthlyScheduledClassesLoaded
);

export const selectUnconfirmedPastScheduledClasses = (currentDate: string) => createSelector(
    selectAllScheduledClasses,
    scheduledClassesState => {
      return scheduledClassesState.filter(
        scheduledClass => 
          scheduledClass.date < currentDate && 
          scheduledClass.class_status === 'scheduled'
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

export const scheduledClassesErrorMsg = createSelector(
    selectScheduledClassesState,
    scheduledClassesState => scheduledClassesState.errorMessage
);
  
export const scheduledClassesSuccessMsg = createSelector(
    selectScheduledClassesState,
    scheduledClassesState => scheduledClassesState.successMessage
);

export const updatedPurchasedHours = createSelector(
    selectScheduledClassesState,
    scheduledClassesState => scheduledClassesState.updatedPurchasedHours
);

export const unconfirmedScheduledClassesLoaded = createSelector(
    selectScheduledClassesState,
    scheduledClassesState => scheduledClassesState.unconfirmedScheduledClassesLoaded
);
