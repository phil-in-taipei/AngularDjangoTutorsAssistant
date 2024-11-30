import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SchedulingRoutingModule } from './scheduling-routing.module';
import { SchedulingComponent } from './scheduling.component';


@NgModule({
  declarations: [
    SchedulingComponent
  ],
  imports: [
    CommonModule,
    SchedulingRoutingModule
  ]
})
export class SchedulingModule { }
