import { ComponentFixture, TestBed, fakeAsync, tick  } from '@angular/core/testing';
import { NO_ERRORS_SCHEMA } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms';
import { Observable, of, throwError } from 'rxjs';
import { ActivatedRoute } from '@angular/router';
import { RegistrationComponent } from './registration.component';
import { RegistrationService } from './registration.service';
import { 
  userRegistrationData, 
  httpRegistrationResponseSuccess, 
  httpRegistrationResponseFailure1,
  httpRegistrationResponseFailure2,
  httpRegistrationResponseFailure3
} 
  from '../test-data/registration-tests/registration-data';
import { UserRegistrationResponseModel } from '../models/user-registration.model';
import { 
  findEl
  } from '../shared-utils/testing-helpers.util';

describe('RegistrationComponent', () => {
  let component: RegistrationComponent;
  let fixture: ComponentFixture<RegistrationComponent>;
  let registrationResponse$: Observable<UserRegistrationResponseModel|undefined>;
  let registrationService: any;


  beforeEach(async () => {
    let mockregistrationervice:RegistrationService = jasmine.createSpyObj(
      ['submitUserRegistration']);

    await TestBed.configureTestingModule({
      imports: [FormsModule],
      declarations: [ 
        //RegistrationComponent 
      ],
      providers: [
        { provide: RegistrationService, useValue: mockregistrationervice },
        // Provide a mock ActivatedRoute
        { provide: ActivatedRoute, useValue: { snapshot: { paramMap: { get: () => 'someValue' } } } }
      ],
      // below is so that the nested components don't raise errors
      schemas: [NO_ERRORS_SCHEMA], 
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RegistrationComponent);
    registrationResponse$ = of(undefined);
    registrationService = TestBed.inject(RegistrationService);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('onSubmitRegistrationForm function should submit the registration service form ' + 
  'to the registration service and clear the form', 
    fakeAsync(() => {
      registrationService.submitUserRegistration.and.returnValue(of(httpRegistrationResponseSuccess));
      const form = <NgForm>{
        invalid: false,
        value: {
          username: userRegistrationData.username,
          password: userRegistrationData.password,
          re_password: userRegistrationData.passwordConfirmation,
          contact_email: userRegistrationData.email,
          surname: userRegistrationData.surname,
          given_name: userRegistrationData.givenName,
        },
        reset: () => {}, // Mock the reset method
      };
      const formSpy = spyOn(form, 'reset');
      component.onSubmitRegistrationForm(form);

      tick(1000);
      fixture.detectChanges();

      expect(registrationService.submitUserRegistration)
        .toHaveBeenCalledWith(
          userRegistrationData
        );
      expect(formSpy).toHaveBeenCalled();
  }));

  it('should display success message if registration service indicates  ' +
  'form submission for creating new user was successful', 
    fakeAsync(() => {
      registrationService.submitUserRegistration.and.returnValue(of(httpRegistrationResponseSuccess));
      const form = <NgForm>{
        invalid: false,
        value: {
          username: userRegistrationData.username,
          password: userRegistrationData.password,
          re_password: userRegistrationData.passwordConfirmation,
          contact_email: userRegistrationData.email,
          surname: userRegistrationData.surname,
          given_name: userRegistrationData.givenName,
        },
        reset: () => {}, // Mock the reset method
      };
      const formSpy = spyOn(form, 'reset');
      component.onSubmitRegistrationForm(form);

      tick(1000);
      fixture.detectChanges();
      let sucessMsg = findEl(fixture, 'registration-success-msg');
      expect(sucessMsg.nativeElement.textContent).toBe('Account successfully created for user');
  }));

  it('should display error message if registration service indicates there has been an error ' +
  'due to username already existing)', 
    fakeAsync(() => {
      const errorObject = { error: httpRegistrationResponseFailure2 }; // Construct error object
      registrationService.submitUserRegistration.and
        .returnValue(throwError(()=> errorObject));
      const form = <NgForm>{
        invalid: false,
        value: {
          username: userRegistrationData.username,
          password: userRegistrationData.password,
          re_password: userRegistrationData.passwordConfirmation,
          contact_email: userRegistrationData.email,
          surname: userRegistrationData.surname,
          given_name: userRegistrationData.givenName,
        },
        reset: () => {}, // Mock the reset method
      };
      const formSpy = spyOn(form, 'reset');
      component.onSubmitRegistrationForm(form);

      tick(1000);
      fixture.detectChanges();
      let errorMsg = findEl(fixture, 'registration-api-failure-msg');
      expect(errorMsg.nativeElement.textContent).toBe(httpRegistrationResponseFailure2.message);
  }));


  it('should display error message if registration service indicates there has been an error ' +
  'due to submission of incomplete registration data)', 
    fakeAsync(() => {
      const errorObject = { error: httpRegistrationResponseFailure3 }; // Construct error object
      registrationService.submitUserRegistration.and
        .returnValue(throwError(()=> errorObject));
      const form = <NgForm>{
        invalid: false,
        value: {
          username: userRegistrationData.username,
          password: userRegistrationData.password,
          re_password: userRegistrationData.passwordConfirmation,
          contact_email: userRegistrationData.email,
          surname: userRegistrationData.surname,
          given_name: userRegistrationData.givenName,
        },
        reset: () => {}, // Mock the reset method
      };
      const formSpy = spyOn(form, 'reset');
      component.onSubmitRegistrationForm(form);

      tick(1000);
      fixture.detectChanges();
      let errorMsg = findEl(fixture, 'registration-api-failure-msg');
      expect(errorMsg.nativeElement.textContent).toBe(httpRegistrationResponseFailure3.message);
  }));

  it('should display error message if the user passes in two different passwords ', 
    fakeAsync(() => {
      const form = <NgForm>{
        invalid: false,
        value: {
          username: userRegistrationData.username,
          password: userRegistrationData.password,
          re_password: "differentPassword",
          contact_email: userRegistrationData.email,
          surname: userRegistrationData.surname,
          given_name: userRegistrationData.givenName,
        },
        reset: () => {}, // Mock the reset method
      };
      const formSpy = spyOn(form, 'reset');
      component.onSubmitRegistrationForm(form);

      tick(1000);
      fixture.detectChanges();
      let errorMsg = findEl(fixture, 'password-confirmation-failure-msg');
      expect(errorMsg.nativeElement.textContent).toBe(httpRegistrationResponseFailure1.message);
  }));


});
