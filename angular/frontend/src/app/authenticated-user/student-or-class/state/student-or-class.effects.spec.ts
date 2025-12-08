// student-or-class.effects.spec.ts
import { TestBed, fakeAsync, flush } from "@angular/core/testing";
import { Action } from "@ngrx/store";
import { provideMockActions } from "@ngrx/effects/testing";
import { from, Observable, of } from "rxjs";
import { toArray } from "rxjs/operators";
import { provideMockStore } from "@ngrx/store/testing";

import { initialStudentsOrClassesState } from "./student-or-class.reducers";
import {
  studentsOrClassesData,
  studentOrClassCreateAndEditData,
  studentOrClassEditData,
  deletionResponseSuccess,
} from "src/app/test-data/authenticated-user-module-tests/student-or-class-related-tests/student-or-class-data";
import {
  StudentsOrClassesRequested,
  StudentsOrClassesLoaded,
  StudentOrClassCreateSubmitted,
  StudentOrClassCreatedAdded,
  StudentOrClassEditSubmitted,
  StudentOrClassEditUpdated,
  StudentOrClassDeletionRequested,
  StudentOrClassDeletionSaved,
} from "./student-or-class.actions";
import { studentsOrClassesLoadedInState } from "./student-or-class.selectors";
import { StudentsOrClassesEffects } from "./student-or-class.effects";
import { StudentOrClassService } from "../service/student-or-class.service";
import { 
  StudentOrClassModel, 
  StudentOrClassCreateAndEditModel,
  StudentOrClassEditModel 
} from "src/app/models/student-or-class.model";

fdescribe("StudentsOrClassesEffects", () => {
  let effects: StudentsOrClassesEffects;
  let studentOrClassService: StudentOrClassService;

  beforeEach(() => {
    const mockStudentOrClassService = {
      fetchUsersStudentsOrClasses(): Observable<StudentOrClassModel[]> {
        return of(studentsOrClassesData);
      },
      deleteStudentOrClass(id: number): Observable<{ id: number; message: string }> {
        return of(deletionResponseSuccess);
      },
      submitStudentOrClass(
        submissionForm: StudentOrClassCreateAndEditModel
      ): Observable<StudentOrClassModel> {
        return of({
          id: 4,
          student_or_class_name: submissionForm.student_or_class_name,
          account_type: submissionForm.account_type,
          school: submissionForm.school,
          comments: submissionForm.comments,
          purchased_class_hours: submissionForm.purchased_class_hours,
          tuition_per_hour: submissionForm.tuition_per_hour,
          account_id: 'STU003',
          slug: 'john-updated-doe',
          template_str: 'John Updated Doe - Individual Student'
        });
      },
      editStudentOrClass(
        id: number,
        submissionForm: StudentOrClassEditModel
      ): Observable<StudentOrClassModel> {
        return of({
          ...studentsOrClassesData[0],
          student_or_class_name: submissionForm.student_or_class_name,
          comments: submissionForm.comments,
          tuition_per_hour: submissionForm.tuition_per_hour
        });
      },
    };

    TestBed.configureTestingModule({
      providers: [
        provideMockStore({
          initialState: initialStudentsOrClassesState,
          selectors: [
            {
              selector: studentsOrClassesLoadedInState,
              value: false,
            },
          ],
        }),
        provideMockActions(
          from([
            new StudentsOrClassesRequested(),
            new StudentOrClassCreateSubmitted({ 
              studentOrClass: studentOrClassCreateAndEditData 
            }),
            new StudentOrClassEditSubmitted({ 
              id: 1, 
              studentOrClass: studentOrClassEditData 
            }),
            new StudentOrClassDeletionRequested({ id: 1 }),
          ])
        ),
        StudentsOrClassesEffects,
        { provide: StudentOrClassService, useValue: mockStudentOrClassService },
      ],
    });

    effects = TestBed.inject(StudentsOrClassesEffects);
    studentOrClassService = TestBed.inject(StudentOrClassService);
  });

  it("StudentsOrClassesRequested should fetch the students or classes and load them into state", fakeAsync(() => {
    spyOn(studentOrClassService, "fetchUsersStudentsOrClasses").and.returnValue(
      of(studentsOrClassesData)
    );
    let actualActions: Action[] | undefined;
    const expectedActions: Action[] = [
      new StudentsOrClassesLoaded({ studentsOrClasses: studentsOrClassesData })
    ];
    effects.fetchUsersStudentsOrClasses$.pipe(toArray()).subscribe({
      next: (actualActions2) => (actualActions = actualActions2),
      error: fail,
    });
    expect(actualActions).toEqual(expectedActions);
    flush();
  }));

  it("StudentOrClassCreateSubmitted should submit new student or class data to backend and save the returned newly created object in state", fakeAsync(() => {
    const createdStudentOrClass: StudentOrClassModel = {
      id: 4,
      student_or_class_name: studentOrClassCreateAndEditData.student_or_class_name,
      account_type: studentOrClassCreateAndEditData.account_type,
      school: studentOrClassCreateAndEditData.school,
      comments: studentOrClassCreateAndEditData.comments,
      purchased_class_hours: studentOrClassCreateAndEditData.purchased_class_hours,
      tuition_per_hour: studentOrClassCreateAndEditData.tuition_per_hour,
      account_id: 'STU003',
      slug: 'john-updated-doe',
      template_str: 'John Updated Doe - Individual Student'
    };

    spyOn(studentOrClassService, "submitStudentOrClass").and.returnValue(
      of(createdStudentOrClass)
    );
    let actualActions: Action[] | undefined;
    const expectedActions: Action[] = [
      new StudentOrClassCreatedAdded({ studentOrClass: createdStudentOrClass })
    ];
    effects.submitStudentOrClass$.pipe(toArray()).subscribe({
      next: (actualActions2) => (actualActions = actualActions2),
      error: fail,
    });
    expect(actualActions).toEqual(expectedActions);
    flush();
  }));

  it("StudentOrClassEditSubmitted should submit the edited student or class to backend and save the returned updated object in state", fakeAsync(() => {
    const editedStudentOrClass: StudentOrClassModel = {
      ...studentsOrClassesData[0],
      student_or_class_name: studentOrClassEditData.student_or_class_name,
      comments: studentOrClassEditData.comments,
      tuition_per_hour: studentOrClassEditData.tuition_per_hour
    };

    spyOn(studentOrClassService, "editStudentOrClass").and.returnValue(
      of(editedStudentOrClass)
    );
    let actualActions: Action[] | undefined;
    const expectedActions: Action[] = [
      new StudentOrClassEditUpdated({
        studentOrClass: {
          id: editedStudentOrClass.id,
          changes: editedStudentOrClass
        }
      })
    ];
    effects.editStudentOrClass$.pipe(toArray()).subscribe({
      next: (actualActions2) => (actualActions = actualActions2),
      error: fail,
    });
    expect(actualActions).toEqual(expectedActions);
    flush();
  }));

  it("StudentOrClassDeletionRequested should handle the deletion response with message/id by calling the save method to remove the student or class from state", fakeAsync(() => {
    spyOn(studentOrClassService, "deleteStudentOrClass").and.returnValue(
      of(deletionResponseSuccess)
    );
    let actualActions: Action[] | undefined;
    const expectedActions: Action[] = [
      new StudentOrClassDeletionSaved(deletionResponseSuccess)
    ];
    effects.deleteStudentOrClass$.pipe(toArray()).subscribe({
      next: (actualActions2) => (actualActions = actualActions2),
      error: fail,
    });
    expect(actualActions).toEqual(expectedActions);
    flush();
  }));
});
