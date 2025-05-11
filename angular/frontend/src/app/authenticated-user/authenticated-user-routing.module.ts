import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { AuthGuard } from '../authentication/auth.guard';
import { AuthenticatedUserComponent } from './authenticated-user/authenticated-user.component';
import { CreateSchoolComponent } from './schools/create/create-school/create-school.component';
import { CreateStudentOrClassComponent } from './student-or-class/create/create-student-or-class/create-student-or-class.component';
import { SchoolDetailComponent } from './schools/detail/school-detail/school-detail.component';
import { SchoolListComponent } from './schools/list/school-list/school-list.component';
import { StudentOrClassDetailComponent } from './student-or-class/detail/student-or-class-detail/student-or-class-detail.component';
import { StudentOrClassListComponent } from './student-or-class/list/student-or-class-list/student-or-class-list.component';
import { UserProfileComponent } from './user/user-profile/user-profile.component';

const routes: Routes = [
  { path: '', component: AuthenticatedUserComponent, children: [ 
      { path: 'create-school', component: CreateSchoolComponent },
      { path: 'create-student-or-class', component: CreateStudentOrClassComponent },
      { path: 'scheduling', loadChildren: () => import(
        './scheduling/scheduling.module').then(m => m.SchedulingModule), 
        canActivate: [AuthGuard]
      },
      { path: 'school/:id', component: SchoolDetailComponent },
      { path: 'student-or-class/:id', component: StudentOrClassDetailComponent },
      { path: 'users-schools', component: SchoolListComponent },
      { path: 'users-students-or-classes', component: StudentOrClassListComponent },
      { path: 'user-profile', component: UserProfileComponent },
      { path: "**", redirectTo: 'user-profile' }
    ] 
  },  
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
  providers: [AuthGuard]
})
export class AuthenticatedUserRoutingModule { }
