import { Component, OnInit } from '@angular/core';
import { select, Store } from '@ngrx/store';
import { Observable, of } from 'rxjs';

import { 
  selectFreelanceStudentsOrClasses 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.selectors';
import { StudentOrClassModel } from 'src/app/models/student-or-class.model';
import { StudentsOrClassesState } from 'src/app/authenticated-user/student-or-class/state/student-or-class.reducers';

@Component({
  selector: 'app-make-purchase',
  standalone: false,
  templateUrl: './make-purchase.component.html',
  styleUrl: './make-purchase.component.css'
})
export class MakePurchaseComponent {

  freelanceStudents$: Observable<StudentOrClassModel[] | undefined> = of(undefined)

  constructor(
    private studentsOrClassesStore: Store<StudentsOrClassesState>
  ) {}

  ngOnInit(): void {
    this.freelanceStudents$ = this.studentsOrClassesStore.pipe(
      select(selectFreelanceStudentsOrClasses)
    );
  }

}
