import { Component, OnInit } from '@angular/core';
import { Dictionary } from '@ngrx/entity';
import { Observable, of } from "rxjs";
import {select, Store } from '@ngrx/store';

import { ScheduledClassesState } from '../../../classes-state/scheduled-classes.reducers';
import { 
  selectAllScheduledClasses, selectMonthlyDateRange, fetchingClassesInProgress 
} from '../../../classes-state/scheduled-classes.selectors';
//import { 
//  selectAllStudentsOrClassesEntities 
//} from 'src/app/authenticated-user/student-or-class/state/student-or-class.selectors';
//import { StudentOrClassModel } from 'src/app/models/student-or-class.model';
//import { 
//  StudentsOrClassesState 
//} from 'src/app/authenticated-user/student-or-class/state/student-or-class.reducers';
import { ScheduledClassModel } from 'src/app/models/scheduled-class.model';


@Component({
  selector: 'app-monthly-view',
  standalone: false,
  templateUrl: './monthly-view.component.html',
  styleUrl: './monthly-view.component.css'
})
export class MonthlyViewComponent implements OnInit {

  scheduledClasses$: Observable<ScheduledClassModel[] | undefined> = of(undefined);
  classesLoaded$: Observable<boolean> = of(false);
  monthlyDateRange$: Observable<[string, string] | undefined> = of(undefined);
  showMonthlySelectForm: Boolean = true;
  //studentsOrClassesDict$: Observable<Dictionary<StudentOrClassModel> | undefined> = of(undefined);

  constructor(
    private scheduledClassesStore: Store<ScheduledClassesState>,
    //private studentsOrClassesStore: Store<StudentsOrClassesState>
  ) { }

  ngOnInit(): void {
    //this.studentsOrClassesDict$ = this.studentsOrClassesStore.pipe(
    //  select(selectAllStudentsOrClassesEntities)
    //);

    this.scheduledClasses$ = this.scheduledClassesStore.pipe(
      select(selectAllScheduledClasses)
    );
    this.monthlyDateRange$ = this.scheduledClassesStore.pipe(
      select(selectMonthlyDateRange)
    );
    this.classesLoaded$ = this.scheduledClassesStore.pipe(
      select(fetchingClassesInProgress)
    );
  }

  closeMonthlySelectFormHander($event: boolean) {
    this.showMonthlySelectForm = $event;
  }

  toggleMonthlySelectForm() {
    if (this.showMonthlySelectForm) {
      this.showMonthlySelectForm = false;
    } else {
      this.showMonthlySelectForm = true;
    }
  }

  trackByFn(index: number, item: any) {
    return item.id;
  }  
}
