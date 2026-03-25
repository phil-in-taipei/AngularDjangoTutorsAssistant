import { Action} from "@ngrx/store";

import { VenueSpaceModel } from "src/app/models/venues.model";


export enum VenuesActionTypes {
    VenuesMessagesCleared = '[All Associated Pages] Venues Messages Cleared',
    VenueSpacesCleared = '[View User Logout] All Venue Spaces Removed',
    VenueSpacesLoaded = '[Venue Spaces API] Venue Spaces Loaded',
    VenueSpacesRequested = '[Authenicated User Component View] Users Venue Spaces Requested',
    VenueSpacesRequestCancelled= '[Authenticated User Component View] Users Venue Spaces Request Cancelled',
}

export class VenueSpacesCleared implements Action {
    readonly type = VenuesActionTypes.VenueSpacesCleared;
}

export class VenuesMessagesCleared implements Action {
    readonly type = VenuesActionTypes.VenuesMessagesCleared;
}

export class VenueSpacesLoaded implements Action {
    readonly type = VenuesActionTypes.VenueSpacesLoaded;

    constructor(
      public payload: { venueSpaces: VenueSpaceModel[] }
    ) {}
}

export class VenueSpacesRequestCancelled implements Action {
    readonly type = VenuesActionTypes.VenueSpacesRequestCancelled;

    constructor(public payload: {  err: any }) {}
  }

export class VenueSpacesRequested implements Action {
    readonly type = VenuesActionTypes.VenueSpacesRequested;
}


export type VenuesActions = VenueSpacesCleared |
    VenuesMessagesCleared | VenueSpacesLoaded | 
    VenueSpacesRequestCancelled | VenueSpacesRequested
