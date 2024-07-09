import { TestBed, fakeAsync, flush, tick } from '@angular/core/testing';
import { environment } from '../../environments/environment';
import { Subscription } from 'rxjs';
import { Router } from '@angular/router';
import { HttpTestingController, HttpClientTestingModule
   } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { httpTokensResponse, httpTokenResponseFailure,
  httpTokenRefreshResponse1, httpTokenRefreshResponse2, 
  httpTokenRefreshResponse3 } from '../test-data/authentication-tests/authentication-data';
import { UserProfileComponent } from '../authenticated-user/user/user-profile/user-profile.component';
import { AuthService } from './auth.service';

describe('AuthService', () => {
  let testRouter: Router; 
  let service: AuthService;
  let httpTestingController: HttpTestingController;

  beforeEach(() => {


    let store: {[index: string]:any} = {};
    
    const mockLocalStorage = {
      getItem: (key: string): string => {
        return key in store ? store[key] : null;
      },
      setItem: (key: string, value: string) => {
        store[key] = `${value}`;
      },
      removeItem: (key: string) => {
        delete store[key];
      },
      clear: () => {
        store = {};
      }
    };

    spyOn(localStorage, 'getItem')
     .and.callFake(mockLocalStorage.getItem);
    spyOn(localStorage, 'setItem')
     .and.callFake(mockLocalStorage.setItem);
    spyOn(localStorage, 'removeItem')
     .and.callFake(mockLocalStorage.removeItem);
    spyOn(localStorage, 'clear')
     .and.callFake(mockLocalStorage.clear);
     

    TestBed.configureTestingModule({
      imports: [ HttpClientTestingModule, RouterTestingModule.withRoutes([
        { path: 'authenticated-user/user-profile', component: UserProfileComponent }
        ]), ],
      providers: [
        AuthService, { provider: localStorage, useValue: mockLocalStorage },
      ]
    });

    testRouter = TestBed.inject(Router);
    spyOn(testRouter, 'navigate').and.returnValue(Promise.resolve(true));  

    service = TestBed.inject(AuthService);
    httpTestingController = TestBed.inject(HttpTestingController);
  });


  it('should be created', () => {
    expect(service).toBeTruthy();
    expect(service.getAuthStatusListener()).toBeTruthy();
    expect(service.getAuthToken()).toBeFalsy()
  });
});
