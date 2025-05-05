import { Component, OnInit } from '@angular/core';
import { select, Store } from '@ngrx/store';
import { Observable, of } from "rxjs";

import { 
  StudentOrClassModel 
} from 'src/app/models/student-or-class.model';
import { 
  StudentOrClassDeletionModeActivated, 
  StudentOrClassDeletionModeDeactivated 
} from '../../state/student-or-class.actions';
import { 
  StudentsOrClassesState 
} from '../../state/student-or-class.reducers';
import { 
  deletionModeForStudentsOrClassesActivated,
  fetchingStudentsOrClassesInProgress,
  selectAllStudentsOrClasses
} from '../../state/student-or-class.selectors';

@Component({
  selector: 'app-student-or-class-list',
  standalone: false,
  templateUrl: './student-or-class-list.component.html',
  styleUrl: './student-or-class-list.component.css'
})
export class StudentOrClassListComponent implements OnInit {
  
  studentsOrClasses$: Observable<StudentOrClassModel[] | undefined> = of(undefined);
  deletionModeForStudentsOrClassesActivated$: Observable<boolean> = of(false);
  fetchingStudentsOrClassesInProgress$: Observable<boolean> = of(false);

  constructor(private store: Store<StudentsOrClassesState>) { }
  
  ngOnInit(): void {
    this.studentsOrClasses$ = this.store.pipe(
      select(selectAllStudentsOrClasses)
    );
    this.deletionModeForStudentsOrClassesActivated$ = this.store.pipe(
      select(deletionModeForStudentsOrClassesActivated)
    );
  this.fetchingStudentsOrClassesInProgress$ = this.store.pipe(
      select(fetchingStudentsOrClassesInProgress)
    );
  }


  onActivateStudentOrClassDeletionMode(): void {
    this.store.dispatch(
      new StudentOrClassDeletionModeActivated()
    );
  }

  onDeactivateStudentOrClassDeletionMode(): void {
    this.store.dispatch(
      new StudentOrClassDeletionModeDeactivated()
    );
  }

  trackByFn(index: number, item: any) {
    return item.id;
  }

}
