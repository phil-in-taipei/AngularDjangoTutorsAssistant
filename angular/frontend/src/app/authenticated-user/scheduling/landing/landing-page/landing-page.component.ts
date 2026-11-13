import { Component, OnInit, ViewChild } from '@angular/core';
import {select, Store} from '@ngrx/store';
import { Router } from "@angular/router";
import { Observable } from "rxjs";
import { NgbDateStruct, NgbInputDatepicker } from '@ng-bootstrap/ng-bootstrap';

import { 
  getDateString, getDayOfWeekRouterStr, monthsAndIntegers 
} from 'src/app/shared-utils/date-time.util';
import { 
  LandingPageScheduleRequested, UnconfirmedScheduledClassesRequested
} from '../../classes-state/scheduled-classes.actions';
import { ScheduledClassModel } from 'src/app/models/scheduled-class.model';
import { ScheduledClassesState } from '../../classes-state/scheduled-classes.reducers';
import { 
  selectScheduledClassesByDate, selectUnconfirmedPastScheduledClasses
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

  //dateModel = {year: 0, month: 0, day: 0};
  searchMode = false;
  dateModel: NgbDateStruct | null = this.todayStruct();

  @ViewChild('dSmall') datepicker?: NgbInputDatepicker;

  readonly monthsAndIntegers = monthsAndIntegers;
  todaysClasses$: Observable<ScheduledClassModel[] | undefined>;
  dayOfWeekString: string;
  todayDateStr: string;
  unconfirmedPastClasses$: Observable<ScheduledClassModel[] | undefined>;
  userProfile$: Observable<UserProfileModel | undefined>;

  constructor(
    private router: Router,
    private store: Store<ScheduledClassesState>
  ) {}

  ngOnInit(): void {
    this.store.dispatch(new LandingPageScheduleRequested());
    this.store.dispatch(new UnconfirmedScheduledClassesRequested());
    //let dateTimeObj = new Date();
    //this.dateModel.year = dateTimeObj.getUTCFullYear();
    //this.dateModel.month = dateTimeObj.getUTCMonth() + 1;
    //this.dateModel.day = dateTimeObj.getUTCDate();
    const today = this.todayStruct();
    this.todayDateStr = getDateString(today.day, today.month, today.year);
    this.dayOfWeekString = getDayOfWeekRouterStr(this.todayDateStr);

    this.todaysClasses$ = this.store.pipe(
      select(selectScheduledClassesByDate(this.todayDateStr)));
    this.unconfirmedPastClasses$ = this.store.pipe(
      select(selectUnconfirmedPastScheduledClasses(this.todayDateStr)));
    this.userProfile$ = this.store.pipe(select(selectUserProfile));
  }

  private todayStruct(): NgbDateStruct {
    const now = new Date();
    return {
      year: now.getFullYear(),
      month: now.getMonth() + 1,
      day: now.getDate()
    };
  }

  //getTodayDateString(): string {
  //  const dateString = getDateString(
  //    this.dateModel.day,
  //    this.dateModel.month,
  //    this.dateModel.year
  //  );
  //  return dateString;
  //}
  onSearchClick(): void {
    if (!this.searchMode) {
      this.searchMode = true;
      this.dateModel = this.todayStruct();
      // wait for *ngIf to render the input, then open the calendar
      setTimeout(() => this.datepicker?.open());
      return;
    }
    this.navToSelectedDateWithToggle();
  }

  navToSelectedDateWithToggle(): void {
    if (!this.dateModel) { return; }
    const dateString = getDateString(
      this.dateModel.day,
      this.dateModel.month,
      this.dateModel.year
    );
    this.router.navigate(
      ['authenticated-user', 'scheduling', 'schedule-daily', dateString]
    );
    this.exitSearchMode();
  }

  navToSelectedDate(): void {
    let dateString = this.todayDateStr
    if (this.dateModel) {
      dateString = getDateString(
        this.dateModel.day,
        this.dateModel.month,
        this.dateModel.year
      );
    }
    this.router.navigate(
      ['authenticated-user', 'scheduling', 'schedule-daily',  dateString]
    );
  }

  // Used by the "View Today's Schedule" button
  navToToday(): void {
    this.router.navigate(
      ['authenticated-user', 'scheduling', 'schedule-daily', this.todayDateStr]
    );
  }

  exitSearchMode(): void {
    this.datepicker?.close();
    this.searchMode = false;
  }

  trackByFn(index: number, item: any) {
    return item.id;
  }
}
