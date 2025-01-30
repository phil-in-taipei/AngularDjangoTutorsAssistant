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
  selector: 'app-select-monthly',
  standalone: false,
  templateUrl: './select-monthly.component.html',
  styleUrl: './select-monthly.component.css'
})
export class SelectMonthlyComponent implements OnInit {

  monthsAndIntegers: [string, number][] = monthsAndIntegers;
  years: Number[] = [];
  @Output() closeMonthlySelectFormEvent = new EventEmitter<boolean>();

  constructor(private store: Store<ScheduledClassesState>) { }

  ngOnInit(): void {
    this.years = getYearsOptions();
  }

  onSubmitMonthlySelectorForm(form: NgForm) {
    if (form.invalid) {
      return;
    }
    this.store.dispatch(new ScheduledClassesCleared);
    console.log('valid!')
    this.store.dispatch(new MonthlyClassesRequested(
      {month: form.value.month, year: form.value.year }
    ));
    this.closeMonthlySelectFormEvent.emit(false);
  }

}
