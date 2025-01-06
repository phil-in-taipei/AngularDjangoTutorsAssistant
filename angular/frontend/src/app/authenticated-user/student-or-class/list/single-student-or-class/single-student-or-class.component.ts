import { Component, Input } from '@angular/core';
import { Store } from '@ngrx/store';

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
export class SingleStudentOrClassComponent {

  @Input() studentOrClass: StudentOrClassModel;

  deletionPopupVisible: boolean = false;

  constructor(
    private store: Store<StudentsOrClassesState>
  ) { }

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
