import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Subject } from 'rxjs';
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

declare global {
  interface Window { 
    FRONTEND_CONFIG: {
      encryptionKey: string;
    }; 
  }
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private isAuthenticated: boolean = false;
  private isLoginError: boolean = false;
  private token: string;
  private tokenExpTime: Date
  private tokenTimer: NodeJS.Timer;
  private refresh: string;
  private refreshExpTime: Date;
  private authStatusListener = new Subject<boolean>();
  private loginErrorListener = new Subject<boolean>();
  private encryptionKey: string | null = null;
  private SECRET_KEY = 'djkljadfsaoasddd82k22kds;o;kjpvsajsjlxoijjdis';

  constructor(
    private http: HttpClient, private router: Router, 
    private store: Store<AppState>
  ) { 
    this.loadEncryptionKey(); 
    if (this.encryptionKey) {
      this.SECRET_KEY = this.encryptionKey
    }
  }

  autoAuthUser(): void {
    const authInformation = this.getAuthData();
    if (authInformation) {
      if (authInformation.accessExpDate && authInformation.token &&
          authInformation.refreshExp && authInformation.refresh) {
          // Auth info in local storage
          const now = new Date();
          if(authInformation.refreshExp > now) {
            //'refresh token is not expired. ' + 
            //  'Setting token variables and authentication status to true
            this.isAuthenticated = true;
            this.authStatusListener.next(true);
            this.token = authInformation.token;
            this.tokenExpTime = new Date(authInformation.accessExpDate);
            this.refresh = authInformation.refresh;
            this.refreshExpTime = new Date(authInformation.refreshExp);
            let timeUntilTokenExp = new Date().getTime() - this.tokenExpTime.getTime();
            // reset timer
            this.setAuthTimer(timeUntilTokenExp); // if the value is negative, the timer will
                                                  // immediately trigger refreshTokenOrLogout();
            //this.router.navigate(['authenticated-user', 'user-profile']);
            this.router.navigate(['authenticated-user', 'scheduling', 'landing']);
          } else {
            //console.log('refresh token expired. Logging out...')
            this.logout();
            //return;
          }
      } else {
        //console.log('Token info incomplete. Logging out...');
        this.logout();
        //return;
      }
    } else {
      //console.log('Token info undefined. Logging out...');
      this.logout();
    }
  }

  private loadEncryptionKey(): void {
    try {
      // Get the script element by ID
      const scriptElement = document.getElementById('encryption-config');
      if (!scriptElement) {
        //'Encryption configuration not found'
        return;
      }
      // Parse the JSON content from the script tag
      const config = JSON.parse(scriptElement.textContent || '{}');
      this.encryptionKey = config.frontend_encryption_key;
      
      // Important security step: Remove the script element so it's not accessible later
      // This makes it harder for malicious scripts to find the key
      scriptElement.remove();
      
    } catch (error) {
      //console.error('Error loading encryption configuration:', error);
      return;
    }
  }


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

  private createSixHourTimeString() {
    return  Math.floor(Date.now() / (6 * 60 * 60 * 1000)).toString(); 
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
          this.setAuthTimer(environment.authTimerAmount); // 50000 (50 seconds) // 285000 (4.75 minutes)
          
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
    //const bytes = AES.decrypt(encryptedToken, `${this.SECRET_KEY}${this.createSixHourTimeString()}`);
    //return bytes.toString(Utf8);
    try {
      const bytes = AES.decrypt(encryptedToken, `${this.SECRET_KEY}${this.createSixHourTimeString()}`);
      const decryptedToken = bytes.toString(Utf8);

      // Add validation to check if the decrypted token is valid
      if (!decryptedToken || decryptedToken.trim() === '') {
        return null; // or throw an error, or handle it as needed
      }

      return decryptedToken;
    } catch (error) {
      // Handle any potential errors during decryption
      //console.error('Decryption failed:', error);
      return null; // or throw an error, or handle it as needed
    }
  }

  public encryptToken(authToken: string): string {
    const encryptedToken: string = AES.encrypt(
      authToken, `${this.SECRET_KEY}${this.createSixHourTimeString()}`
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
          // for testing, the refresh expires in 2 mins and 50 seconds
          // in production, the refresh expires in 23 hours and 45 minutes
          dtRfrshTken.setHours(dtRfrshTken.getHours() + environment.tokenRefreshHoursAmount);
          dtRfrshTken.setMinutes(dtRfrshTken.getMinutes() + environment.tokenRefreshMinsAmount);
          dtRfrshTken.setSeconds(dtRfrshTken.getSeconds() + environment.tokenRefreshSecondsAmount);
          this.refreshExpTime = new Date(dtRfrshTken);
          this.setAuthTimer(environment.authTimerAmount); // 285000 (4 minutes 45 seconds) // 50000 (50 seconds)
          this.saveAuthData(this.refresh, this.refreshExpTime,
            this.token, this.tokenExpTime);
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


  logout() {
    this.isAuthenticated = false;
    this.authStatusListener.next(false);
    clearTimeout(this.tokenTimer);
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

  private setAuthTimer(duration: number) {
    // auth timer is being set');
    // for this long: ${duration}`);
    this.tokenTimer = setTimeout(() => {
      //'time is up
      let dt:Date = new Date();
      console.log(dt);
      this.refreshTokenOrLogout();
    }, duration);
  }
  
}
