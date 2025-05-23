import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Subject, interval, Subscription } from 'rxjs';
import { takeWhile } from 'rxjs/operators';
// Use require-style imports instead of ES modules
// for encryption
const AES = require('crypto-js/aes');
const Utf8 = require('crypto-js/enc-utf8');
import { Store } from '@ngrx/store';
import { environment } from '../../environments/environment';
import { AuthDataModel } from '../models/auth-data.model';
import { 
  AuthLoginModel, AuthLoginResponseModel, 
  AuthTokenRefreshResponseModel 
} from '../models/auth-login.model';
import { AppState } from './../reducers';
import { 
  RecurringClassAppliedMonthlysCleared 
} from '../authenticated-user/scheduling/recurring-schedule/state/recurring-classes-applied-monthly-state/recurring-class-applied-monthly.actions';
import { 
  RecurringClassesCleared 
} from '../authenticated-user/scheduling/recurring-schedule/state/recurring-schedule-state/recurring-schedule.actions';
import { 
  ScheduledClassesCleared 
} from '../authenticated-user/scheduling/classes-state/scheduled-classes.actions';
import { SchoolsCleared } from '../authenticated-user/schools/state/school.actions';
import { 
  StudentsOrClassesCleared 
} from '../authenticated-user/student-or-class/state/student-or-class.actions';
import { 
  UserProfileCleared 
} from '../authenticated-user/user/user-state/user.actions';


@Injectable({
  providedIn: 'root'
})
export class AuthService { // testing out alternative version with subsription for timer

  private isAuthenticated: boolean = false;
  private isLoginError: boolean = false;
  private token: string;
  private tokenExpTime: Date
  private tokenSubscription: Subscription | null = null;
  private lastActivity: number = Date.now();
  private refresh: string;
  private refreshExpTime: Date;
  private authStatusListener = new Subject<boolean>();
  private loginErrorListener = new Subject<boolean>();
  //private encryptionKey: string | null = null;
  //private SECRET_KEY = 'djkljadfsaoasddd82k22kds;o;kjpvsajsjlxoijjdis';
  private checkIntervalMs = 30000; // Check every 30 seconds

  constructor(
    private http: HttpClient, private router: Router, 
    private store: Store<AppState>
  ) { 
    //this.loadEncryptionKey(); 
    //if (this.encryptionKey) {
    //  this.SECRET_KEY = this.encryptionKey
    //}
    // Monitor user activity
    this.setupActivityListeners();
  }


  // Set up event listeners to track user activity
  private setupActivityListeners(): void {
    const events = ['mousedown', 'keydown', 'touchstart', 'scroll', 'visibilitychange'];
    events.forEach(event => {
      document.addEventListener(event, () => this.updateLastActivity());
    });
  }

  // Update the timestamp of the last user activity
  private updateLastActivity(): void {
    this.lastActivity = Date.now();
  }


  autoAuthUser(): void {
    const authInformation = this.getAuthData();
    if (authInformation) {
      if (authInformation.accessExpDate && authInformation.token &&
          authInformation.refreshExp && authInformation.refresh) {
          // Auth info in local storage
          const now = new Date();
          if(authInformation.refreshExp > now) {
            this.isAuthenticated = true;
            this.authStatusListener.next(true);
            this.token = authInformation.token;
            this.tokenExpTime = new Date(authInformation.accessExpDate);
            this.refresh = authInformation.refresh;
            this.refreshExpTime = new Date(authInformation.refreshExp);
            
            // Use the token monitoring system instead of setTimeout
            this.startTokenExpirationTimer();
            
            this.router.navigate(['authenticated-user', 'scheduling', 'landing']);
          } else {
            this.logout();
          }
      } else {
        this.logout();
      }
    } else {
      this.logout();
    }
  }

