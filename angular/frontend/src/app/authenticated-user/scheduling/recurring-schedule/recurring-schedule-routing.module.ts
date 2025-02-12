import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RecurringClassesComponent } from './list/recurring-classes/recurring-classes.component';
import { RecurringScheduleComponent } from './recurring_schedule/recurring-schedule.component';

const routes: Routes = [
  { path: '', component: RecurringScheduleComponent, 
    children: [
      { path: 'list', component: RecurringClassesComponent },
    ] 
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RecurringScheduleRoutingModule { }
