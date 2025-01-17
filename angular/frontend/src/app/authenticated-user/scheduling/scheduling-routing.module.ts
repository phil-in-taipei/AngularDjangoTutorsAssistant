import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DailyListComponent } from './classes/daily/daily-list/daily-list.component';
import { LandingPageComponent } from './landing/landing-page/landing-page.component';
import { SchedulingComponent } from './scheduling/scheduling.component';
import { ScheduleSingleClassComponent } from './single-class/create/schedule-single-class/schedule-single-class.component';
import { 
  SingleClassInfoComponent 
} from './single-class/detail/single-class-info/single-class-info.component';

const routes: Routes = [{ path: '', component: SchedulingComponent, children: [
  { path: 'landing', component: LandingPageComponent },
  { path: 'schedule-daily/:date', component: DailyListComponent },
  { path: 'schedule-single-class', component: ScheduleSingleClassComponent },
  { path: 'single-class/:id', component: SingleClassInfoComponent },
] }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SchedulingRoutingModule { }
