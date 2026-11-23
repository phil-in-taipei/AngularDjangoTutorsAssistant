import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable, map, of } from 'rxjs';
import { select, Store } from '@ngrx/store';
import { NgbDateStruct } from '@ng-bootstrap/ng-bootstrap';

import { getDateString } from 'src/app/shared-utils/date-time.util';
import { ScheduledClassModel } from 'src/app/models/scheduled-class.model';
import { ScheduledClassesState } from '../../../classes-state/scheduled-classes.reducers';
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
export class UpcomingClassesByStudentComponent {

  fetchingClasses$: Observable<boolean> = of(false);
  studentOrClassIdFromRouteDate: string;
  todayDateStr: string;
  upcomingScheduledClasses$: Observable<ScheduledClassModel[] | undefined>;

  constructor(
    private route: ActivatedRoute,
    private store: Store<ScheduledClassesState>
  ) { }


  ngOnInit(): void {
    this.studentOrClassIdFromRouteDate = this.route.snapshot.params['id'];
    const today = this.todayStruct();
    this.todayDateStr = getDateString(today.day, today.month, today.year);

    this.store.dispatch(new FutureSOCClassesRequested({
      id: +this.studentOrClassIdFromRouteDate
    }));

    this.upcomingScheduledClasses$ = this.store.pipe(
      select(selectFutureScheduledClassesForStudentOrClass(
        this.todayDateStr,
        +this.studentOrClassIdFromRouteDate
      ))
    );
    
  }



  //currentDate: string,
  //studentOrClassId: number

  private todayStruct(): NgbDateStruct {
    const now = new Date();
    return {
      year: now.getFullYear(),
      month: now.getMonth() + 1,
      day: now.getDate()
    };
  }

}
