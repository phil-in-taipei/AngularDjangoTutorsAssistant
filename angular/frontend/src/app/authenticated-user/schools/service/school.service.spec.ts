import { TestBed, fakeAsync, flush } from '@angular/core/testing';
import { HttpErrorResponse } from '@angular/common/http';
import { HttpTestingController, HttpClientTestingModule } from '@angular/common/http/testing';

import { authData } from 'src/app/test-data/authentication-tests/authentication-data';
import { AuthService } from 'src/app/authentication/auth.service';
import { environment } from 'src/environments/environment';
import { SchoolService } from './school.service';
import { 
  schoolData, 
  schoolsData, 
  schoolCreateAndEditData,
  httpSchoolCreateError1,
  httpSchoolEditError1,
  httpSchoolDeleteError1,
  deletionResponseSuccess
} from 'src/app/test-data/authenticated-user-module-tests/school-related-tests/school-data';

describe('SchoolService', () => {
  let service: SchoolService;
  let httpTestingController: HttpTestingController;
  let authServiceSpy: jasmine.SpyObj<AuthService>;

  beforeEach(() => {
    authServiceSpy = jasmine.createSpyObj('AuthService', ['getAuthToken']);
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [
        SchoolService,
        { provide: AuthService, useValue: authServiceSpy }
      ]
    });
    service = TestBed.inject(SchoolService);
    httpTestingController = TestBed.inject(HttpTestingController);
    authServiceSpy = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
  });

  afterEach(() => {
    httpTestingController.verify();
  });

  it('should return a list of user schools from the api', 
    fakeAsync(() => {
    authServiceSpy.getAuthToken.and.returnValue(authData.token);
    
    service.fetchUsersSchools().subscribe(response => {
      expect(response).toEqual(schoolsData);
    });

    const request = httpTestingController.expectOne({
      method: 'GET',
      url: `${environment.apiUrl}/api/schools/users-schools/`,
    });

    expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
    request.flush(schoolsData);
  }));

  it('should create a new school and return the created school', 
    fakeAsync(() => {
    authServiceSpy.getAuthToken.and.returnValue(authData.token);
    
    service.submitSchool(schoolCreateAndEditData).subscribe(response => {
      expect(response).toEqual(schoolData);
    });

    const request = httpTestingController.expectOne({
      method: 'POST',
      url: `${environment.apiUrl}/api/schools/users-schools/`,
    });

    expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
    expect(request.request.body).toEqual(schoolCreateAndEditData);
    request.flush(schoolData);
  }));

  it('should return an error message when creating school with incorrect data', 
    fakeAsync(() => {
    authServiceSpy.getAuthToken.and.returnValue(authData.token);
    
    service.submitSchool(schoolCreateAndEditData).subscribe({
      next: () => {},
      error: (error: HttpErrorResponse) => {
        expect(error.status).toEqual(400);
        expect(error.error).toEqual(httpSchoolCreateError1);
      }
    });

    const request = httpTestingController.expectOne({
      method: 'POST',
      url: `${environment.apiUrl}/api/schools/users-schools/`,
    });

    request.flush(
      httpSchoolCreateError1,
      { status: 400, statusText: 'Bad Request' }
    );
  }));

  it('should return an updated school after submitting edited school', 
    fakeAsync(() => {
    authServiceSpy.getAuthToken.and.returnValue(authData.token);
    const schoolId = 1;
    const updatedSchoolData = {
      ...schoolData,
      school_name: schoolCreateAndEditData.school_name,
      address_line_1: schoolCreateAndEditData.address_line_1,
      address_line_2: schoolCreateAndEditData.address_line_2,
      contact_phone: schoolCreateAndEditData.contact_phone,
      other_information: schoolCreateAndEditData.other_information
    };

    service.editSchool(schoolId, schoolCreateAndEditData).subscribe(response => {
      expect(response).toEqual(updatedSchoolData);
    });

    const request = httpTestingController.expectOne({
      method: 'PATCH',
      url: `${environment.apiUrl}/api/schools/users-school/${schoolId}/`,
    });

    expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
    expect(request.request.body).toEqual(schoolCreateAndEditData);
    request.flush(updatedSchoolData);
  }));

  it('should return an error message when editing school with incorrect data', 
    fakeAsync(() => {
    authServiceSpy.getAuthToken.and.returnValue(authData.token);
    const schoolId = 1;

    service.editSchool(schoolId, schoolCreateAndEditData).subscribe({
      next: () => {},
      error: (error: HttpErrorResponse) => {
        expect(error.status).toEqual(400);
        expect(error.error).toEqual(httpSchoolEditError1);
      }
    });

    const request = httpTestingController.expectOne({
      method: 'PATCH',
      url: `${environment.apiUrl}/api/schools/users-school/${schoolId}/`,
    });

    request.flush(
      httpSchoolEditError1,
      { status: 400, statusText: 'Bad Request' }
    );
  }));

  it('should return an error message when editing non-existent school', 
    fakeAsync(() => {
    authServiceSpy.getAuthToken.and.returnValue(authData.token);
    const nonExistentSchoolId = 999;

    service.editSchool(nonExistentSchoolId, schoolCreateAndEditData).subscribe({
      next: () => {},
      error: (error: HttpErrorResponse) => {
        expect(error.status).toEqual(404);
        expect(error.error).toEqual({ detail: 'Not found.' });
      }
    });

    const request = httpTestingController.expectOne({
      method: 'PATCH',
      url: `${environment.apiUrl}/api/schools/users-school/${nonExistentSchoolId}/`,
    });

    request.flush(
      { detail: 'Not found.' },
      { status: 404, statusText: 'Not Found' }
    );
  }));

  it('should successfully delete a school', 
    fakeAsync(() => {
    authServiceSpy.getAuthToken.and.returnValue(authData.token);
    const schoolId = 1;

    service.deleteSchool(schoolId).subscribe(response => {
      expect(response).toEqual(deletionResponseSuccess);
    });

    const request = httpTestingController.expectOne({
      method: 'DELETE',
      url: `${environment.apiUrl}/api/schools/users-school/${schoolId}/`,
    });

    expect(request.request.headers.get('Authorization')).toBe(`Token ${authData.token}`);
    request.flush(deletionResponseSuccess);
  }));

  it('should return an error message when deleting non-existent school', 
    fakeAsync(() => {
    authServiceSpy.getAuthToken.and.returnValue(authData.token);
    const nonExistentSchoolId = 999;

    service.deleteSchool(nonExistentSchoolId).subscribe({
      next: () => {},
      error: (error: HttpErrorResponse) => {
        expect(error.status).toEqual(404);
        expect(error.error).toEqual({ detail: 'Not found.' });
      }
    });

    const request = httpTestingController.expectOne({
      method: 'DELETE',
      url: `${environment.apiUrl}/api/schools/users-school/${nonExistentSchoolId}/`,
    });

    request.flush(
      { detail: 'Not found.' },
      { status: 404, statusText: 'Not Found' }
    );
  }));

  it('should return an error message when deleting school with permission issues', 
    fakeAsync(() => {
    authServiceSpy.getAuthToken.and.returnValue(authData.token);
    const schoolId = 1;

    service.deleteSchool(schoolId).subscribe({
      next: () => {},
      error: (error: HttpErrorResponse) => {
        expect(error.status).toEqual(403);
        expect(error.error).toEqual(httpSchoolDeleteError1);
      }
    });

    const request = httpTestingController.expectOne({
      method: 'DELETE',
      url: `${environment.apiUrl}/api/schools/users-school/${schoolId}/`,
    });

    request.flush(
      httpSchoolDeleteError1,
      { status: 403, statusText: 'Forbidden' }
    );
  }));
});
