import { Component, Input, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';

import { 
  RecurringClassesAppliedMonthlyMessagesCleared 
} from '../../state/recurring-classes-applied-monthly-state/recurring-class-applied-monthly.actions';
import { 
  RecurringClassAppliedMonthlysState 
} from '../../state/recurring-classes-applied-monthly-state/recurring-class-applied-monthly.reducers';
import { 
  ScheduledClassBatchDeletionDataModel 
} from 'src/app/models/scheduled-class.model';
import { 
  ScheduledClassesBatchDeletionSubmitted 
} from '../../../classes-state/scheduled-classes.actions';
import { 
  ScheduledClassesState 
} from '../../../classes-state/scheduled-classes.reducers';


@Component({
  selector: 'app-recurring-class-deletion-response',
  standalone: false,
  templateUrl: './recurring-class-deletion-response.component.html',
  styleUrl: './recurring-class-deletion-response.component.css'
})
export class RecurringClassDeletionResponseComponent implements OnInit {

  @Input() scheduledClassesOptionalDeletionData: ScheduledClassBatchDeletionDataModel;

  constructor(
    private recurringClassAppliedMonthlysStore: Store<RecurringClassAppliedMonthlysState>,
    private scheduledClassesStore: Store<ScheduledClassesState>
  ) { }

  ngOnInit(): void {

  }

  onClearStatusMsgs() {
    this.recurringClassAppliedMonthlysStore.dispatch(new RecurringClassesAppliedMonthlyMessagesCleared())
  }

  onDeleteMonthlyBatch() {
    console.log(this.scheduledClassesOptionalDeletionData.obsolete_class_ids);
    console.log(this.scheduledClassesOptionalDeletionData.obsolete_class_strings);
    let payload = {
      obsolete_class_data: this.scheduledClassesOptionalDeletionData
    }
    this.scheduledClassesStore.dispatch(new ScheduledClassesBatchDeletionSubmitted(payload));
    this.onClearStatusMsgs();
  }

}
