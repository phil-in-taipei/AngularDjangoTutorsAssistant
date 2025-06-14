import { Component, OnInit, OnDestroy } from '@angular/core';
import { NgIf } from '@angular/common';
import { Subscription } from 'rxjs';
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
    FormsModule,
    NgIf,
    UnauthenticatedFooterComponent,
    UnauthenticatedHeaderComponent
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent implements OnInit, OnDestroy {

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

  ngOnDestroy() {
    if (this.errorLogin$) {
      this.errorLogin$.unsubscribe();
    }
  }

  onLogin(form: NgForm) {
    if (form.invalid) {
      return;
    }
    this.authService.login(form.value.username, form.value.password);
    form.reset();
  }

}
