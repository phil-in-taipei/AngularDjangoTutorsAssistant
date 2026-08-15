import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AddMinutePipe } from './pipes/add-minute.pipe';



@NgModule({
  declarations: [
    AddMinutePipe
  ],
  imports: [
    CommonModule
  ],
  exports: [
    AddMinutePipe
  ]
})
export class SharedModule { }
