import { Component, OnInit } from '@angular/core';
import { Observable, of } from 'rxjs';
import { ActivatedRoute } from "@angular/router";
import { select, Store } from '@ngrx/store';

import { RecurringClassAppliedMonthlyModel } from 'src/app/models/recurring-schedule.model';
import { 
  RecurringClassAppliedMonthlysCleared,
  RecurringClassAppliedMonthlysRequested 
} from '../../state/recurring-classes-applied-monthly-state/recurring-class-applied-monthly.actions';
import { 
  RecurringClassAppliedMonthlysState 
} from '../../state/recurring-classes-applied-monthly-state/recurring-class-applied-monthly.reducers';
import { ScheduledClassesState } from '../../../classes-state/scheduled-classes.reducers';
import { 
  ScheduledClassesCleared 
} from '../../../classes-state/scheduled-classes.actions';
import { 
  selectAllRecurringClassAppliedMonthlys 
} from '../../state/recurring-classes-applied-monthly-state/recurring-class-applied-monthly.selectors';


@Component({
  selector: 'app-recurring-classes-applied-monthly',
  standalone: false,
  templateUrl: './recurring-classes-applied-monthly.component.html',
  styleUrl: './recurring-classes-applied-monthly.component.css'
})
export class RecurringClassesAppliedMonthlyComponent implements OnInit {

  rCAMs$: Observable<RecurringClassAppliedMonthlyModel[] | undefined> = of(undefined);
  monthFromRouteData:number;
  yearFromRouteData:number;
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
  }

  toggleApplySchedulerSubmitForm() {
    if (this.showApplyRecurringClassSubmitForm) {
      this.showApplyRecurringClassSubmitForm = false;
    } else {
      this.showApplyRecurringClassSubmitForm = true;
    }
  }

}
