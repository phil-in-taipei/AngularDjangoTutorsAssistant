import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { select, Store } from '@ngrx/store';
import { of } from 'rxjs';
import { catchError, filter, map,
    mergeMap, withLatestFrom 
} from "rxjs/operators";

import { 
    DailyClassesLoaded, DailyClassesRequestCancelled, 
    DailyClassesRequested, LandingPageScheduleLoaded,
    LandingPageScheduleRequestCancelled, LandingPageScheduleRequested, 
    RescheduleClassCancelled, RescheduleClassSubmitted, 
    RescheduledClassUpdatedWithDailyBatchAdded,
    ScheduleSingleClassCancelled, ScheduleSingleClassSubmitted,
    ScheduledSingleClassWithDailyBatchAdded,
    ScheduledClassesActionTypes, ScheduledClassDeletionCancelled,
    ScheduledClassDeletionRequested, ScheduledClassDeletionSaved
} from './scheduled-classes.actions';
import { landingPageScheduleLoaded } from './scheduled-classes.selectors';
import { ClassesService } from '../classes-service/classes.service';
import { ScheduledClassesState } from './scheduled-classes.reducers';



@Injectable()
export class ScheduledClassesEffects {

    constructor(
        private actions$: Actions, 
        private scheduledClassesService: ClassesService, 
        private store: Store<ScheduledClassesState>
    ) {}

 
    deleteScheduledClass$ = createEffect(() => {
      return this.actions$
          .pipe(
              ofType<ScheduledClassDeletionRequested>(
                ScheduledClassesActionTypes.ScheduledClassDeletionRequested),
                  mergeMap(action => this.scheduledClassesService
                      .deleteSingleClass(action.payload.id)
                          .pipe(
                              map(deletionResponse => new ScheduledClassDeletionSaved(
                                  deletionResponse)
                              ),
                              catchError(err => {
                                  this.store.dispatch(
                                      new ScheduledClassDeletionCancelled({ err })
                                  );
                                  return of();
                              })
                          )
                  )
          )
      });



    fetchDailyClasses$ = createEffect(() => {
        return this.actions$
          .pipe(
            ofType<DailyClassesRequested>(
                ScheduledClassesActionTypes.DailyClassesRequested
            ),
            mergeMap(action => this.scheduledClassesService.fetchScheduledClassesByDate(
                action.payload.date
              )
              .pipe(
                map(scheduledClasses => new DailyClassesLoaded({ scheduledClasses })),
                catchError(err => {
                  this.store.dispatch(
                      new DailyClassesRequestCancelled({ err })
                  );
                  return of();
                })
              )
            )
          )
      });

   
      fetchLandingPageClasses$ = createEffect(() => {
        return this.actions$
          .pipe(
            ofType<LandingPageScheduleRequested>(
                ScheduledClassesActionTypes.LandingPageScheduleRequested
            ),
            withLatestFrom(this.store.pipe(select(landingPageScheduleLoaded))),
            filter(([action, landingPageScheduleLoaded]) => !landingPageScheduleLoaded),
            mergeMap(action => this.scheduledClassesService.fetchTodaysClasses()
              .pipe(
                map(scheduledClasses => new LandingPageScheduleLoaded({ scheduledClasses })),
                catchError(err => {
                  this.store.dispatch(
                      new LandingPageScheduleRequestCancelled({ err })
                  );
                  return of();
                })
              )
            )
          )
      });

      submitRescheduledClass$ = createEffect(() => {
        return this.actions$
            .pipe(
                ofType<RescheduleClassSubmitted>(
                    ScheduledClassesActionTypes.RescheduleClassSubmitted),
                    mergeMap(action => this.scheduledClassesService
                        .submitRescheduledClass(
                            action.payload.scheduledClass,
                            ).pipe(catchError(err => {
                                this.store.dispatch(
                                    new RescheduleClassCancelled({ err })
                                );
                                return of();
                            }),
                        )
                  ),
                  map(
                    scheduledClasses => new RescheduledClassUpdatedWithDailyBatchAdded(
                            { scheduledClasses }
                        ),
                  )
            )
    });

      submitScheduledClass$ = createEffect(() => {
        return this.actions$
            .pipe(
                ofType<ScheduleSingleClassSubmitted>(
                    ScheduledClassesActionTypes.ScheduleSingleClassSubmitted),
                    mergeMap(action => this.scheduledClassesService
                        .submitScheduledClass(
                            action.payload.scheduledClass,
                            ).pipe(catchError(err => {
                                this.store.dispatch(
                                    new ScheduleSingleClassCancelled({ err })
                                );
                                return of();
                            }),
                        )
                  ),
                  map(
                    scheduledClasses => new ScheduledSingleClassWithDailyBatchAdded(
                            { scheduledClasses }
                        ),
                  )
            )
    });



}
