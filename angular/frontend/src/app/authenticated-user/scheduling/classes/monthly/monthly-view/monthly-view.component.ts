import { Component } from '@angular/core';
import { Dictionary } from '@ngrx/entity';
import { Observable, of } from "rxjs";
import {select, Store } from '@ngrx/store';

import { ScheduledClassesState } from '../../../classes-state/scheduled-classes.reducers';
import { selectAllScheduledClasses } from '../../../classes-state/scheduled-classes.selectors';
import { 
  selectAllStudentsOrClassesEntities 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.selectors';
import { 
  StudentsOrClassesState 
} from 'src/app/authenticated-user/student-or-class/state/student-or-class.reducers';


@Component({
  selector: 'app-monthly-view',
  standalone: false,
  templateUrl: './monthly-view.component.html',
  styleUrl: './monthly-view.component.css'
})
export class MonthlyViewComponent {

}
