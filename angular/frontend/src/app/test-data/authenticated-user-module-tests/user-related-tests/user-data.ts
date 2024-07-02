import { ErrorResponseModel } from "src/app/models/error-response.model";
import { 
    UserProfileEditModel, UserProfileModel 
} from "src/app/models/user-profile.model";

export const userProfileData: UserProfileModel = {
    id: 1,
    username: "Test User 1",
    surname: "McTest",
    givenName: "Testy",
    email: "testuser@gmx.com"
}

export const userProfileEditData: UserProfileEditModel = {
    surname: "Edited",
    givenName: "Altered",
    email: "updated@gmx.com"
}

export const userProfileEdited: UserProfileModel = {
    id: 1,
    username: "Test User 1",
    surname: "Edited",
    givenName: "Altered",
    email: "updated@gmx.com"
}

export const httpProfileEditError1: ErrorResponseModel = {
    "message": "There was an error updating the user info",
}

export const httpProfileEditError2: ErrorResponseModel = {
    "message": "The user does not exist",
}