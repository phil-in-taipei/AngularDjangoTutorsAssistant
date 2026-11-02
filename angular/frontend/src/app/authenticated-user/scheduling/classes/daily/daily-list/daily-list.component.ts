import { Component, DestroyRef, OnInit, inject } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable, map, of } from 'rxjs';
import { select, Store } from '@ngrx/store';

import { 
  deletionModeForScheduledClassesActivated 
} from '../../../classes-state/scheduled-classes.selectors';
import { ScheduledClassesState } from '../../../classes-state/scheduled-classes.reducers';
import { ScheduledClassModel } from 'src/app/models/scheduled-class.model';
import { 
  DailyClassesRequested, 
  ScheduledClassDeletionModeActivated, 
  ScheduledClassDeletionModeDeactivated 
} from '../../../classes-state/scheduled-classes.actions';
import { getDateString, monthsAndIntegers } from 'src/app/shared-utils/date-time.util';
import { 
  selectScheduledClassesByDate, fetchingClassesInProgress 
} from '../../../classes-state/scheduled-classes.selectors';

@Component({
  selector: 'app-daily-list',
  standalone: false,
  templateUrl: './daily-list.component.html',
  styleUrl: './daily-list.component.css'
})
export class DailyListComponent implements OnInit {

  dateFromRouteData: string;
  dailyScheduledClasses$: Observable<ScheduledClassModel[] | undefined>;
  deletionModeForScheduledClassesActivated$: Observable<boolean> = of(false);
  fetchingClasses$: Observable<boolean> = of(false);
  readonly monthsAndIntegers = monthsAndIntegers;
  tmrwRouterStr: string;
  ystrdyRouterStr: string;

  private destroyRef = inject(DestroyRef);

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private store: Store<ScheduledClassesState>
  ) { }

  ngOnInit(): void {
    this.deletionModeForScheduledClassesActivated$ = this.store.pipe(
      select(deletionModeForScheduledClassesActivated)
    );
    this.fetchingClasses$ = this.store.pipe(
      select(fetchingClassesInProgress)
    );
  
    // Runs once on init and again every time the :date param changes,
    // whether from the prev/next buttons, the navbar search, or the browser's back button.
    this.route.paramMap
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe(params => {
        this.dateFromRouteData = params.get('date')!;
        this.tmrwRouterStr = this.getTmrwRouterStr(this.dateFromRouteData);
        this.ystrdyRouterStr = this.getYstrdyRouterStr(this.dateFromRouteData);
        this.dailyScheduledClasses$ = this.buildDailyClasses$(this.dateFromRouteData);
      });
  }

  private buildDailyClasses$(date: string): Observable<ScheduledClassModel[] | undefined> {
    return this.store.pipe(
      select(selectScheduledClassesByDate(date)))
      .pipe(map((scheduledClasses: ScheduledClassModel[] | undefined) => {
        if (scheduledClasses !== undefined) {
          if (!scheduledClasses.length) {
            this.store.dispatch(new DailyClassesRequested({ date }));
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
    this.router.navigate(['/', 'authenticated-user', 'scheduling', 'schedule-daily',  this.tmrwRouterStr]);
  }

  navToYsdtrdy() {
    this.router.navigate(['/', 'authenticated-user', 'scheduling', 'schedule-daily',  this.ystrdyRouterStr]);
  }

  onActivateScheduledClassDeletionMode(): void {
    this.store.dispatch(
      new ScheduledClassDeletionModeActivated()
    );
  }

  onDeactivateScheduledClassDeletionMode(): void {
    this.store.dispatch(
      new ScheduledClassDeletionModeDeactivated()
    );
  }

  trackByFn(index: number, item: any) {
    return item.id;
  }

}
