import { NgModule } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { EffectsModule } from '@ngrx/effects';
import { StoreModule } from '@ngrx/store';

import { CalendarScheduleComponent } from './classes/monthly/calendar-schedule/calendar-schedule.component';
import { DailyListComponent } from './classes/daily/daily-list/daily-list.component';
import { LandingPageComponent } from './landing/landing-page/landing-page.component';
import { MonthlyViewComponent } from './classes/monthly/monthly-view/monthly-view.component';
import { ScheduledClassComponent } from './classes/daily/scheduled-class/scheduled-class.component';
import { SchedulingRoutingModule } from './scheduling-routing.module';
import { SchedulingComponent } from './scheduling/scheduling.component';

import { ScheduledClassesEffects } from './classes-state/scheduled-classes.effects';
import { scheduledClassesReducer } from './classes-state/scheduled-classes.reducers';
import { 
  StudentOrClassTemplateStringComponent 
} from '../student-or-class/student-or-class-template-string/student-or-class-template-string.component';
import { StudentsOrClassesEffects } from '../student-or-class/state/student-or-class.effects';
import { studentsOrClassesReducer } from '../student-or-class/state/student-or-class.reducers';
import { UnconfirmedClassesComponent } from './landing/unconfirmed-classes/unconfirmed-classes.component';



@NgModule({
  declarations: [
    CalendarScheduleComponent,
    DailyListComponent,
    LandingPageComponent,
    MonthlyViewComponent,
    ScheduledClassComponent,
    SchedulingComponent,
    StudentOrClassTemplateStringComponent,
    UnconfirmedClassesComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    NgbModule,
    StoreModule.forFeature('scheduledClasses', scheduledClassesReducer),
    EffectsModule.forFeature([ScheduledClassesEffects]),
    StoreModule.forFeature('studentsOrClasses', studentsOrClassesReducer),
    EffectsModule.forFeature([StudentsOrClassesEffects]),
    SchedulingRoutingModule
  ]
})
export class SchedulingModule { }
