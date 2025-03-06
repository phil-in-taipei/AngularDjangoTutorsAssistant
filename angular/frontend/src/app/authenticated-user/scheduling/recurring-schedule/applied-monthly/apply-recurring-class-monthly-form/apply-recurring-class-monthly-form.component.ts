import { Component, Input, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { select, Store } from '@ngrx/store';
import { Observable, of } from 'rxjs';

import { 
  RecurringClassAppliedMonthlyCreateModel, 
  RecurringClassModel
} from 'src/app/models/recurring-schedule.model';
import { 
  RecurringClassesState 
} from '../../state/recurring-schedule-state/recurring-schedule.reducers';
import { 
  recurringClassAppliedMonthlysErrorMsg, recurringClassAppliedMonthysSuccessMsg 
} from '../../state/recurring-classes-applied-monthly-state/recurring-class-applied-monthly.selectors';
import { 
  RecurringClassAppliedMonthlysState 
} from '../../state/recurring-classes-applied-monthly-state/recurring-class-applied-monthly.reducers';
import { 
  RecurringClassAppliedMonthlyCreationCancelled,
  RecurringClassAppliedMonthlyCreateSubmitted,
  RecurringClassesAppliedMonthlyMessagesCleared 
} from '../../state/recurring-classes-applied-monthly-state/recurring-class-applied-monthly.actions';
import { 
  selectAllRecurringClasses 
} from '../../state/recurring-schedule-state/recurring-schedule.selectors';

@Component({
  selector: 'app-apply-recurring-class-monthly-form',
  standalone: false,
  templateUrl: './apply-recurring-class-monthly-form.component.html',
  styleUrl: './apply-recurring-class-monthly-form.component.css'
})
export class ApplyRecurringClassMonthlyFormComponent implements OnInit {


  recurringClasses$: Observable<RecurringClassModel[] | undefined> = of(undefined);
  @Input() month:number;
  @Input() year:number;
  errorMsg$: Observable<string | undefined>;
  successMsg$: Observable<string | undefined>;


  constructor( 
    private rCAMStore: Store<RecurringClassAppliedMonthlysState>,
    private recurringClassesStore: Store<RecurringClassesState>
  ) {}


  ngOnInit(): void {
    this.rCAMStore.dispatch(
      new RecurringClassesAppliedMonthlyMessagesCleared()
    );
    this.errorMsg$ = this.rCAMStore.pipe(
      select(recurringClassAppliedMonthlysErrorMsg)
    );
    this.successMsg$ = this.rCAMStore.pipe(
      select(recurringClassAppliedMonthysSuccessMsg)
    );
    this.recurringClasses$ = this.recurringClassesStore.pipe(
      select(selectAllRecurringClasses)
    );
  }

  onClearStatusMsgs() {
    this.rCAMStore.dispatch(new RecurringClassesAppliedMonthlyMessagesCleared());
  }

  onSubmitRCAM(form: NgForm) {

    if (form.invalid) {
      this.rCAMStore.dispatch(new RecurringClassAppliedMonthlyCreationCancelled({err: {
        error: {
          message: "The form values were not properly filled in!"
        }
      }} ));
      form.reset();
    }
    let submissionForm: RecurringClassAppliedMonthlyCreateModel = {
        scheduling_month: this.month,
        scheduling_year: this.year,
        recurring_class: form.value.recurring_class,
    }
    console.log(submissionForm);
    this.rCAMStore.dispatch(new RecurringClassAppliedMonthlyCreateSubmitted(
      { recurringClassAppliedMonthly: submissionForm }
    ));
    form.reset();
    }

}
