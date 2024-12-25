import { Component, OnInit } from '@angular/core';
import {select, Store} from '@ngrx/store';
import { Router } from "@angular/router";
import { Observable } from "rxjs";

import { AppState } from 'src/app/reducers';
import { getDateString } from 'src/app/shared-utils/date-time.util';
import { 
  LandingPageScheduleRequested 
} from '../../classes-state/scheduled-classes.actions';
import { ScheduledClassModel } from 'src/app/models/scheduled-class.model';
import { 
  selectScheduledClassesByDate 
} from '../../classes-state/scheduled-classes.selectors';
import { 
  selectUserProfile 
} from 'src/app/authenticated-user/user/user-state/user.selectors';
import { UserProfileModel } from 'src/app/models/user-profile.model';


@Component({
  selector: 'app-landing-page',
  standalone: false,
  templateUrl: './landing-page.component.html',
  styleUrl: './landing-page.component.css'
})
export class LandingPageComponent implements OnInit {

  dateModel = {year: 0, month: 0, day: 0};
  todaysClasses$: Observable<ScheduledClassModel[] | undefined>;
  userProfile$: Observable<UserProfileModel | undefined>;

  constructor(
    private router: Router,
    private store: Store<AppState>
  ) {}

  ngOnInit(): void {
    console.log('*****landing page initializing*****')
    this.store.dispatch(new LandingPageScheduleRequested());
    let dateTimeObj = new Date();
    this.dateModel.year = dateTimeObj.getUTCFullYear();
    this.dateModel.month = dateTimeObj.getUTCMonth() + 1;
    this.dateModel.day = dateTimeObj.getUTCDate();
    let todayDateStr = this.getTodayDateString();
    this.todaysClasses$ = this.store.pipe(
      select(selectScheduledClassesByDate(todayDateStr)));
    this.userProfile$ = this.store.pipe(select(selectUserProfile));
  }

  getTodayDateString(): string {
    const dateString = getDateString(
      this.dateModel.day,
      this.dateModel.month,
      this.dateModel.year
    );
    return dateString;
  }

  navToSelectedDate(): void {
    let dateString = getDateString(
      this.dateModel.day,
      this.dateModel.month,
      this.dateModel.year
    );
    this.router.navigate(
      ['/', 'authenticated-user', 'scheduling', 'schedule-daily',  dateString]
    );
  }

}
