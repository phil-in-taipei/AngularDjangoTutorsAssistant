import { Component, OnInit } from '@angular/core';
import { Observable, of } from "rxjs";
import {select, Store } from '@ngrx/store';

import { ScheduledClassesState } from '../../../classes-state/scheduled-classes.reducers';
import { 
  selectAllScheduledClasses, selectMonthlyDateRange, fetchingClassesInProgress 
} from '../../../classes-state/scheduled-classes.selectors';
import { ScheduledClassModel } from 'src/app/models/scheduled-class.model';

@Component({
  selector: 'app-monthly-view',
  standalone: false,
  templateUrl: './monthly-view.component.html',
  styleUrl: './monthly-view.component.css'
})
export class MonthlyViewComponent implements OnInit {

  scheduledClasses$: Observable<ScheduledClassModel[] | undefined> = of(undefined);
  classesLoaded$: Observable<boolean> = of(false);
  monthlyDateRange$: Observable<[string, string] | undefined> = of(undefined);
  showMonthlySelectForm: Boolean = true;

  constructor(
    private scheduledClassesStore: Store<ScheduledClassesState>,
  ) { }

  ngOnInit(): void {
    this.scheduledClasses$ = this.scheduledClassesStore.pipe(
      select(selectAllScheduledClasses)
    );
    this.monthlyDateRange$ = this.scheduledClassesStore.pipe(
      select(selectMonthlyDateRange)
    );
    this.classesLoaded$ = this.scheduledClassesStore.pipe(
      select(fetchingClassesInProgress)
    );
  }

  closeMonthlySelectFormHander($event: boolean) {
    this.showMonthlySelectForm = $event;
  }

  toggleMonthlySelectForm() {
    if (this.showMonthlySelectForm) {
      this.showMonthlySelectForm = false;
    } else {
      this.showMonthlySelectForm = true;
    }
  }

}
