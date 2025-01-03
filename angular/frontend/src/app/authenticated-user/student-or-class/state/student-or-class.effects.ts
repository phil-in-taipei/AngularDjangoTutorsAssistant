import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { select, Store } from '@ngrx/store';
import { of } from 'rxjs';
import { catchError, filter, map,
    mergeMap, withLatestFrom 
} from "rxjs/operators";

import { AppState } from 'src/app/reducers';

import {
    StudentOrClassActionTypes, StudentOrClassCreatedAdded,
    StudentOrClassCreateSubmitted, StudentOrClassCreationCancelled,
    StudentOrClassDeletionCancelled, StudentOrClassDeletionRequested,
    StudentOrClassDeletionSaved, StudentOrClassEditCancelled,
    StudentOrClassEditSubmitted, StudentOrClassEditUpdated, StudentsOrClassesLoaded,
    StudentsOrClassesRequestCancelled, StudentsOrClassesRequested
} from './student-or-class.actions';
import { studentsOrClassesLoadedInState } from './student-or-class.selectors';
import { StudentOrClassService } from '../service/student-or-class.service';

@Injectable()
export class StudentsOrClassesEffects {

    deleteStudentOrClass$ = createEffect(() => {
        return this.actions$
            .pipe(
                ofType<StudentOrClassDeletionRequested>(
                  StudentOrClassActionTypes.StudentOrClassDeletionRequested),
                    mergeMap(action => this.studentOrClassService
                        .deleteStudentOrClass(action.payload.id)
                            .pipe(
                                map(deletionResponse => new StudentOrClassDeletionSaved(
                                    deletionResponse)
                                ),
                                catchError(err => {
                                    this.store.dispatch(
                                        new StudentOrClassDeletionCancelled({ err })
                                    );
                                    return of();
                                })
                            )
                    )
            )
    });

    editStudentOrClass$ = createEffect(() => {
        return this.actions$
            .pipe(
                ofType<StudentOrClassEditSubmitted>(
                    StudentOrClassActionTypes.StudentOrClassEditSubmitted),
                    mergeMap(action => this.studentOrClassService
                        .editStudentOrClass(
                            action.payload.id,
                            action.payload.studentOrClass
                            ).pipe(catchError(err => {
                                this.store.dispatch(
                                    new StudentOrClassEditCancelled({ err })
                                );
                                return of();
                            }),
                        )
                    ),
                    map(studentOrClass => new StudentOrClassEditUpdated(
                        { studentOrClass:
                            { id: studentOrClass.id, changes: studentOrClass }
                        }
                    ),
                )
            )
    });

    fetchUsersStudentsOrClasses$ = createEffect(() => {
        return this.actions$
          .pipe(
            ofType<StudentsOrClassesRequested>(
                StudentOrClassActionTypes.StudentsOrClassesRequested
            ),
            withLatestFrom(this.store.pipe(select(studentsOrClassesLoadedInState))),
            filter(([action, studentsOrClassesLoaded]) => !studentsOrClassesLoaded),
            mergeMap(action => this.studentOrClassService.fetchUsersStudentsOrClasses()
              .pipe(
                map(studentsOrClasses => new StudentsOrClassesLoaded({ studentsOrClasses })),
                catchError(err => {
                  this.store.dispatch(
                      new StudentsOrClassesRequestCancelled({ err })
                  );
                  return of();
                })
              )
            )
        )
    });

    submitStudentOrClass$ = createEffect(() => {
        return this.actions$
            .pipe(
                ofType<StudentOrClassCreateSubmitted>(
                    StudentOrClassActionTypes.StudentOrClassCreateSubmitted),
                    mergeMap(action => this.studentOrClassService
                        .submitStudentOrClass(
                            action.payload.studentOrClass,
                            ).pipe(catchError(err => {
                                this.store.dispatch(
                                    new StudentOrClassCreationCancelled({ err })
                                );
                                return of();
                            }),
                        )
                  ),
                  map(
                    studentOrClass => new StudentOrClassCreatedAdded(
                            { studentOrClass }
                        ),
                  )
            )
    });

    constructor(
        private actions$: Actions,
        private studentOrClassService: StudentOrClassService,
        private store: Store<AppState>
    ) {}
}
