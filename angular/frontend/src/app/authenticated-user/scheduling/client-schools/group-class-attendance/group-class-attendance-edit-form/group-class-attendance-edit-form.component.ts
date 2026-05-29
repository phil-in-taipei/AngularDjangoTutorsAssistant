import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { single } from 'rxjs';

import {
  GroupClassAttendanceBulkUpdateResponseModel,
  GroupClassAttendanceSubmitModel,
  GroupClassMeetingRecordModel,
  GroupClassStudentAttendanceRecordModel
} from 'src/app/models/client-group-class-attendance.model';
import { GroupClassAttendanceService } from '../../service/group-class-attendance.service';


@Component({
  selector: 'app-group-class-attendance-edit-form',
  standalone: false,
  templateUrl: './group-class-attendance-edit-form.component.html',
  styleUrl: './group-class-attendance-edit-form.component.css'
})
export class GroupClassAttendanceEditFormComponent implements OnInit  {

  @Input() meetingRecord: GroupClassMeetingRecordModel;
  @Output() closeEvent = new EventEmitter<boolean>();
  @Output() submitSuccessEvent = new EventEmitter<GroupClassAttendanceBulkUpdateResponseModel>();
  @Output() submitErrorEvent = new EventEmitter<string>();

  attendanceStatuses: string[] = ['completed', 'cancelled', 'same_day_cancellation'];
  editRecords: GroupClassStudentAttendanceRecordModel[] = [];
  submittingInProgress: boolean = false;

  constructor(private groupClassAttendanceService: GroupClassAttendanceService) { }

  ngOnInit(): void {
    this.editRecords = this.meetingRecord.student_attendance_records.map(
      record => ({ ...record })
    );
  }

  onStatusChange(index: number, value: string) {
    this.editRecords[index] = { ...this.editRecords[index], attendance_status: value };
  }

  getStatusValue(record: GroupClassStudentAttendanceRecordModel): string | null {
    return record.attendance_status === 'scheduled' ? null : record.attendance_status;
  }

  onSubmit(form: NgForm) {
    const allFilled = this.editRecords.every(
      record => record.attendance_status !== 'scheduled'
    );
    if (!allFilled) {
      this.submitErrorEvent.emit('Please select an attendance status for every student.');
      return;
    }
    const submitData: GroupClassAttendanceSubmitModel = {
      attendance_records: this.editRecords
    };
    this.submittingInProgress = true;
    this.groupClassAttendanceService.bulkUpdateGroupClassAttendanceRecords(
      submitData
    ).pipe(single()
    ).subscribe({
      next: (res) => {
        this.submittingInProgress = false;
        this.submitSuccessEvent.emit(res);
        this.closeEvent.emit(false);
      },
      error: (err) => {
        this.submittingInProgress = false;
        let errorMsg = 'There was an error updating the attendance records.';
        if (err.error?.error) {
          errorMsg = err.error.error;
        }
        this.submitErrorEvent.emit(errorMsg);
      }
    });
  }

}
