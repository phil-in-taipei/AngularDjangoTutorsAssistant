import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { map,  } from 'rxjs';
import { environment } from 'src/environments/environment';
import { AuthService } from 'src/app/authentication/auth.service';

import { StudentOrClassAttendanceRecordResponse } from 'src/app/models/scheduled-class.model';

@Injectable({
  providedIn: 'root'
})
export class AttendanceService {

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) { }

  fetchPastClassesByStudentOrClass(
    student_or_class_id: number,
    pageNum: number
  ) {
    let token = this.authService.getAuthToken();
    return this.http.get<StudentOrClassAttendanceRecordResponse>(
    `${
      environment.apiUrl
    }/api/scheduling/classes/student-or-class-attendance/${
      student_or_class_id
    }/?page=${pageNum}`,
      {
        headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
      }).pipe(
        map(res =>
          Object.values(res['results'])
        )
    )
    }
}
