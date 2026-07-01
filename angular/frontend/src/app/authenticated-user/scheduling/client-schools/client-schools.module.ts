import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { ClientSchoolsRoutingModule } from './client-schools-routing.module';
import { ClientSchoolsComponent } from './client-schools/client-schools.component';
import { FormatHoursPipe } from './pipes/format-hours.pipe';
import { GroupClassAttendanceDetailComponent } from './group-class-attendance/group-class-attendance-detail/group-class-attendance-detail.component';
import { GroupClassAttendanceEditFormComponent } from './group-class-attendance/group-class-attendance-edit-form/group-class-attendance-edit-form.component';


@NgModule({
  declarations: [
    FormatHoursPipe,
    GroupClassAttendanceDetailComponent,
    GroupClassAttendanceEditFormComponent,
    ClientSchoolsComponent,
  ],
  imports: [
    CommonModule,
    FormsModule,
    NgbModule,
    ClientSchoolsRoutingModule
  ]
})
export class ClientSchoolsModule { }
