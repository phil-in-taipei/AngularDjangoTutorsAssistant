import { Component, OnInit } from '@angular/core';
import { first, map, Observable, of } from 'rxjs';
import { select, Store } from '@ngrx/store';

import { ActivatedRoute } from '@angular/router';

import { AttendanceService } from '../service/attendance.service';
import { ScheduledClassModel } from 'src/app/models/scheduled-class.model';
import { 
  selectStudentOrClassById 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.selectors';
import { 
  StudentOrClassAttendanceRecordResponse 
} from 'src/app/models/scheduled-class.model';
import { StudentOrClassModel } from 'src/app/models/student-or-class.model';
import { 
  StudentsOrClassesState 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.reducers';


@Component({
  selector: 'app-attendance-record',
  standalone: false,
  templateUrl: './attendance-record.component.html',
  styleUrl: './attendance-record.component.css'
})
export class AttendanceRecordComponent {

  idFromRouteData: number;
  studentOrClass$: Observable<StudentOrClassModel | undefined> = of(undefined);
  pastClasses$: Observable<ScheduledClassModel[] | undefined>
  pageNum: number = 1;

  constructor(
    private route: ActivatedRoute,
    private attendanceService: AttendanceService,
    private store: Store<StudentsOrClassesState>
  ) { }

  ngOnInit(): void {
    this.idFromRouteData = +this.route.snapshot.params['student_or_class_id'];
    this.studentOrClass$ = this.store.pipe(
      select(selectStudentOrClassById(this.idFromRouteData))
    );
    this.pastClasses$ = this.attendanceService.fetchPastClassesByStudentOrClass(
      this.idFromRouteData, this.pageNum
    );
  }

  onNextPagRequest() {
    this.pageNum += 1;
    this.pastClasses$ = this.attendanceService.fetchPastClassesByStudentOrClass(
      this.idFromRouteData, this.pageNum
    );
  }

  onPrevPageRequest() {
    if (this.pageNum > 1) {
      this.pageNum -= 1;
      this.pastClasses$ = this.attendanceService.fetchPastClassesByStudentOrClass(
        this.idFromRouteData, this.pageNum
      );
    }
  }

}
