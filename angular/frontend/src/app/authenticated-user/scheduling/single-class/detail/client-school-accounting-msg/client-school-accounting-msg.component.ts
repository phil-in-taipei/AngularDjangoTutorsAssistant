import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';

import { 
  ScheduledClassesState 
} from '../../../classes-state/scheduled-classes.reducers';
import { 
  ClientSchoolAccountingUpdateMessageCleared 
} from '../../../classes-state/scheduled-classes.actions';

@Component({
  selector: 'app-client-school-accounting-msg',
  standalone: false,
  templateUrl: './client-school-accounting-msg.component.html',
  styleUrl: './client-school-accounting-msg.component.css'
})
export class ClientSchoolAccountingMsgComponent implements OnInit {

  @Input() clientSchoolAccountingUpdateMsg: string;
  private timeoutForClientMsgID: ReturnType<typeof setTimeout> | undefined = undefined;

  constructor(
    private store: Store<ScheduledClassesState>
  ) { }
  
  ngOnInit(): void {
    this.timeoutForClientMsgID = setTimeout(
      () => this.onClearUpdatedClientSchoolAccountingResponseData(), 3000
    );    
  }

  onClearUpdatedClientSchoolAccountingResponseData() {
    this.store.dispatch(new ClientSchoolAccountingUpdateMessageCleared());
  }

  ngOnDestroy(): void {
    if (this.timeoutForClientMsgID) {
      clearTimeout(this.timeoutForClientMsgID);
    }
  }


}
