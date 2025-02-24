import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { Store } from '@ngrx/store';
import { of } from 'rxjs';
import { catchError, map, mergeMap } from 'rxjs/operators';

import {  
    RecurringClassAppliedMonthlyActionTypes,
    RecurringClassAppliedMonthlyAdded,
    RecurringClassAppliedMonthlyCreateSubmitted,
    RecurringClassAppliedMonthlyCreationCancelled,
    RecurringClassAppliedMonthlyDeletionCancelled,
    RecurringClassAppliedMonthlyDeletionRequested,
    RecurringClassAppliedMonthlyDeletionSaved,
    RecurringClassAppliedMonthlysLoaded,
    RecurringClassAppliedMonthlysRequestCancelled,
    RecurringClassAppliedMonthlysRequested
} from './recurring-class-applied-monthly.actions';
import { RecurringClassAppliedMonthlysState } from './recurring-class-applied-monthly.reducers';

import { 
    RecurringScheduleService 
} from '../../recurring-schedule-service/recurring-schedule.service';

@Injectable()
export class RecurringClassAppliedMonthlysEffects {

    deleteRecurringClassAppliedMonthly$ = createEffect(() => {
        return this.actions$
          .pipe(
            ofType<RecurringClassAppliedMonthlyDeletionRequested>(
              RecurringClassAppliedMonthlyActionTypes.RecurringClassAppliedMonthlyDeletionRequested
            ),
            mergeMap(action => this.recurringScheduleService
              .deleteRecurringClassAppliedMonthly(action.payload.id)
              .pipe(
                map(recurringClassAppliedMonthlyDeletionResponse => new RecurringClassAppliedMonthlyDeletionSaved(
                  { recurringClassAppliedMonthlyDeletionResponse }
                )),
                catchError(err => {
                  this.store.dispatch(
                    new RecurringClassAppliedMonthlyDeletionCancelled({ err })
                  );
                  return of();
                })
              )
            )
          )
      });
    
    fetchRecurringClassesAppliedMonthlys$ = createEffect(() => {
        return this.actions$
          .pipe(
            ofType<RecurringClassAppliedMonthlysRequested>(
                RecurringClassAppliedMonthlyActionTypes.RecurringClassAppliedMonthlysRequested
            ),
            mergeMap(action => this.recurringScheduleService
                .fetchRecurringClassAppliedMonthlysByMonthAndYear(
                    action.payload.month, action.payload.year
                )
              .pipe(
                map(recurringClassesAppliedMonthly => new RecurringClassAppliedMonthlysLoaded(
                    { recurringClassesAppliedMonthly }
                )),
                catchError(err => {
                  this.store.dispatch(
                    new RecurringClassAppliedMonthlysRequestCancelled({ err })
                  );
                  return of();
                })
              )
            )
          )
      });

      submitRecurringClassAppliedMonthly$ = createEffect(() => {
        return this.actions$
          .pipe(
            ofType<RecurringClassAppliedMonthlyCreateSubmitted>(
                RecurringClassAppliedMonthlyActionTypes.RecurringClassAppliedMonthlyCreateSubmitted
            ),
            mergeMap(action => this.recurringScheduleService
              .applyRecurringClassToMonthAndYear(
                action.payload.recurringClassAppliedMonthly,
              ).pipe(catchError(err => {
                this.store.dispatch(
                  new RecurringClassAppliedMonthlyCreationCancelled({ err })
                );
                return of();
              }),
            )),
            map(
              recurringClassAppliedMonthly => new RecurringClassAppliedMonthlyAdded(
                { recurringClassAppliedMonthly }
              ),
            )
          )
      });

      constructor(
        private actions$: Actions,
        private recurringScheduleService: RecurringScheduleService,
        private store: Store<RecurringClassAppliedMonthlysState>
      ) {}
    
}