// recurring-class-applied-monthly.effects.spec.ts
import { TestBed, fakeAsync, flush } from "@angular/core/testing";
import { Action } from "@ngrx/store";
import { provideMockActions } from "@ngrx/effects/testing";
import { from, Observable, of } from "rxjs";
import { toArray } from "rxjs/operators";
import { provideMockStore } from "@ngrx/store/testing";

import { initialRecurringClassAppliedMonthlysState } from "./recurring-class-applied-monthly.reducers";
import {
  recurringClassAppliedMonthliesData,
  recurringClassAppliedMonthlyCreateData,
  newlyCreatedRecurringClassAppliedMonthlyData,
  recurringClassAppliedMonthlyDeletionResponse,
} from "src/app/test-data/authenticated-user-module-tests/scheduling-module-tests/scheduled-classes-related-tests/recurring-schedule-module-tests/recurring-schedule-related-tests/recurring-schedule-data";
import {
  RecurringClassAppliedMonthlysRequested,
  RecurringClassAppliedMonthlysLoaded,
  RecurringClassAppliedMonthlyCreateSubmitted,
  RecurringClassAppliedMonthlyAdded,
  RecurringClassAppliedMonthlyDeletionRequested,
  RecurringClassAppliedMonthlyDeletionSaved,
} from "./recurring-class-applied-monthly.actions";
import { RecurringClassAppliedMonthlysEffects } from "./recurring-class-applied-monthly.effects";
import { RecurringScheduleService } from "../../recurring-schedule-service/recurring-schedule.service";
import {
  RecurringClassAppliedMonthlyModel,
  RecurringClassAppliedMonthlyDeletionResponse,
} from "src/app/models/recurring-schedule.model";

fdescribe("RecurringClassAppliedMonthlysEffects", () => {
  let effects: RecurringClassAppliedMonthlysEffects;
  let recurringScheduleService: RecurringScheduleService;

  beforeEach(() => {
    const mockRecurringScheduleService = {
      fetchRecurringClassAppliedMonthlysByMonthAndYear(
        month: number,
        year: number
      ): Observable<RecurringClassAppliedMonthlyModel[]> {
        return of(recurringClassAppliedMonthliesData);
      },
      deleteRecurringClassAppliedMonthly(
        id: number
      ): Observable<RecurringClassAppliedMonthlyDeletionResponse> {
        return of(recurringClassAppliedMonthlyDeletionResponse);
      },
      applyRecurringClassToMonthAndYear(
        submissionForm: any
      ): Observable<RecurringClassAppliedMonthlyModel> {
        return of(newlyCreatedRecurringClassAppliedMonthlyData);
      },
    };

    TestBed.configureTestingModule({
      providers: [
        provideMockStore({
          initialState: initialRecurringClassAppliedMonthlysState,
        }),
        provideMockActions(
          from([
            new RecurringClassAppliedMonthlysRequested({ month: 3, year: 2025 }),
            new RecurringClassAppliedMonthlyCreateSubmitted({
              recurringClassAppliedMonthly: recurringClassAppliedMonthlyCreateData,
            }),
            new RecurringClassAppliedMonthlyDeletionRequested({ id: 3 }),
          ])
        ),
        RecurringClassAppliedMonthlysEffects,
        { provide: RecurringScheduleService, useValue: mockRecurringScheduleService },
      ],
    });

    effects = TestBed.inject(RecurringClassAppliedMonthlysEffects);
    recurringScheduleService = TestBed.inject(RecurringScheduleService);
  });

  it("RecurringClassAppliedMonthlysRequested should fetch the recurring classes applied monthly for the given month and year and load them into state", fakeAsync(() => {
    spyOn(
      recurringScheduleService,
      "fetchRecurringClassAppliedMonthlysByMonthAndYear"
    ).and.returnValue(of(recurringClassAppliedMonthliesData));
    let actualActions: Action[] | undefined;
    const expectedActions: Action[] = [
      new RecurringClassAppliedMonthlysLoaded({
        recurringClassesAppliedMonthly: recurringClassAppliedMonthliesData,
      }),
    ];
    effects.fetchRecurringClassesAppliedMonthlys$.pipe(toArray()).subscribe({
      next: (actualActions2) => (actualActions = actualActions2),
      error: fail,
    });
    expect(actualActions).toEqual(expectedActions);
    flush();
  }));

  it("RecurringClassAppliedMonthlyCreateSubmitted should submit new recurring class applied monthly data to backend and save the returned newly created object in state", fakeAsync(() => {
    spyOn(recurringScheduleService, "applyRecurringClassToMonthAndYear").and.returnValue(
      of(newlyCreatedRecurringClassAppliedMonthlyData)
    );
    let actualActions: Action[] | undefined;
    const expectedActions: Action[] = [
      new RecurringClassAppliedMonthlyAdded({
        recurringClassAppliedMonthly: newlyCreatedRecurringClassAppliedMonthlyData,
      }),
    ];
    effects.submitRecurringClassAppliedMonthly$.pipe(toArray()).subscribe({
      next: (actualActions2) => (actualActions = actualActions2),
      error: fail,
    });
    expect(actualActions).toEqual(expectedActions);
    flush();
  }));

  it("RecurringClassAppliedMonthlyDeletionRequested should handle the deletion response with message/id and optional batch deletion data by calling the save method to remove the recurring class applied monthly from state", fakeAsync(() => {
    spyOn(recurringScheduleService, "deleteRecurringClassAppliedMonthly").and.returnValue(
      of(recurringClassAppliedMonthlyDeletionResponse)
    );
    let actualActions: Action[] | undefined;
    const expectedActions: Action[] = [
      new RecurringClassAppliedMonthlyDeletionSaved({
        recurringClassAppliedMonthlyDeletionResponse:
          recurringClassAppliedMonthlyDeletionResponse,
      }),
    ];
    effects.deleteRecurringClassAppliedMonthly$.pipe(toArray()).subscribe({
      next: (actualActions2) => (actualActions = actualActions2),
      error: fail,
    });
    expect(actualActions).toEqual(expectedActions);
    flush();
  }));
});