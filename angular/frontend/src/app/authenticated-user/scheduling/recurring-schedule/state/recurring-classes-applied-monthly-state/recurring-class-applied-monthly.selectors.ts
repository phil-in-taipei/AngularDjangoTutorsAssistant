import { createFeatureSelector, createSelector } from '@ngrx/store';
import { RecurringClassAppliedMonthlysState } from './recurring-class-applied-monthly.reducers';
import * as fromRecurringClassesAppliedMonthly from './recurring-class-applied-monthly.reducers';

export const selectRecurringClassesAppliedMonthlyState =
  createFeatureSelector<RecurringClassAppliedMonthlysState>("recurringClassesAppliedMonthly");

export const selectAllRecurringClassAppliedMonthlys = createSelector(
  selectRecurringClassesAppliedMonthlyState,
  fromRecurringClassesAppliedMonthly.selectAll
);

export const selectRecurringClassAppliedMonthlyById = (id: number) => createSelector(
  selectRecurringClassesAppliedMonthlyState,
  state => state.entities[id]
);

export const selectRecurringClassAppliedMonthlysLoaded = createSelector(
  selectRecurringClassesAppliedMonthlyState,
  state => state.recurringClassAppliedMonthlysLoaded
);

export const recurringClassAppliedMonthlysErrorMsg = createSelector(
  selectRecurringClassesAppliedMonthlyState,
  state => state.errorMessage
);

export const recurringClassAppliedMonthysSuccessMsg = createSelector(
  selectRecurringClassesAppliedMonthlyState,
  state => state.successMessage
);

export const optionalScheduledClassBatchDeletionData = createSelector(
  selectRecurringClassesAppliedMonthlyState,
  state => state.optionalBatchDeletionData
);