import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
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
export class StudentOrClassEditFormComponent implements OnInit {

  @Input() studentOrClass: StudentOrClassModel;
  @Output() closeEvent = new EventEmitter<boolean>();

  // Local copy used for two-way binding
  editModel: StudentOrClassEditModel = {
    student_or_class_name: '',
    comments: '',
    tuition_per_hour: 0
  };
  constructor(private store: Store<StudentsOrClassesState>) { }

  ngOnInit() {
    this.initEditModel();
  }

  // ngOnChanges no longer needed — component is recreated on each toggle
  private initEditModel() {
    if (!this.studentOrClass) return;
    this.editModel = structuredClone({
      student_or_class_name: this.studentOrClass.student_or_class_name,
      comments: this.studentOrClass.comments,
      tuition_per_hour: this.studentOrClass.tuition_per_hour
    });
  }

  onNameChange(value: string) {
    this.editModel = { ...this.editModel, student_or_class_name: value };
  }

  onCommentsChange(value: string) {
    this.editModel = { ...this.editModel, comments: value };
  }

  onTuitionChange(value: number) {
    this.editModel = { ...this.editModel, tuition_per_hour: value };
  }

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
    this.store.dispatch(new StudentOrClassEditSubmitted(
      {  id: this.studentOrClass.id, studentOrClass: this.editModel }
    ));
    form.resetForm();
    this.closeEvent.emit(false);
  }

}
