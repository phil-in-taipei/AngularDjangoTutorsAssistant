import { TestBed, fakeAsync, flush } from '@angular/core/testing';
import { HttpErrorResponse } from '@angular/common/http';
import { HttpTestingController, HttpClientTestingModule } from '@angular/common/http/testing';

import { authData } from 'src/app/test-data/authentication-tests/authentication-data';
import { AuthService } from 'src/app/authentication/auth.service';
import { environment } from 'src/environments/environment';
import { ClassesService } from './classes.service';
import { 
  scheduledClassData,
  scheduledClassesData,
  scheduledClassesByDateData,
  scheduledClassesByMonthData,
  unconfirmedStatusClassesData,
  createScheduledClassData,
  rescheduleClassData,
  modifyClassStatusData,
  modifyClassStatusResponse,
  scheduledClassBatchDeletionData,
  batchDeletionResponseSuccess,
  deletionResponseSuccess,
  httpScheduledClassCreateError1,
  httpScheduledClassRescheduleError1,
  httpModifyClassStatusError1,
  httpBatchDeleteError1,
  httpSingleDeleteError1
} from 'src/app/test-data/authenticated-user-module-tests/scheduling-module-tests/scheduled-classes-related-tests/scheduled-classes-data';

fdescribe('ClassesService', () => {
  let service: ClassesService;
  let httpTestingController: HttpTestingController;
  let authServiceSpy: jasmine.SpyObj<AuthService>;

  beforeEach(() => {
    authServiceSpy = jasmine.createSpyObj('AuthService', ['getAuthToken']);
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        ClassesService,
        { provide: AuthService, useValue: authServiceSpy }
      ]
    });
    service = TestBed.inject(ClassesService);
    httpTestingController = TestBed.inject(HttpTestingController);
    authServiceSpy = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
  });

  afterEach(() => {
    httpTestingController.verify();
  });

  describe('fetchScheduledClassesByDate', () => {
    it('should return scheduled classes for a specific date from the api', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const testDate = '2025-03-15';
      
      service.fetchScheduledClassesByDate(testDate).subscribe(response => {
        expect(response).toEqual(scheduledClassesByDateData);
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/scheduling/classes/by-teacher/by-date/${testDate}/`,
      });

      expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
      request.flush(scheduledClassesByDateData);
    }));
  });

  describe('fetchClassesByMonth', () => {
    it('should return scheduled classes for a specific month and year from the api', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const month = 3;
      const year = 2025;
      
      service.fetchClassesByMonth(month, year).subscribe(response => {
        expect(response).toEqual(scheduledClassesByMonthData);
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/scheduling/classes/by-teacher/by-month-year/${month}/${year}/`,
      });

      expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
      request.flush(scheduledClassesByMonthData);
    }));
  });

  describe('fetchTodaysClasses', () => {
    it('should return scheduled classes for today from the api', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      
      service.fetchTodaysClasses().subscribe(response => {
        expect(response).toEqual(scheduledClassesByDateData);
      });

      const request = httpTestingController.expectOne((req) => {
        return req.method === 'GET' && 
               req.url.includes('/api/scheduling/classes/by-teacher/by-date/');
      });

      expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
      request.flush(scheduledClassesByDateData);
    }));
  });

  describe('fetchUnconfirmedStatusClasses', () => {
    it('should return unconfirmed status classes from the api', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      
      service.fetchUnconfirmedStatusClasses().subscribe(response => {
        expect(response).toEqual(unconfirmedStatusClassesData);
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/scheduling/classes/unconfirmed-status/`,
      });

      expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
      request.flush(unconfirmedStatusClassesData);
    }));
  });

  describe('submitScheduledClass', () => {
    it('should create a new scheduled class and return the created classes array', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      
      service.submitScheduledClass(createScheduledClassData).subscribe(response => {
        expect(response).toEqual(scheduledClassesData);
      });

      const request = httpTestingController.expectOne({
        method: 'POST',
        url: `${environment.apiUrl}/api/scheduling/class/submit/`,
      });

      expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
      expect(request.request.body).toEqual(createScheduledClassData);
      request.flush(scheduledClassesData);
    }));

    it('should return an error message when creating scheduled class with incorrect data', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      
      service.submitScheduledClass(createScheduledClassData).subscribe({
        next: () => {},
        error: (error: HttpErrorResponse) => {
          expect(error.status).toEqual(400);
          expect(error.error).toEqual(httpScheduledClassCreateError1);
        }
      });

      const request = httpTestingController.expectOne({
        method: 'POST',
        url: `${environment.apiUrl}/api/scheduling/class/submit/`,
      });

      request.flush(
        httpScheduledClassCreateError1,
        { status: 400, statusText: 'Bad Request' }
      );
    }));
  });

  describe('submitRescheduledClass', () => {
    it('should reschedule a class and return the updated classes array', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const classId = 1;
      const rescheduleData = { ...rescheduleClassData, id: classId };
      
      service.submitRescheduledClass(rescheduleData).subscribe(response => {
        expect(response).toEqual(scheduledClassesData);
      });

      const request = httpTestingController.expectOne({
        method: 'PATCH',
        url: `${environment.apiUrl}/api/scheduling/class/submit/${classId}/`,
      });

      expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
      expect(request.request.body).toEqual(rescheduleData);
      request.flush(scheduledClassesData);
    }));

    it('should return an error message when rescheduling class with incorrect data', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const classId = 1;
      const rescheduleData = { ...rescheduleClassData, id: classId };
      
      service.submitRescheduledClass(rescheduleData).subscribe({
        next: () => {},
        error: (error: HttpErrorResponse) => {
          expect(error.status).toEqual(400);
          expect(error.error).toEqual(httpScheduledClassRescheduleError1);
        }
      });

      const request = httpTestingController.expectOne({
        method: 'PATCH',
        url: `${environment.apiUrl}/api/scheduling/class/submit/${classId}/`,
      });

      request.flush(
        httpScheduledClassRescheduleError1,
        { status: 400, statusText: 'Bad Request' }
      );
    }));

    it('should return an error message when rescheduling non-existent class', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const nonExistentClassId = 999;
      const rescheduleData = { ...rescheduleClassData, id: nonExistentClassId };
      
      service.submitRescheduledClass(rescheduleData).subscribe({
        next: () => {},
        error: (error: HttpErrorResponse) => {
          expect(error.status).toEqual(404);
          expect(error.error).toEqual({ detail: 'Not found.' });
        }
      });

      const request = httpTestingController.expectOne({
        method: 'PATCH',
        url: `${environment.apiUrl}/api/scheduling/class/submit/${nonExistentClassId}/`,
      });

      request.flush(
        { detail: 'Not found.' },
        { status: 404, statusText: 'Not Found' }
      );
    }));
  });

  describe('modifyClassStatus', () => {
    it('should modify class status and return the updated class with student update', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      
      service.modifyClassStatus(modifyClassStatusData).subscribe(response => {
        expect(response).toEqual(modifyClassStatusResponse);
      });

      const request = httpTestingController.expectOne({
        method: 'PATCH',
        url: `${environment.apiUrl}/api/scheduling/class-status-confirmation/`,
      });

      expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
      expect(request.request.body).toEqual(modifyClassStatusData);
      request.flush(modifyClassStatusResponse);
    }));

    it('should return an error message when modifying class status with incorrect data', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      
      service.modifyClassStatus(modifyClassStatusData).subscribe({
        next: () => {},
        error: (error: HttpErrorResponse) => {
          expect(error.status).toEqual(400);
          expect(error.error).toEqual(httpModifyClassStatusError1);
        }
      });

      const request = httpTestingController.expectOne({
        method: 'PATCH',
        url: `${environment.apiUrl}/api/scheduling/class-status-confirmation/`,
      });

      request.flush(
        httpModifyClassStatusError1,
        { status: 400, statusText: 'Bad Request' }
      );
    }));
  });

  describe('deleteSingleClass', () => {
    it('should successfully delete a single scheduled class', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const classId = 1;

      service.deleteSingleClass(classId).subscribe(response => {
        expect(response).toEqual(deletionResponseSuccess);
      });

      const request = httpTestingController.expectOne({
        method: 'DELETE',
        url: `${environment.apiUrl}/api/scheduling/class/submit/${classId}/`,
      });

      expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
      request.flush(deletionResponseSuccess);
    }));

    it('should return an error message when deleting non-existent class', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const nonExistentClassId = 999;

      service.deleteSingleClass(nonExistentClassId).subscribe({
        next: () => {},
        error: (error: HttpErrorResponse) => {
          expect(error.status).toEqual(404);
          expect(error.error).toEqual({ detail: 'Not found.' });
        }
      });

      const request = httpTestingController.expectOne({
        method: 'DELETE',
        url: `${environment.apiUrl}/api/scheduling/class/submit/${nonExistentClassId}/`,
      });

      request.flush(
        { detail: 'Not found.' },
        { status: 404, statusText: 'Not Found' }
      );
    }));

    it('should return an error message when deleting class with permission issues', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const classId = 1;

      service.deleteSingleClass(classId).subscribe({
        next: () => {},
        error: (error: HttpErrorResponse) => {
          expect(error.status).toEqual(403);
          expect(error.error).toEqual(httpSingleDeleteError1);
        }
      });

      const request = httpTestingController.expectOne({
        method: 'DELETE',
        url: `${environment.apiUrl}/api/scheduling/class/submit/${classId}/`,
      });

      request.flush(
        httpSingleDeleteError1,
        { status: 403, statusText: 'Forbidden' }
      );
    }));
  });

  describe('deleteBatchOfScheduledClasses', () => {
    it('should successfully delete a batch of scheduled classes', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);

      service.deleteBatchOfScheduledClasses(scheduledClassBatchDeletionData).subscribe(response => {
        expect(response).toEqual(batchDeletionResponseSuccess);
      });

      const request = httpTestingController.expectOne({
        method: 'DELETE',
        url: `${environment.apiUrl}/api/scheduling/classes/batch-delete/`,
      });

      expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
      expect(request.request.body).toEqual({
        obsolete_class_ids: scheduledClassBatchDeletionData.obsolete_class_ids
      });
      request.flush(batchDeletionResponseSuccess);
    }));

    it('should return an error message when batch deleting with invalid data', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);

      service.deleteBatchOfScheduledClasses(scheduledClassBatchDeletionData).subscribe({
        next: () => {},
        error: (error: HttpErrorResponse) => {
          expect(error.status).toEqual(400);
          expect(error.error).toEqual(httpBatchDeleteError1);
        }
      });

      const request = httpTestingController.expectOne({
        method: 'DELETE',
        url: `${environment.apiUrl}/api/scheduling/classes/batch-delete/`,
      });

      request.flush(
        httpBatchDeleteError1,
        { status: 400, statusText: 'Bad Request' }
      );
    }));

    it('should return an error message when batch deleting with permission issues', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);

      service.deleteBatchOfScheduledClasses(scheduledClassBatchDeletionData).subscribe({
        next: () => {},
        error: (error: HttpErrorResponse) => {
          expect(error.status).toEqual(403);
          expect(error.error).toEqual({ detail: 'You do not have permission to perform this action.' });
        }
      });

      const request = httpTestingController.expectOne({
        method: 'DELETE',
        url: `${environment.apiUrl}/api/scheduling/classes/batch-delete/`,
      });

      request.flush(
        { detail: 'You do not have permission to perform this action.' },
        { status: 403, statusText: 'Forbidden' }
      );
    }));
  });
});
