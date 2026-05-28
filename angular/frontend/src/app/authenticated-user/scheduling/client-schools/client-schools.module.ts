import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ClientSchoolsRoutingModule } from './client-schools-routing.module';
import { ClientSchoolsComponent } from './client-schools/client-schools.component';


@NgModule({
  declarations: [
    ClientSchoolsComponent,
  ],
  imports: [
    CommonModule,
    ClientSchoolsRoutingModule
  ]
})
export class ClientSchoolsModule { }
