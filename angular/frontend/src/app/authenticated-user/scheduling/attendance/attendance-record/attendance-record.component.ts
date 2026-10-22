import { Component, OnInit } from '@angular/core';
import { 
  first, map, Observable, of, catchError, startWith 
} from 'rxjs';
import { select, Store } from '@ngrx/store';

import { ActivatedRoute } from '@angular/router';

import { AttendanceService } from '../service/attendance.service';
import { 
  StudentOrClassAttendancePageState 
} from 'src/app/models/scheduled-class.model'; //ScheduledClassModel, 
import { 
  selectStudentOrClassById 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.selectors';
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
  //pastClasses$: Observable<ScheduledClassModel[] | undefined>
  pageState$: Observable<StudentOrClassAttendancePageState>;
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
    //this.pastClasses$ = this.attendanceService.fetchPastClassesByStudentOrClass(
    //  this.idFromRouteData, this.pageNum
    //);
    this.loadPage();
  }

  private loadPage(): void {
    this.pageState$ = this.attendanceService
      .fetchPastClassesByStudentOrClass(this.idFromRouteData, this.pageNum)
      .pipe(
        map(classes => ({ loading: false, classes })),
        // Django REST pagination returns 404 for pages past the end
        catchError(() => of({ loading: false, classes: [] })),
        startWith({ loading: true, classes: [] })
      );
  }

  onNextPagRequest() {
    this.pageNum += 1;
    //this.pastClasses$ = this.attendanceService.fetchPastClassesByStudentOrClass(
    //  this.idFromRouteData, this.pageNum
    //);
    this.loadPage();
  }

  onPrevPageRequest() {
    if (this.pageNum > 1) {
      this.pageNum -= 1;
      //this.pastClasses$ = this.attendanceService.fetchPastClassesByStudentOrClass(
      //  this.idFromRouteData, this.pageNum
      //);
      this.loadPage();
    }
  }

}
