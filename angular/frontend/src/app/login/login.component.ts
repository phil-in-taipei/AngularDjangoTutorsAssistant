import { Component, OnInit } from '@angular/core';
import { AsyncPipe, NgIf } from '@angular/common';
import { first, Subscription } from 'rxjs';
import { NgForm } from '@angular/forms';
import { FormsModule } from '@angular/forms';

import { AuthService } from '../authentication/auth.service';
import { 
  UnauthenticatedFooterComponent 
} from '../unauthenticated-layout/unauthenticated-footer/unauthenticated-footer.component';
import { 
  UnauthenticatedHeaderComponent 
} from '../unauthenticated-layout/unauthenticated-header/unauthenticated-header.component';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    AsyncPipe,
    FormsModule,
    NgIf,
    UnauthenticatedFooterComponent,
    UnauthenticatedHeaderComponent
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent implements OnInit {

  isErrorLogin:boolean = false;
  private errorLogin$: Subscription;
  errorMsg:string = 'There was an error logging in'

  constructor(public authService: AuthService) { }

  ngOnInit(): void {
    this.isErrorLogin = this.authService.getIsLoginError();
    this.errorLogin$ = this.authService
      .getLoginErrorListener()
      .subscribe(isErrorLogin => {
        this.isErrorLogin = isErrorLogin;
    });
  }


  onClearLoginError() {
    this.authService.clearLoginError();
  }

  onLogin(form: NgForm) {
    if (form.invalid) {
      return;
    }
    this.authService.login(form.value.username, form.value.password);
    form.reset();
  }

}
