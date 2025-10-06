import { TestBed, fakeAsync, flush } from '@angular/core/testing';
import { HttpErrorResponse } from '@angular/common/http';
import { HttpTestingController, HttpClientTestingModule } from '@angular/common/http/testing';

import { authData } from 'src/app/test-data/authentication-tests/authentication-data';
import { AuthService } from 'src/app/authentication/auth.service';
import { environment } from 'src/environments/environment';
import { AccountingService } from './accounting.service';
import { 
  freelanceTuitionTransactionData,
  freelanceTuitionTransactionRecordData,
  freelanceTuitionTransactionRecordsData,
  purchasedHoursModificationRecordsData,
  schoolAccountingReportData,
  schoolAccountingReportDateRangeData,
  schoolsAndFreelanceStudentsAccountingReportData,
  emailSuccessResponse,
  httpFreelanceTuitionTransactionCreateError1,
  httpFreelancePaymentsFetchError1,
  httpSchoolAccountingReportError1,
  httpEmailReportError1
} from 'src/app/test-data/authenticated-user-module-tests/scheduling-module-tests/accounting-data';

fdescribe('AccountingService', () => {
  let service: AccountingService;
  let httpTestingController: HttpTestingController;
  let authServiceSpy: jasmine.SpyObj<AuthService>;

  beforeEach(() => {
    authServiceSpy = jasmine.createSpyObj('AuthService', ['getAuthToken']);
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        AccountingService,
        { provide: AuthService, useValue: authServiceSpy }
      ]
    });
    service = TestBed.inject(AccountingService);
    httpTestingController = TestBed.inject(HttpTestingController);
    authServiceSpy = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
  });

  afterEach(() => {
    httpTestingController.verify();
  });

  describe('fetchFreelancePaymentsByMonthAndYear', () => {
    it('should return freelance tuition transaction records for a specific month and year from the api', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const month = 3;
      const year = 2025;
      
      service.fetchFreelancePaymentsByMonthAndYear(month, year).subscribe(response => {
        expect(response).toEqual(freelanceTuitionTransactionRecordsData);
        expect(response.length).toBe(3);
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/accounting/received-tuition-transactions-by-month-year/${month}/${year}/`,
      });

      expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
      request.flush(freelanceTuitionTransactionRecordsData);
    }));

    it('should return an empty array when no freelance payments exist for the month', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const month = 12;
      const year = 2024;
      
      service.fetchFreelancePaymentsByMonthAndYear(month, year).subscribe(response => {
        expect(response).toEqual([]);
        expect(response.length).toBe(0);
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/accounting/received-tuition-transactions-by-month-year/${month}/${year}/`,
      });

      request.flush([]);
    }));

    it('should return an error message when fetching with invalid month or year', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const month = 13;
      const year = 2025;
      
      service.fetchFreelancePaymentsByMonthAndYear(month, year).subscribe({
        next: () => {},
        error: (error: HttpErrorResponse) => {
          expect(error.status).toEqual(400);
          expect(error.error).toEqual(httpFreelancePaymentsFetchError1);
        }
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/accounting/received-tuition-transactions-by-month-year/${month}/${year}/`,
      });

      request.flush(
        httpFreelancePaymentsFetchError1,
        { status: 400, statusText: 'Bad Request' }
      );
    }));
  });

  describe('fetchPurchasedHoursModificationRecordsByMonthAndYear', () => {
    it('should return purchased hours modification records for a specific month, year, and account from the api', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const month = 3;
      const year = 2025;
      const accountId = 1;
      
      service.fetchPurchasedHoursModificationRecordsByMonthAndYear(month, year, accountId).subscribe(response => {
        expect(response).toEqual(purchasedHoursModificationRecordsData);
        expect(response.length).toBe(4);
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/accounting/purchased-hours-modifications/by-month-and-account/${month}/${year}/${accountId}/`,
      });

      expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
      request.flush(purchasedHoursModificationRecordsData);
    }));

    it('should return an empty array when no modification records exist', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const month = 3;
      const year = 2025;
      const accountId = 999;
      
      service.fetchPurchasedHoursModificationRecordsByMonthAndYear(month, year, accountId).subscribe(response => {
        expect(response).toEqual([]);
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/accounting/purchased-hours-modifications/by-month-and-account/${month}/${year}/${accountId}/`,
      });

      request.flush([]);
    }));
  });

  describe('fetchSchoolAccountingReportByMonthAndYear', () => {
    it('should return school accounting report for a specific month, year, and school from the api', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const month = 3;
      const year = 2025;
      const schoolId = 1;
      
      service.fetchSchoolAccountingReportByMonthAndYear(month, year, schoolId).subscribe(response => {
        expect(response).toEqual(schoolAccountingReportData);
        expect(response.school_name).toBe('Test Elementary School');
        expect(response.students_reports.length).toBe(2);
        expect(response.school_total).toBe(190.00);
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/accounting/estimated-school-earnings-by-month-year/${month}/${year}/${schoolId}/`,
      });

      expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
      request.flush(schoolAccountingReportData);
    }));

    it('should return an error message when fetching report for non-existent school', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const month = 3;
      const year = 2025;
      const nonExistentSchoolId = 999;
      
      service.fetchSchoolAccountingReportByMonthAndYear(month, year, nonExistentSchoolId).subscribe({
        next: () => {},
        error: (error: HttpErrorResponse) => {
          expect(error.status).toEqual(404);
          expect(error.error).toEqual({ detail: 'Not found.' });
        }
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/accounting/estimated-school-earnings-by-month-year/${month}/${year}/${nonExistentSchoolId}/`,
      });

      request.flush(
        { detail: 'Not found.' },
        { status: 404, statusText: 'Not Found' }
      );
    }));

    it('should return an error message when fetching with invalid parameters', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const month = 13;
      const year = 2025;
      const schoolId = 1;
      
      service.fetchSchoolAccountingReportByMonthAndYear(month, year, schoolId).subscribe({
        next: () => {},
        error: (error: HttpErrorResponse) => {
          expect(error.status).toEqual(400);
          expect(error.error).toEqual(httpSchoolAccountingReportError1);
        }
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/accounting/estimated-school-earnings-by-month-year/${month}/${year}/${schoolId}/`,
      });

      request.flush(
        httpSchoolAccountingReportError1,
        { status: 400, statusText: 'Bad Request' }
      );
    }));
  });

  describe('fetchSchoolAccountingReportWithinDateRange', () => {
    it('should return school accounting report for a specific date range and school from the api', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const startDate = '2025-03-01';
      const finishDate = '2025-03-31';
      const schoolId = 1;
      
      service.fetchSchoolAccountingReportWithinDateRange(startDate, finishDate, schoolId).subscribe(response => {
        expect(response).toEqual(schoolAccountingReportDateRangeData);
        expect(response.school_name).toBe('Test Elementary School');
        expect(response.school_total).toBe(245.00);
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/accounting/estimated-school-earnings-within-date-range/${startDate}/${finishDate}/${schoolId}/`,
      });

      expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
      request.flush(schoolAccountingReportDateRangeData);
    }));

    it('should return an error message when start date is after finish date', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const startDate = '2025-03-31';
      const finishDate = '2025-03-01';
      const schoolId = 1;
      
      service.fetchSchoolAccountingReportWithinDateRange(startDate, finishDate, schoolId).subscribe({
        next: () => {},
        error: (error: HttpErrorResponse) => {
          expect(error.status).toEqual(400);
          expect(error.error).toEqual({ detail: 'Start date must be before finish date.' });
        }
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/accounting/estimated-school-earnings-within-date-range/${startDate}/${finishDate}/${schoolId}/`,
      });

      request.flush(
        { detail: 'Start date must be before finish date.' },
        { status: 400, statusText: 'Bad Request' }
      );
    }));
  });

  describe('fetchSchoolsAndFreelanceStudentsAccountingReportByMonthAndYear', () => {
    it('should return combined schools and freelance students accounting report from the api', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const month = 3;
      const year = 2025;
      
      service.fetchSchoolsAndFreelanceStudentsAccountingReportByMonthAndYear(month, year).subscribe(response => {
        expect(response).toEqual(schoolsAndFreelanceStudentsAccountingReportData);
        expect(response.classes_in_schools.length).toBe(2);
        expect(response.freelance_students.length).toBe(2);
        expect(response.overall_monthly_total).toBe(541.00);
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/accounting/estimated-earnings-by-month-year/${month}/${year}/`,
      });

      expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
      request.flush(schoolsAndFreelanceStudentsAccountingReportData);
    }));

    it('should return a report with zero total when no classes were held', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const month = 12;
      const year = 2024;
      const emptyReport = {
        classes_in_schools: [],
        freelance_students: [],
        overall_monthly_total: 0
      };
      
      service.fetchSchoolsAndFreelanceStudentsAccountingReportByMonthAndYear(month, year).subscribe(response => {
        expect(response.overall_monthly_total).toBe(0);
        expect(response.classes_in_schools.length).toBe(0);
        expect(response.freelance_students.length).toBe(0);
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/accounting/estimated-earnings-by-month-year/${month}/${year}/`,
      });

      request.flush(emptyReport);
    }));
  });

  describe('submitFreelanceTuitionTransaction', () => {
    it('should create a new freelance tuition transaction and return the transaction record', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      
      service.submitFreelanceTuitionTransaction(freelanceTuitionTransactionData).subscribe(response => {
        expect(response).toEqual(freelanceTuitionTransactionRecordData);
        expect(response.id).toBe(1);
        expect(response.transaction_amount).toBe(250.00);
      });

      const request = httpTestingController.expectOne({
        method: 'POST',
        url: `${environment.apiUrl}/api/accounting/tuition-transactions/`,
      });

      expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
      expect(request.request.body).toEqual(freelanceTuitionTransactionData);
      request.flush(freelanceTuitionTransactionRecordData);
    }));

    it('should return an error message when creating transaction with incorrect data', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      
      service.submitFreelanceTuitionTransaction(freelanceTuitionTransactionData).subscribe({
        next: () => {},
        error: (error: HttpErrorResponse) => {
          expect(error.status).toEqual(400);
          expect(error.error).toEqual(httpFreelanceTuitionTransactionCreateError1);
        }
      });

      const request = httpTestingController.expectOne({
        method: 'POST',
        url: `${environment.apiUrl}/api/accounting/tuition-transactions/`,
      });

      request.flush(
        httpFreelanceTuitionTransactionCreateError1,
        { status: 400, statusText: 'Bad Request' }
      );
    }));

    it('should return an error message when creating transaction for non-existent student', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      
      service.submitFreelanceTuitionTransaction(freelanceTuitionTransactionData).subscribe({
        next: () => {},
        error: (error: HttpErrorResponse) => {
          expect(error.status).toEqual(400);
          expect(error.error).toEqual({ 
            student_or_class: ['Invalid pk "999" - object does not exist.'] 
          });
        }
      });

      const request = httpTestingController.expectOne({
        method: 'POST',
        url: `${environment.apiUrl}/api/accounting/tuition-transactions/`,
      });

      request.flush(
        { student_or_class: ['Invalid pk "999" - object does not exist.'] },
        { status: 400, statusText: 'Bad Request' }
      );
    }));
  });

  describe('submitSchoolAccountingEmailReportRequest', () => {
    it('should successfully request email report and return success response', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const month = 3;
      const year = 2025;
      const schoolId = 1;
      
      service.submitSchoolAccountingEmailReportRequest(month, year, schoolId).subscribe(response => {
        expect(response).toEqual(emailSuccessResponse);
        expect(response.message).toBe('Accounting report email sent successfully');
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/accounting/email-estimated-school-earnings-by-month-year/${month}/${year}/${schoolId}/`,
      });

      expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
      request.flush(emailSuccessResponse);
    }));

    it('should return an error message when requesting email for non-existent school', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const month = 3;
      const year = 2025;
      const nonExistentSchoolId = 999;
      
      service.submitSchoolAccountingEmailReportRequest(month, year, nonExistentSchoolId).subscribe({
        next: () => {},
        error: (error: HttpErrorResponse) => {
          expect(error.status).toEqual(404);
          expect(error.error).toEqual({ detail: 'Not found.' });
        }
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/accounting/email-estimated-school-earnings-by-month-year/${month}/${year}/${nonExistentSchoolId}/`,
      });

      request.flush(
        { detail: 'Not found.' },
        { status: 404, statusText: 'Not Found' }
      );
    }));

    it('should return an error message when email sending fails', 
      fakeAsync(() => {
      authServiceSpy.getAuthToken.and.returnValue(authData.token);
      const month = 3;
      const year = 2025;
      const schoolId = 1;
      
      service.submitSchoolAccountingEmailReportRequest(month, year, schoolId).subscribe({
        next: () => {},
        error: (error: HttpErrorResponse) => {
          expect(error.status).toEqual(500);
          expect(error.error).toEqual(httpEmailReportError1);
        }
      });

      const request = httpTestingController.expectOne({
        method: 'GET',
        url: `${environment.apiUrl}/api/accounting/email-estimated-school-earnings-by-month-year/${month}/${year}/${schoolId}/`,
      });

      request.flush(
        httpEmailReportError1,
        { status: 500, statusText: 'Internal Server Error' }
      );
    }));
  });
});
