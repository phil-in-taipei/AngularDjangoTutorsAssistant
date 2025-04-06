import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AccountingComponent } from './accounting/accounting.component';
import { 
  FreelancePaymentsAndRefundsComponent 
} from './freelance-transactions/freelance-payments-and-refunds/freelance-payments-and-refunds.component';
import { 
  MonthlySchoolAccountingReportComponent 
} from './reports/monthly-school-accounting-report/monthly-school-accounting-report.component';
import { 
  OverallMonthlyAccountingReportComponent 
} from './reports/overall-monthly-accounting-report/overall-monthly-accounting-report.component';
import { 
  SchoolAccountingReportWithinDateRangeComponent 
} from './reports/school-accounting-report-within-date-range/school-accounting-report-within-date-range.component';
import { 
  SelectDateRangeAndSchoolComponent 
} from './reports/select-date-range-and-school/select-date-range-and-school.component';
import { 
  SelectMonthYearAndSchoolComponent 
} from './reports/select-month-year-and-school/select-month-year-and-school.component';

const routes: Routes = [
  { path: '', component: AccountingComponent, children: [
      { path: 'monthly-freelance-transactions', component: FreelancePaymentsAndRefundsComponent },
      { path: 'overall-monthly-accounting-report/:month/:year', component: OverallMonthlyAccountingReportComponent },
      { path: 'monthly-school-accounting-report/:month/:year/:school_id', component: MonthlySchoolAccountingReportComponent },
      { path: 'school-accounting-report-within-date-range/:start_date/:finish_date/:school_id', component: SchoolAccountingReportWithinDateRangeComponent },
      { path: 'select-date-range-and-school', component: SelectDateRangeAndSchoolComponent },
      { path: 'select-month-year-and-school', component: SelectMonthYearAndSchoolComponent },
    ] 
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AccountingRoutingModule { }
