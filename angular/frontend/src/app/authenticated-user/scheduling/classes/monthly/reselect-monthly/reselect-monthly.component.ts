import { Component, OnInit, EventEmitter, Output, Input } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Store } from '@ngrx/store';

import { 
  getYearsOptions, monthsAndIntegers 
} from 'src/app/shared-utils/date-time.util';
import { 
  MonthlyClassesRequested, ScheduledClassesCleared 
} from '../../../classes-state/scheduled-classes.actions';
import { ScheduledClassesState } from '../../../classes-state/scheduled-classes.reducers';

@Component({
  selector: 'app-reselect-monthly',
  standalone: false,
  templateUrl: './reselect-monthly.component.html',
  styleUrl: './reselect-monthly.component.css'
})
export class ReselectMonthlyComponent implements OnInit {

  monthsAndIntegers: [string, number][] = monthsAndIntegers;
  @Input() monthlyDateRange: [string, string];
  years: Number[] = [];
  @Output() closeMonthlySelectFormEvent = new EventEmitter<boolean>();

  constructor(private store: Store<ScheduledClassesState>) { }

  ngOnInit(): void {
    this.years = getYearsOptions();
  }

  onReSubmitMonthlyTasksForm(form: NgForm) {
    console.log(form.value);
    if (form.invalid) {
      console.log(form.errors);
      return;
    }
    let previousYear = +this.monthlyDateRange[0].split('-')[0];
    let previousMonth = +this.monthlyDateRange[0].split('-')[1];
    console.log(previousYear);
    console.log(previousMonth);
    if (+form.value.month === previousMonth && +form.value.year === previousYear) {
      console.log('it is the same month/year')
      this.closeMonthlySelectFormEvent.emit(false);
    } else {
      this.store.dispatch(new ScheduledClassesCleared);
      this.store.dispatch(new MonthlyClassesRequested(
        {month: form.value.month, year: form.value.year }))
      this.closeMonthlySelectFormEvent.emit(false);
    }
  }

}
