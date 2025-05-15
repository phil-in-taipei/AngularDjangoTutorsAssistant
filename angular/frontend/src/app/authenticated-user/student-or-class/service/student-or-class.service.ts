import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

import { AuthService } from 'src/app/authentication/auth.service';
import { DeletionResponse } from 'src/app/models/deletion-response';
import { environment } from 'src/environments/environment';
import { 
  StudentOrClassCreateAndEditModel, StudentOrClassEditModel, 
  StudentOrClassModel, 
  StudentOrClassConfirmationModificationResponse 
} from 'src/app/models/student-or-class.model';

@Injectable({
  providedIn: 'root'
})
export class StudentOrClassService {

  constructor(
    private http: HttpClient,
    private authService: AuthService,
  ) { }

  deleteStudentOrClass(
    id: number
  ): Observable<DeletionResponse> {
    let token = this.authService.getAuthToken();
    return this.http.delete<DeletionResponse>(
      `${environment.apiUrl}/api/accounts/student-or-class/${id}/`,
        {
          headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
        })
  }

  editStudentOrClass(
    id: number,
    submissionForm: StudentOrClassEditModel
  ): Observable<StudentOrClassModel> {
    let token = this.authService.getAuthToken();
    return this.http.patch<StudentOrClassModel>(
      `${environment.apiUrl}/api/accounts/student-or-class/${id}/`, submissionForm,
        {
          headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
        });
  }

  fetchUsersStudentsOrClasses(): Observable<StudentOrClassModel[]> {
    let token = this.authService.getAuthToken();
    return this.http.get<StudentOrClassModel[]>(
      `${environment.apiUrl}/api/accounts/students-or-classes/`,
        {
          headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
        })
  }

  submitStudentOrClass(
    submissionForm: StudentOrClassCreateAndEditModel
    ): Observable<StudentOrClassModel> {
    let token = this.authService.getAuthToken();
    return this.http.post<StudentOrClassModel>(
      `${environment.apiUrl}/api/accounts/students-or-classes/`, submissionForm,
      {
        headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
      });
  }
  
}
