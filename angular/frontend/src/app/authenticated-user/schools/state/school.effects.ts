import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { select, Store } from '@ngrx/store';
import { of } from 'rxjs';
import { catchError, filter, map,
    mergeMap, withLatestFrom 
} from "rxjs/operators";

import { AppState } from 'src/app/reducers';

import {
    SchoolActionTypes, SchoolCreatedAdded,
    SchoolCreateSubmitted, SchoolCreationCancelled,
    SchoolDeletionCancelled, SchoolDeletionRequested,
    SchoolDeletionSaved, SchoolEditCancelled, 
    SchoolEditSubmitted, SchoolEditUpdated, SchoolsLoaded,
    SchoolsRequestCancelled, SchoolsRequested 
} from './school.actions';
import { schoolsLoadedInState } from './school.selectors';
import { SchoolService } from '../service/school.service';

@Injectable()
export class SchoolsEffects {
  
    deleteSchool$ = createEffect(() => {
        return this.actions$
            .pipe(
                ofType<SchoolDeletionRequested>(
                  SchoolActionTypes.SchoolDeletionRequested),
                    mergeMap(action => this.schoolService
                        .deleteSchool(action.payload.id)
                            .pipe(
                                map(deletionResponse => new SchoolDeletionSaved(
                                    deletionResponse)
                                ),
                                catchError(err => {
                                    this.store.dispatch(
                                        new SchoolDeletionCancelled({ err })
                                    );
                                    return of();
                                })
                            )
                    )
            )
    });

    editSchool$ = createEffect(() => {
        return this.actions$
            .pipe(
                ofType<SchoolEditSubmitted>(
                    SchoolActionTypes.SchoolEditSubmitted),
                    mergeMap(action => this.schoolService
                        .editSchool(
                            action.payload.id,
                            action.payload.school
                            ).pipe(catchError(err => {
                                this.store.dispatch(
                                    new SchoolEditCancelled({ err })
                                );
                                return of();
                            }),
                        )
                    ),
                    map(school => new SchoolEditUpdated(
                        { school:
                            { id: school.id, changes: school }
                        }
                    ),
                )   
            )
    });
    
    fetchUsersSchools$ = createEffect(() => {
        return this.actions$
          .pipe(
            ofType<SchoolsRequested>(
                SchoolActionTypes.SchoolsRequested
            ),
            withLatestFrom(this.store.pipe(select(schoolsLoadedInState))),
            filter(([action, schoolsLoaded]) => !schoolsLoaded),
            mergeMap(action => this.schoolService.fetchUsersSchools()
              .pipe(
                map(schools => new SchoolsLoaded({ schools })),
                catchError(err => {
                  this.store.dispatch(
                      new SchoolsRequestCancelled({ err })
                  );
                  return of();
                })
              )
            )
        )
    });

    submitSchool$ = createEffect(() => {
        return this.actions$
            .pipe(
                ofType<SchoolCreateSubmitted>(
                    SchoolActionTypes.SchoolCreateSubmitted),
                    mergeMap(action => this.schoolService
                        .submitSchool(
                            action.payload.school,
                            ).pipe(catchError(err => {
                                this.store.dispatch(
                                    new SchoolCreationCancelled({ err })
                                );
                                return of();
                            }),
                        )
                  ),
                  map(
                    school => new SchoolCreatedAdded(
                            { school }
                        ),
                  )
            )
    });


    constructor(
        private actions$: Actions, 
        private schoolService: SchoolService, 
        private store: Store<AppState>
    ) {}
}
