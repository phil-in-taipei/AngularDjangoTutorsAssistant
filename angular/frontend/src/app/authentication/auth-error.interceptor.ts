import { Injectable } from "@angular/core";
import { 
  HttpInterceptor, HttpHandler, HttpRequest, HttpEvent, 
  HttpEventType, HttpErrorResponse 
} from "@angular/common/http";
import { Observable, throwError } from "rxjs";
import { tap, catchError } from 'rxjs/operators';
import { AuthService } from './auth.service';

@Injectable()
export class AuthErrorInterceptor implements HttpInterceptor {
  constructor(private authService: AuthService) {}
  
  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {    
    return next.handle(request).pipe(
      tap(event => {
        // Only process Response events
        if (event.type === HttpEventType.Response) {          
          // Safely check for auth errors in the response body
          try {
            if (event.body) {
              if (event.body.detail === 'Given token not valid for any token type') {
                this.authService.logout();
              } else if (event.body.err && event.body.err.detail === "Given token not valid for any token type") {
                this.authService.logout();
              }
            }
          } catch (error) {
            console.error('Error processing response body:', error);
          }
        }
      }),
      // Add proper error handling
      catchError((error: HttpErrorResponse) => {
        //HTTP error intercepted
        
        // Check for authentication errors
        if (error.status === 401) {
          this.authService.logout();
        }
        
        // Also check response body for token errors
        try {
          const errorBody = error.error;
          if (
            errorBody?.detail === 'Given token not valid for any token type' || 
            errorBody?.err?.detail === 'Given token not valid for any token type'
          ) {
            this.authService.logout();
          }
        } catch (e) {
          console.error('Error processing error body:', e);
        }
        
        // Re-throw the error for other error handlers
        return throwError(() => error);
      })
    );
  }
}
