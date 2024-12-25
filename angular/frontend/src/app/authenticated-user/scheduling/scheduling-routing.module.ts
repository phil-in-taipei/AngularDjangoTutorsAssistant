import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SchedulingComponent } from './scheduling/scheduling.component';
import { LandingPageComponent } from './landing/landing-page/landing-page.component';

const routes: Routes = [{ path: '', component: SchedulingComponent, children: [
  { path: 'landing', component: LandingPageComponent },
] }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class SchedulingRoutingModule { }
