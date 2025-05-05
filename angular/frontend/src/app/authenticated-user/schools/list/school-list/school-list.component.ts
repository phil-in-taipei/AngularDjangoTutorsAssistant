import { Component, OnInit } from '@angular/core';
import { select, Store } from '@ngrx/store';
import { Observable, of } from "rxjs";

import { 
  SchoolDeletionModeActivated, 
  SchoolDeletionModeDeactivated 
} from '../../state/school.actions';
import { SchoolModel } from 'src/app/models/school.model';
import { SchoolsState } from '../../state/school.reducers';
import { 
  deletionModeActivated,
  fetchingSchoolsInProgress,
  selectAllSchools,
} from '../../state/school.selectors';

@Component({
  selector: 'app-school-list',
  standalone: false,
  templateUrl: './school-list.component.html',
  styleUrl: './school-list.component.css'
})
export class SchoolListComponent implements OnInit {

  schools$: Observable<SchoolModel[] | undefined> = of(undefined);
  deletionModeActivated$: Observable<boolean> = of(false);
  fetchingSchoolsInProgress$: Observable<boolean> = of(false);

  constructor(private store: Store<SchoolsState>) { }

  ngOnInit(): void {
    this.schools$ = this.store.pipe(
      select(selectAllSchools)
    );
    this.deletionModeActivated$ = this.store.pipe(
      select(deletionModeActivated)
    );
    this.fetchingSchoolsInProgress$ = this.store.pipe(
      select(fetchingSchoolsInProgress)
    );
  }

  onActivateSchoolDeletionMode(): void {
    this.store.dispatch(
      new SchoolDeletionModeActivated()
    );
  }

  onDeactivateSchoolDeletionMode(): void {
    this.store.dispatch(
      new SchoolDeletionModeDeactivated()
    );
  }

  trackByFn(index: number, item: any) {
    return item.id;
  }

}
