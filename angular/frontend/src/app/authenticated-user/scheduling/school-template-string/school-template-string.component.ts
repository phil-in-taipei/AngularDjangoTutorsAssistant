import { Component, OnInit, Input } from '@angular/core';
import { of, Observable } from 'rxjs';
import { select, Store } from '@ngrx/store';

import { SchoolModel } from 'src/app/models/school.model';
import { SchoolsState } from '../../schools/state/school.reducers';
import { selectSchoolById } from '../../schools/state/school.selectors';

@Component({
  selector: 'app-school-template-str',
  standalone: false,
  templateUrl: './school-template-string.component.html',
  styleUrl: './school-template-string.component.css'
})
export class SchoolTemplateStringComponent implements OnInit{

  school$: Observable<SchoolModel | undefined> = of(undefined);
  @Input() schoolId: number;

  ngOnInit(): void {
    this.school$ = this.store.pipe(select(
      selectSchoolById(this.schoolId)
    ));
  }

  constructor(
    private store: Store<SchoolsState>
  ) {}

}
