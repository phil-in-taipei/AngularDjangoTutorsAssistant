import { Component, Input, OnInit } from '@angular/core';
import { select, Store } from '@ngrx/store';
import { Observable } from "rxjs";

import { FreelanceTuitionTransactionRecordModel } from 'src/app/models/accounting.model';
import { 
  selectStudentOrClassById 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.selectors';
import { StudentOrClassModel } from 'src/app/models/student-or-class.model';
import { 
  StudentsOrClassesState 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.reducers';


@Component({
  selector: 'app-refund-response-display',
  standalone: false,
  templateUrl: './refund-response-display.component.html',
  styleUrl: './refund-response-display.component.css'
})
export class RefundResponseDisplayComponent {

    @Input() refundRecord: FreelanceTuitionTransactionRecordModel;
    freelanceAccount$: Observable<StudentOrClassModel | undefined>;
    
    constructor(private store: Store<StudentsOrClassesState>) { }
  
    ngOnInit(): void {
      this.freelanceAccount$ = this.store.pipe(select(
        selectStudentOrClassById(this.refundRecord.student_or_class)
      ));
    }

}
