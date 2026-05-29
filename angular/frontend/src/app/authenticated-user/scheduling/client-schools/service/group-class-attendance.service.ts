import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from 'src/environments/environment';
import { AuthService } from 'src/app/authentication/auth.service';
import { 
  GroupClassAttendanceSubmitModel, 
  GroupClassAttendanceBulkUpdateResponseModel,
  GroupClassMeetingRecordModel,
  GroupClassStudentAttendanceRecordModel, 
} from 'src/app/models/client-group-class-attendance.model';


@Injectable({
  providedIn: 'root'
})
export class GroupClassAttendanceService {

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) { }


  fetchGroupClassMeetingRecordModelByClassID(scheduled_class_id: number) {
    let token = this.authService.getAuthToken();
    return this.http.get<GroupClassMeetingRecordModel[]>(
      `${environment.apiUrl}/api/client-school-group-attendance/group-class-meeting-record/${scheduled_class_id}/`,
        {
          headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
        })
  }

  
  bulkUpdateGroupClassAttendanceRecords(
    attendanceSubmitData: GroupClassAttendanceSubmitModel
  ): Observable<GroupClassAttendanceBulkUpdateResponseModel> {
    let token = this.authService.getAuthToken();
    return this.http.patch<GroupClassAttendanceBulkUpdateResponseModel>(
      `${environment.apiUrl}/api/client-school-group-attendance/group-class-attendance-bulk-update/`,
      attendanceSubmitData,
      {
        headers: new HttpHeaders({ 'Authorization': `Token ${token}` })
      }
    )
  }

}
