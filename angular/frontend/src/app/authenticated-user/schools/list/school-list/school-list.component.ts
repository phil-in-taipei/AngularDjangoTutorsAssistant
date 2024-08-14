import { Component, OnInit } from '@angular/core';
import { select, Store } from '@ngrx/store';
import { Observable, of } from "rxjs";

import { SchoolModel } from 'src/app/models/school.model';
import { SchoolsState } from '../../state/school.reducers';
import { selectAllSchools, fetchingSchoolsInProgress } from '../../state/school.selectors';

@Component({
  selector: 'app-school-list',
  standalone: false,
  templateUrl: './school-list.component.html',
  styleUrl: './school-list.component.css'
})
export class SchoolListComponent implements OnInit {


  schools$: Observable<SchoolModel[] | undefined> = of(undefined);
  fetchingSchoolsInProgress$: Observable<boolean> = of(false);


  constructor(private store: Store<SchoolsState>) { }


  ngOnInit(): void {
    this.schools$ = this.store.pipe(
      select(selectAllSchools)
    );
    this.fetchingSchoolsInProgress$ = this.store.pipe(
      select(fetchingSchoolsInProgress)
    );
  }

  trackByFn(index: number, item: any) {
    return item.id;
  }

}
