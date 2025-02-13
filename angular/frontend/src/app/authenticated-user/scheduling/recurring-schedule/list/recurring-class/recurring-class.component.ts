import { Component, Input } from '@angular/core';
import { Store } from '@ngrx/store';

import { 
  RecurringClassesState
 } from '../../recurring-schedule-state/recurring-schedule.reducers';
import { RecurringClassModel } from 'src/app/models/recurring-schedule.model';
import { 
  RecurringClassDeletionRequested 
} from '../../recurring-schedule-state/recurring-schedule.actions';

@Component({
  selector: 'app-recurring-class',
  standalone: false,
  templateUrl: './recurring-class.component.html',
  styleUrl: './recurring-class.component.css'
})
export class RecurringClassComponent {

  @Input() recurringClass: RecurringClassModel;

  deletionPopupVisible: boolean = false;

  constructor(private store: Store<RecurringClassesState>) { }


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
