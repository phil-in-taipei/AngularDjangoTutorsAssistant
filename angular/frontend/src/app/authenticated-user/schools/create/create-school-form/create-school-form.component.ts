import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Store } from '@ngrx/store';

import { SchoolsState } from '../../state/school.reducers';
import { SchoolCreateAndEditModel } from 'src/app/models/school.model';
import { 
  SchoolCreateSubmitted, SchoolCreationCancelled 
} from '../../state/school.actions';

@Component({
  selector: 'app-create-school-form',
  standalone: false,
  templateUrl: './create-school-form.component.html',
  styleUrl: './create-school-form.component.css'
})
export class CreateSchoolFormComponent {


  constructor(private store: Store<SchoolsState>) { }


  onSubmitSchool(form: NgForm) {

    if (form.invalid) {
      this.store.dispatch(new SchoolCreationCancelled({err: {
        error: {
          message: "The form values were not properly filled in!"
        }
      }} ));
      form.reset();
      return;
    }
    let submissionForm: SchoolCreateAndEditModel = {
      school_name: form.value.school_name,
      address_line_1: form.value.address_line_1,
      address_line_2: form.value.address_line_2,
      contact_phone: form.value.contact_phone,
      other_information: form.value.other_information,
    }
    this.store.dispatch(new SchoolCreateSubmitted(
      { school: submissionForm }
    ));
    form.resetForm();
  }


}
