// scheduled-classes.effects.spec.ts
import { TestBed, fakeAsync, flush } from "@angular/core/testing";
import { 
    modifyClassStatusData, 
} from "src/app/test-data/authenticated-user-module-tests/scheduling-module-tests/scheduled-classes-related-tests/scheduled-classes-data";
import { 
    CreateScheduledClassModel, RescheduleClassModel,
    ScheduledClassModel, ScheduledClassBatchDeletionDataModel, 
    ModifyClassStatusModel, ModifyClassStatusResponse
} from "src/app/models/scheduled-class.model";
import { Action } from "@ngrx/store";
import { provideMockActions } from "@ngrx/effects/testing";
import { from, Observable, of } from "rxjs";
import { toArray } from "rxjs/operators";
import { provideMockStore } from "@ngrx/store/testing";
import { initialScheduledClassesState } from "./scheduled-classes.reducers";
import { 
    scheduledClassesByDateData,
    scheduledClassesByMonthData,
    unconfirmedStatusClassesData,
    modifyClassStatusResponse,
    scheduledClassBatchDeletionData,
    batchDeletionResponseSuccess,
    deletionResponseSuccess,
    createScheduledClassData,
    rescheduleClassData,
} from "src/app/test-data/authenticated-user-module-tests/scheduling-module-tests/scheduled-classes-related-tests/scheduled-classes-data";

import {
  MonthlyClassesLoaded,
  MonthlyClassesRequested,
  ScheduleSingleClassSubmitted,
  ScheduledSingleClassWithDailyBatchAdded,
  ScheduledClassDeletionRequested,
  ScheduledClassDeletionSaved,
  ScheduledClassesBatchDeletionSubmitted,
  ScheduledClassesBatchDeletionSaved,
  DailyClassesRequested,
  DailyClassesLoaded,
  LandingPageScheduleRequested,
  LandingPageScheduleLoaded,
  UnconfirmedScheduledClassesRequested,
  UnconfirmedScheduledClassesLoaded,
  ClassStatusUpdateSubmitted,
  ClassStatusUpdateSaved,
  RescheduleClassSubmitted,
  RescheduledClassUpdatedWithDailyBatchAdded,
} from "./scheduled-classes.actions";
import {
  landingPageScheduleLoaded,
  unconfirmedScheduledClassesLoaded,
} from "./scheduled-classes.selectors";
import { ScheduledClassesEffects } from "./scheduled-classes.effects";
import { ClassesService } from "../classes-service/classes.service";

