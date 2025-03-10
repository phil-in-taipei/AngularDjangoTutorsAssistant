import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { select, Store } from '@ngrx/store';
import { of } from 'rxjs';
import { 
    catchError, filter, map,
    mergeMap, withLatestFrom 
} from "rxjs/operators";

import { 
    ClassStatusUpdateCancelled,
    ClassStatusUpdateSaved, ClassStatusUpdateSubmitted,
    DailyClassesLoaded, DailyClassesRequestCancelled, 
    DailyClassesRequested, LandingPageScheduleLoaded,
    LandingPageScheduleRequestCancelled, LandingPageScheduleRequested, 
    MonthlyClassesRequested, MonthlyClassesRequestCancelled, MonthlyClassesLoaded,
    RescheduleClassCancelled, RescheduleClassSubmitted, 
    RescheduledClassUpdatedWithDailyBatchAdded, ScheduledClassesBatchDeletionCancelled, 
    ScheduledClassesBatchDeletionSaved, ScheduledClassesBatchDeletionSubmitted,
    ScheduleSingleClassCancelled, ScheduleSingleClassSubmitted,
    ScheduledSingleClassWithDailyBatchAdded, ScheduledClassesActionTypes, 
    ScheduledClassDeletionCancelled, ScheduledClassDeletionRequested, 
    ScheduledClassDeletionSaved, UnconfirmedScheduledClassesLoaded,
    UnconfirmedScheduledClassesRequestCancelled, UnconfirmedScheduledClassesRequested
} from './scheduled-classes.actions';
import { 
    landingPageScheduleLoaded, unconfirmedScheduledClassesLoaded 
} from './scheduled-classes.selectors';
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

      deleteBatchOfScheduledClasses$ = createEffect(() => {
        return this.actions$
            .pipe(
                ofType<ScheduledClassesBatchDeletionSubmitted>(
                  ScheduledClassesActionTypes.ScheduledClassesBatchDeletionSubmitted),
                    mergeMap(action => this.scheduledClassesService
                        .deleteBatchOfScheduledClasses(action.payload.obsolete_class_data)
                            .pipe(
                                map(
                                    batchDeletionResponse => new ScheduledClassesBatchDeletionSaved(
                                        batchDeletionResponse
                                    )
                                ),
                                catchError(err => {
                                    this.store.dispatch(
                                        new ScheduledClassesBatchDeletionCancelled({ err })
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

    fetchMonthlyClassse$ = createEffect(() => {
        return this.actions$
          .pipe(
            ofType<MonthlyClassesRequested>(ScheduledClassesActionTypes
              .MonthlyClassesRequested),
                  mergeMap(({payload}) => this.scheduledClassesService
                    .fetchClassesByMonth(payload.month, payload.year)
                        .pipe(
                            map(scheduledClasses => new MonthlyClassesLoaded(
                                { scheduledClasses })
                            ),
                            catchError(err => {
                                this.store.dispatch(
                                  new MonthlyClassesRequestCancelled({ err })
                                );
                                return of();
                            })
                        )
                )
          )
      });

    fetchUnconfirmedScheduledClasses$ = createEffect(() => {
        return this.actions$
          .pipe(
            ofType<UnconfirmedScheduledClassesRequested>(
                ScheduledClassesActionTypes.UnconfirmedScheduledClassesRequested
            ),
            withLatestFrom(this.store.pipe(select(unconfirmedScheduledClassesLoaded))),
            filter(([action, unconfirmedScheduledClassesLoaded]) => !unconfirmedScheduledClassesLoaded),
            mergeMap(action => this.scheduledClassesService.fetchUnconfirmedStatusClasses()
              .pipe(
                map(scheduledClasses => new UnconfirmedScheduledClassesLoaded({ scheduledClasses })),
                catchError(err => {
                  this.store.dispatch(
                      new UnconfirmedScheduledClassesRequestCancelled({ err })
                  );
                  return of();
                })
              )
            )
          )
      });

    submitEditedClassStatus$ = createEffect(() => {
        return this.actions$
            .pipe(
                ofType<ClassStatusUpdateSubmitted>(
                    ScheduledClassesActionTypes.ClassStatusUpdateSubmitted),
                    mergeMap(action => this.scheduledClassesService
                        .modifyClassStatus(
                            action.payload.scheduledClass,
                            ).pipe(catchError(err => {
                                this.store.dispatch(
                                    new ClassStatusUpdateCancelled({ err })
                                );
                                return of();
                            }),
                        )
                  ),
                  map(
                    scheduledClassUpdateResponse => new ClassStatusUpdateSaved(
                            { scheduledClassUpdateResponse }
                        ),
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
