import { Component, OnInit } from '@angular/core';
import { select, Store } from '@ngrx/store';
import { Observable, of } from "rxjs";

import { AppState } from 'src/app/reducers';
import { UserProfileMessagesCleared } from '../user-state/user.actions';
import { 
  selectUserProfile,
  selectUserProfileLoaded,
  userProfileSubmissionErrorMsg, 
  userProfileSubmissionSuccessMsg
} from '../user-state/user.selectors';
import { UserProfileModel } from 'src/app/models/user-profile.model';

@Component({
  selector: 'app-user-profile',
  standalone: false,
  templateUrl: './user-profile.component.html',
  styleUrl: './user-profile.component.css'
})
export class UserProfileComponent implements OnInit {

  showForm:boolean = false;
  usrProfileLoaded$: Observable<boolean> = of(false);
  userProfileSubmitErrMsg$: Observable<string | undefined>;
  userProfileSubmitSuccessMsg$: Observable<string | undefined>;
  usrProfile$: Observable<UserProfileModel|undefined>;

  constructor(private store: Store<AppState>) { }

  ngOnInit(): void {
    this.store.dispatch(new UserProfileMessagesCleared());
    this.usrProfile$ = this.store.pipe(select(selectUserProfile));
    this.usrProfileLoaded$ = this.store.pipe(select(selectUserProfileLoaded));
    this.userProfileSubmitErrMsg$ = this.store.pipe(
      select(userProfileSubmissionErrorMsg)
    );
    this.userProfileSubmitSuccessMsg$ = this.store.pipe(
      select(userProfileSubmissionSuccessMsg)
    );
  }

  toggleForm() {
    if (this.showForm) {
      this.showForm = false;
    } else {
      this.showForm = true;
    }
  }

  closeFormHander($event: boolean) {
    this.showForm = $event;
  };

  onClearStatusMsgs() {
    this.store.dispatch(new UserProfileMessagesCleared());
  }

}
