import { Component, OnInit, Input } from '@angular/core';
import { select, Store } from '@ngrx/store';
import { Observable, of } from "rxjs";

import { 
  FreelanceAccountRefundedHoursSaved, StudentsOrClassesMessagesCleared 
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
  selector: 'app-post-refund-hours-update',
  standalone: false,
  templateUrl: './post-refund-hours-update.component.html',
  styleUrl: './post-refund-hours-update.component.css'
})
export class PostRefundHoursUpdateComponent implements OnInit {

  @Input() refundRecord: FreelanceTuitionTransactionRecordModel;
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
      class_hours_purchased_or_refunded: this.refundRecord.class_hours_purchased_or_refunded, 
      studentOrClass: this.freelanceAccount
    }

    this.store.dispatch(
      new FreelanceAccountRefundedHoursSaved(payload)
    );
    this.successMsg$ = this.store.pipe(
      select(studentsOrClassesSuccessMsg)
    );
  }

}
