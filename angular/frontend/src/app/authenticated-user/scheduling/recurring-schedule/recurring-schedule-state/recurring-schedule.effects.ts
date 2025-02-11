import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { select, Store } from '@ngrx/store';
import { of } from 'rxjs';
import { catchError, filter, map, mergeMap, withLatestFrom } from 'rxjs/operators';

import { RecurringClassesState } from './recurring-schedule.reducers';

import { selectRecurringClassesLoaded } from './recurring-schedule.selectors';
import {
  RecurringClassesActionTypes,
  RecurringClassAdded,
  RecurringClassCreateSubmitted,
  RecurringClassCreationCancelled,
  RecurringClassDeletionCancelled,
  RecurringClassDeletionRequested,
  RecurringClassDeletionSaved,
  RecurringClassesLoaded,
  RecurringClassesRequestCancelled,
  RecurringClassesRequested
} from './recurring-schedule.actions';
import { RecurringScheduleService } from '../recurring-schedule-service/recurring-schedule.service';

@Injectable()
export class RecurringClassesEffects {

  deleteRecurringClass$ = createEffect(() => {
    return this.actions$
      .pipe(
        ofType<RecurringClassDeletionRequested>(
          RecurringClassesActionTypes.RecurringClassDeletionRequested
        ),
        mergeMap(action => this.recurringClassService
          .deleteRecurringClass(action.payload.id)
          .pipe(
            map(deletionResponse => new RecurringClassDeletionSaved(
              deletionResponse
            )),
            catchError(err => {
              this.store.dispatch(
                new RecurringClassDeletionCancelled({ err })
              );
              return of();
            })
          )
        )
      )
  });

  fetchRecurringClasses$ = createEffect(() => {
    return this.actions$
      .pipe(
        ofType<RecurringClassesRequested>(
          RecurringClassesActionTypes.RecurringClassesRequested
        ),
        withLatestFrom(this.store.pipe(select(selectRecurringClassesLoaded))),
        filter(([action, recurringClassesLoaded]) => !recurringClassesLoaded),
        mergeMap(action => this.recurringClassService.fetchRecurringClasses()
          .pipe(
            map(recurringClasses => new RecurringClassesLoaded({ monthlyTasks: recurringClasses })),
            catchError(err => {
              this.store.dispatch(
                new RecurringClassesRequestCancelled({ err })
              );
              return of();
            })
          )
        )
      )
  });

  submitRecurringClass$ = createEffect(() => {
    return this.actions$
      .pipe(
        ofType<RecurringClassCreateSubmitted>(
          RecurringClassesActionTypes.RecurringClassCreateSubmitted
        ),
        mergeMap(action => this.recurringClassService
          .submitRecurringClass(
            action.payload.monthlyTask,
          ).pipe(catchError(err => {
            this.store.dispatch(
              new RecurringClassCreationCancelled({ err })
            );
            return of();
          }),
          )
        ),
        map(
          recurringClass => new RecurringClassAdded(
            { recurringClass }
          ),
        )
      )
  });

  constructor(
    private actions$: Actions,
    private recurringClassService: RecurringScheduleService,
    private store: Store<RecurringClassesState>
  ) {}
}
