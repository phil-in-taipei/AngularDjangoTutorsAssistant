import { Component, OnInit } from '@angular/core';
import { select, Store } from '@ngrx/store';
import { Observable, of } from 'rxjs';

import { 
  selectFreelanceStudentsOrClasses 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.selectors';
import { StudentOrClassModel } from 'src/app/models/student-or-class.model';
import { 
  StudentsOrClassesState 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.reducers';


@Component({
  selector: 'app-select-month-year-and-freelance-account',
  standalone: false,
  templateUrl: './select-month-year-and-freelance-account.component.html',
  styleUrl: './select-month-year-and-freelance-account.component.css'
})
export class SelectMonthYearAndFreelanceAccountComponent implements OnInit {

  freelanceAccounts$: Observable<StudentOrClassModel[] | undefined> = of(undefined);

  constructor( 
    private store: Store<StudentsOrClassesState>
  ) {}

  ngOnInit(): void {
    this.freelanceAccounts$ = this.store.pipe(
      select(selectFreelanceStudentsOrClasses)
    );
  }

}
