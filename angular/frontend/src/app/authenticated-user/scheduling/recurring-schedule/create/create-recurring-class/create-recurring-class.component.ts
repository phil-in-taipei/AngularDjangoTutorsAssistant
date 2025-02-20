import { Component } from '@angular/core';
import { Observable, of } from 'rxjs';
import { select, Store } from '@ngrx/store';

import { 
  recurringClassErrorMsg, 
  recurringClassSuccessMsg 
} from '../../state/recurring-schedule-state/recurring-schedule.selectors';
import { 
  RecurringClassesMessagesCleared 
} from '../../state/recurring-schedule-state/recurring-schedule.actions';
import { 
  RecurringClassesState 
} from '../../state/recurring-schedule-state/recurring-schedule.reducers';
import { 
  selectAllStudentsOrClasses 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.selectors';
import { 
  selectUserProfile 
} from 'src/app/authenticated-user/user/user-state/user.selectors';
import { StudentOrClassModel } from 'src/app/models/student-or-class.model';
import { 
  StudentsOrClassesState 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.reducers';
import { UserProfileModel } from 'src/app/models/user-profile.model';
import { 
  UserProfileState
 } from 'src/app/authenticated-user/user/user-state/user.reducers';

@Component({
  selector: 'app-create-recurring-class',
  standalone: false,
  templateUrl: './create-recurring-class.component.html',
  styleUrl: './create-recurring-class.component.css'
})
export class CreateRecurringClassComponent {

  errorMessage$: Observable<string | undefined> = of(undefined);
  successMessage$: Observable<string | undefined> = of(undefined);
  studentsOrClasses$: Observable<StudentOrClassModel[]>;
  userProfile$: Observable<UserProfileModel | undefined>;

  constructor(
    private recurringClassesStore: Store<RecurringClassesState>,
    private studentsOrClassesStore: Store<StudentsOrClassesState>,
    private userStore: Store<UserProfileState>
  ) {}

  ngOnit(): void {
    this.recurringClassesStore.dispatch(
      new RecurringClassesMessagesCleared()
    )
    this.errorMessage$ = this.recurringClassesStore.pipe(
      select(recurringClassErrorMsg)
    );
    this.successMessage$ = this.recurringClassesStore.pipe(select(
      recurringClassSuccessMsg)
    );
    this.studentsOrClasses$ = this.studentsOrClassesStore.pipe(
      select(selectAllStudentsOrClasses)
    );
    this.userProfile$ = this.userStore.pipe(
      select(selectUserProfile)
    );
  }  

  onClearStatusMsgs() {
    this.recurringClassesStore.dispatch(
      new RecurringClassesMessagesCleared()
    );
  } 

}
