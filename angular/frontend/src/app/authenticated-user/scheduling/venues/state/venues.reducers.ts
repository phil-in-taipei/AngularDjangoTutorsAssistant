import {createEntityAdapter, EntityAdapter, EntityState} from '@ngrx/entity';

import { VenueSpaceModel } from 'src/app/models/venues.model';
import { VenuesActionTypes, VenuesActions } from './venues.actions';


function compareVenueSpacesByName(
    a: VenueSpaceModel, b: VenueSpaceModel
): number {
  const venueA = a.venue.venue_name;
  const venueB = b.venue.venue_name;
  const spaceA = a.space_name;
  const spaceB = b.space_name;

  if (venueA !== venueB) {
    return venueA > venueB ? 1 : -1;
  }

  if (spaceA !== spaceB) {
    return spaceA > spaceB ? 1 : -1;
  }

  return 0;
}

export interface VenuesSpacesState extends EntityState<VenueSpaceModel> {
    deletionModeActivated: boolean;
    fetchingVenueSpacesInProgress: boolean;
    errorMessage: string | undefined,
    venueSpacesLoaded: boolean,
    successMessage: string | undefined,
};

export const adapter: EntityAdapter<VenueSpaceModel> = 
    createEntityAdapter<VenueSpaceModel>(
        { sortComparer: compareVenueSpacesByName }
    );

export const initialVenueSpacesState: VenuesSpacesState = adapter.getInitialState({
    deletionModeActivated: false,
    errorMessage: undefined,
    fetchingVenueSpacesInProgress: false,
    venueSpacesLoaded: false,
    successMessage: undefined
});

export function venueSpacesReducer(
    state = initialVenueSpacesState,
    action: VenuesActions): VenuesSpacesState {

    let reducerErrorMessage: string | undefined = undefined;
    let reducerSuccessMessage: string | undefined = undefined;

    switch(action.type) {

        case VenuesActionTypes.VenuesMessagesCleared:
            reducerErrorMessage = undefined;
            reducerSuccessMessage = undefined;
            return {
                ...state,  successMessage: reducerSuccessMessage,
                errorMessage: reducerErrorMessage
            }

        case VenuesActionTypes.VenueSpacesCleared:
            return initialVenueSpacesState;
    
        case VenuesActionTypes.VenueSpacesLoaded:
            reducerErrorMessage = undefined;
            reducerSuccessMessage = undefined;
    
            return adapter.upsertMany(action.payload.venueSpaces, {...state,
                errorMessage: reducerErrorMessage,
                fetchingVenueSpacesInProgress: false,
                venueSpacesLoaded: true,
                successMessage: reducerSuccessMessage
            });   

        case VenuesActionTypes.VenueSpacesRequestCancelled:
            reducerErrorMessage = "Error fetching class locations!";
            reducerSuccessMessage = undefined;

            if (action.payload.err.error.Error) {
                reducerErrorMessage = action.payload.err.error.Error;
            }
            return {
                 ...state,  errorMessage: reducerErrorMessage, 
                 successMessage: reducerSuccessMessage,
            }

        case VenuesActionTypes.VenueSpacesRequested:
            return {
                ...state, 
                fetchingVenueSpacesInProgress: true
            } 

        default: {
            return state
        }
    }

}

export const {
    selectAll,
    selectEntities,
    selectIds,
} = adapter.getSelectors();