import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { ClientSchoolsComponent } from './client-schools/client-schools.component';

const routes: Routes = [
    { path: '', component: ClientSchoolsComponent, children: [
      
    ] }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ClientSchoolsRoutingModule { }
