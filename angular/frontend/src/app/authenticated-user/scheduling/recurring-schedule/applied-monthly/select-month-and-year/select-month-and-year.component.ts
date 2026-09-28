import { Component, OnInit, EventEmitter, Output, Input } from '@angular/core';
import { NgForm } from '@angular/forms';
//import { Router } from '@angular/router';
import { select, Store } from '@ngrx/store';

import { getYearsOptions, monthsAndIntegers } from 'src/app/shared-utils/date-time.util';
import { 
  RecurringClassAppliedMonthlysRequested, RecurringClassAppliedMonthlysCleared
} from '../../state/recurring-classes-applied-monthly-state/recurring-class-applied-monthly.actions';
import { 
  RecurringClassAppliedMonthlysState 
} from '../../state/recurring-classes-applied-monthly-state/recurring-class-applied-monthly.reducers';

@Component({
  selector: 'app-select-month-and-year',
  standalone: false,
  templateUrl: './select-month-and-year.component.html',
  styleUrl: './select-month-and-year.component.css'
})
export class SelectMonthAndYearComponent implements OnInit {

  years: number[];

  readonly monthsAndIntegers = monthsAndIntegers;

  @Input() batchSchedulingMonthAndYear?: [number, number] | null;
  @Output() closeMonthlySelectFormEvent = new EventEmitter<boolean>();


  defaultMonth?: number;
  defaultYear?: number;

  constructor(
    //private router: Router
    private rCAMStore: Store<RecurringClassAppliedMonthlysState>,
  ) { }

  ngOnInit(): void {
    this.years = getYearsOptions();
    if (this.batchSchedulingMonthAndYear) {
      const [month, year] = this.batchSchedulingMonthAndYear;
      this.defaultYear = year;
      this.defaultMonth = month;
    }
  }


  onMonthAndYearSelect(form: NgForm) {
    if (form.invalid) {
      return;
    }
    const month = +form.value.month;
    const year = +form.value.year;
    const sameMonth = this.batchSchedulingMonthAndYear
      && +form.value.month === this.defaultMonth
      && +form.value.year === this.defaultYear;
    if (!sameMonth) {
      this.rCAMStore.dispatch(new RecurringClassAppliedMonthlysCleared());
      this.rCAMStore.dispatch(new RecurringClassAppliedMonthlysRequested({
        month: month,
        year: year
      }));
    }
    this.closeMonthlySelectFormEvent.emit(false);
  }


}
