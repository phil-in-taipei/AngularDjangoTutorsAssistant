import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from "@angular/router";
import {select, Store } from '@ngrx/store';
import { Observable, of } from "rxjs";

import { 
  selectStudentOrClassById, 
  studentsOrClassesErrorMsg, 
  studentsOrClassesSuccessMsg 
} from '../../state/student-or-class.selectors';
import { StudentOrClassModel } from 'src/app/models/student-or-class.model';
import { StudentsOrClassesState } from '../../state/student-or-class.reducers';
import { StudentsOrClassesMessagesCleared } from '../../state/student-or-class.actions';

@Component({
  selector: 'app-student-or-class-detail',
  standalone: false,
  templateUrl: './student-or-class-detail.component.html',
  styleUrl: './student-or-class-detail.component.css'
})
export class StudentOrClassDetailComponent {

  errMsg$: Observable<string | undefined> = of(undefined);
  formVisible: boolean = false;
  idFromRouteData:number;
  studentOrClass$: Observable<StudentOrClassModel | undefined>;
  successMsg$: Observable<string | undefined> = of(undefined);
  
  constructor(
    private route: ActivatedRoute, 
    private store: Store<StudentsOrClassesState>
  ) { }


  ngOnInit(): void {
    this.store.dispatch(new StudentsOrClassesMessagesCleared());
    this.idFromRouteData = this.route.snapshot.params['id'];
    this.studentOrClass$ = this.store.pipe(select(
      selectStudentOrClassById(this.idFromRouteData)
    ));
    this.errMsg$ = this.store.pipe(
      select(studentsOrClassesErrorMsg)
    );
    this.successMsg$ = this.store.pipe(
      select(studentsOrClassesSuccessMsg)
    );
  }

  toggleForm() {
    if (this.formVisible) {
      this.formVisible = false;
    } else {
      this.formVisible = true;
    }
  }

  closeFormHander($event: boolean) {
    this.formVisible = $event;
  }

  onClearStatusMsgs() {
    this.store.dispatch(
      new StudentsOrClassesMessagesCleared()
    );
  }
  
}
