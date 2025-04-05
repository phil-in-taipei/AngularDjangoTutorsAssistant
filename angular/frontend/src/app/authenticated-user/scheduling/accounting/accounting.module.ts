import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { FormsModule } from '@angular/forms';
import { EffectsModule } from '@ngrx/effects';
import { StoreModule } from '@ngrx/store';

import { AccountingComponent } from './accounting/accounting.component';
import { AccountingRoutingModule } from './accounting-routing.module';

import { SchoolsEffects } from '../../schools/state/school.effects';
import { schoolsReducer } from '../../schools/state/school.reducers';
import { 
  SelectMonthYearAndSchoolComponent 
} from './reports/select-month-year-and-school/select-month-year-and-school.component';
import { 
  SelectMonthYearAndSchoolFormComponent 
} from './reports/select-month-year-and-school-form/select-month-year-and-school-form.component';
import { 
  StudentsOrClassesEffects 
} from '../../student-or-class/state/student-or-class.effects';
import { 
  studentsOrClassesReducer 
} from '../../student-or-class/state/student-or-class.reducers';


@NgModule({
  declarations: [
    AccountingComponent,
    SelectMonthYearAndSchoolComponent,
    SelectMonthYearAndSchoolFormComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    AccountingRoutingModule,
    NgbModule,
    StoreModule.forFeature('schools', schoolsReducer),
    EffectsModule.forFeature([SchoolsEffects]),
    StoreModule.forFeature('studentsOrClasses', studentsOrClassesReducer),
    EffectsModule.forFeature([StudentsOrClassesEffects]),
  ]
})
export class AccountingModule { }
