import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';

import { RecurringClassesState } from '../recurring-schedule-state/recurring-schedule.reducers';
import { RecurringClassesRequested } from '../recurring-schedule-state/recurring-schedule.actions';

@Component({
  selector: 'app-recurring-schedule',
  standalone: false,
  templateUrl: './recurring-schedule.component.html',
  styleUrl: './recurring-schedule.component.css'
})
export class RecurringScheduleComponent implements OnInit {
  constructor(private store: Store<RecurringClassesState>) { }

  ngOnInit(): void {
    this.store.dispatch(new RecurringClassesRequested());
  }
}
