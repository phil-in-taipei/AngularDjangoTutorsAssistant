import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthenticatedUserComponent } from './authenticated-user/authenticated-user.component';
import { CreateSchoolComponent } from './schools/create/create-school/create-school.component';
import { SchoolDetailComponent } from './schools/detail/school-detail/school-detail.component';
import { SchoolListComponent } from './schools/list/school-list/school-list.component';
import { UserProfileComponent } from './user/user-profile/user-profile.component';

const routes: Routes = [
  { path: '', component: AuthenticatedUserComponent, children: [ 
      { path: 'create-school', component: CreateSchoolComponent },
      { path: 'school/:id', component: SchoolDetailComponent },
      { path: 'users-schools', component: SchoolListComponent },
      { path: 'user-profile', component: UserProfileComponent },
      { path: "**", redirectTo: '/user-profile' }
    ] 
  },
  { path: 'scheduling', loadChildren: () => import('./scheduling/scheduling.module').then(m => m.SchedulingModule) },
  
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AuthenticatedUserRoutingModule { }
