import { Component, Input, Output, EventEmitter } from '@angular/core';
import { NgForm } from '@angular/forms';
import { AppState } from '../../../reducers';
import { Store } from '@ngrx/store';

import { 
  UserProfileEditModel, UserProfileModel 
} from 'src/app/models/user-profile.model';
import { 
  UserProfileSubmissionCancelled, UserProfileSubmitted 
} from '../user-state/user.actions';

@Component({
  selector: 'app-edit-profile-form',
  standalone: false,
  templateUrl: './edit-profile-form.component.html',
  styleUrl: './edit-profile-form.component.css'
})
export class EditProfileFormComponent {

  @Input() profile: UserProfileModel;
  @Output() closeEvent = new EventEmitter<boolean>();

  constructor(private store: Store<AppState>) { }

  onSubmitEditedProfile(form: NgForm) {

    if (form.invalid) {
      //console.log('the form is invalid!')
      this.store.dispatch(new UserProfileSubmissionCancelled({err: {
        error: {
          message: "The form values were not properly filled in!"
        }
      }} ));
      form.reset();
      this.closeEvent.emit(false);
      return;
    }
    let submissionForm: UserProfileEditModel = {
      contact_email: form.value.contact_email,
      given_name: form.value.given_name,
      surname: form.value.surname,
    }
    this.store.dispatch(new UserProfileSubmitted(
      { submissionForm: submissionForm }
    ));
    form.resetForm();
    this.closeEvent.emit(false);
  }
}
