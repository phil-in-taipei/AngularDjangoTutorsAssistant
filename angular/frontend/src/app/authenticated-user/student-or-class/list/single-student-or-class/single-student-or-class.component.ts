import { Component, Input, OnInit } from '@angular/core';
import { Observable, of } from "rxjs";
import { select, Store } from '@ngrx/store';

import { 
  deletionModeForStudentsOrClassesActivated
} from '../../state/student-or-class.selectors';
import { StudentOrClassDeletionRequested } from '../../state/student-or-class.actions';
import { StudentOrClassModel } from 'src/app/models/student-or-class.model';
import { 
  StudentsOrClassesState 
} from '../../state/student-or-class.reducers';


@Component({
  selector: 'app-single-student-or-class',
  standalone: false,
  templateUrl: './single-student-or-class.component.html',
  styleUrl: './single-student-or-class.component.css'
})
export class SingleStudentOrClassComponent implements OnInit {

  @Input() studentOrClass: StudentOrClassModel;
  deletionPopupVisible: boolean = false;
  deletionModeForStudentsOrClassesActivated$: Observable<boolean> = of(false);

  constructor(
    private store: Store<StudentsOrClassesState>
  ) { }

  ngOnInit(): void {
    this.deletionModeForStudentsOrClassesActivated$ = this.store.pipe(
      select(deletionModeForStudentsOrClassesActivated)
    );
  }

  showDeletionPopup() {
    this.deletionPopupVisible = true;
  }

  hideDeletionPopup() {
    this.deletionPopupVisible = false;
  }

  onRemoveStudentOrClass() {
    const payload = { id: +this.studentOrClass.id };
    this.store.dispatch(
      new StudentOrClassDeletionRequested(payload)
    );
  }

}
