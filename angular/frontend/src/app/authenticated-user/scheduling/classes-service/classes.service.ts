import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from 'src/environments/environment';
import { AuthService } from 'src/app/authentication/auth.service';
import { DeletionResponse } from 'src/app/models/deletion-response';
import { getDateString } from 'src/app/shared-utils/date-time.util';
import { 
  CreateScheduledClassModel, 
  ModifyClassStatusModel,
  ModifyClassStatusResponse,
  RescheduleClassModel,
  ScheduledClassModel 
} from 'src/app/models/scheduled-class.model';


@Injectable({
  providedIn: 'root'
})
export class ClassesService {

  constructor(
    private http: HttpClient,
    private authService: AuthService,
  ) { }

  deleteSingleClass(id: number): Observable<DeletionResponse> {
    let token = this.authService.getAuthToken();
    return this.http.delete<DeletionResponse>(
      `${environment.apiUrl}/api/scheduling/class/submit/${id}/`,
        {
          headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
        })
  }

  fetchClassesByMonth(month: number, year: number) {
    let token = this.authService.getAuthToken();
    return this.http.get<ScheduledClassModel[]>(
      `${environment.apiUrl}/api/scheduling/classes/by-teacher/by-month-year/${month}/${year}/`,
        {
          headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
        })
  }

  fetchScheduledClassesByDate(date: string): Observable<ScheduledClassModel[]> {
    let token = this.authService.getAuthToken();
    return this.http.get<ScheduledClassModel[]>(
      `${environment.apiUrl}/api/scheduling/classes/by-teacher/by-date/${date}/`,
        {
          headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
        })
  }

  fetchTodaysClasses(): Observable<ScheduledClassModel[]> {
    let dateTimeObj = new Date();
    const date = getDateString(
      dateTimeObj.getUTCDate(),
      dateTimeObj.getUTCMonth() + 1,
      dateTimeObj.getUTCFullYear()
    );
    return this.fetchScheduledClassesByDate(date);
  }

  fetchUnconfirmedStatusClasses(): Observable<ScheduledClassModel[]> {
    let token = this.authService.getAuthToken();
    return this.http.get<ScheduledClassModel[]>(
      `${environment.apiUrl}/api/scheduling/classes/unconfirmed-status/`,
      {
        headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
      })
  }

  //note: possible issue with patch -> may have to change to post
  modifyClassStatus(submissionForm: ModifyClassStatusModel): 
    Observable<ModifyClassStatusResponse> {
    let token = this.authService.getAuthToken();
    return this.http.patch<ModifyClassStatusResponse>(
      `${environment.apiUrl}/api/scheduling/class-status-confirmation/`, submissionForm,
        {
          headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
        })
    }

  submitRescheduledClass(
    submissionForm: RescheduleClassModel
    ): Observable<ScheduledClassModel[]> {
    let token = this.authService.getAuthToken();
    return this.http.post<ScheduledClassModel[]>(
      `${environment.apiUrl}/api/scheduling/class/submit/${submissionForm.id}/`, submissionForm,
        {
          headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
        });
    }

  submitScheduledClass(
    submissionForm: CreateScheduledClassModel
    ): Observable<ScheduledClassModel[]> {
    let token = this.authService.getAuthToken();
    return this.http.post<ScheduledClassModel[]>(
      `${environment.apiUrl}/api/scheduling/class/submit/`, submissionForm,
      {
        headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
      });
  }

}
