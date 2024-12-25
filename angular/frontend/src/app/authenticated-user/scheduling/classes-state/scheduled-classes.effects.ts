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
    ScheduledClassesActionTypes
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

}
