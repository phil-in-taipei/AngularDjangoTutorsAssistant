import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { FormsModule } from '@angular/forms';
import { EffectsModule } from '@ngrx/effects';
import { StoreModule } from '@ngrx/store';

import { AccountingComponent } from './accounting/accounting.component';
import { AccountingRoutingModule } from './accounting-routing.module';
import { 
  MonthlySchoolAccountingReportComponent 
} from './reports/monthly-school-accounting-report/monthly-school-accounting-report.component';
import { 
  OverallMonthlyAccountingReportComponent 
} from './reports/overall-monthly-accounting-report/overall-monthly-accounting-report.component';
import { 
  SchoolAccountingReportWithinDateRangeComponent 
} from './reports/school-accounting-report-within-date-range/school-accounting-report-within-date-range.component';

import { SchoolsEffects } from '../../schools/state/school.effects';
import { schoolsReducer } from '../../schools/state/school.reducers';
import { 
  SelectDateRangeAndSchoolComponent 
} from './reports/select-date-range-and-school/select-date-range-and-school.component';
import { 
  SelectDateRangeAndSchoolFormComponent 
} from './reports/select-date-range-and-school-form/select-date-range-and-school-form.component';
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
    MonthlySchoolAccountingReportComponent,
    OverallMonthlyAccountingReportComponent,
    SchoolAccountingReportWithinDateRangeComponent,
    SelectDateRangeAndSchoolComponent,
    SelectDateRangeAndSchoolFormComponent,
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
