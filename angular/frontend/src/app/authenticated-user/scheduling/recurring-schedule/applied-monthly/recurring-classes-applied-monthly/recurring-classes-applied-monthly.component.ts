import { Component, OnInit } from '@angular/core';
import { Observable, of } from 'rxjs';
import { ActivatedRoute } from "@angular/router";
import { select, Store } from '@ngrx/store';

import { 
  monthsAndIntegers 
} from 'src/app/shared-utils/date-time.util';
import { RecurringClassAppliedMonthlyModel } from 'src/app/models/recurring-schedule.model';
import { 
  RecurringClassAppliedMonthlysCleared,
  RecurringClassAppliedMonthlysRequested, 
  RecurringClassesAppliedMonthlyMessagesCleared 
} from '../../state/recurring-classes-applied-monthly-state/recurring-class-applied-monthly.actions';
import { 
  RecurringClassAppliedMonthlysState 
} from '../../state/recurring-classes-applied-monthly-state/recurring-class-applied-monthly.reducers';
import { ScheduledClassBatchDeletionDataModel } from 'src/app/models/scheduled-class.model';
import { ScheduledClassesState } from '../../../classes-state/scheduled-classes.reducers';
import { 
  ScheduledClassesCleared, ScheduledClassesMessagesCleared 
} from '../../../classes-state/scheduled-classes.actions';
import { 
  scheduledClassesSuccessMsg, scheduledClassesErrorMsg 
} from '../../../classes-state/scheduled-classes.selectors';
import { 
  optionalScheduledClassBatchDeletionData,
  selectAllRecurringClassAppliedMonthlys, 
  selectRecurringClassAppliedMonthlysLoaded 
} from '../../state/recurring-classes-applied-monthly-state/recurring-class-applied-monthly.selectors';


@Component({
  selector: 'app-recurring-classes-applied-monthly',
  standalone: false,
  templateUrl: './recurring-classes-applied-monthly.component.html',
  styleUrl: './recurring-classes-applied-monthly.component.css'
})
export class RecurringClassesAppliedMonthlyComponent implements OnInit {

  rCAMs$: Observable<RecurringClassAppliedMonthlyModel[] | undefined> = of(undefined);
  rCAMsLoaded$: Observable<boolean> = of(false);
  monthFromRouteData:number;
  yearFromRouteData:number;
  batchDeletionData$: Observable<ScheduledClassBatchDeletionDataModel | undefined> = of(undefined);
  batchDeletionErrMsg$: Observable<string | undefined> = of(undefined);
  batchDeletionSuccessMsg$: Observable<string | undefined> = of(undefined);
  monthsAndIntegers: [string, number][] = monthsAndIntegers;
  showApplyRecurringClassSubmitForm:boolean = false;


  constructor(
    private route: ActivatedRoute,
    private rCAMStore: Store<RecurringClassAppliedMonthlysState>,
    private scheduledClassesStore: Store<ScheduledClassesState>
  ) { }

  ngOnInit(): void {
    this.scheduledClassesStore.dispatch(new ScheduledClassesCleared());
    this.rCAMStore.dispatch(new RecurringClassAppliedMonthlysCleared());
    this.monthFromRouteData = +this.route.snapshot.params['month'];
    this.yearFromRouteData = +this.route.snapshot.params['year'];
    this.rCAMStore.dispatch(new RecurringClassAppliedMonthlysRequested({
      month: this.monthFromRouteData,
      year: this.yearFromRouteData
    }));
    this.rCAMs$ = this.rCAMStore.pipe(
      select(selectAllRecurringClassAppliedMonthlys)
    );
    this.rCAMsLoaded$ = this.rCAMStore.pipe(
      select(selectRecurringClassAppliedMonthlysLoaded)
    );
    this.batchDeletionData$ = this.rCAMStore.pipe(
      select(optionalScheduledClassBatchDeletionData)
    );
    this.batchDeletionErrMsg$ = this.scheduledClassesStore.pipe(
      select(scheduledClassesErrorMsg)
    );
    this.batchDeletionSuccessMsg$ = this.scheduledClassesStore.pipe(
      select(scheduledClassesSuccessMsg)
    );
  }


  onClearStatusMsgs() {
    this.scheduledClassesStore.dispatch(new ScheduledClassesMessagesCleared());
    this.rCAMStore.dispatch(new RecurringClassesAppliedMonthlyMessagesCleared())
  }

  toggleApplySchedulerSubmitForm() {
    if (this.showApplyRecurringClassSubmitForm) {
      this.showApplyRecurringClassSubmitForm = false;
    } else {
      this.showApplyRecurringClassSubmitForm = true;
    }
  }


  trackByFn(index: number, item: any) {
    return item.id;
  }  

}
