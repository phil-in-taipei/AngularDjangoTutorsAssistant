import { TestBed, fakeAsync, flush } from '@angular/core/testing';
import { HttpErrorResponse } from '@angular/common/http';
import { HttpTestingController, HttpClientTestingModule } from '@angular/common/http/testing';

import { authData } from 'src/app/test-data/authentication-tests/authentication-data';
import { AuthService } from 'src/app/authentication/auth.service';
import { environment } from 'src/environments/environment';
import { RecurringScheduleService } from './recurring-schedule.service';
import { 
  recurringClassData,
  recurringClassesData,
  recurringClassCreateData,
  recurringClassAppliedMonthlyData,
  recurringClassAppliedMonthliesData,
  recurringClassAppliedMonthlyCreateData,
  recurringClassAppliedMonthlyDeletionResponse,
  deletionResponseSuccess,
  httpRecurringClassCreateError1,
  httpRecurringClassAppliedMonthlyCreateError1,
  httpRecurringClassDeleteError1,
  httpRecurringClassAppliedMonthlyDeleteError1
 } from 'src/app/test-data/authenticated-user-module-tests/scheduling-module-tests/scheduled-classes-related-tests/recurring-schedule-module-tests/recurring-schedule-related-tests/recurring-schedule-data';


describe('RecurringScheduleService', () => {
  let service: RecurringScheduleService;
  let httpTestingController: HttpTestingController;
  let authServiceSpy: jasmine.SpyObj<AuthService>;

  beforeEach(() => {
    authServiceSpy = jasmine.createSpyObj('AuthService', ['getAuthToken']);
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        RecurringScheduleService,
        { provide: AuthService, useValue: authServiceSpy }
      ]
    });
    service = TestBed.inject(RecurringScheduleService);
    httpTestingController = TestBed.inject(HttpTestingController);
    authServiceSpy = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
  });

  afterEach(() => {
    httpTestingController.verify();
  });

  describe('fetchRecurringClasses', () => {
    it('should return a list of recurring classes from the api', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      
      service.fetchRecurringClasses().subscribe(response => {
        expect(response).toEqual(recurringClassesData);
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/recurring/schedule/by-teacher/`,
      });

      expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
      request.flush(recurringClassesData);
    }));
  });

  describe('fetchRecurringClassAppliedMonthlysByMonthAndYear', () => {
    it('should return recurring classes applied monthly for a specific month and year from the api', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const month = 3;
      const year = 2025;
      
      service.fetchRecurringClassAppliedMonthlysByMonthAndYear(month, year).subscribe(response => {
        expect(response).toEqual(recurringClassAppliedMonthliesData);
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/recurring/monthly/recurring/by-teacher/${month}/${year}/`,
      });

      expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
      request.flush(recurringClassAppliedMonthliesData);
    }));
  });

  describe('submitRecurringClass', () => {
    it('should create a new recurring class and return the created recurring class', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      
      service.submitRecurringClass(recurringClassCreateData).subscribe(response => {
        expect(response).toEqual(recurringClassData);
      });

      const request = httpTestingController.expectOne({
        method: 'POST',
        url: `${environment.apiUrl}/api/recurring/recurring-class/`,
      });

      expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
      expect(request.request.body).toEqual(recurringClassCreateData);
      request.flush(recurringClassData);
    }));

    it('should return an error message when creating recurring class with incorrect data', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      
      service.submitRecurringClass(recurringClassCreateData).subscribe({
        next: () => {},
        error: (error: HttpErrorResponse) => {
          expect(error.status).toEqual(400);
          expect(error.error).toEqual(httpRecurringClassCreateError1);
        }
      });

      const request = httpTestingController.expectOne({
        method: 'POST',
        url: `${environment.apiUrl}/api/recurring/recurring-class/`,
      });

      request.flush(
        httpRecurringClassCreateError1,
        { status: 400, statusText: 'Bad Request' }
      );
    }));
  });

  describe('applyRecurringClassToMonthAndYear', () => {
    it('should apply a recurring class to a month and year and return the applied monthly record', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      
      service.applyRecurringClassToMonthAndYear(recurringClassAppliedMonthlyCreateData).subscribe(response => {
        expect(response).toEqual(recurringClassAppliedMonthlyData);
      });

      const request = httpTestingController.expectOne({
        method: 'POST',
        url: `${environment.apiUrl}/api/recurring/applied-monthly/`,
      });

      expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
      expect(request.request.body).toEqual(recurringClassAppliedMonthlyCreateData);
      request.flush(recurringClassAppliedMonthlyData);
    }));

    it('should return an error message when applying recurring class with incorrect data', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      
      service.applyRecurringClassToMonthAndYear(recurringClassAppliedMonthlyCreateData).subscribe({
        next: () => {},
        error: (error: HttpErrorResponse) => {
          expect(error.status).toEqual(400);
          expect(error.error).toEqual(httpRecurringClassAppliedMonthlyCreateError1);
        }
      });

      const request = httpTestingController.expectOne({
        method: 'POST',
        url: `${environment.apiUrl}/api/recurring/applied-monthly/`,
      });

      request.flush(
        httpRecurringClassAppliedMonthlyCreateError1,
        { status: 400, statusText: 'Bad Request' }
      );
    }));

    it('should return an error message when applying recurring class that is already applied', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      
      service.applyRecurringClassToMonthAndYear(recurringClassAppliedMonthlyCreateData).subscribe({
        next: () => {},
        error: (error: HttpErrorResponse) => {
          expect(error.status).toEqual(400);
          expect(error.error).toEqual({ 
            detail: 'This recurring class is already applied to this month and year.' 
          });
        }
      });

      const request = httpTestingController.expectOne({
        method: 'POST',
        url: `${environment.apiUrl}/api/recurring/applied-monthly/`,
      });

      request.flush(
        { detail: 'This recurring class is already applied to this month and year.' },
        { status: 400, statusText: 'Bad Request' }
      );
    }));
  });

  describe('deleteRecurringClass', () => {
    it('should successfully delete a recurring class', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const recurringClassId = 1;

      service.deleteRecurringClass(recurringClassId).subscribe(response => {
        expect(response).toEqual(deletionResponseSuccess);
      });

      const request = httpTestingController.expectOne({
        method: 'DELETE',
        url: `${environment.apiUrl}/api/recurring/recurring-class/${recurringClassId}/`,
      });

      expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
      request.flush(deletionResponseSuccess);
    }));

    it('should return an error message when deleting non-existent recurring class', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const nonExistentRecurringClassId = 999;

      service.deleteRecurringClass(nonExistentRecurringClassId).subscribe({
        next: () => {},
        error: (error: HttpErrorResponse) => {
          expect(error.status).toEqual(404);
          expect(error.error).toEqual({ detail: 'Not found.' });
        }
      });

      const request = httpTestingController.expectOne({
        method: 'DELETE',
        url: `${environment.apiUrl}/api/recurring/recurring-class/${nonExistentRecurringClassId}/`,
      });

      request.flush(
        { detail: 'Not found.' },
        { status: 404, statusText: 'Not Found' }
      );
    }));

    it('should return an error message when deleting recurring class with permission issues', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const recurringClassId = 1;

      service.deleteRecurringClass(recurringClassId).subscribe({
        next: () => {},
        error: (error: HttpErrorResponse) => {
          expect(error.status).toEqual(403);
          expect(error.error).toEqual(httpRecurringClassDeleteError1);
        }
      });

      const request = httpTestingController.expectOne({
        method: 'DELETE',
        url: `${environment.apiUrl}/api/recurring/recurring-class/${recurringClassId}/`,
      });

      request.flush(
        httpRecurringClassDeleteError1,
        { status: 403, statusText: 'Forbidden' }
      );
    }));
  });

  describe('deleteRecurringClassAppliedMonthly', () => {
    it('should successfully delete a recurring class applied monthly and return deletion data', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const appliedMonthlyId = 1;

      service.deleteRecurringClassAppliedMonthly(appliedMonthlyId).subscribe(response => {
        expect(response).toEqual(recurringClassAppliedMonthlyDeletionResponse);
      });

      const request = httpTestingController.expectOne({
        method: 'DELETE',
        url: `${environment.apiUrl}/api/recurring/applied-monthly/${appliedMonthlyId}/`,
      });

      expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
      request.flush(recurringClassAppliedMonthlyDeletionResponse);
    }));

    it('should return an error message when deleting non-existent applied monthly record', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const nonExistentAppliedMonthlyId = 999;

      service.deleteRecurringClassAppliedMonthly(nonExistentAppliedMonthlyId).subscribe({
        next: () => {},
        error: (error: HttpErrorResponse) => {
          expect(error.status).toEqual(404);
          expect(error.error).toEqual({ detail: 'Not found.' });
        }
      });

      const request = httpTestingController.expectOne({
        method: 'DELETE',
        url: `${environment.apiUrl}/api/recurring/applied-monthly/${nonExistentAppliedMonthlyId}/`,
      });

      request.flush(
        { detail: 'Not found.' },
        { status: 404, statusText: 'Not Found' }
      );
    }));

    it('should return an error message when deleting applied monthly record with permission issues', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const appliedMonthlyId = 1;

      service.deleteRecurringClassAppliedMonthly(appliedMonthlyId).subscribe({
        next: () => {},
        error: (error: HttpErrorResponse) => {
          expect(error.status).toEqual(403);
          expect(error.error).toEqual(httpRecurringClassAppliedMonthlyDeleteError1);
        }
      });

      const request = httpTestingController.expectOne({
        method: 'DELETE',
        url: `${environment.apiUrl}/api/recurring/applied-monthly/${appliedMonthlyId}/`,
      });

      request.flush(
        httpRecurringClassAppliedMonthlyDeleteError1,
        { status: 403, statusText: 'Forbidden' }
      );
    }));
  });
});
