import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable, map, of } from 'rxjs';
import { select, Store } from '@ngrx/store';

import { ScheduledClassesState } from '../../../classes-state/scheduled-classes.reducers';
import { ScheduledClassModel } from 'src/app/models/scheduled-class.model';
import { DailyClassesRequested } from '../../../classes-state/scheduled-classes.actions';
import { getDateString } from 'src/app/shared-utils/date-time.util';
import { 
  selectScheduledClassesByDate, fetchingClassesInProgress 
} from '../../../classes-state/scheduled-classes.selectors';

@Component({
  selector: 'app-daily-list',
  standalone: false,
  templateUrl: './daily-list.component.html',
  styleUrl: './daily-list.component.css'
})
export class DailyListComponent implements OnInit{

  dateFromRouteData: string;
  dailyScheduledClasses$: Observable<ScheduledClassModel[] | undefined>;
  fetchingClasses$: Observable<boolean> = of(false);
  tmrwRouterStr: string;
  ystrdyRouterStr: string;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private store: Store<ScheduledClassesState>
  ) { }

  ngOnInit(): void {
    this.dateFromRouteData = this.route.snapshot.params['date'];
    this.tmrwRouterStr = this.getTmrwRouterStr(this.dateFromRouteData);
    this.ystrdyRouterStr = this.getYstrdyRouterStr(this.dateFromRouteData);
    this.fetchingClasses$ = this.store.pipe(
      select(fetchingClassesInProgress)
    );
  
    this.dailyScheduledClasses$ = this.store.pipe(
      select(selectScheduledClassesByDate(this.dateFromRouteData)))
      .pipe(map((scheduledClasses: ScheduledClassModel[] | undefined) => {
        if (scheduledClasses !== undefined) {
          if (!scheduledClasses.length) {
            this.store.dispatch(new DailyClassesRequested(
              {date: this.dateFromRouteData }
            ));
          }
        }
        return scheduledClasses;
      }));
  }

  getTmrwRouterStr(dateFromRouteData: string) {
    let date = new Date(dateFromRouteData);
    let tomorrow = new Date(date);
    tomorrow.setDate(tomorrow.getDate() + 1);
    let dateTimeObj = tomorrow;
    return getDateString(
      dateTimeObj.getUTCDate(),
      dateTimeObj.getUTCMonth() + 1,
      dateTimeObj.getUTCFullYear()
    );
  }

  getYstrdyRouterStr(dateFromRouteData: string) {
    let date = new Date(dateFromRouteData);
    let yesterday = new Date(date);
    yesterday.setDate(yesterday.getDate() - 1);
    let dateTimeObj = yesterday;
    return getDateString(
      dateTimeObj.getUTCDate(),
      dateTimeObj.getUTCMonth() + 1,
      dateTimeObj.getUTCFullYear()
    );
  }


  navToTmrrow() {
    console.log(this.tmrwRouterStr);
    this.router.navigate(['/', 'authenticated-user', 'scheduling', 'schedule-daily',  this.tmrwRouterStr]);
    this.dateFromRouteData = this.tmrwRouterStr;
    this.tmrwRouterStr = this.getTmrwRouterStr(this.dateFromRouteData);
    this.ystrdyRouterStr = this.getYstrdyRouterStr(this.dateFromRouteData);
    this.dailyScheduledClasses$ = this.store.pipe(
      select(selectScheduledClassesByDate(this.dateFromRouteData)))
      .pipe(map((scheduledClasses: ScheduledClassModel[] | undefined) => {
        if (scheduledClasses !== undefined) {
          if (!scheduledClasses.length) {
            this.store.dispatch(new DailyClassesRequested(
              {date: this.dateFromRouteData }
            ));
          }
        }
        return scheduledClasses;
      }));
  }

  navToYsdtrdy() {
    console.log(this.ystrdyRouterStr); 
    this.router.navigate(['/', 'authenticated-user', 'scheduling', 'schedule-daily',  this.ystrdyRouterStr]);
    this.dateFromRouteData = this.ystrdyRouterStr;
    this.tmrwRouterStr = this.getTmrwRouterStr(this.dateFromRouteData);
    this.ystrdyRouterStr = this.getYstrdyRouterStr(this.dateFromRouteData);
    this.dailyScheduledClasses$ = this.store.pipe(
      select(selectScheduledClassesByDate(this.dateFromRouteData)))
      .pipe(map((scheduledClasses: ScheduledClassModel[] | undefined) => {
        if (scheduledClasses !== undefined) {
          if (!scheduledClasses.length) {
            this.store.dispatch(new DailyClassesRequested(
              {date: this.dateFromRouteData }
            ));
          }
        }
        return scheduledClasses;
      }));
  }

  trackByFn(index: number, item: any) {
    return item.id;
  }

}
