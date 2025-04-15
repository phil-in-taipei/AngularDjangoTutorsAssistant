import { Component, OnInit, Input } from '@angular/core';
import { of, Observable } from 'rxjs';
import { select, Store } from '@ngrx/store';

import { 
  selectStudentOrClassById 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.selectors';
import { StudentOrClassModel } from 'src/app/models/student-or-class.model';
import { 
  StudentsOrClassesState 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.reducers';

@Component({
  selector: 'app-freelance-account-template-display',
  standalone: false,
  templateUrl: './freelance-account-template-display.component.html',
  styleUrl: './freelance-account-template-display.component.css'
})
export class FreelanceAccountTemplateDisplayComponent implements OnInit{

  freelanceAccount$: Observable<StudentOrClassModel | undefined> = of(undefined);
  @Input() studentOrClassId: number;


  constructor(
    private store: Store<StudentsOrClassesState>
  ) {}
  

  ngOnInit(): void {
    this.freelanceAccount$ = this.store.pipe(select(
      selectStudentOrClassById(this.studentOrClassId)
    ));
  }
}
