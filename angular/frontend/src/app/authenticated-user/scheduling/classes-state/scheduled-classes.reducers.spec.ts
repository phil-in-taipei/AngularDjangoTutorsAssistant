// scheduled-classes.reducer.spec.ts
import {
  initialScheduledClassesState,
  scheduledClassesReducer,
} from "./scheduled-classes.reducers";
import {
   statePriorToNewScheduledClassSubmitted,
  stateAfterNewScheduledClassSubmitted,
  stateAfterNewScheduledClassSubmissionFailure,
  stateAfterClassStatusUpdate,
  stateAfterClassStatusUpdateFailure,
  stateAfterClassRescheduled,
  stateAfterClassRescheduleFailure,
  stateAfterClassDeleted,
  stateAfterClassDeletionFailure,
  stateAfterBatchDeletion,
  stateAfterBatchDeletionFailure,
} from "src/app/test-data/authenticated-user-module-tests/scheduling-module-tests/scheduled-classes-state";
import {
  ScheduledClassesCleared,
  ScheduledSingleClassWithDailyBatchAdded,
  ScheduleSingleClassCancelled,
  ClassStatusUpdateSaved,
  ClassStatusUpdateCancelled,
  RescheduledClassUpdatedWithDailyBatchAdded,
  RescheduleClassCancelled,
  ScheduledClassDeletionSaved,
  ScheduledClassDeletionCancelled,
  ScheduledClassesBatchDeletionSaved,
  ScheduledClassesBatchDeletionCancelled,
} from "./scheduled-classes.actions";
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


fdescribe("scheduledClassesReducer", () => {
  it("returns an initial state when cleared", () => {
    const state = scheduledClassesReducer(
      { ...initialScheduledClassesState, successMessage: "Test" },
      new ScheduledClassesCleared()
    );
    expect(state).toEqual(initialScheduledClassesState);
  });

  
  it("returns the state with new scheduled class entity and indicates that the scheduled class has been successfully submitted", () => {
    const newClass = {
      id: 6,
      date: createScheduledClassData.date,
      start_time: createScheduledClassData.start_time,
      finish_time: createScheduledClassData.finish_time,
      student_or_class: createScheduledClassData.student_or_class,
      teacher: createScheduledClassData.teacher,
      class_status: "scheduled",
      teacher_notes: "",
      class_content: "",
    };
    const allClasses = [...scheduledClassesByMonthData, newClass];
    const state = scheduledClassesReducer(
      statePriorToNewScheduledClassSubmitted.scheduledClasses,
      new ScheduledSingleClassWithDailyBatchAdded({ scheduledClasses: allClasses })
    );
    expect(state).toEqual(stateAfterNewScheduledClassSubmitted.scheduledClasses);
  });

  it("returns the state with originally loaded scheduled classes entity and indicates that submission of a new scheduled class has been unsuccessful", () => {
    const state = scheduledClassesReducer(
      statePriorToNewScheduledClassSubmitted.scheduledClasses,
      new ScheduleSingleClassCancelled({
        err: { error: { Error: "Error scheduling class!" } },
      })
    );
    expect(state).toEqual(stateAfterNewScheduledClassSubmissionFailure.scheduledClasses);
  });

  it("returns the state with updated scheduled class entity and indicates that the class status has been successfully updated", () => {
    const state = scheduledClassesReducer(
      statePriorToNewScheduledClassSubmitted.scheduledClasses,
      new ClassStatusUpdateSaved({ scheduledClassUpdateResponse: modifyClassStatusResponse })
    );
    // Remove errMsg from expected state (it was a typo in the reducer)
    const expectedState = {
      ...stateAfterClassStatusUpdate.scheduledClasses,
      errorMessage: undefined,
    };
    expect(state).toEqual(expectedState);
  });

  it("returns the state with originally loaded scheduled classes entity and indicates that the class status update has failed", () => {
    const state = scheduledClassesReducer(
      statePriorToNewScheduledClassSubmitted.scheduledClasses,
      new ClassStatusUpdateCancelled({
        err: { error: { Error: "Error! Class Status Update Failed!" } },
      })
    );
    expect(state).toEqual(stateAfterClassStatusUpdateFailure.scheduledClasses);
  });

  it("returns the state with rescheduled class entity and indicates that the class has been successfully rescheduled", () => {
    const rescheduledClass = {
      ...scheduledClassesByDateData[0],
      date: rescheduleClassData.date,
      start_time: rescheduleClassData.start_time,
      finish_time: rescheduleClassData.finish_time,
    };
    const allClasses = [...scheduledClassesByMonthData.filter((sc) => sc.id !== 1), rescheduledClass];
    const state = scheduledClassesReducer(
      statePriorToNewScheduledClassSubmitted.scheduledClasses,
      new RescheduledClassUpdatedWithDailyBatchAdded({ scheduledClasses: allClasses })
    );
    expect(state).toEqual(stateAfterClassRescheduled.scheduledClasses);
  });

  it("returns the state with originally loaded scheduled classes entity and indicates that the class rescheduling has failed", () => {
    const state = scheduledClassesReducer(
      statePriorToNewScheduledClassSubmitted.scheduledClasses,
      new RescheduleClassCancelled({
        err: { error: { Error: "Error! Rescheduling Failed!" } },
      })
    );
    expect(state).toEqual(stateAfterClassRescheduleFailure.scheduledClasses);
  });

  it("returns the state with the scheduled class removed and indicates that the class has been successfully deleted", () => {
    const state = scheduledClassesReducer(
      statePriorToNewScheduledClassSubmitted.scheduledClasses,
      new ScheduledClassDeletionSaved(deletionResponseSuccess)
    );
    expect(state).toEqual(stateAfterClassDeleted.scheduledClasses);
  });

  it("returns the state with originally loaded scheduled classes entity and indicates that the class deletion has failed", () => {
    const state = scheduledClassesReducer(
      statePriorToNewScheduledClassSubmitted.scheduledClasses,
      new ScheduledClassDeletionCancelled({
        err: { error: { Error: "Error! Scheduled Class Deletion Failed!" } },
      })
    );
    expect(state).toEqual(stateAfterClassDeletionFailure.scheduledClasses);
  });

  it("returns the state with the scheduled classes removed and indicates that the batch deletion has been successful", () => {
    const state = scheduledClassesReducer(
      statePriorToNewScheduledClassSubmitted.scheduledClasses,
      new ScheduledClassesBatchDeletionSaved(batchDeletionResponseSuccess)
    );
    expect(state).toEqual(stateAfterBatchDeletion.scheduledClasses);
  });

  it("returns the state with originally loaded scheduled classes entity and indicates that the batch deletion has failed", () => {
    const state = scheduledClassesReducer(
      statePriorToNewScheduledClassSubmitted.scheduledClasses,
      new ScheduledClassesBatchDeletionCancelled({
        err: { error: { Error: "Error! Batch Deletion Failed!" } },
      })
    );
    expect(state).toEqual(stateAfterBatchDeletionFailure.scheduledClasses);
  });
});
