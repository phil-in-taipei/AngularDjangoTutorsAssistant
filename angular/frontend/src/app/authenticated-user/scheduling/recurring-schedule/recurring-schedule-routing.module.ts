import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RecurringScheduleComponent } from './recurring_schedule/recurring-schedule.component';

const routes: Routes = [
  { path: '', component: RecurringScheduleComponent, 
    children: [

    ] 
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RecurringScheduleRoutingModule { }
