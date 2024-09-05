import { Component } from '@angular/core';
import { select, Store } from '@ngrx/store';
import { Observable, of } from "rxjs";

import { SchoolsState } from '../../state/school.reducers';
import { 
  schoolsErrorMsg, schoolsSuccessMsg 
} from '../../state/school.selectors';
import { SchoolsMessagesCleared } from '../../state/school.actions';

@Component({
  selector: 'app-create-school',
  standalone: false,
  templateUrl: './create-school.component.html',
  styleUrl: './create-school.component.css'
})
export class CreateSchoolComponent {

  errMsg$: Observable<string | undefined> = of(undefined);
  successMsg$: Observable<string | undefined> = of(undefined);

  constructor(private store: Store<SchoolsState>) { }

  ngOnInit(): void {
    this.store.dispatch(new SchoolsMessagesCleared());
    this.errMsg$ = this.store.pipe(
      select(schoolsErrorMsg)
    );
    this.successMsg$ = this.store.pipe(
      select(schoolsSuccessMsg)
    );
  }

  onClearStatusMsgs() {
    this.store.dispatch(new SchoolsMessagesCleared());
  }

}
