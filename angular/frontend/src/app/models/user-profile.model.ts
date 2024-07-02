/*export interface UserProfileEditModel {
    givenName: string;
    surname: string;
    email: string;
}

export interface UserProfileModel {
    id: number;
    givenName: string;
    surname: string;
    email: string;
    username: string;
} */

export interface UserModel {
    username: string;
    id: number;
  }

export interface UserProfileModel {
    id: number;
    user: UserModel;
    contact_email: string;
    surname: string;
    given_name: string;
  }
  
export interface UserProfileEditModel {
    contact_email: string;
    surname: string;
    given_name: string;
  }
