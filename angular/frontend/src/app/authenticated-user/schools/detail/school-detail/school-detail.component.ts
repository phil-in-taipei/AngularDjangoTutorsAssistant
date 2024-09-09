import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from "@angular/router";
import {select, Store } from '@ngrx/store';
import { Observable, of } from "rxjs";

import { SchoolModel } from 'src/app/models/school.model';
import { SchoolsState } from '../../state/school.reducers';
import { 
  schoolsErrorMsg, schoolsSuccessMsg, 
  selectSchoolById
} from '../../state/school.selectors';
import { SchoolsMessagesCleared } from '../../state/school.actions';

@Component({
  selector: 'app-school-detail',
  standalone: false,
  templateUrl: './school-detail.component.html',
  styleUrl: './school-detail.component.css'
})
export class SchoolDetailComponent implements OnInit {

  errMsg$: Observable<string | undefined> = of(undefined);
  idFromRouteData:number;
  school$: Observable<SchoolModel | undefined>;
  successMsg$: Observable<string | undefined> = of(undefined);

  constructor(
    private route: ActivatedRoute, 
    private store: Store<SchoolsState>
  ) { }

  ngOnInit(): void {
    this.store.dispatch(new SchoolsMessagesCleared());
    this.idFromRouteData = this.route.snapshot.params['id'];
    this.school$ = this.store.pipe(select(
      selectSchoolById(this.idFromRouteData)
    ));
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
