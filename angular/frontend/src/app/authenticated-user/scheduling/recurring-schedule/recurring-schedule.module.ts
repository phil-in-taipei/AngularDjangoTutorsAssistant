import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { RecurringScheduleRoutingModule } from './recurring-schedule-routing.module';
import { RecurringScheduleComponent } from './recurring_schedule/recurring-schedule.component';


@NgModule({
  declarations: [
    RecurringScheduleComponent
  ],
  imports: [
    CommonModule,
    RecurringScheduleRoutingModule
  ]
})
export class RecurringScheduleModule { }
