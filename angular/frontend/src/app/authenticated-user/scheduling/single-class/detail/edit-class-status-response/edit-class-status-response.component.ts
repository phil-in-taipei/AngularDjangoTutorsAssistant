import { Component, Input, OnDestroy } from '@angular/core';
import { Store } from '@ngrx/store';


import { 
  StudentOrClassConfirmationModificationResponse 
} from 'src/app/models/student-or-class.model';
import { 
  ScheduledClassesState 
} from '../../../classes-state/scheduled-classes.reducers';
import { 
  UpdatedPurchasedHoursCleared 
} from '../../../classes-state/scheduled-classes.actions';


@Component({
  selector: 'app-edit-class-status-response',
  standalone: false,
  templateUrl: './edit-class-status-response.component.html',
  styleUrl: './edit-class-status-response.component.css'
})
export class EditClassStatusResponseComponent {

  @Input() studentOrClassModificationResponse: StudentOrClassConfirmationModificationResponse;
  private timeoutId: ReturnType<typeof setTimeout> | undefined = undefined;

    constructor(
      private store: Store<ScheduledClassesState>
    ) { }
  
    ngOnInit(): void {
      this.timeoutId = setTimeout(() => this.onClearUpdatedClassStatusResponseData(), 3000);    
    }

    onClearUpdatedClassStatusResponseData() {
        this.store.dispatch(new UpdatedPurchasedHoursCleared());
    }

    ngOnDestroy(): void {
      if (this.timeoutId) {
        clearTimeout(this.timeoutId);
      }
    }

}
