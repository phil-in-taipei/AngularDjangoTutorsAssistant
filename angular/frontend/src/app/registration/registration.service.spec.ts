import { TestBed, fakeAsync, flush  } from '@angular/core/testing';
import { HttpTestingController, HttpClientTestingModule
} from '@angular/common/http/testing';
import { environment } from '../../environments/environment';
import { HttpErrorResponse } from '@angular/common/http';
import { RegistrationService } from './registration.service';
import { 
  userRegistrationData, 
  httpRegistrationResponseSuccess, 
  httpRegistrationResponseFailure1,
  httpRegistrationResponseFailure2,
  httpRegistrationResponseFailure3
} 
  from '../test-data/registration-tests/registration-data';

describe('RegistrationService', () => {
  let service: RegistrationService;
  let httpTestingController: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [ HttpClientTestingModule ],
      providers: [ RegistrationService ]
    });
    service = TestBed.inject(RegistrationService);
    httpTestingController = TestBed.inject(HttpTestingController);
  });

  it('should accept user registration data to make the request', 
    fakeAsync(() => {
    service.submitUserRegistration(userRegistrationData).subscribe();

    const request = httpTestingController.expectOne({
      method: 'POST',
      url:`${environment.apiUrl}/api/register/user`,
    });

    expect(request.request.body).toEqual(userRegistrationData);

    request.flush(httpRegistrationResponseSuccess);
  }));

  it('should return a success message upon successfully submitting new user registration', 
    fakeAsync(() => {
    service.submitUserRegistration(userRegistrationData).subscribe(response => {
      expect(response).toEqual(httpRegistrationResponseSuccess);
    });

    const request = httpTestingController.expectOne({
      method: 'POST',
      url:`${environment.apiUrl}/api/register/user`,
    });

    request.flush(httpRegistrationResponseSuccess);

  }));


  it('should return a failure message upon unsuccessfully submitting ' +
    'new user registration due to mismatched passwords', 
      fakeAsync(() => {
        userRegistrationData.passwordConfirmation = 'anotherpassword';
        service.submitUserRegistration(userRegistrationData).subscribe({
          next: () => {},
          error: (error: HttpErrorResponse) => {
            expect(error.status).toEqual(400);
            expect(error.error).toEqual(httpRegistrationResponseFailure1);
          }
        });

        const request = httpTestingController.expectOne({
          method: 'POST',
          url:`${environment.apiUrl}/api/register/user`,
        });

        request.flush(
          httpRegistrationResponseFailure1, 
          { status: 400, statusText: 'Bad Request' }
        );
    }));


    it('should return a failure message upon unsuccessfully submitting ' +
    'new user registration due to incomplete data submission', 
      fakeAsync(() => {
        // it is actually impossible to submit incomplete data due to typescript model
        service.submitUserRegistration(userRegistrationData).subscribe({
          next: () => {},
          error: (error: HttpErrorResponse) => {
            expect(error.status).toEqual(400);
            expect(error.error).toEqual(httpRegistrationResponseFailure3);
          }
        });

        const request = httpTestingController.expectOne({
          method: 'POST',
          url:`${environment.apiUrl}/api/register/user`,
        });

        request.flush(
          httpRegistrationResponseFailure3, 
          { status: 400, statusText: 'Bad Request' }
        );
    }));

    it('should return a failure message upon unsuccessfully submitting ' +
    'new user registration due to user already in existence', 
      fakeAsync(() => {
        service.submitUserRegistration(userRegistrationData).subscribe({
          next: () => {},
          error: (error: HttpErrorResponse) => {
            expect(error.status).toEqual(400);
            expect(error.error).toEqual(httpRegistrationResponseFailure2);
          }
        });

        const request = httpTestingController.expectOne({
          method: 'POST',
          url:`${environment.apiUrl}/api/register/user`,
        });

        request.flush(
          httpRegistrationResponseFailure2, 
          { status: 400, statusText: 'Bad Request' }
        );

    }));

    it('should handle error due to network error when submitting user registration', 
      fakeAsync(() => {
          service.submitUserRegistration(userRegistrationData).subscribe({
              next: () => {},
              error: (error) => { expect(error).toBeTruthy();}
              });
      
        const request = httpTestingController.expectOne({
          method: 'POST',
          url:`${environment.apiUrl}/api/register/user`,
        });
        request.error(new ProgressEvent('network error'));
        flush
    }));

    afterEach(() => {
      httpTestingController.verify();
    });
});
