import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from 'src/environments/environment';
import { AuthService } from 'src/app/authentication/auth.service';
import { 
  FreelanceTuitionTransactionModel, FreelanceTuitionTransactionRecordModel, 
  PurchasedHoursModificationRecordModel, SchoolAccountingReportModel, 
  SchoolsAndFreelanceStudentsAccountingReportModel 
} from 'src/app/models/accounting.model';

@Injectable({
  providedIn: 'root'
})
export class AccountingService {

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) { }

  fetchFreelancePaymentsByMonthAndYear(month: number, year: number) {
    let token = this.authService.getAuthToken();
    return this.http.get<FreelanceTuitionTransactionRecordModel[]>(
      `${environment.apiUrl}/api/accounting/received-tuition-transactions-by-month-year/${month}/${year}/`,
        {
          headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
        })
  }

  fetchPurchasedHoursModificationRecordsByMonthAndYear(
    month: number, year: number, account_id: number
  ) {
    let token = this.authService.getAuthToken();
    return this.http.get<PurchasedHoursModificationRecordModel[]>(
      `${environment.apiUrl}/api/accounting/purchased-hours-modifications/by-month-and-account/${month}/${year}/${account_id}/`,
        {
          headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
        })
  }

  fetchSchoolAccountingReportByMonthAndYear(
    month: number, year: number, school_id: number
  ) {
    let token = this.authService.getAuthToken();
    return this.http.get<SchoolAccountingReportModel>(
      `${environment.apiUrl}/api/accounting/estimated-school-earnings-by-month-year/${month}/${year}/${school_id}/`,
        {
          headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
        })
  }

  fetchSchoolAccountingReportWithinDateRange(
    start_date: string, finish_date: string, school_id: number
  ) {
    let token = this.authService.getAuthToken();
    return this.http.get<SchoolAccountingReportModel>(
      `${environment.apiUrl}/api/accounting/estimated-school-earnings-within-date-range/${start_date}/${finish_date}/${school_id}/`,
        {
          headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
        })
  }

  fetchSchoolsAndFreelanceStudentsAccountingReportByMonthAndYear(
    month: number, year: number
  ) {
    let token = this.authService.getAuthToken();
    return this.http.get<SchoolsAndFreelanceStudentsAccountingReportModel>(
      `${environment.apiUrl}/api/accounting/estimated-earnings-by-month-year/${month}/${year}/`,
        {
          headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
        })
  }

  submitFreelanceTuitionTransaction(
    submissionForm: FreelanceTuitionTransactionModel
  ): Observable<FreelanceTuitionTransactionRecordModel> {
    let token = this.authService.getAuthToken();
    return this.http.post<FreelanceTuitionTransactionRecordModel>(
      `${environment.apiUrl}/api/accounting/tuition-transactions/`, submissionForm,
      {
        headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
      });
  }

}
