import { TestBed, fakeAsync, flush } from '@angular/core/testing';
import { HttpErrorResponse } from '@angular/common/http';
import { HttpTestingController, HttpClientTestingModule } from '@angular/common/http/testing';

import { authData } from 'src/app/test-data/authentication-tests/authentication-data';
import { AuthService } from 'src/app/authentication/auth.service';
import { environment } from 'src/environments/environment';
import { AttendanceService } from './attendance.service';
import { 
  studentOrClassAttendanceRecordResponse,
  studentOrClassAttendanceRecordResponsePage2,
  studentOrClassAttendanceRecordResponseLastPage,
  pastClassesArray,
  pastClassesArrayPage2,
  pastClassesArrayLastPage,
  httpAttendanceRecordError1
} from 'src/app/test-data/authenticated-user-module-tests/scheduling-module-tests/scheduled-classes-related-tests/attendance-data';

fdescribe('AttendanceService', () => {
  let service: AttendanceService;
  let httpTestingController: HttpTestingController;
  let authServiceSpy: jasmine.SpyObj<AuthService>;

  beforeEach(() => {
    authServiceSpy = jasmine.createSpyObj('AuthService', ['getAuthToken']);
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        AttendanceService,
        { provide: AuthService, useValue: authServiceSpy }
      ]
    });
    service = TestBed.inject(AttendanceService);
    httpTestingController = TestBed.inject(HttpTestingController);
    authServiceSpy = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
  });

  afterEach(() => {
    httpTestingController.verify();
  });

  describe('fetchPastClassesByStudentOrClass', () => {
    it('should return past classes for a student or class from the api (first page)', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const studentOrClassId = 1;
      const pageNum = 1;
      
      service.fetchPastClassesByStudentOrClass(studentOrClassId, pageNum).subscribe(response => {
        expect(response).toEqual(pastClassesArray);
        expect(response.length).toBe(3);
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/scheduling/classes/student-or-class-attendance/${studentOrClassId}/?page=${pageNum}`,
      });

      expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
      request.flush(studentOrClassAttendanceRecordResponse);
    }));

    it('should return past classes for a student or class from the api (second page)', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const studentOrClassId = 1;
      const pageNum = 2;
      
      service.fetchPastClassesByStudentOrClass(studentOrClassId, pageNum).subscribe(response => {
        expect(response).toEqual(pastClassesArrayPage2);
        expect(response.length).toBe(3);
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/scheduling/classes/student-or-class-attendance/${studentOrClassId}/?page=${pageNum}`,
      });

      expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
      request.flush(studentOrClassAttendanceRecordResponsePage2);
    }));

    it('should return past classes for a student or class from the api (last page)', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const studentOrClassId = 1;
      const pageNum = 3;
      
      service.fetchPastClassesByStudentOrClass(studentOrClassId, pageNum).subscribe(response => {
        expect(response).toEqual(pastClassesArrayLastPage);
        expect(response.length).toBe(2);
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/scheduling/classes/student-or-class-attendance/${studentOrClassId}/?page=${pageNum}`,
      });

      expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
      request.flush(studentOrClassAttendanceRecordResponseLastPage);
    }));

    it('should correctly transform the paginated response to an array of classes', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const studentOrClassId = 1;
      const pageNum = 1;
      
      service.fetchPastClassesByStudentOrClass(studentOrClassId, pageNum).subscribe(response => {
        expect(Array.isArray(response)).toBe(true);
        expect(response[0].id).toBeDefined();
        expect(response[0].date).toBeDefined();
        expect(response[0].start_time).toBeDefined();
        expect(response[0].class_status).toBeDefined();
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/scheduling/classes/student-or-class-attendance/${studentOrClassId}/?page=${pageNum}`,
      });

      request.flush(studentOrClassAttendanceRecordResponse);
    }));

    it('should return an empty array when no past classes exist', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const studentOrClassId = 999;
      const pageNum = 1;
      const emptyResponse = {
        count: 0,
        next: null,
        previous: null,
        results: []
      };
      
      service.fetchPastClassesByStudentOrClass(studentOrClassId, pageNum).subscribe(response => {
        expect(response).toEqual([]);
        expect(response.length).toBe(0);
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/scheduling/classes/student-or-class-attendance/${studentOrClassId}/?page=${pageNum}`,
      });

      request.flush(emptyResponse);
    }));

    it('should return an error message when fetching attendance for non-existent student or class', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const nonExistentStudentOrClassId = 999;
      const pageNum = 1;
      
      service.fetchPastClassesByStudentOrClass(nonExistentStudentOrClassId, pageNum).subscribe({
        next: () => {},
        error: (error: HttpErrorResponse) => {
          expect(error.status).toEqual(404);
          expect(error.error).toEqual({ detail: 'Not found.' });
        }
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/scheduling/classes/student-or-class-attendance/${nonExistentStudentOrClassId}/?page=${pageNum}`,
      });

      request.flush(
        { detail: 'Not found.' },
        { status: 404, statusText: 'Not Found' }
      );
    }));

    it('should return an error message when fetching attendance with invalid page number', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const studentOrClassId = 1;
      const invalidPageNum = 999;
      
      service.fetchPastClassesByStudentOrClass(studentOrClassId, invalidPageNum).subscribe({
        next: () => {},
        error: (error: HttpErrorResponse) => {
          expect(error.status).toEqual(404);
          expect(error.error).toEqual(httpAttendanceRecordError1);
        }
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/scheduling/classes/student-or-class-attendance/${studentOrClassId}/?page=${invalidPageNum}`,
      });

      request.flush(
        httpAttendanceRecordError1,
        { status: 404, statusText: 'Not Found' }
      );
    }));

    it('should return an error message when fetching attendance with permission issues', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const studentOrClassId = 1;
      const pageNum = 1;
      
      service.fetchPastClassesByStudentOrClass(studentOrClassId, pageNum).subscribe({
        next: () => {},
        error: (error: HttpErrorResponse) => {
          expect(error.status).toEqual(403);
          expect(error.error).toEqual({ detail: 'You do not have permission to perform this action.' });
        }
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/scheduling/classes/student-or-class-attendance/${studentOrClassId}/?page=${pageNum}`,
      });

      request.flush(
        { detail: 'You do not have permission to perform this action.' },
        { status: 403, statusText: 'Forbidden' }
      );
    }));
  });
});
