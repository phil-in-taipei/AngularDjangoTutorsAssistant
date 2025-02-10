import { NgModule } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { EffectsModule } from '@ngrx/effects';
import { StoreModule } from '@ngrx/store';

import { 
  RecurringClassComponent 
} from './list/recurring-class/recurring-class.component';
import { 
  RecurringClassesComponent 
} from './list/recurring-classes/recurring-classes.component';
import { RecurringScheduleRoutingModule } from './recurring-schedule-routing.module';
import { RecurringScheduleComponent } from './recurring_schedule/recurring-schedule.component';


@NgModule({
  declarations: [
    RecurringClassComponent,
    RecurringClassesComponent,
    RecurringScheduleComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    NgbModule,
    RecurringScheduleRoutingModule
  ]
})
export class RecurringScheduleModule { }
