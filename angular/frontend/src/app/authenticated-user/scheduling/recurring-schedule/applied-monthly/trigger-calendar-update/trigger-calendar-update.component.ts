import { Component, Input, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';

import { 
  MonthlyClassesRequested 
} from '../../../classes-state/scheduled-classes.actions';
import { 
  ScheduledClassesState 
} from '../../../classes-state/scheduled-classes.reducers';


@Component({
  selector: 'app-trigger-calendar-update',
  standalone: false,
  templateUrl: './trigger-calendar-update.component.html',
  styleUrl: './trigger-calendar-update.component.css'
})
export class TriggerCalendarUpdateComponent {

  @Input() month:number;
  @Input() year:number;

  constructor(
    private scheduledClassesStore: Store<ScheduledClassesState>
  ) { }

  ngOnInit(): void {
    this.onUpdateCalendar();
  }

  onUpdateCalendar() {
    this.scheduledClassesStore.dispatch(new MonthlyClassesRequested(
        { month: this.month, year: this.year }
   ));
  }

}
