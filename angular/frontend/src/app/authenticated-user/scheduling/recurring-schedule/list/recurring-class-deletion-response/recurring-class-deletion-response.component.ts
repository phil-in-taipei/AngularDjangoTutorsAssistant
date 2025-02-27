import { Component, Input, OnInit } from '@angular/core';
import { Observable, of } from 'rxjs';
import {select, Store} from '@ngrx/store';

//import { 
//  RecurringClassesAppliedMonthlyMessagesCleared 
//} from '../../state/recurring-classes-applied-monthly-state/recurring-class-applied-monthly.actions';
import { 
  ScheduledClassBatchDeletionDataModel 
} from 'src/app/models/scheduled-class.model';
import { 
  ScheduledClassesMessagesCleared 
} from '../../../classes-state/scheduled-classes.actions';
import { 
  ScheduledClassesState 
} from '../../../classes-state/scheduled-classes.reducers';
import { 
  scheduledClassesSuccessMsg, scheduledClassesErrorMsg 
} from '../../../classes-state/scheduled-classes.selectors';

@Component({
  selector: 'app-recurring-class-deletion-response',
  standalone: false,
  templateUrl: './recurring-class-deletion-response.component.html',
  styleUrl: './recurring-class-deletion-response.component.css'
})
export class RecurringClassDeletionResponseComponent implements OnInit {

  @Input() scheduledClassesOptionalDeletionData: ScheduledClassBatchDeletionDataModel;
  batchDeletionErrMsg$: Observable<string | undefined> = of(undefined);
  batchDeletionSuccessMsg$: Observable<string | undefined> = of(undefined);

  constructor(private store: Store<ScheduledClassesState>) { }

  ngOnInit(): void {
    this.batchDeletionErrMsg$ = this.store.pipe(
      select(scheduledClassesErrorMsg)
    );
    this.batchDeletionSuccessMsg$ = this.store.pipe(
      select(scheduledClassesSuccessMsg)
    );
  }

  onClearStatusMsgs() {
    this.store.dispatch(new ScheduledClassesMessagesCleared());
  }

  onDeleteMonthlyBatch() {
    console.log(this.scheduledClassesOptionalDeletionData.obsolete_class_ids);
    console.log(this.scheduledClassesOptionalDeletionData.obsolete_class_strings);
    let payload = {
      obsolete_class_ids: this.scheduledClassesOptionalDeletionData.obsolete_class_ids
    }
  }

}
