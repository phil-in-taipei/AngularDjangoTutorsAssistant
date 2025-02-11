import { createFeatureSelector, createSelector } from '@ngrx/store';

import { RecurringClassesState } from './recurring-schedule.reducers';
import * as fromRecurringClasses from './recurring-schedule.reducers';

export const selectRecurringClassesState = 
  createFeatureSelector<RecurringClassesState>("recurringClasses");

export const selectAllRecurringClasses = createSelector(
  selectRecurringClassesState,
  fromRecurringClasses.selectAll
);

export const selectRecurringClassById = (id: number) => createSelector(
  selectRecurringClassesState,
  recurringClassesState => recurringClassesState.entities[id]
);

export const selectRecurringClassesLoaded = createSelector(
  selectRecurringClassesState,
  recurringClassesState => recurringClassesState.recurringClassesLoaded
);

export const recurringClassErrorMsg = createSelector(
  selectRecurringClassesState,
  recurringClassesState => recurringClassesState.errorMessage
);

export const recurringClassSuccessMsg = createSelector(
  selectRecurringClassesState,
  recurringClassesState => recurringClassesState.successMessage
);
