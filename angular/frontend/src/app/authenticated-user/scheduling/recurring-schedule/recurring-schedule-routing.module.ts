import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { 
  CreateRecurringClassComponent 
} from './create/create-recurring-class/create-recurring-class.component';
import { RecurringClassesComponent } from './list/recurring-classes/recurring-classes.component';
import { RecurringScheduleComponent } from './recurring-schedule/recurring-schedule.component';

const routes: Routes = [
  { path: '', component: RecurringScheduleComponent, 
    children: [
      { path: 'create', component: CreateRecurringClassComponent },
      { path: 'list', component: RecurringClassesComponent },
    ] 
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RecurringScheduleRoutingModule { }
