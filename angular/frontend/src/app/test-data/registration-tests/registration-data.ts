import { 
    UserRegistrationModel, 
    UserRegistrationResponseModel 
} from '../../models/user-registration.model';


export const userRegistrationData: UserRegistrationModel = {
    "username": "UserDude",
    "password": "testpassword",
    "re_password": "testpassword",
    "profile": {
        "contact_email": "testmail@gmx.com",
        "surname": "Surname",
        "given_name": "GivenName",
    } 
}

export const httpRegistrationResponseFailure1: UserRegistrationResponseModel = {
    "message": "The passwords do not match. Please try again.",
}

export const httpRegistrationResponseFailure2: UserRegistrationResponseModel = {
    "message": "A user with that username already exists. Please try again",
}

export const httpRegistrationResponseFailure3: UserRegistrationResponseModel = {
    "message": "There was an error. Please try again",
}


export const httpRegistrationResponseSuccess: UserRegistrationResponseModel = {
    "message": "Account successfully created for user",
}