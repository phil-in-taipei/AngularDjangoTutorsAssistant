import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { select, Store } from '@ngrx/store';
import { Observable, of } from 'rxjs';

import { 
  StudentsOrClassesMessagesCleared 
} from '../../state/student-or-class.actions';
import { 
  StudentOrClassCreateAndEditModel 
} from 'src/app/models/student-or-class.model';
import { 
  studentsOrClassesErrorMsg, studentsOrClassesSuccessMsg 
} from '../../state/student-or-class.selectors';
import { StudentsOrClassesState } from '../../state/student-or-class.reducers';

@Component({
  selector: 'app-create-student-or-class',
  standalone: false,
  templateUrl: './create-student-or-class.component.html',
  styleUrl: './create-student-or-class.component.css'
})
export class CreateStudentOrClassComponent implements OnInit {

  errMsg$: Observable<string | undefined>;
  showFreelanceStudentSubmitForm:boolean = false;
  showClassSubmitForm:boolean = false;
  successMsg$: Observable<string | undefined>;

  constructor(
    private studentsOrClassesStore: Store<StudentsOrClassesState>
  ) {}

  ngOnInit(): void {
    this.studentsOrClassesStore.dispatch(
      new StudentsOrClassesMessagesCleared()
    );
    this.errMsg$ = this.studentsOrClassesStore.pipe(
      select(studentsOrClassesErrorMsg)
    );
    this.successMsg$ = this.studentsOrClassesStore.pipe(
      select(studentsOrClassesSuccessMsg)
    );
  }

  onClearStatusMsgs() {
    this.studentsOrClassesStore.dispatch(new StudentsOrClassesMessagesCleared());
  }

  toggleFreelanceStudentSubmitForm() {
    if (this.showFreelanceStudentSubmitForm) {
      this.showFreelanceStudentSubmitForm = false;
    } else {
      this.showFreelanceStudentSubmitForm = true;
      this.showClassSubmitForm = false;
    }
  }

  toggleClassSubmitForm() {
    if (this.showClassSubmitForm) {
      this.showClassSubmitForm = false;
    } else {
      this.showClassSubmitForm = true;
      this.showFreelanceStudentSubmitForm = false;
    }
  }
}
