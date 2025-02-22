import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { 
  CreateRecurringClassComponent 
} from './create/create-recurring-class/create-recurring-class.component';
import { 
  RecurringClassesAppliedMonthlyComponent 
} from './applied-monthly/recurring-classes-applied-monthly/recurring-classes-applied-monthly.component';
import { RecurringClassesComponent } from './list/recurring-classes/recurring-classes.component';
import { RecurringScheduleComponent } from './recurring-schedule/recurring-schedule.component';
import { 
  SelectMonthAndYearComponent 
} from './applied-monthly/select-month-and-year/select-month-and-year.component';

const routes: Routes = [
  { path: '', component: RecurringScheduleComponent, 
    children: [
      { path: 'create', component: CreateRecurringClassComponent },
      { 
        path: 'applied-monthly/:month/:year', 
        component: RecurringClassesAppliedMonthlyComponent 
      },
      { path: 'list', component: RecurringClassesComponent },
      { path: 'select-month-year', component: SelectMonthAndYearComponent },
    ] 
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RecurringScheduleRoutingModule { }