  // the encryption key fetched from backend in this prototype is insecure,
  // so this approach was abandoned in favor of using environment variables
  //  on a separate frontend server with SSR in the future
  /*
  private loadEncryptionKey(): void {
    try {
      // Get the script element by ID
      const scriptElement = document.getElementById('encryption-config');
      if (!scriptElement) {
        return;
      }
      // Parse the JSON content from the script tag
      const config = JSON.parse(scriptElement.textContent || '{}');
      this.encryptionKey = config.frontend_encryption_key;
      
      // Important security step: Remove the script element so it's not accessible later
      // This makes it harder for malicious scripts to find the key
      scriptElement.remove();
      
    } catch (error) {
      return;
    }
  }
  */

  private clearLocalStorage():void {
    localStorage.removeItem('token');
    localStorage.removeItem('expiration');
    localStorage.removeItem('refresh');
    localStorage.removeItem('refreshExpiration');
    localStorage.removeItem('userId');
  }

  clearLoginError() {
    this.loginErrorListener.next(false);
  }


  private clearNgrxStore():void {
    this.store.dispatch(new RecurringClassAppliedMonthlysCleared());
    this.store.dispatch(new RecurringClassesCleared());
    this.store.dispatch(new ScheduledClassesCleared());
    this.store.dispatch(new SchoolsCleared());
    this.store.dispatch(new StudentsOrClassesCleared());
    this.store.dispatch(new UserProfileCleared());
  }

  // public for testing purposes
  public fetchRefreshToken() {
    let refresh = this.refresh;
    this.http.post<AuthTokenRefreshResponseModel>(
      `${environment.apiUrl}/auth/jwt/refresh`, {refresh: refresh})
      .subscribe(response => {
        if (response.access) {
          this.token = response.access;
          this.isAuthenticated = true;
          this.authStatusListener.next(true);
          const dtToken:Date = new Date();
          dtToken.setMinutes(dtToken.getMinutes() + environment.tokenMinsAmount);
          dtToken.setSeconds(dtToken.getSeconds() + environment.tokenSecondsAmount);
          this.tokenExpTime = dtToken;
          
          // Save the updated auth data
          this.saveAuthData(
            this.refresh, this.refreshExpTime,
            this.token, this.tokenExpTime
          );
        }
      }, error => {
        //Error: set auth status to false and logout
        this.authStatusListener.next(false);
        this.logout();
      });
  }


  public decryptToken(encryptedToken: string): string|null {
    try {
      const bytes = AES.decrypt(
        encryptedToken, environment.serial//`${this.SECRET_KEY}`
      );
      const decryptedToken = bytes.toString(Utf8);

      // Add validation to check if the decrypted token is valid
      if (!decryptedToken || decryptedToken.trim() === '') {
        return null; // or throw an error, or handle it as needed
      }

      return decryptedToken;
    } catch (error) {
      return null; // or throw an error, or handle it as needed
    }
  }

  public encryptToken(authToken: string): string {
    const encryptedToken: string = AES.encrypt(
      authToken, environment.serial//`${this.SECRET_KEY}`
    ).toString();
    return encryptedToken
  }


  private getAuthData():AuthDataModel | undefined {
    const token = localStorage.getItem('token');
    const accessExpDate = localStorage.getItem('expiration');
    const refresh = localStorage.getItem('refresh');
    const refreshExpDate = localStorage.getItem('refreshExpiration');
    if (!token || !accessExpDate || !refreshExpDate || !refresh) {
      return;
    }
    const decryptedToken = this.decryptToken(token);
    const decryptedRefreshToken = this.decryptToken(refresh);
    if (!decryptedToken || !decryptedRefreshToken) {
      return;
    }
    return {
      token: decryptedToken,
      accessExpDate: new Date(accessExpDate),
      refresh: decryptedRefreshToken,
      refreshExp: new Date(refreshExpDate)
    }
  }

  getAuthStatusListener() {
    return this.authStatusListener.asObservable();
  }

  getAuthToken(): string {
    return this.token;
  }

  getIsAuth(): boolean {
    return this.isAuthenticated;
  }

  getIsLoginError(): boolean {
    return this.isLoginError;
  }

  getLoginErrorListener() {
    return this.loginErrorListener.asObservable();
  }


