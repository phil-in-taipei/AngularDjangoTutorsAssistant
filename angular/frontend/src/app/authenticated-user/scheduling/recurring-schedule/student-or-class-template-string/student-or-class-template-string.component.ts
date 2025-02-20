import { Component, OnInit, Input } from '@angular/core';
import { of, Observable } from 'rxjs';
import { select, Store } from '@ngrx/store';

import { selectStudentOrClassById } from 'src/app/authenticated-user/student-or-class/state/student-or-class.selectors';
import { StudentOrClassModel } from 'src/app/models/student-or-class.model';
import { StudentsOrClassesState } from 'src/app/authenticated-user/student-or-class/state/student-or-class.reducers';

@Component({
  selector: 'app-student-or-class-templ-string',
  standalone: false,
  templateUrl: './student-or-class-template-string.component.html',
  styleUrl: './student-or-class-template-string.component.css'
})
export class StudentOrClassTemplateStringComponent implements OnInit{

  studentOrClass$: Observable<StudentOrClassModel | undefined> = of(undefined);
  @Input() studentOrClassId: number;


  constructor(
    private store: Store<StudentsOrClassesState>
  ) {}
  

  ngOnInit(): void {
    this.studentOrClass$ = this.store.pipe(select(
      selectStudentOrClassById(this.studentOrClassId)
    ));
  }

}
