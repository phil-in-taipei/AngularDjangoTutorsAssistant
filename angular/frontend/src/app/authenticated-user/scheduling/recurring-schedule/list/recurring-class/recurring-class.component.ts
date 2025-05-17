import { Component, Input, OnInit } from '@angular/core';
import { select, Store } from '@ngrx/store';
import { Observable, of } from 'rxjs';

import { 
  deletionModeForRecurringClassesActivated 
} from '../../state/recurring-schedule-state/recurring-schedule.selectors';
import { 
  RecurringClassesState
 } from '../../state/recurring-schedule-state/recurring-schedule.reducers';
import { RecurringClassModel } from 'src/app/models/recurring-schedule.model';
import { 
  RecurringClassDeletionRequested 
} from '../../state/recurring-schedule-state/recurring-schedule.actions';
import { O } from '@fullcalendar/core/internal-common';

@Component({
  selector: 'app-recurring-class',
  standalone: false,
  templateUrl: './recurring-class.component.html',
  styleUrl: './recurring-class.component.css'
})
export class RecurringClassComponent implements OnInit {

  @Input() recurringClass: RecurringClassModel;
  deletionModeForRecurringClassesActivated$: Observable<boolean> = of(false);
  deletionPopupVisible: boolean = false;

  constructor(private store: Store<RecurringClassesState>) { }

  ngOnInit(): void {
    this.deletionModeForRecurringClassesActivated$ = this.store.pipe(
      select(deletionModeForRecurringClassesActivated)
    );
  }

  showDeletionPopup() {
    this.deletionPopupVisible = true;
  }

  hideDeletionPopup() {
    this.deletionPopupVisible = false;
  }

  onRemoveRecurringClass() {
    const payload = { id: +this.recurringClass.id };
    this.store.dispatch(
      new RecurringClassDeletionRequested(payload)
    );
  }  

}
