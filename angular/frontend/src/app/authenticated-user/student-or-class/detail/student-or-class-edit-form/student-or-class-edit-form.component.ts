import { Component, Input, Output, EventEmitter } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Store} from '@ngrx/store';

import { 
  StudentOrClassEditModel, StudentOrClassModel 
} from 'src/app/models/student-or-class.model';
import { StudentsOrClassesState } from '../../state/student-or-class.reducers';
import { 
  StudentOrClassEditCancelled, StudentOrClassEditSubmitted 
} from '../../state/student-or-class.actions';

@Component({
  selector: 'app-student-or-class-edit-form',
  standalone: false,
  templateUrl: './student-or-class-edit-form.component.html',
  styleUrl: './student-or-class-edit-form.component.css'
})
export class StudentOrClassEditFormComponent {

  @Input() studentOrClass: StudentOrClassModel;
  @Output() closeEvent = new EventEmitter<boolean>();

  constructor(private store: Store<StudentsOrClassesState>) { }


  onSubmitEditedStudentOrClass(form: NgForm) {
    console.log(form.value)
    if (form.invalid) {
      this.store.dispatch(new StudentOrClassEditCancelled({err: {
        error: {
          Error: "The form value was not properly filled in!"
        }
      }} ));
      form.reset();
      return;
    }
    let editedStudentOrClassData: StudentOrClassEditModel = {
      student_or_class_name: form.value.student_or_class_name,
      comments: form.value.comments,
      tuition_per_hour: form.value.tuition_per_hour
    }
    this.store.dispatch(new StudentOrClassEditSubmitted(
      {  id: this.studentOrClass.id, studentOrClass: editedStudentOrClassData }
    ));
    form.resetForm();
    this.closeEvent.emit(false);
  }

}
