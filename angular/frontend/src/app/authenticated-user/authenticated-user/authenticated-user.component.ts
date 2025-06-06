import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';
import { AppState } from 'src/app/reducers';

import { SchoolsRequested } from '../schools/state/school.actions';
import { 
  StudentsOrClassesRequested 
} from '../student-or-class/state/student-or-class.actions';
import { UserProfileRequested } from '../user/user-state/user.actions';

@Component({
  selector: 'app-authenticated-user',
  standalone: false,
  templateUrl: './authenticated-user.component.html',
  styleUrl: './authenticated-user.component.css'
})
export class AuthenticatedUserComponent implements OnInit {

  constructor(private store: Store<AppState>) { }


  ngOnInit(): void {
    this.store.dispatch(new SchoolsRequested());
    this.store.dispatch(new StudentsOrClassesRequested());
    this.store.dispatch(new UserProfileRequested());
  }

}
