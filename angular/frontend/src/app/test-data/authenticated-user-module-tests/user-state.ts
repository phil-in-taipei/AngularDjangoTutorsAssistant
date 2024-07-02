import { UserProfileState } from "src/app/authenticated-user/user/user-state/user.reducers";
import { 
    userProfileData, 
    userProfileEdited
} from "./user-related-tests/user-data";

export const stateWithLoadedUser: UserProfileState = {
    errorMessage: undefined,
    successMessage: undefined,
    userProfileLoaded: true,
    usrProfile: userProfileData
};

export const stateWithRevisedUser: UserProfileState = {
    errorMessage: undefined,
    successMessage: "User Profile has been Sucessfully Updated!",
    userProfileLoaded: true,
    usrProfile: userProfileEdited
}