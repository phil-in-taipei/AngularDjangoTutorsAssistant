import { TestBed, fakeAsync, flush } from "@angular/core/testing";
import { Action } from "@ngrx/store";
import { provideMockActions } from "@ngrx/effects/testing";
import { from, Observable, of } from "rxjs";
import { toArray } from "rxjs/operators";
import { provideMockStore } from "@ngrx/store/testing";

import { initialSchoolsState } from "./school.reducers";
import {
  schoolsData,
  creatSchoolData,
  newlyCreatedSchoolData,
  schoolCreateAndEditData,
  deletionResponseSuccess,
} from "src/app/test-data/authenticated-user-module-tests/school-related-tests/school-data";
import {
  SchoolsRequested,
  SchoolsLoaded,
  SchoolCreateSubmitted,
  SchoolCreatedAdded,
  SchoolEditSubmitted,
  SchoolEditUpdated,
  SchoolDeletionRequested,
  SchoolDeletionSaved,
} from "./school.actions";
import { schoolsLoadedInState } from "./school.selectors";
import { SchoolsEffects } from "./school.effects";
import { SchoolService } from "../service/school.service";
import { 
  SchoolModel, 
  SchoolCreateAndEditModel 
} from "src/app/models/school.model";

fdescribe("SchoolsEffects", () => {
  let effects: SchoolsEffects;
  let schoolService: SchoolService;

  beforeEach(() => {
    const mockSchoolService = {
      fetchUsersSchools(): Observable<SchoolModel[]> {
        return of(schoolsData);
      },
      deleteSchool(id: number): Observable<{ id: number; message: string }> {
        return of(deletionResponseSuccess);
      },
      submitSchool(
        submissionForm: SchoolCreateAndEditModel
      ): Observable<SchoolModel> {
        return of(newlyCreatedSchoolData);
      },
      editSchool(
        id: number,
        submissionForm: SchoolCreateAndEditModel
      ): Observable<SchoolModel> {
        return of({
          ...schoolsData[0],
          school_name: submissionForm.school_name,
          address_line_1: submissionForm.address_line_1,
          address_line_2: submissionForm.address_line_2,
          contact_phone: submissionForm.contact_phone,
          other_information: submissionForm.other_information
        });
      },
    };

    TestBed.configureTestingModule({
      providers: [
        provideMockStore({
          initialState: initialSchoolsState,
          selectors: [
            {
              selector: schoolsLoadedInState,
              value: false,
            },
          ],
        }),
        provideMockActions(
          from([
            new SchoolsRequested(),
            new SchoolCreateSubmitted({ school: creatSchoolData }),
            new SchoolEditSubmitted({ id: 1, school: schoolCreateAndEditData }),
            new SchoolDeletionRequested({ id: 1 }),
          ])
        ),
        SchoolsEffects,
        { provide: SchoolService, useValue: mockSchoolService },
      ],
    });

    effects = TestBed.inject(SchoolsEffects);
    schoolService = TestBed.inject(SchoolService);
  });

  it("SchoolsRequested should fetch the schools and load them into state", fakeAsync(() => {
    spyOn(schoolService, "fetchUsersSchools").and.returnValue(
      of(schoolsData)
    );
    let actualActions: Action[] | undefined;
    const expectedActions: Action[] = [
      new SchoolsLoaded({ schools: schoolsData })
    ];
    effects.fetchUsersSchools$.pipe(toArray()).subscribe({
      next: (actualActions2) => (actualActions = actualActions2),
      error: fail,
    });
    expect(actualActions).toEqual(expectedActions);
    flush();
  }));

  it("SchoolCreateSubmitted should submit new school data to backend and save the returned newly created object in state", fakeAsync(() => {
    spyOn(schoolService, "submitSchool").and.returnValue(
      of(newlyCreatedSchoolData)
    );
    let actualActions: Action[] | undefined;
    const expectedActions: Action[] = [
      new SchoolCreatedAdded({ school: newlyCreatedSchoolData })
    ];
    effects.submitSchool$.pipe(toArray()).subscribe({
      next: (actualActions2) => (actualActions = actualActions2),
      error: fail,
    });
    expect(actualActions).toEqual(expectedActions);
    flush();
  }));

  it("SchoolEditSubmitted should submit the edited school to backend and save the returned updated object in state", fakeAsync(() => {
    const editedSchool: SchoolModel = {
      ...schoolsData[0],
      school_name: schoolCreateAndEditData.school_name,
      address_line_1: schoolCreateAndEditData.address_line_1,
      address_line_2: schoolCreateAndEditData.address_line_2,
      contact_phone: schoolCreateAndEditData.contact_phone,
      other_information: schoolCreateAndEditData.other_information
    };

    spyOn(schoolService, "editSchool").and.returnValue(
      of(editedSchool)
    );
    let actualActions: Action[] | undefined;
    const expectedActions: Action[] = [
      new SchoolEditUpdated({
        school: {
          id: editedSchool.id,
          changes: editedSchool
        }
      })
    ];
    effects.editSchool$.pipe(toArray()).subscribe({
      next: (actualActions2) => (actualActions = actualActions2),
      error: fail,
    });
    expect(actualActions).toEqual(expectedActions);
    flush();
  }));

  it("SchoolDeletionRequested should handle the deletion response with message/id by calling the save method to remove the school from state", fakeAsync(() => {
    spyOn(schoolService, "deleteSchool").and.returnValue(
      of(deletionResponseSuccess)
    );
    let actualActions: Action[] | undefined;
    const expectedActions: Action[] = [
      new SchoolDeletionSaved(deletionResponseSuccess)
    ];
    effects.deleteSchool$.pipe(toArray()).subscribe({
      next: (actualActions2) => (actualActions = actualActions2),
      error: fail,
    });
    expect(actualActions).toEqual(expectedActions);
    flush();
  }));
});