/*export interface UserRegistrationModel {
    givenName: string | null;
    surname: string | null;
    email: string | null;
    username: string | null;
    password: string | null;
    re_password: string | null;
 }

 export interface UserRegistrationResponseModel {
    message: string;
 }
    */
import { UserProfileEditModel } from "./user-profile.model";

 export interface UserRegistrationModel {
     username: string;
     password: string;
     re_password: string;
     profile: UserProfileEditModel;
  }
 
  export interface UserRegistrationResponseModel {
     message?: string;
     detail?: string;
  }
 