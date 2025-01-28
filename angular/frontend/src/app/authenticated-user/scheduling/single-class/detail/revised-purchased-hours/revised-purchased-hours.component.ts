import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { select, Store } from '@ngrx/store';
import { Observable, of } from 'rxjs';

import { 
  selectStudentOrClassById, studentsOrClassesSuccessMsg 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.selectors';
import { StudentOrClassModel } from 'src/app/models/student-or-class.model';
import { StudentOrClassConfirmationModificationResponse } from 'src/app/models/student-or-class.model';
import { 
  StudentsOrClassesState 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.reducers';
import { 
  StudentsOrClassesMessagesCleared, StudentOrClassPurchasedHoursUpdated 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.actions';

@Component({
  selector: 'app-revised-purchased-hours',
  standalone: false,
  templateUrl: './revised-purchased-hours.component.html',
  styleUrl: './revised-purchased-hours.component.css'
})
export class RevisedPurchasedHoursComponent implements OnInit{

    @Input() studentOrClassHoursUpdate: StudentOrClassConfirmationModificationResponse;
    studentsOrClassesSuccessMsg$: Observable<string | undefined> = of(undefined);
    private timeoutId: any;

    constructor(
      private store: Store<StudentsOrClassesState>
    ) { }
  
    ngOnInit(): void {
      let payload = { studentOrClass: this.studentOrClassHoursUpdate };
      this.store.dispatch(
        new StudentOrClassPurchasedHoursUpdated(payload)
      );
      this.studentsOrClassesSuccessMsg$ = this.store.pipe(
        select(studentsOrClassesSuccessMsg)
      );
      this.timeoutId = setTimeout(() => this.onClearStatusMsgs(), 1800);    
    }

    onClearStatusMsgs() {
      this.store.dispatch(new StudentsOrClassesMessagesCleared());
    }

    ngOnDestroy(): void {
      if (this.timeoutId) {
        clearTimeout(this.timeoutId);
      }
    }
}
