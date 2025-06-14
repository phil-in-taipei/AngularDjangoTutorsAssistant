import { Component } from '@angular/core';
import { AsyncPipe, NgIf } from '@angular/common';
import { first } from 'rxjs';
import { NgForm } from '@angular/forms';
import { FormsModule } from '@angular/forms';
import { 
  UnauthenticatedHeaderComponent 
} from '../unauthenticated-layout/unauthenticated-header/unauthenticated-header.component';
import { 
  UnauthenticatedFooterComponent 
} from '../unauthenticated-layout/unauthenticated-footer/unauthenticated-footer.component';

import { UserRegistrationModel, 
  UserRegistrationResponseModel 
} from '../models/user-registration.model';
import { RegistrationService } from './registration.service';

@Component({
  selector: 'app-registration',
  standalone: true,
  imports: [
    UnauthenticatedHeaderComponent, 
    UnauthenticatedFooterComponent,
    NgIf,
    FormsModule,
  ],
  templateUrl: './registration.component.html',
  styleUrl: './registration.component.css'
})
export class RegistrationComponent {

  constructor(private registrationService: RegistrationService) { }

  passwordErrorMsg: string|undefined = undefined;

  apiErrorMsg: string|undefined = undefined;

  apiSuccessResponse: UserRegistrationResponseModel|undefined = undefined;

  clearTemplateMessages(): void {
    this.passwordErrorMsg = undefined;
    this.apiSuccessResponse = undefined;
    this.apiErrorMsg = undefined;
  }

  implementRegistrationRequest(userRegistrationData: UserRegistrationModel): void {
    this.registrationService
      .submitUserRegistration(userRegistrationData)
        .pipe(first())
        .subscribe({
          next: (response) => {
            this.apiSuccessResponse = response;
          },
          error: (error) => {
            this.apiErrorMsg = 'An error occurred during registration.';
            if (error.error && error.error.message) {
              console.log(error.error)
              this.apiErrorMsg = error.error.message;
            }}
        });
  }

  onClearApiError(): void {
    this.apiErrorMsg = undefined;
  }

  onClearApiSuccessResponse(): void {
    this.apiSuccessResponse = undefined;
  }

  onClearFormPasswordError(): void {
    this.passwordErrorMsg = undefined;
  }

  onSubmitRegistrationForm(form: NgForm): void {
    this.clearTemplateMessages();
    console.log(form)
    if (form.invalid) {
      return;
    }
    if (form.value.password !== form.value.re_password) {
      this.passwordErrorMsg = 'The passwords do not match. Please try again.';
      form.reset();
      return;
    }
    this.implementRegistrationRequest({
      username: form.value.username,
      password: form.value.password,
      re_password: form.value.re_password,
      profile: {
        surname:form.value.surname,
        given_name:form.value.given_name,
        contact_email: form.value.contact_email,
      }
    });
    form.reset();
  }

}
