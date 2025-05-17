import { Component, Input, OnInit } from '@angular/core';
import { Observable, of } from 'rxjs';
import { select, Store } from '@ngrx/store';

import { 
  deletionModeForRecurringClassesAppliedMonthlyActivated 
} from '../../state/recurring-classes-applied-monthly-state/recurring-class-applied-monthly.selectors';
import { 
  RecurringClassAppliedMonthlysState 
} from '../../state/recurring-classes-applied-monthly-state/recurring-class-applied-monthly.reducers';
import { 
  RecurringClassAppliedMonthlyModel 
} from 'src/app/models/recurring-schedule.model';
import { 
  RecurringClassAppliedMonthlyDeletionRequested 
} from '../../state/recurring-classes-applied-monthly-state/recurring-class-applied-monthly.actions';
import { 
  RecurringClassesState 
} from '../../state/recurring-schedule-state/recurring-schedule.reducers';
import { RecurringClassModel } from 'src/app/models/recurring-schedule.model';
import { 
  selectRecurringClassById 
} from '../../state/recurring-schedule-state/recurring-schedule.selectors';

@Component({
  selector: 'app-recurring-class-applied-monthly',
  standalone: false,
  templateUrl: './recurring-class-applied-monthly.component.html',
  styleUrl: './recurring-class-applied-monthly.component.css'
})
export class RecurringClassAppliedMonthlyComponent implements OnInit {

  @Input() recurringClassAppliedMonthly: RecurringClassAppliedMonthlyModel;
  deletionModeForRecurringClassesAppliedMonthlyActivated$: Observable<boolean> = of(false);
  recurringClass$: Observable<RecurringClassModel | undefined> = of(undefined);

  deletionPopupVisible: boolean = false;

  constructor(
    private rCAMStore: Store<RecurringClassAppliedMonthlysState>,
    private recurringClassesStore: Store<RecurringClassesState>
  ) { }


  ngOnInit(): void {
    this.deletionModeForRecurringClassesAppliedMonthlyActivated$ = this.rCAMStore.pipe(
      select(deletionModeForRecurringClassesAppliedMonthlyActivated)
    );
    this.recurringClass$ = this.recurringClassesStore.pipe(select(
      selectRecurringClassById(this.recurringClassAppliedMonthly.recurring_class)
    ));
  }

  showDeletionPopup() {
    this.deletionPopupVisible = true;
  }

  hideDeletionPopup() {
    this.deletionPopupVisible = false;
  }

  onRemoveRecurringClassAppliedMonthly() {
    const payload = { id: +this.recurringClassAppliedMonthly.id };
    this.rCAMStore.dispatch(
      new RecurringClassAppliedMonthlyDeletionRequested(payload)
    );
  }  

}
