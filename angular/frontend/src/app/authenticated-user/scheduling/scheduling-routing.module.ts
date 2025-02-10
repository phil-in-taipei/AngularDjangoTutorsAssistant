import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DailyListComponent } from './classes/daily/daily-list/daily-list.component';
import { LandingPageComponent } from './landing/landing-page/landing-page.component';
import { MonthlyViewComponent } from './classes/monthly/monthly-view/monthly-view.component';
import { SchedulingComponent } from './scheduling/scheduling.component';
import { ScheduleSingleClassComponent } from './single-class/create/schedule-single-class/schedule-single-class.component';
import { 
  SingleClassInfoComponent 
} from './single-class/detail/single-class-info/single-class-info.component';

const routes: Routes = [{ path: '', component: SchedulingComponent, children: [
  { path: 'calendar', component: MonthlyViewComponent },
  { path: 'landing', component: LandingPageComponent },
  { path: 'schedule-daily/:date', component: DailyListComponent },
  { path: 'schedule-single-class', component: ScheduleSingleClassComponent },
  { path: 'single-class/:id', component: SingleClassInfoComponent },
] },
  { path: 'recurring-schedule', loadChildren: () => import('./recurring-schedule/recurring-schedule.module').then(m => m.RecurringScheduleModule) }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SchedulingRoutingModule { }
