import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthenticatedUserComponent } from './authenticated-user/authenticated-user.component';
import { SchoolListComponent } from './schools/list/school-list/school-list.component';
import { UserProfileComponent } from './user/user-profile/user-profile.component';

const routes: Routes = [
  { path: '', component: AuthenticatedUserComponent, children: [ 
      { path: 'users-schools', component: SchoolListComponent },
      { path: 'user-profile', component: UserProfileComponent },
      { path: "**", redirectTo: '/user-profile' }
    ] 
  },
  
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AuthenticatedUserRoutingModule { }
