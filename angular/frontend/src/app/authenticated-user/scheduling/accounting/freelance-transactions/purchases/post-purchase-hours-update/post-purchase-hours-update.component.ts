import { Component, OnInit, Input } from '@angular/core';
import { select, Store } from '@ngrx/store';
import { Observable, of } from "rxjs";

import { 
  FreelanceAccountPurchasedHoursSaved, StudentsOrClassesMessagesCleared 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.actions';
import { 
  FreelanceTuitionTransactionRecordModel 
} from 'src/app/models/accounting.model';
import { 
  StudentsOrClassesState 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.reducers';
import { 
  studentsOrClassesSuccessMsg 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.selectors';
import { StudentOrClassModel } from 'src/app/models/student-or-class.model';

@Component({
  selector: 'app-post-purchase-hours-update',
  standalone: false,
  templateUrl: './post-purchase-hours-update.component.html',
  styleUrl: './post-purchase-hours-update.component.css'
})
export class PostPurchaseHoursUpdateComponent implements OnInit{
  
  @Input() purchaseRecord: FreelanceTuitionTransactionRecordModel;
  @Input() freelanceAccount: StudentOrClassModel;
  successMsg$: Observable<string | undefined> = of(undefined)

  constructor(
    private store: Store<StudentsOrClassesState>
  ) { }

  onClearStatusMsgs() {
    this.store.dispatch(new StudentsOrClassesMessagesCleared());
  }

  ngOnInit(): void {
    let payload = {
      class_hours_purchased_or_refunded: this.purchaseRecord.class_hours_purchased_or_refunded, 
      studentOrClass: this.freelanceAccount
    }
    this.store.dispatch(
      new FreelanceAccountPurchasedHoursSaved(payload)
    );
    this.successMsg$ = this.store.pipe(
      select(studentsOrClassesSuccessMsg)
    );
  }


}
