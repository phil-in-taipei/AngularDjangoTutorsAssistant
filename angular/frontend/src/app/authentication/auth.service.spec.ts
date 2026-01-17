import { TestBed, fakeAsync, flush, tick, discardPeriodicTasks } from '@angular/core/testing';
import { environment } from '../../environments/environment';
import { Subscription } from 'rxjs';
import { Router } from '@angular/router';
import { HttpTestingController, HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { 
  httpTokensResponse, 
  httpTokenResponseFailure,
  httpTokenRefreshResponse1, 
  httpTokenRefreshResponse2, 
  httpTokenRefreshResponse3 
} from '../test-data/authentication-tests/authentication-data';
import { UserProfileComponent } from '../authenticated-user/user/user-profile/user-profile.component';
import { AuthService } from './auth.service';
import { MockStore, provideMockStore } from '@ngrx/store/testing';

fdescribe('AuthService', () => {
  let testRouter: Router; 
  let service: AuthService;
  let httpTestingController: HttpTestingController;
  let store: MockStore;
  const initialState = { 
    user: {
      userProfileLoaded: false,
      usrProfile: undefined
    }
  };

  beforeEach(() => {
    let storage: {[index: string]:any} = {};
    
    const mockLocalStorage = {
      getItem: (key: string): string | null => {
        return key in storage ? storage[key] : null;
      },
      setItem: (key: string, value: string) => {
        storage[key] = `${value}`;
      },
      removeItem: (key: string) => {
        delete storage[key];
      },
      clear: () => {
        storage = {};
      }
    };

    spyOn(localStorage, 'getItem').and.callFake(mockLocalStorage.getItem);
    spyOn(localStorage, 'setItem').and.callFake(mockLocalStorage.setItem);
    spyOn(localStorage, 'removeItem').and.callFake(mockLocalStorage.removeItem);
    spyOn(localStorage, 'clear').and.callFake(mockLocalStorage.clear);

    TestBed.configureTestingModule({
      imports: [ 
        HttpClientTestingModule, 
        RouterTestingModule.withRoutes([
          { path: 'authenticated-user/scheduling/landing', component: UserProfileComponent }
        ]), 
      ],
      providers: [
        provideMockStore({ initialState }),
        AuthService, 
        { provider: localStorage, useValue: mockLocalStorage },
      ]
    });

    testRouter = TestBed.inject(Router);
    spyOn(testRouter, 'navigate').and.returnValue(Promise.resolve(true));  

    service = TestBed.inject(AuthService);
    httpTestingController = TestBed.inject(HttpTestingController);
    store = TestBed.inject(MockStore);
  });

  afterEach(() => {
    // Logout to clean up any running intervals
    service.logout();
    
    // Verify no outstanding HTTP requests
    httpTestingController.verify();
    
    // Clean up any remaining periodic tasks
    try {
      discardPeriodicTasks();
    } catch (e) {
      // Ignore if no tasks to discard
    }
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
    expect(service.getAuthStatusListener()).toBeTruthy();
    expect(service.getAuthToken()).toBeFalsy();
  });

  it('should accept user login data to make the request', fakeAsync(() => {
    service.login('testusername', 'testpassword');
    const request = httpTestingController.expectOne({
      method: 'POST',
      url:`${environment.apiUrl}/auth/jwt/create`,
    });

    expect(request.request.body).toEqual(
      {username: 'testusername', password: 'testpassword'}
    );

    request.flush(httpTokensResponse);
    
    // Clean up
    service.logout();
    discardPeriodicTasks();
  }));

  it('should enable login error listener observable to return true after unsuccessful login attempt with incorrect data', 
    fakeAsync(() => {
    let isLoginError = false;
    const authErrorListenerSubs$: Subscription = service.getLoginErrorListener()
      .subscribe(isError => {
        isLoginError = isError;
      });
    
    service.login('incorrectusername', 'incorrectpassword');
    const request = httpTestingController.expectOne({
      method: 'POST',
      url:`${environment.apiUrl}/auth/jwt/create`,
    });
    
    request.flush(httpTokenResponseFailure, { status: 400, statusText: 'Unauthorized' });
    expect(isLoginError).toBe(true);
    
    authErrorListenerSubs$.unsubscribe();
    flush();
  }));

  it('should save the token, refresh token, and expiration times in local storage after login', 
    fakeAsync(() => {
    service.login('testusername', 'testpassword');
    const request = httpTestingController.expectOne({
      method: 'POST',
      url:`${environment.apiUrl}/auth/jwt/create`,
    });

    request.flush(httpTokensResponse);

    expect(localStorage.setItem).toHaveBeenCalledTimes(4); 

    // Tokens are now encrypted, so we check they exist rather than exact values
    expect(localStorage.getItem('refresh')).toBeTruthy();
    expect(localStorage.getItem('token')).toBeTruthy(); 

    // saved to Date.prototype.toISOString should be 24 or 27 chars in length
    expect(localStorage.getItem('refreshExpiration')?.length).toBeGreaterThanOrEqual(24);
    expect(localStorage.getItem('expiration')?.length).toBeGreaterThanOrEqual(24);

    expect(service.getAuthToken()).toEqual(httpTokensResponse['access']);

    service.logout();
    discardPeriodicTasks();
  }));

  it('should make the access token accessible by calling the getAuthToken() function after successful login', 
    fakeAsync(() => {
    service.login('testusername', 'testpassword');
    const request = httpTestingController.expectOne({
      method: 'POST',
      url:`${environment.apiUrl}/auth/jwt/create`,
    });

    request.flush(httpTokensResponse);

    expect(service.getAuthToken()).toEqual(httpTokensResponse['access']);

    service.logout();
    discardPeriodicTasks();
  }));

  it('should set auth status to true upon successful login', fakeAsync(() => {
    service.login('testusername', 'testpassword');
    const request = httpTestingController.expectOne({
      method: 'POST',
      url:`${environment.apiUrl}/auth/jwt/create`,
    });

    request.flush(httpTokensResponse);

    expect(service.getIsAuth()).toBe(true);

    service.logout();
    discardPeriodicTasks();
  }));

  it('should enable auth status listener observable to return true upon successful login', 
    fakeAsync(() => {
    let userIsAuthenticated = false;
    const authListenerSubs$: Subscription = service.getAuthStatusListener()
      .subscribe(isAuthenticated => {
        userIsAuthenticated = isAuthenticated;
      });
    
    service.login('testusername', 'testpassword');
    const request = httpTestingController.expectOne({
      method: 'POST',
      url:`${environment.apiUrl}/auth/jwt/create`,
    });

    request.flush(httpTokensResponse);

    expect(userIsAuthenticated).toBe(true);

    authListenerSubs$.unsubscribe();
    service.logout();
    discardPeriodicTasks();
  }));

  it('should navigate to scheduling landing page upon successful login', fakeAsync(() => {
    service.login('testusername', 'testpassword');
    const request = httpTestingController.expectOne({
      method: 'POST',
      url:`${environment.apiUrl}/auth/jwt/create`,
    });

    request.flush(httpTokensResponse);
    
    expect(testRouter.navigate).toHaveBeenCalledWith(
      ['authenticated-user', 'scheduling', 'landing']
    );

    service.logout();
    discardPeriodicTasks();
  }));

  it('should check token expiration periodically using interval', fakeAsync(() => {
    service.login('testusername', 'testpassword');
    const loginRequest = httpTestingController.expectOne({
      method: 'POST',
      url:`${environment.apiUrl}/auth/jwt/create`,
    });

    loginRequest.flush(httpTokensResponse);

    // Verify interval is running by checking that time advances without errors
    // The interval checks every 30 seconds
    tick(30000);
    
    // No refresh should happen yet since token hasn't expired
    httpTestingController.expectNone({
      method: 'POST',
      url:`${environment.apiUrl}/auth/jwt/refresh`,
    });

    service.logout();
    discardPeriodicTasks();
  }));

  it('should fetch a replacement token when token is about to expire', fakeAsync(() => {
    service.login('testusername', 'testpassword');
    const loginRequest = httpTestingController.expectOne({
      method: 'POST',
      url:`${environment.apiUrl}/auth/jwt/create`,
    });

    loginRequest.flush(httpTokensResponse);

    // Token expires in 9 mins 51 secs (environment.tokenMinsAmount * 60 * 1000 + environment.tokenSecondsAmount * 1000)
    // It should refresh when less than 60 seconds remain
    // So we tick to 9 mins 50 secs (10 seconds before expiration) and then trigger interval check
    const tokenLifetime = (environment.tokenMinsAmount * 60 + environment.tokenSecondsAmount) * 1000;
    tick(tokenLifetime - 10000); // 10 seconds before expiration
    
    // Trigger the 30-second interval check
    tick(30000);

    // Handle all refresh requests that may have been triggered
    const refreshRequests = httpTestingController.match({
      method: 'POST',
      url:`${environment.apiUrl}/auth/jwt/refresh`,
    });

    // Flush the first request (or all if multiple)
    expect(refreshRequests.length).toBeGreaterThan(0);
    refreshRequests[0].flush(httpTokenRefreshResponse1);
    
    // Flush any additional requests with the same response
    for (let i = 1; i < refreshRequests.length; i++) {
      refreshRequests[i].flush(httpTokenRefreshResponse1);
    }

    // 4 variables saved at least twice (login + refresh(es))
    expect(localStorage.setItem).toHaveBeenCalledWith('token', jasmine.any(String));
    expect(service.getAuthToken()).toEqual(httpTokenRefreshResponse1['access']);

    service.logout();
    discardPeriodicTasks();
  }));

  it('should redirect the router to the login page after logging out', fakeAsync(() => {
    service.logout();
    expect(testRouter.navigate).toHaveBeenCalledWith(['/']);
    flush();
  }));

  it('should set authentication status to false after logging out', fakeAsync(() => {
    service.logout();
    expect(service.getIsAuth()).toBe(false);
    flush();
  }));

  it('should clear all items from local storage after logging out', fakeAsync(() => {
    // Mock setting tokens and expiration times in local storage
    const dtToken:Date = new Date();
    dtToken.setSeconds(dtToken.getSeconds() + environment.tokenSecondsAmount);
    const dtRfrshTken:Date = new Date();

    dtRfrshTken.setMinutes(dtRfrshTken.getMinutes() + environment.tokenRefreshMinsAmount);
    dtRfrshTken.setSeconds(dtRfrshTken.getSeconds() + environment.tokenRefreshSecondsAmount);
    
    localStorage.setItem('refresh', service.encryptToken(httpTokensResponse.refresh));
    localStorage.setItem('refreshExpiration', dtRfrshTken.toISOString());
    localStorage.setItem('token', service.encryptToken(httpTokensResponse.access));
    localStorage.setItem('expiration', dtToken.toISOString());

    service.logout();

    // After logout, the items are no longer in local storage
    expect(localStorage.getItem('refresh')).toEqual(null);
    expect(localStorage.getItem('token')).toEqual(null); 
    expect(localStorage.getItem('refreshExpiration')).toEqual(null); 
    expect(localStorage.getItem('expiration')).toEqual(null); 
    
    flush();
  }));

  it('should enable auth status listener observable to return false after logout is called', 
    fakeAsync(() => {
    let userIsAuthenticated = true;
    const authListenerSubs$: Subscription = service.getAuthStatusListener()
      .subscribe(isAuthenticated => {
        userIsAuthenticated = isAuthenticated;
      });

    service.logout();
    expect(userIsAuthenticated).toBe(false);

    authListenerSubs$.unsubscribe();
    flush();
  }));

  it('should decrypt tokens correctly', () => {
    const originalToken = 'test-token-value';
    const encrypted = service.encryptToken(originalToken);
    const decrypted = service.decryptToken(encrypted);
    
    expect(decrypted).toEqual(originalToken);
  });

  it('should return null for invalid encrypted tokens', () => {
    const result = service.decryptToken('invalid-encrypted-string');
    expect(result).toBeNull();
  });

  it('should clear login error when clearLoginError is called', fakeAsync(() => {
    let isLoginError = true;
    const authErrorListenerSubs$: Subscription = service.getLoginErrorListener()
      .subscribe(isError => {
        isLoginError = isError;
      });

    service.clearLoginError();
    expect(isLoginError).toBe(false);

    authErrorListenerSubs$.unsubscribe();
    flush();
  }));

  it('should call fetchRefreshToken method when manually invoked', fakeAsync(() => {
    // First login to set up refresh token
    service.login('testusername', 'testpassword');
    const loginRequest = httpTestingController.expectOne({
      method: 'POST',
      url:`${environment.apiUrl}/auth/jwt/create`,
    });
    loginRequest.flush(httpTokensResponse);

    // Manually call fetchRefreshToken (it's public for testing)
    service.fetchRefreshToken();

    const refreshRequest = httpTestingController.expectOne({
      method: 'POST',
      url:`${environment.apiUrl}/auth/jwt/refresh`,
    });
    refreshRequest.flush(httpTokenRefreshResponse1);

    expect(service.getAuthToken()).toEqual(httpTokenRefreshResponse1['access']);

    service.logout();
    discardPeriodicTasks();
  }));
});
