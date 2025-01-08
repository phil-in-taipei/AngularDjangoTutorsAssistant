import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { select, Store } from '@ngrx/store';

import { 
  StudentOrClassCreationCancelled, 
  StudentOrClassCreateSubmitted, 
} from '../../state/student-or-class.actions';
import { 
  StudentOrClassCreateAndEditModel 
} from 'src/app/models/student-or-class.model';
import { StudentsOrClassesState } from '../../state/student-or-class.reducers';

@Component({
  selector: 'app-create-freelance-student-form',
  standalone: false,
  templateUrl: './create-freelance-student-form.component.html',
  styleUrl: './create-freelance-student-form.component.css'
})
export class CreateFreelanceStudentFormComponent {

    constructor(
      private studentsOrClassesStore: Store<StudentsOrClassesState>
    ) {}

  onSubmitClass(form: NgForm) {
    if (form.invalid) {
      this.studentsOrClassesStore.dispatch(
        new StudentOrClassCreationCancelled(
          { err: {
              error: {
                message: "The form values were not properly filled in!"
              }
            }
          } 
      )
    );
      form.reset();
    }
    let submissionForm: StudentOrClassCreateAndEditModel = {
        student_or_class_name: form.value.student_or_class_name,
        account_type: "freelance",
        school: undefined,
        tuition_per_hour: +form.value.tuition_per_hour,
        comments: form.value.comments,
        purchased_class_hours: 0,
    }
    console.log(submissionForm);
    this.studentsOrClassesStore.dispatch(new StudentOrClassCreateSubmitted(
      { studentOrClass: submissionForm }
    ));
    form.reset();
    }
}
