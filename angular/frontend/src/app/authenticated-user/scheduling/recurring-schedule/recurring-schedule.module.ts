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
import { recurringClassesReducer } from './recurring-schedule-state/recurring-schedule.reducers';
import { RecurringClassesEffects } from './recurring-schedule-state/recurring-schedule.effects';
import { StudentOrClassTemplateStringComponent } from './student-or-class-template-string/student-or-class-template-string.component';   
import { StudentsOrClassesEffects } from '../../student-or-class/state/student-or-class.effects';
import { studentsOrClassesReducer } from '../../student-or-class/state/student-or-class.reducers';


@NgModule({
  declarations: [
    RecurringClassComponent,
    RecurringClassesComponent,
    RecurringScheduleComponent,
    StudentOrClassTemplateStringComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    NgbModule,
    RecurringScheduleRoutingModule,
    StoreModule.forFeature('recurringClasses', recurringClassesReducer),
    EffectsModule.forFeature([RecurringClassesEffects]),
    StoreModule.forFeature('studentsOrClasses', studentsOrClassesReducer),
    EffectsModule.forFeature([StudentsOrClassesEffects]),
  ]
})
export class RecurringScheduleModule { }
