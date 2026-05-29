import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { ClientSchoolsComponent } from './client-schools/client-schools.component';
import { GroupClassAttendanceDetailComponent } from './group-class-attendance/group-class-attendance-detail/group-class-attendance-detail.component';

const routes: Routes = [
    { path: '', component: ClientSchoolsComponent, children: [
    { 
      path: 'group-class-attendance/:scheduled_class_id', 
      component: GroupClassAttendanceDetailComponent 
    }
    ] }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ClientSchoolsRoutingModule { }
