import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable, of } from 'rxjs';
import { Router } from '@angular/router';
import { select, Store } from '@ngrx/store';
import { NgbDateStruct } from '@ng-bootstrap/ng-bootstrap';

import { getDateString } from 'src/app/shared-utils/date-time.util';
import { ScheduledClassModel } from 'src/app/models/scheduled-class.model';
import { ScheduledClassesState } from '../../../classes-state/scheduled-classes.reducers';
import { StudentOrClassModel } from 'src/app/models/student-or-class.model';
import { 
  selectStudentOrClassById 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.selectors';
import { 
  StudentsOrClassesState 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.reducers';
import { 
  FutureSOCClassesRequested,
  ScheduledClassDeletionModeActivated, 
  ScheduledClassDeletionModeDeactivated 
} from '../../../classes-state/scheduled-classes.actions';
import { 
  deletionModeForScheduledClassesActivated,
  fetchingFutureClassesInProgress,
  selectFutureScheduledClassesForStudentOrClass 
} from '../../../classes-state/scheduled-classes.selectors';


@Component({
  selector: 'app-upcoming-classes-by-student',
  standalone: false,
  templateUrl: './upcoming-classes-by-student.component.html',
  styleUrl: './upcoming-classes-by-student.component.css'
})
export class UpcomingClassesByStudentComponent implements OnInit {

  deletionModeForScheduledClassesActivated$: Observable<boolean> = of(false);
  fetchingClasses$: Observable<boolean> = of(false);
  studentOrClassIdFromRoute: string;
  studentOrClass$: Observable<StudentOrClassModel | undefined> = of(undefined);
  todayDateStr: string;
  upcomingScheduledClasses$: Observable<ScheduledClassModel[] | undefined>;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private scheduledClassesStore: Store<ScheduledClassesState>,
    private studentsOrClassesStore: Store<StudentsOrClassesState>
  ) { }


  ngOnInit(): void {
    this.deletionModeForScheduledClassesActivated$ = this.studentsOrClassesStore.pipe(
      select(deletionModeForScheduledClassesActivated)
    );
    this.studentOrClassIdFromRoute = this.route.snapshot.params['student_or_class_id'];
    this.fetchingClasses$ = this.studentsOrClassesStore.pipe(
      select(fetchingFutureClassesInProgress)
    );
    this.studentOrClass$ = this.studentsOrClassesStore.pipe(
      select(selectStudentOrClassById(+this.studentOrClassIdFromRoute))
    );
    const today = this.todayStruct();
    this.todayDateStr = getDateString(today.day, today.month, today.year);

    this.scheduledClassesStore.dispatch(new FutureSOCClassesRequested({
      id: +this.studentOrClassIdFromRoute
    }));

    this.upcomingScheduledClasses$ = this.scheduledClassesStore.pipe(
      select(selectFutureScheduledClassesForStudentOrClass(
        this.todayDateStr,
        +this.studentOrClassIdFromRoute
      ))
    );
    
  }

  navToPastClasses(student_or_class_id: number): void {
    this.router.navigate(
      ['authenticated-user', 'scheduling', 'attendance', student_or_class_id]
    );
  }

  onActivateScheduledClassDeletionMode(): void {
    this.scheduledClassesStore.dispatch(
      new ScheduledClassDeletionModeActivated()
    );
  }

  onDeactivateScheduledClassDeletionMode(): void {
    this.scheduledClassesStore.dispatch(
      new ScheduledClassDeletionModeDeactivated()
    );
  }

  private todayStruct(): NgbDateStruct {
    const now = new Date();
    return {
      year: now.getFullYear(),
      month: now.getMonth() + 1,
      day: now.getDate()
    };
  }

  trackByFn(index: number, item: any) {
    return item.id;
  }

}
