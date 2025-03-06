import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

import { AuthService } from 'src/app/authentication/auth.service';
import { DeletionResponse } from 'src/app/models/deletion-response';
import { environment } from 'src/environments/environment';
import { 
  RecurringClassCreateModel, RecurringClassModel 
} from 'src/app/models/recurring-schedule.model';
import { 
  RecurringClassAppliedMonthlyCreateModel,
  RecurringClassAppliedMonthlyModel,
  RecurringClassAppliedMonthlyDeletionResponse 
} from 'src/app/models/recurring-schedule.model';

@Injectable({
  providedIn: 'root'
})
export class RecurringScheduleService {

  constructor(
    private http: HttpClient,
    private authService: AuthService,
  ) { }


  applyRecurringClassToMonthAndYear(
    submissionForm: RecurringClassAppliedMonthlyCreateModel
  ): Observable<RecurringClassAppliedMonthlyModel>  {
    let token = this.authService.getAuthToken();
    return this.http.post<RecurringClassAppliedMonthlyModel>(
      `${environment.apiUrl}/api/recurring/applied-monthly/`, submissionForm,
      {
        headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
      });
  }
    

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


  deleteRecurringClassAppliedMonthly(
    id: number
  ): Observable<RecurringClassAppliedMonthlyDeletionResponse> {
    let token = this.authService.getAuthToken();
    return this.http.delete<RecurringClassAppliedMonthlyDeletionResponse>(
      `${environment.apiUrl}/api/recurring/applied-monthly/${id}/`,
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


  fetchRecurringClassAppliedMonthlysByMonthAndYear(
    month: number, year: number
  ): Observable<RecurringClassAppliedMonthlyModel[]> {
    let token = this.authService.getAuthToken();
    return this.http.get<RecurringClassAppliedMonthlyModel[]>(
      `${environment.apiUrl}/api/recurring/monthly/recurring/by-teacher/${month}/${year}/`,
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