fdescribe("ScheduledClassesEffects", () => {
  let effects: ScheduledClassesEffects;
  let classesService: ClassesService;

  beforeEach(() => {
    const mockClassesService = {
      fetchClassesByMonth(month: number, year: number): Observable<ScheduledClassModel[]> {
        return of(scheduledClassesByMonthData);
      },
      fetchScheduledClassesByDate(date: string): Observable<ScheduledClassModel[]> {
        return of(scheduledClassesByDateData);
      },
      fetchTodaysClasses(): Observable<ScheduledClassModel[]> {
        return of(scheduledClassesByDateData);
      },
      fetchUnconfirmedStatusClasses(): Observable<ScheduledClassModel[]> {
        return of(unconfirmedStatusClassesData);
      },
      deleteSingleClass(id: number): Observable<{ id: number; message: string }> {
        return of(deletionResponseSuccess);
      },
      deleteBatchOfScheduledClasses(
        obsolete_class_data: ScheduledClassBatchDeletionDataModel
      ): Observable<{ ids: number[]; message: string }> {
        return of(batchDeletionResponseSuccess);
      },
      modifyClassStatus(
        submissionForm: ModifyClassStatusModel
      ): Observable<ModifyClassStatusResponse> {
        return of(modifyClassStatusResponse);
      },
      submitRescheduledClass(
        submissionForm: RescheduleClassModel
      ): Observable<ScheduledClassModel[]> {
        return of([
          {
            ...scheduledClassesByDateData[0],
            date: rescheduleClassData.date,
            start_time: rescheduleClassData.start_time,
            finish_time: rescheduleClassData.finish_time,
          },
        ]);
      },
      submitScheduledClass(
        submissionForm: CreateScheduledClassModel
      ): Observable<ScheduledClassModel[]> {
        return of([
          ...scheduledClassesByMonthData,
          {
            id: 6,
            date: createScheduledClassData.date,
            start_time: createScheduledClassData.start_time,
            finish_time: createScheduledClassData.finish_time,
            student_or_class: createScheduledClassData.student_or_class,
            teacher: createScheduledClassData.teacher,
            class_status: "scheduled",
            teacher_notes: "",
            class_content: "",
          },
        ]);
      },
    };

    TestBed.configureTestingModule({
      providers: [
        provideMockStore({
          initialState: initialScheduledClassesState,
          selectors: [
            {
              selector: landingPageScheduleLoaded,
              value: false,
            },
            {
              selector: unconfirmedScheduledClassesLoaded,
              value: false,
            },
          ],
        }),
        provideMockActions(
          from([
            new MonthlyClassesRequested({ month: 3, year: 2025 }),
            new DailyClassesRequested({ date: "2025-03-15" }),
            new LandingPageScheduleRequested(),
            new UnconfirmedScheduledClassesRequested(),
            new ScheduledClassDeletionRequested({ id: 1 }),
            new ScheduledClassesBatchDeletionSubmitted({
              obsolete_class_data: scheduledClassBatchDeletionData,
            }),
            new ScheduleSingleClassSubmitted({ scheduledClass: createScheduledClassData }),
            new ClassStatusUpdateSubmitted({ scheduledClass: modifyClassStatusData }),
            new RescheduleClassSubmitted(
                { id: rescheduleClassData.id, scheduledClass: rescheduleClassData }
            ),
          ])
        ),
        ScheduledClassesEffects,
        { provide: ClassesService, useValue: mockClassesService },
      ],
    });

    effects = TestBed.inject(ScheduledClassesEffects);
    classesService = TestBed.inject(ClassesService);
  });

  it("MonthlyClassesRequested should call fetch the scheduled classes for the current month and load them into state", fakeAsync(() => {
    spyOn(classesService, "fetchClassesByMonth").and.returnValue(
      of(scheduledClassesByMonthData)
    );
    let actualActions: Action[] | undefined;
    const expectedActions: Action[] = [new MonthlyClassesLoaded({ scheduledClasses: scheduledClassesByMonthData })];
    effects.fetchMonthlyClassse$.pipe(toArray()).subscribe({
      next: (actualActions2) => (actualActions = actualActions2),
      error: fail,
    });
    expect(actualActions).toEqual(expectedActions);
    flush();
  }));

  it("DailyClassesRequested should call fetch the scheduled classes for the given date and load them into state", fakeAsync(() => {
    spyOn(classesService, "fetchScheduledClassesByDate").and.returnValue(
      of(scheduledClassesByDateData)
    );
    let actualActions: Action[] | undefined;
    const expectedActions: Action[] = [new DailyClassesLoaded({ scheduledClasses: scheduledClassesByDateData })];
    effects.fetchDailyClasses$.pipe(toArray()).subscribe({
      next: (actualActions2) => (actualActions = actualActions2),
      error: fail,
    });
    expect(actualActions).toEqual(expectedActions);
    flush();
  }));

  it("LandingPageScheduleRequested should call fetch the scheduled classes for today and load them into state", fakeAsync(() => {
    spyOn(classesService, "fetchTodaysClasses").and.returnValue(
      of(scheduledClassesByDateData)
    );
    let actualActions: Action[] | undefined;
    const expectedActions: Action[] = [new LandingPageScheduleLoaded({ scheduledClasses: scheduledClassesByDateData })];
    effects.fetchLandingPageClasses$.pipe(toArray()).subscribe({
      next: (actualActions2) => (actualActions = actualActions2),
      error: fail,
    });
    expect(actualActions).toEqual(expectedActions);
    flush();
  }));

  it("UnconfirmedScheduledClassesRequested should call fetch the unconfirmed scheduled classes and load them into state", fakeAsync(() => {
    spyOn(classesService, "fetchUnconfirmedStatusClasses").and.returnValue(
      of(unconfirmedStatusClassesData)
    );
    let actualActions: Action[] | undefined;
    const expectedActions: Action[] = [new UnconfirmedScheduledClassesLoaded({ scheduledClasses: unconfirmedStatusClassesData })];
    effects.fetchUnconfirmedScheduledClasses$.pipe(toArray()).subscribe({
      next: (actualActions2) => (actualActions = actualActions2),
      error: fail,
    });
    expect(actualActions).toEqual(expectedActions);
    flush();
  }));

  it("ScheduledClassDeletionRequested should handle the deletion response with message/id by calling the save method to remove the scheduled class from state", fakeAsync(() => {
    spyOn(classesService, "deleteSingleClass").and.returnValue(
      of(deletionResponseSuccess)
    );
    let actualActions: Action[] | undefined;
    const expectedActions: Action[] = [new ScheduledClassDeletionSaved(deletionResponseSuccess)];
    effects.deleteScheduledClass$.pipe(toArray()).subscribe({
      next: (actualActions2) => (actualActions = actualActions2),
      error: fail,
    });
    expect(actualActions).toEqual(expectedActions);
    flush();
  }));

  it("ScheduledClassesBatchDeletionSubmitted should handle the batch deletion response with message/ids by calling the save method to remove the scheduled classes from state", fakeAsync(() => {
    spyOn(classesService, "deleteBatchOfScheduledClasses").and.returnValue(
      of(batchDeletionResponseSuccess)
    );
    let actualActions: Action[] | undefined;
    const expectedActions: Action[] = [new ScheduledClassesBatchDeletionSaved(batchDeletionResponseSuccess)];
    effects.deleteBatchOfScheduledClasses$.pipe(toArray()).subscribe({
      next: (actualActions2) => (actualActions = actualActions2),
      error: fail,
    });
    expect(actualActions).toEqual(expectedActions);
    flush();
  }));

  it("ScheduleSingleClassSubmitted should submit new scheduled class data to backend and save the returned newly created object along with other classes scheduled on given date in state", fakeAsync(() => {
    spyOn(classesService, "submitScheduledClass").and.returnValue(
      of([
        ...scheduledClassesByMonthData,
        {
          id: 6,
          date: createScheduledClassData.date,
          start_time: createScheduledClassData.start_time,
          finish_time: createScheduledClassData.finish_time,
          student_or_class: createScheduledClassData.student_or_class,
          teacher: createScheduledClassData.teacher,
          class_status: "scheduled",
          teacher_notes: "",
          class_content: "",
        },
      ])
    );
    let actualActions: Action[] | undefined;
    const expectedActions: Action[] = [
      new ScheduledSingleClassWithDailyBatchAdded({
        scheduledClasses: [
          ...scheduledClassesByMonthData,
          {
            id: 6,
            date: createScheduledClassData.date,
            start_time: createScheduledClassData.start_time,
            finish_time: createScheduledClassData.finish_time,
            student_or_class: createScheduledClassData.student_or_class,
            teacher: createScheduledClassData.teacher,
            class_status: "scheduled",
            teacher_notes: "",
            class_content: "",
          },
        ],
      }),
    ];
    effects.submitScheduledClass$.pipe(toArray()).subscribe({
      next: (actualActions2) => (actualActions = actualActions2),
      error: fail,
    });
    expect(actualActions).toEqual(expectedActions);
    flush();
  }));

  it("ClassStatusUpdateSubmitted should submit the updated class status to backend and save the returned updated object in state", fakeAsync(() => {
    spyOn(classesService, "modifyClassStatus").and.returnValue(
      of(modifyClassStatusResponse)
    );
    let actualActions: Action[] | undefined;
    const expectedActions: Action[] = [new ClassStatusUpdateSaved({ scheduledClassUpdateResponse: modifyClassStatusResponse })];
    effects.submitEditedClassStatus$.pipe(toArray()).subscribe({
      next: (actualActions2) => (actualActions = actualActions2),
      error: fail,
    });
    expect(actualActions).toEqual(expectedActions);
    flush();
  }));

  it("RescheduleClassSubmitted should submit the rescheduled class to backend and save the returned updated object in state", fakeAsync(() => {
    spyOn(classesService, "submitRescheduledClass").and.returnValue(
      of([
        {
          ...scheduledClassesByDateData[0],
          date: rescheduleClassData.date,
          start_time: rescheduleClassData.start_time,
          finish_time: rescheduleClassData.finish_time,
        },
      ])
    );
    let actualActions: Action[] | undefined;
    const expectedActions: Action[] = [
      new RescheduledClassUpdatedWithDailyBatchAdded({
        scheduledClasses: [
          {
            ...scheduledClassesByDateData[0],
            date: rescheduleClassData.date,
            start_time: rescheduleClassData.start_time,
            finish_time: rescheduleClassData.finish_time,
          },
        ],
      }),
    ];
    effects.submitRescheduledClass$.pipe(toArray()).subscribe({
      next: (actualActions2) => (actualActions = actualActions2),
      error: fail,
    });
    expect(actualActions).toEqual(expectedActions);
    flush();
  }));
});
