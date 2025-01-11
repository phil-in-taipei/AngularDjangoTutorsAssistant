import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { select, Store } from '@ngrx/store';
import { Observable, of } from 'rxjs';

import { SchoolModel } from 'src/app/models/school.model';
import { 
  SchoolsState
} from 'src/app/authenticated-user/schools/state/school.reducers';
import { 
  selectAllSchools 
} from 'src/app/authenticated-user/schools/state/school.selectors';
import { 
  StudentOrClassCreationCancelled, 
  StudentOrClassCreateSubmitted, 
} from '../../state/student-or-class.actions';
import { 
  StudentOrClassCreateAndEditModel 
} from 'src/app/models/student-or-class.model';
import { StudentsOrClassesState } from '../../state/student-or-class.reducers';

@Component({
  selector: 'app-create-class-form',
  standalone: false,
  templateUrl: './create-class-form.component.html',
  styleUrl: './create-class-form.component.css'
})
export class CreateClassFormComponent implements OnInit{

  schools$: Observable<SchoolModel[] | undefined> = of(undefined);

  constructor(
    private schoolStore: Store<SchoolsState>,
    private studentsOrClassesStore: Store<StudentsOrClassesState>
  ) {}

  ngOnInit(): void {
    this.schools$ = this.schoolStore.pipe(
      select(selectAllSchools)
    );
  }

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
        account_type: "school",
        school: form.value.school,
        tuition_per_hour: +form.value.tuition_per_hour,
        comments: form.value.comments,
        purchased_class_hours: undefined,
    }
    console.log(submissionForm);
    this.studentsOrClassesStore.dispatch(new StudentOrClassCreateSubmitted(
      { studentOrClass: submissionForm }
    ));
    form.reset();
    }
}
