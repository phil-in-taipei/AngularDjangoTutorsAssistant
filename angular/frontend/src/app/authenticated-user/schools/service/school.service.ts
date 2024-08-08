import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

import { AuthService } from 'src/app/authentication/auth.service';
import { DeletionResponse } from 'src/app/models/deletion-response';
import { environment } from 'src/environments/environment';
import { 
  SchoolCreateAndEditModel, SchoolModel 
} from 'src/app/models/school.model';


@Injectable({
  providedIn: 'root'
})
export class SchoolService {

  constructor(
    private http: HttpClient,
    private authService: AuthService,
  ) { }

  deleteSchool(
    id: number
  ): Observable<DeletionResponse> {
    let token = this.authService.getAuthToken();
    return this.http.delete<DeletionResponse>(
      `${environment.apiUrl}/api/schools/users-school/${id}/`,
        {
          headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
        })
  }

  editSchool(id: number,
    submissionForm: SchoolCreateAndEditModel
    ): Observable<SchoolModel> {
    let token = this.authService.getAuthToken();
    return this.http.patch<SchoolModel>(
      `${environment.apiUrl}/api/schools/users-school/${id}`, submissionForm,
      {
        headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
      });
  }

  fetchUsersSchools(): Observable<SchoolModel[]> {
    let token = this.authService.getAuthToken();
    return this.http.get<SchoolModel[]>(
      `${environment.apiUrl}/api/schools/users-schools/`,
        {
          headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
        })
  }

  submitSchool(
    submissionForm: SchoolCreateAndEditModel
    ): Observable<SchoolModel> {
    let token = this.authService.getAuthToken();
    return this.http.post<SchoolModel>(
      `${environment.apiUrl}/api/schools/users-schools/`, submissionForm,
      {
        headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
      });
  }

}
