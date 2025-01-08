import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { select, Store } from '@ngrx/store';
import { Observable, of } from 'rxjs';

import { SchoolModel } from 'src/app/models/school.model';
import { 
  SchoolsState
} from 'src/app/authenticated-user/schools/state/school.reducers';
import { 
  selectAllSchools 
} from 'src/app/authenticated-user/schools/state/school.selectors';
import { 
  StudentOrClassCreationCancelled, 
  StudentOrClassCreateSubmitted, 
} from '../../state/student-or-class.actions';
import { 
  StudentOrClassCreateAndEditModel 
} from 'src/app/models/student-or-class.model';
import { StudentsOrClassesState } from '../../state/student-or-class.reducers';

@Component({
  selector: 'app-create-class-form',
  standalone: false,
  templateUrl: './create-class-form.component.html',
  styleUrl: './create-class-form.component.css'
})
export class CreateClassFormComponent {

  schools$: Observable<SchoolModel[] | undefined> = of(undefined);

  constructor(
    private schoolStore: Store<SchoolsState>,
    private studentsOrClassesStore: Store<StudentsOrClassesState>
  ) {}

  ngOnInit(): void {
    this.schools$ = this.schoolStore.pipe(
      select(selectAllSchools)
    );
  }

}
