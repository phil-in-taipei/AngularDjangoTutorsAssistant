// recurring-schedule.effects.spec.ts
import { TestBed, fakeAsync, flush } from "@angular/core/testing";
import { Action } from "@ngrx/store";
import { provideMockActions } from "@ngrx/effects/testing";
import { from, Observable, of } from "rxjs";
import { toArray } from "rxjs/operators";
import { provideMockStore } from "@ngrx/store/testing";

import { initialRecurringClassesState } from "./recurring-schedule.reducers";
import {
  recurringClassesData,
  recurringClassCreateData,
  recurringClassCreatedResponseData,
  deletionResponseSuccess,
} from "src/app/test-data/authenticated-user-module-tests/scheduling-module-tests/scheduled-classes-related-tests/recurring-schedule-module-tests/recurring-schedule-related-tests/recurring-schedule-data";
import {
  RecurringClassesRequested,
  RecurringClassesLoaded,
  RecurringClassCreateSubmitted,
  RecurringClassAdded,
  RecurringClassDeletionRequested,
  RecurringClassDeletionSaved,
} from "./recurring-schedule.actions";
import { selectRecurringClassesLoaded } from "./recurring-schedule.selectors";
import { RecurringClassesEffects } from "./recurring-schedule.effects";
import { RecurringScheduleService } from "../../recurring-schedule-service/recurring-schedule.service";
import { RecurringClassModel } from "src/app/models/recurring-schedule.model";

fdescribe("RecurringClassesEffects", () => {
  let effects: RecurringClassesEffects;
  let recurringScheduleService: RecurringScheduleService;

  beforeEach(() => {
    const mockRecurringScheduleService = {
      fetchRecurringClasses(): Observable<RecurringClassModel[]> {
        return of(recurringClassesData);
      },
      deleteRecurringClass(id: number): Observable<{ id: number; message: string }> {
        return of(deletionResponseSuccess);
      },
      submitRecurringClass(submissionForm: any): Observable<RecurringClassModel> {
        return of(recurringClassCreatedResponseData);
      },
    };

    TestBed.configureTestingModule({
      providers: [
        provideMockStore({
          initialState: initialRecurringClassesState,
          selectors: [
            {
              selector: selectRecurringClassesLoaded,
              value: false,
            },
          ],
        }),
        provideMockActions(
          from([
            new RecurringClassesRequested(),
            new RecurringClassCreateSubmitted({ recurringClass: recurringClassCreateData }),
            new RecurringClassDeletionRequested({ id: 1 }),
          ])
        ),
        RecurringClassesEffects,
        { provide: RecurringScheduleService, useValue: mockRecurringScheduleService },
      ],
    });

    effects = TestBed.inject(RecurringClassesEffects);
    recurringScheduleService = TestBed.inject(RecurringScheduleService);
  });

  it("RecurringClassesRequested should fetch the recurring classes and load them into state", fakeAsync(() => {
    spyOn(recurringScheduleService, "fetchRecurringClasses").and.returnValue(
      of(recurringClassesData)
    );
    let actualActions: Action[] | undefined;
    const expectedActions: Action[] = [
      new RecurringClassesLoaded({ recurringClasses: recurringClassesData })
    ];
    effects.fetchRecurringClasses$.pipe(toArray()).subscribe({
      next: (actualActions2) => (actualActions = actualActions2),
      error: fail,
    });
    expect(actualActions).toEqual(expectedActions);
    flush();
  }));

  it("RecurringClassCreateSubmitted should submit new recurring class data to backend and save the returned newly created object in state", fakeAsync(() => {
    spyOn(recurringScheduleService, "submitRecurringClass").and.returnValue(
      of(recurringClassCreatedResponseData)
    );
    let actualActions: Action[] | undefined;
    const expectedActions: Action[] = [
      new RecurringClassAdded({ recurringClass: recurringClassCreatedResponseData })
    ];
    effects.submitRecurringClass$.pipe(toArray()).subscribe({
      next: (actualActions2) => (actualActions = actualActions2),
      error: fail,
    });
    expect(actualActions).toEqual(expectedActions);
    flush();
  }));

  it("RecurringClassDeletionRequested should handle the deletion response with message/id by calling the save method to remove the recurring class from state", fakeAsync(() => {
    spyOn(recurringScheduleService, "deleteRecurringClass").and.returnValue(
      of(deletionResponseSuccess)
    );
    let actualActions: Action[] | undefined;
    const expectedActions: Action[] = [
      new RecurringClassDeletionSaved(deletionResponseSuccess)
    ];
    effects.deleteRecurringClass$.pipe(toArray()).subscribe({
      next: (actualActions2) => (actualActions = actualActions2),
      error: fail,
    });
    expect(actualActions).toEqual(expectedActions);
    flush();
  }));
});
