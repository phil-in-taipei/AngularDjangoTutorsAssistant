import { Component, OnInit } from '@angular/core';
import {select, Store} from '@ngrx/store';
import { Observable, of } from 'rxjs';

import { SchoolModel } from 'src/app/models/school.model';
import { 
  SchoolsState 
} from 'src/app/authenticated-user/schools/state/school.reducers';
import { 
  selectAllSchools 
} from 'src/app/authenticated-user/schools/state/school.selectors';


@Component({
  selector: 'app-select-date-range-and-school',
  standalone: false,
  templateUrl: './select-date-range-and-school.component.html',
  styleUrl: './select-date-range-and-school.component.css'
})
export class SelectDateRangeAndSchoolComponent implements OnInit {

  schools$: Observable<SchoolModel[] | undefined> = of(undefined);

  constructor( 
    private schoolsStore: Store<SchoolsState>
  ) {}

  ngOnInit(): void {
    this.schools$ = this.schoolsStore.pipe(
      select(selectAllSchools)
    );
  }

}