  login(username: string, password: string): void {
    const authData: AuthLoginModel = {username: username, password: password};
    this.http.post<AuthLoginResponseModel>(
      `${environment.apiUrl}/auth/jwt/create`, authData
      )
      .subscribe(response => {
        if (response.access && response.refresh) {
          this.refresh = response.refresh;
          this.token = response.access;
          this.isAuthenticated = true;
          this.authStatusListener.next(true);
          this.loginErrorListener.next(false);
          const dtToken:Date = new Date();
          dtToken.setMinutes(dtToken.getMinutes() + environment.tokenMinsAmount);
          dtToken.setSeconds(dtToken.getSeconds() + environment.tokenSecondsAmount);
          this.tokenExpTime = dtToken;
          const dtRfrshTken:Date = new Date();
          
          dtRfrshTken.setHours(dtRfrshTken.getHours() + environment.tokenRefreshHoursAmount);
          dtRfrshTken.setMinutes(dtRfrshTken.getMinutes() + environment.tokenRefreshMinsAmount);
          dtRfrshTken.setSeconds(dtRfrshTken.getSeconds() + environment.tokenRefreshSecondsAmount);
          this.refreshExpTime = new Date(dtRfrshTken);
          
          // Save auth data and start token monitoring
          this.saveAuthData(this.refresh, this.refreshExpTime,
            this.token, this.tokenExpTime);
            
          // Start the token monitoring system
          this.startTokenExpirationTimer();
          
          this.router.navigate(['authenticated-user', 'scheduling', 'landing']);
        } else {
          this.loginErrorListener.next(true);
          this.authStatusListener.next(false);
        }
      }, error => {
        this.loginErrorListener.next(true);
        this.authStatusListener.next(false);
      })
  }

  private refreshTokenOrLogout() {
    const now = new Date();
    if(this.refreshExpTime < now) {
      this.logout();
    } else {
      this.fetchRefreshToken();
    }
  }

 // Start a more reliable token expiration monitoring system using interval
  private startTokenExpirationTimer() {
    // Clear any existing timer
    this.stopTokenExpirationTimer();
    
    // Create a more reliable monitoring system using intervals
    this.tokenSubscription = interval(this.checkIntervalMs)
      .pipe(
        takeWhile(() => this.isAuthenticated)
      )
      .subscribe(() => {
        // Check if token is about to expire (within 1 minute)
        const now = new Date();
        const expiresIn = this.tokenExpTime.getTime() - now.getTime();
        
        // If token expires in less than 1 minute and user was active recently, refresh token
        if (expiresIn < 60000) {
          console.log('Token is about to expire, refreshing...');
          this.refreshTokenOrLogout();
        }
        
        // As an additional safety measure, check if refresh token has expired
        if (this.refreshExpTime < now) {
          console.log('Refresh token expired');
          this.logout();
        }
      });
    
    // Add event listener for visibility changes for mobile support
    document.addEventListener('visibilitychange', this.handleVisibilityChange.bind(this));
  }
  
 // Handle browser visibility changes (when app comes to foreground)
  private handleVisibilityChange() {
    if (document.visibilityState === 'visible' && this.isAuthenticated) {
      // Check token when app comes back to foreground
      const now = new Date();
      if (this.tokenExpTime <= now) {
        console.log('Token has expired while app was in background');
        this.refreshTokenOrLogout();
      }
    }
  }
  
  // Stop token monitoring
  private stopTokenExpirationTimer() {
    if (this.tokenSubscription) {
      this.tokenSubscription.unsubscribe();
      this.tokenSubscription = null;
    }
    
    // Remove visibility change event listener
    document.removeEventListener('visibilitychange', this.handleVisibilityChange.bind(this));
  }

  logout() {
    this.isAuthenticated = false;
    this.authStatusListener.next(false);
    this.stopTokenExpirationTimer();
    this.clearLocalStorage();
    this.clearNgrxStore();
    this.router.navigate(['/']);
  }


  private saveAuthData(refresh: string, refreshExpDate: Date,
    token: string, expirationDate: Date) {
      localStorage.setItem('refresh', this.encryptToken(refresh));
      localStorage.setItem('refreshExpiration', refreshExpDate.toISOString());
      localStorage.setItem('token', this.encryptToken(token));
      localStorage.setItem('expiration', expirationDate.toISOString());
  }

}
