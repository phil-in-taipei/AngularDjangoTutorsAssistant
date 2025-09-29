import { TestBed, fakeAsync, flush } from '@angular/core/testing';
import { HttpErrorResponse } from '@angular/common/http';
import { HttpTestingController, HttpClientTestingModule } from '@angular/common/http/testing';

import { authData } from 'src/app/test-data/authentication-tests/authentication-data';
import { AuthService } from 'src/app/authentication/auth.service';
import { environment } from 'src/environments/environment';
import { StudentOrClassService } from './student-or-class.service';
import { 
  studentOrClassData, 
  studentsOrClassesData, 
  studentOrClassCreateAndEditData,
  studentOrClassEditData,
  httpStudentOrClassCreateError1,
  httpStudentOrClassEditError1,
  httpStudentOrClassDeleteError1,
  deletionResponseSuccess
} from 'src/app/test-data/authenticated-user-module-tests/student-or-class-related-tests/student-or-class-data';

describe('StudentOrClassService', () => {
  let service: StudentOrClassService;
  let httpTestingController: HttpTestingController;
  let authServiceSpy: jasmine.SpyObj<AuthService>;

  beforeEach(() => {
    authServiceSpy = jasmine.createSpyObj('AuthService', ['getAuthToken']);
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        StudentOrClassService,
        { provide: AuthService, useValue: authServiceSpy }
      ]
    });
    service = TestBed.inject(StudentOrClassService);
    httpTestingController = TestBed.inject(HttpTestingController);
    authServiceSpy = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
  });

  afterEach(() => {
    httpTestingController.verify();
  });

  it('should return a list of user students or classes from the api', 
    fakeAsync(() => {
    authServiceSpy.getAuthToken.and.returnValue(authData.token);
    
    service.fetchUsersStudentsOrClasses().subscribe(response => {
      expect(response).toEqual(studentsOrClassesData);
    });

    const request = httpTestingController.expectOne({
      method: 'GET',
      url: `${environment.apiUrl}/api/accounts/students-or-classes/`,
    });

    expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
    request.flush(studentsOrClassesData);
  }));

  it('should create a new student or class and return the created student or class', 
    fakeAsync(() => {
    authServiceSpy.getAuthToken.and.returnValue(authData.token);
    
    service.submitStudentOrClass(studentOrClassCreateAndEditData).subscribe(response => {
      expect(response).toEqual(studentOrClassData);
    });

    const request = httpTestingController.expectOne({
      method: 'POST',
      url: `${environment.apiUrl}/api/accounts/students-or-classes/`,
    });

    expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
    expect(request.request.body).toEqual(studentOrClassCreateAndEditData);
    request.flush(studentOrClassData);
  }));

  it('should return an error message when creating student or class with incorrect data', 
    fakeAsync(() => {
    authServiceSpy.getAuthToken.and.returnValue(authData.token);
    
    service.submitStudentOrClass(studentOrClassCreateAndEditData).subscribe({
      next: () => {},
      error: (error: HttpErrorResponse) => {
        expect(error.status).toEqual(400);
        expect(error.error).toEqual(httpStudentOrClassCreateError1);
      }
    });

    const request = httpTestingController.expectOne({
      method: 'POST',
      url: `${environment.apiUrl}/api/accounts/students-or-classes/`,
    });

    request.flush(
      httpStudentOrClassCreateError1,
      { status: 400, statusText: 'Bad Request' }
    );
  }));

  it('should return an updated student or class after submitting edited student or class', 
    fakeAsync(() => {
    authServiceSpy.getAuthToken.and.returnValue(authData.token);
    const studentOrClassId = 1;
    const updatedStudentOrClassData = {
      ...studentOrClassData,
      student_or_class_name: studentOrClassEditData.student_or_class_name,
      comments: studentOrClassEditData.comments,
      tuition_per_hour: studentOrClassEditData.tuition_per_hour
    };

    service.editStudentOrClass(studentOrClassId, studentOrClassEditData).subscribe(response => {
      expect(response).toEqual(updatedStudentOrClassData);
    });

    const request = httpTestingController.expectOne({
      method: 'PATCH',
      url: `${environment.apiUrl}/api/accounts/student-or-class/${studentOrClassId}/`,
    });

    expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
    expect(request.request.body).toEqual(studentOrClassEditData);
    request.flush(updatedStudentOrClassData);
  }));

  it('should return an error message when editing student or class with incorrect data', 
    fakeAsync(() => {
    authServiceSpy.getAuthToken.and.returnValue(authData.token);
    const studentOrClassId = 1;

    service.editStudentOrClass(studentOrClassId, studentOrClassEditData).subscribe({
      next: () => {},
      error: (error: HttpErrorResponse) => {
        expect(error.status).toEqual(400);
        expect(error.error).toEqual(httpStudentOrClassEditError1);
      }
    });

    const request = httpTestingController.expectOne({
      method: 'PATCH',
      url: `${environment.apiUrl}/api/accounts/student-or-class/${studentOrClassId}/`,
    });

    request.flush(
      httpStudentOrClassEditError1,
      { status: 400, statusText: 'Bad Request' }
    );
  }));

  it('should return an error message when editing non-existent student or class', 
    fakeAsync(() => {
    authServiceSpy.getAuthToken.and.returnValue(authData.token);
    const nonExistentStudentOrClassId = 999;

    service.editStudentOrClass(nonExistentStudentOrClassId, studentOrClassEditData).subscribe({
      next: () => {},
      error: (error: HttpErrorResponse) => {
        expect(error.status).toEqual(404);
        expect(error.error).toEqual({ detail: 'Not found.' });
      }
    });

    const request = httpTestingController.expectOne({
      method: 'PATCH',
      url: `${environment.apiUrl}/api/accounts/student-or-class/${nonExistentStudentOrClassId}/`,
    });

    request.flush(
      { detail: 'Not found.' },
      { status: 404, statusText: 'Not Found' }
    );
  }));

  it('should successfully delete a student or class', 
    fakeAsync(() => {
    authServiceSpy.getAuthToken.and.returnValue(authData.token);
    const studentOrClassId = 1;

    service.deleteStudentOrClass(studentOrClassId).subscribe(response => {
      expect(response).toEqual(deletionResponseSuccess);
    });

    const request = httpTestingController.expectOne({
      method: 'DELETE',
      url: `${environment.apiUrl}/api/accounts/student-or-class/${studentOrClassId}/`,
    });

    expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
    request.flush(deletionResponseSuccess);
  }));

  it('should return an error message when deleting non-existent student or class', 
    fakeAsync(() => {
    authServiceSpy.getAuthToken.and.returnValue(authData.token);
    const nonExistentStudentOrClassId = 999;

    service.deleteStudentOrClass(nonExistentStudentOrClassId).subscribe({
      next: () => {},
      error: (error: HttpErrorResponse) => {
        expect(error.status).toEqual(404);
        expect(error.error).toEqual({ detail: 'Not found.' });
      }
    });

    const request = httpTestingController.expectOne({
      method: 'DELETE',
      url: `${environment.apiUrl}/api/accounts/student-or-class/${nonExistentStudentOrClassId}/`,
    });

    request.flush(
      { detail: 'Not found.' },
      { status: 404, statusText: 'Not Found' }
    );
  }));

  it('should return an error message when deleting student or class with permission issues', 
    fakeAsync(() => {
    authServiceSpy.getAuthToken.and.returnValue(authData.token);
    const studentOrClassId = 1;

    service.deleteStudentOrClass(studentOrClassId).subscribe({
      next: () => {},
      error: (error: HttpErrorResponse) => {
        expect(error.status).toEqual(403);
        expect(error.error).toEqual(httpStudentOrClassDeleteError1);
      }
    });

    const request = httpTestingController.expectOne({
      method: 'DELETE',
      url: `${environment.apiUrl}/api/accounts/student-or-class/${studentOrClassId}/`,
    });

    request.flush(
      httpStudentOrClassDeleteError1,
      { status: 403, statusText: 'Forbidden' }
    );
  }));
});
