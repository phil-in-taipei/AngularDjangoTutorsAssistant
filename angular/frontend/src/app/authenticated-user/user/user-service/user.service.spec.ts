import { TestBed, fakeAsync, flush  } from '@angular/core/testing';
import { HttpErrorResponse } from '@angular/common/http';
import { HttpTestingController, HttpClientTestingModule
} from '@angular/common/http/testing';

import { 
  authData 
} from 'src/app/test-data/authentication-tests/authentication-data';
import { AuthService } from 'src/app/authentication/auth.service';
import { environment } from 'src/environments/environment';
import { 
  httpProfileEditError1, httpProfileEditError2,
  userProfileData, userProfileEditData 
} from 'src/app/test-data/authenticated-user-module-tests/user-related-tests/user-data';
import { UserService } from './user.service';

fdescribe('UserService', () => {
  let service: UserService;
  let httpTestingController: HttpTestingController;
  let authServiceSpy: jasmine.SpyObj<AuthService>;

  beforeEach(() => {
    authServiceSpy = jasmine.createSpyObj('AuthService', ['getAuthToken']);
    TestBed.configureTestingModule({
      imports: [ HttpClientTestingModule ],
      providers: [ UserService,
        { provide: AuthService, useValue: authServiceSpy }
      ]
    });
    service = TestBed.inject(UserService);
    httpTestingController = TestBed.inject(HttpTestingController);
    authServiceSpy = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
  });

  it('should return a user profile from the api', 
    fakeAsync(() => {
    authServiceSpy.getAuthToken.and.returnValue(authData.token);
    service.fetchUserProfile().subscribe(response => {
      expect(response).toEqual(userProfileData);
    });

    const request = httpTestingController.expectOne({
      method: 'GET',
      url:`${environment.apiUrl}/api/user/authenticated`,
    });

    request.flush(userProfileData);
  }));

  it('should return an updated user profile after submitting edited profile', 
    fakeAsync(() => {
    authServiceSpy.getAuthToken.and.returnValue(authData.token);
    userProfileData.email = userProfileEditData.email;
    userProfileData.surname = userProfileEditData.surname;
    userProfileData.givenName = userProfileEditData.givenName;

    service.editUserProfile(userProfileEditData).subscribe(response => {
      expect(response).toEqual(userProfileData);
    });

    const request = httpTestingController.expectOne({
      method: 'PATCH',
      url:`${environment.apiUrl}/api/user/edit`,
    });

    request.flush(userProfileData);
  }));

  it('should return an error message when submitting edited ' 
    + ' profile with incorrect data', 
    fakeAsync(() => {
    authServiceSpy.getAuthToken.and.returnValue(authData.token);
    userProfileData.email = userProfileEditData.email;
    userProfileData.surname = userProfileEditData.surname;
    userProfileData.givenName = userProfileEditData.givenName;

    service.editUserProfile(userProfileEditData).subscribe({
      next: () => {},
      error: (error: HttpErrorResponse) => {
        expect(error.status).toEqual(400);
        expect(error.error).toEqual(httpProfileEditError1);
      }
    });

    const request = httpTestingController.expectOne({
      method: 'PATCH',
      url:`${environment.apiUrl}/api/user/edit`,
    });

    request.flush(
      httpProfileEditError1, 
      { status: 400, statusText: 'Bad Request' }
    );
  }));

  it('should return an error message when submitting edited ' 
    + 'profile for non-existant user', 
    fakeAsync(() => {
    authServiceSpy.getAuthToken.and.returnValue(authData.token);
    userProfileData.email = userProfileEditData.email;
    userProfileData.surname = userProfileEditData.surname;
    userProfileData.givenName = userProfileEditData.givenName;

    service.editUserProfile(userProfileEditData).subscribe({
      next: () => {},
      error: (error: HttpErrorResponse) => {
        expect(error.status).toEqual(400);
        expect(error.error).toEqual(httpProfileEditError2);
      }
    });

    const request = httpTestingController.expectOne({
      method: 'PATCH',
      url:`${environment.apiUrl}/api/user/edit`,
    });

    request.flush(
      httpProfileEditError2, 
      { status: 400, statusText: 'Bad Request' }
    );
  }));
});
