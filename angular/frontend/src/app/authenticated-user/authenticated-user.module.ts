import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { EffectsModule } from '@ngrx/effects';
import { StoreModule } from '@ngrx/store';
import { AuthenticatedUserRoutingModule } from './authenticated-user-routing.module';

import { 
  CreateSchoolComponent 
} from './schools/create/create-school/create-school.component';
import { 
  CreateSchoolFormComponent 
} from './schools/create/create-school-form/create-school-form.component';
import { 
  SchoolDetailComponent 
} from './schools/detail/school-detail/school-detail.component';
import { 
  SchoolEditFormComponent 
} from './schools/detail/school-edit-form/school-edit-form.component';
import { 
  SchoolListComponent 
} from './schools/list/school-list/school-list.component';
import { 
  SingleSchoolComponent 
} from './schools/list/single-school/single-school.component';

import { SchoolsEffects } from './schools/state/school.effects';
import { schoolsReducer } from './schools/state/school.reducers';

import { UserEffects } from './user/user-state/user.effects';
import { userProfileReducer } from './user/user-state/user.reducers';

import { 
  AuthenticatedFooterComponent 
} from './authenticated-layout/authenticated-footer/authenticated-footer.component';
import { 
  AuthenticatedHeaderComponent 
} from './authenticated-layout/authenticated-header/authenticated-header.component';
import { 
  AuthenticatedUserComponent 
} from './authenticated-user/authenticated-user.component';
import { 
  UserProfileComponent 
} from './user/user-profile/user-profile.component';
import { 
  EditProfileFormComponent 
} from './user/edit-profile-form/edit-profile-form.component';


@NgModule({
  declarations: [
    AuthenticatedFooterComponent,
    AuthenticatedHeaderComponent,
    AuthenticatedUserComponent,
    CreateSchoolComponent,
    CreateSchoolFormComponent,
    EditProfileFormComponent,
    SchoolDetailComponent,
    SchoolEditFormComponent,
    SchoolListComponent,
    SingleSchoolComponent,
    UserProfileComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    AuthenticatedUserRoutingModule,
    StoreModule.forFeature('user', userProfileReducer),
    EffectsModule.forFeature([UserEffects]),
    StoreModule.forFeature('schools', schoolsReducer),
    EffectsModule.forFeature([SchoolsEffects]),
  ]
})
export class AuthenticatedUserModule { }
