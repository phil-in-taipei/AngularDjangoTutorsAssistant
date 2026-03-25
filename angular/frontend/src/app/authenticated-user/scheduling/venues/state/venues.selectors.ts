import {createFeatureSelector, createSelector} from '@ngrx/store';

import { VenuesSpacesState } from './venues.reducers';
import * as fromVenuesSpaces from './venues.reducers';


export const selectVenuesSpacesState = 
            createFeatureSelector<VenuesSpacesState>("venue-spaces");

export const deletionModeActivated = createSelector(
            selectVenuesSpacesState,
            state => state.deletionModeActivated
        );


export const fetchingVenueSpacesInProgress = createSelector(
            selectVenuesSpacesState,
            state => state.fetchingVenueSpacesInProgress
        );

export const selectAllVenueSpaces = createSelector(
    selectVenuesSpacesState,
        fromVenuesSpaces.selectAll
    );

export const selectVenueSpaceById = (id:number) => createSelector(
    selectVenuesSpacesState,
    state => state.entities[id]
);

export const venueSpacesLoadedInState = createSelector(
        selectVenuesSpacesState,
        state => state.venueSpacesLoaded
    );

    
export const venueSpacesErrorMsg = createSelector(
        selectVenuesSpacesState,
        state => state.errorMessage
    );
          
export const venueSpacesSuccessMsg = createSelector(
        selectVenuesSpacesState,
        state => state.successMessage
    );
