import { NgModule } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { EffectsModule } from '@ngrx/effects';
import { StoreModule } from '@ngrx/store';

import { 
  ApplyRecurringClassMonthlyFormComponent 
} from './applied-monthly/apply-recurring-class-monthly-form/apply-recurring-class-monthly-form.component';
import { 
  CreateRecurringClassComponent 
} from './create/create-recurring-class/create-recurring-class.component';
import { 
  CreateRecurringClassFormComponent 
} from './create/create-recurring-class-form/create-recurring-class-form.component';
import { 
  RecurringClassAppliedMonthlyComponent 
} from './applied-monthly/recurring-class-applied-monthly/recurring-class-applied-monthly.component';
import { 
  RecurringClassComponent 
} from './list/recurring-class/recurring-class.component';
import { 
  RecurringClassesAppliedMonthlyComponent 
} from './applied-monthly/recurring-classes-applied-monthly/recurring-classes-applied-monthly.component';
import { 
  RecurringClassesComponent 
} from './list/recurring-classes/recurring-classes.component';
import { RecurringScheduleRoutingModule } from './recurring-schedule-routing.module';
import { RecurringScheduleComponent } from './recurring-schedule/recurring-schedule.component';
import { 
  RecurringClassAppliedMonthlysEffects 
} from './state/recurring-classes-applied-monthly-state/recurring-class-applied-monthly.effects';
import { 
  recurringClassAppliedMonthlysReducer 
} from './state/recurring-classes-applied-monthly-state/recurring-class-applied-monthly.reducers';
import { recurringClassesReducer } from './state/recurring-schedule-state/recurring-schedule.reducers';
import { RecurringClassesEffects } from './state/recurring-schedule-state/recurring-schedule.effects';
import { 
  SelectMonthAndYearComponent 
} from './applied-monthly/select-month-and-year/select-month-and-year.component';
import { StudentOrClassTemplateStringComponent } from './student-or-class-template-string/student-or-class-template-string.component';   
import { StudentsOrClassesEffects } from '../../student-or-class/state/student-or-class.effects';
import { studentsOrClassesReducer } from '../../student-or-class/state/student-or-class.reducers';
import { UserEffects } from '../../user/user-state/user.effects';
import { userProfileReducer } from '../../user/user-state/user.reducers';

@NgModule({
  declarations: [
    ApplyRecurringClassMonthlyFormComponent,
    CreateRecurringClassComponent,
    CreateRecurringClassFormComponent,
    RecurringClassAppliedMonthlyComponent,
    RecurringClassComponent,
    RecurringClassesAppliedMonthlyComponent,
    RecurringClassesComponent,
    RecurringScheduleComponent,
    SelectMonthAndYearComponent,
    StudentOrClassTemplateStringComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    NgbModule,
    RecurringScheduleRoutingModule,
    StoreModule.forFeature('recurringClassesAppliedMonthly', recurringClassAppliedMonthlysReducer),
    EffectsModule.forFeature([RecurringClassAppliedMonthlysEffects]),
    StoreModule.forFeature('recurringClasses', recurringClassesReducer),
    EffectsModule.forFeature([RecurringClassesEffects]),
    StoreModule.forFeature('studentsOrClasses', studentsOrClassesReducer),
    EffectsModule.forFeature([StudentsOrClassesEffects]),
    StoreModule.forFeature('user', userProfileReducer),
    EffectsModule.forFeature([UserEffects]),
  ]
})
export class RecurringScheduleModule { }
