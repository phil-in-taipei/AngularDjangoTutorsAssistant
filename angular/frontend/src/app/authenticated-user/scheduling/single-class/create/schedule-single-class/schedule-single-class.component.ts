import { Component, OnInit } from '@angular/core';
import {select, Store} from '@ngrx/store';
import {Observable} from "rxjs";

import { 
  ScheduledClassesState 
} from '../../../classes-state/scheduled-classes.reducers';
import { 
  ScheduledClassesMessagesCleared 
} from '../../../classes-state/scheduled-classes.actions';
import { 
  selectAllStudentsOrClasses 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.selectors';
import { 
  selectUserProfile 
} from 'src/app/authenticated-user/user/user-state/user.selectors';
import { 
  scheduledClassesErrorMsg, scheduledClassesSuccessMsg 
} from '../../../classes-state/scheduled-classes.selectors';
import { StudentOrClassModel } from 'src/app/models/student-or-class.model';
import { 
  StudentsOrClassesState
 } from 'src/app/authenticated-user/student-or-class/state/student-or-class.reducers';
import { UserProfileModel } from 'src/app/models/user-profile.model';
import { UserProfileState } from 'src/app/authenticated-user/user/user-state/user.reducers';

@Component({
  selector: 'app-schedule-single-class',
  standalone: false,
  templateUrl: './schedule-single-class.component.html',
  styleUrl: './schedule-single-class.component.css'
})
export class ScheduleSingleClassComponent implements OnInit {

  classSubmitErrMsg$: Observable<string | undefined>;
  classSubmitSuccess$: Observable<string | undefined>;
  studentsOrClasses$: Observable<StudentOrClassModel[]>;
  userProfile$: Observable<UserProfileModel | undefined>;

  constructor(
    private scheduledClassesStore: Store<ScheduledClassesState>,
    private studentsOrClassesStore: Store<StudentsOrClassesState>,
    private userStore: Store<UserProfileState>
  ) { }

  ngOnInit(): void {
    this.scheduledClassesStore.dispatch(
      new ScheduledClassesMessagesCleared()
    );
    this.classSubmitErrMsg$ = this.scheduledClassesStore.pipe(
      select(scheduledClassesErrorMsg)
    );
    this.classSubmitSuccess$ = this.scheduledClassesStore.pipe(
      select(scheduledClassesSuccessMsg)
    );
    this.studentsOrClasses$ = this.studentsOrClassesStore.pipe(
      select(selectAllStudentsOrClasses)
    );
    this.userProfile$ = this.userStore.pipe(select(selectUserProfile));
  }

  onClearStatusMsgs() {
    this.scheduledClassesStore.dispatch(
      new ScheduledClassesMessagesCleared()
    );
  }  

}
