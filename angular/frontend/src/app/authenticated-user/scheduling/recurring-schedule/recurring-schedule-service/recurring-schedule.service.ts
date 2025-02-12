import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

import { AuthService } from 'src/app/authentication/auth.service';
import { DeletionResponse } from 'src/app/models/deletion-response';
import { environment } from 'src/environments/environment';
import { 
  RecurringClassCreateModel, RecurringClassModel 
} from 'src/app/models/recurring-schedule.model';

@Injectable({
  providedIn: 'root'
})
export class RecurringScheduleService {

  constructor(
    private http: HttpClient,
    private authService: AuthService,
  ) { }

  deleteRecurringClass(
    id: number
  ): Observable<DeletionResponse> {
    let token = this.authService.getAuthToken();
    return this.http.delete<DeletionResponse>(
      `${environment.apiUrl}/api/recurring/recurring-class/${id}/`,
      {
        headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
      })
    }

  fetchRecurringClasses(): Observable<RecurringClassModel[]> {
    let token = this.authService.getAuthToken();
    return this.http.get<RecurringClassModel[]>(
      `${environment.apiUrl}/api/recurring/schedule/by-teacher/`,
      {
        headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
      });
  }

  submitRecurringClass(
    submissionForm: RecurringClassCreateModel
  ): Observable<RecurringClassModel> {
    let token = this.authService.getAuthToken();
    return this.http.post<RecurringClassModel>(
      `${environment.apiUrl}/api/recurring/recurring-class/`, submissionForm,
      {
        headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
      });
  }
 
}
