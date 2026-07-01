import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { single } from 'rxjs';

import { GroupClassAttendanceBulkUpdateResponseModel, GroupClassMeetingRecordModel } from 'src/app/models/client-group-class-attendance.model';
import { GroupClassAttendanceService } from '../../service/group-class-attendance.service';


@Component({
  selector: 'app-group-class-attendance-detail',
  standalone: false,
  templateUrl: './group-class-attendance-detail.component.html',
  styleUrl: './group-class-attendance-detail.component.css'
})
export class GroupClassAttendanceDetailComponent implements OnInit {

  errorMessage: string | undefined = undefined;
  fetchingRecordInProgress: boolean = true;
  formVisible: boolean = false;
  groupClassMeetingRecord: GroupClassMeetingRecordModel | undefined = undefined;
  hoursModificationsMessages: string[] | undefined;
  scheduledClassIdFromRoute: number;
  successMessage: string | undefined = undefined;
  submittingInProgress: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private groupClassAttendanceService: GroupClassAttendanceService
  ) { }

  ngOnInit(): void {
    this.scheduledClassIdFromRoute = +this.route.snapshot.params['scheduled_class_id'];
    this.groupClassAttendanceService.fetchGroupClassMeetingRecordModelByClassID(
      this.scheduledClassIdFromRoute
    ).pipe(single()
    ).subscribe({
      next: (res) => {
        this.groupClassMeetingRecord = res;
        this.fetchingRecordInProgress = false;
      },
      error: (err) => {
        this.errorMessage = 'There was an error fetching the attendance record.';
        this.fetchingRecordInProgress = false;
        if (err.error?.detail) {
          this.errorMessage = err.error.detail;
        }
      }
    });
  }

  toggleForm() {
    this.formVisible = !this.formVisible;
  }

  closeFormHandler($event: boolean) {
    this.formVisible = $event;
  }

  onClearErrorMessage() {
    this.errorMessage = undefined;
  }

  onClearSuccessMessage() {
    this.successMessage = undefined;
    this.hoursModificationsMessages = undefined;
  }

  onSubmitSuccess($event: GroupClassAttendanceBulkUpdateResponseModel) {
    if (this.groupClassMeetingRecord) {
      this.groupClassMeetingRecord = {
        ...this.groupClassMeetingRecord,
        student_attendance_records: $event.updated_records
      };
    }
    this.successMessage = 'Attendance records updated successfully.';
    this.hoursModificationsMessages = $event.hours_modification_messages;
    this.formVisible = false;
  }

  onSubmitError($event: string) {
    this.errorMessage = $event;
  }

  get attendanceByStatus(): { label: string, names: string }[] {
    if (!this.groupClassMeetingRecord) return [];

    const statusLabels: { [key: string]: string } = {
      'scheduled': 'Pending',
      'completed': 'Completed',
      'cancelled': 'Cancelled',
      'same_day_cancellation': 'Same Day Cancellation'
    };

    const groups: { [key: string]: string[] } = {};

    for (const record of this.groupClassMeetingRecord.student_attendance_records) {
      const status = record.attendance_status;
      if (!groups[status]) {
        groups[status] = [];
      }
      groups[status].push(record.student_name);
    }

    return Object.keys(groups).map(status => ({
      label: statusLabels[status] || status,
      names: groups[status].join(', ')
    }));
  }

}
