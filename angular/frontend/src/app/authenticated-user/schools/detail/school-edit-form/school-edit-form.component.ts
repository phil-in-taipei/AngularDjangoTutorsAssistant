import { Component, Input, Output, EventEmitter } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Store} from '@ngrx/store';

import { 
  SchoolCreateAndEditModel, SchoolModel 
} from 'src/app/models/school.model';
import { SchoolsState } from '../../state/school.reducers';
import { 
  SchoolEditCancelled, SchoolEditSubmitted 
} from '../../state/school.actions';

@Component({
  selector: 'app-school-edit-form',
  standalone: false,
  templateUrl: './school-edit-form.component.html',
  styleUrl: './school-edit-form.component.css'
})
export class SchoolEditFormComponent {

  @Input() school: SchoolModel;
  @Output() closeEvent = new EventEmitter<boolean>();

  constructor(private store: Store<SchoolsState>) { }

  onSubmitEditedSchool(form: NgForm) {
    console.log(form.value)
    if (form.invalid) {
      this.store.dispatch(new SchoolEditCancelled({err: {
        error: {
          Error: "The form value was not properly filled in!"
        }
      }} ));
      form.reset();
      return;
    }
    let editedSchoolData: SchoolCreateAndEditModel = {
      school_name: form.value.school_name,
      address_line_1: form.value.address_line_1,
      address_line_2: form.value.address_line_2,
      contact_phone: form.value.contact_phone,
      other_information: form.value.other_information,    }
    this.store.dispatch(new SchoolEditSubmitted(
      {  id: this.school.id, school: editedSchoolData }
    ));
    form.resetForm();
    this.closeEvent.emit(false);
  }


}
