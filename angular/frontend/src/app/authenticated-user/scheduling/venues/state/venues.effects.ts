import { Injectable } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { select, Store } from '@ngrx/store';
import { of } from 'rxjs';
import { catchError, filter, map,
    mergeMap, withLatestFrom 
} from "rxjs/operators";

import { VenuesSpacesState } from './venues.reducers';
import { venueSpacesLoadedInState } from './venues.selectors';

import { VenuesServiceService } from '../service/venues-service.service';

import { 
    VenuesActionTypes, VenueSpacesLoaded, 
    VenueSpacesRequestCancelled, VenueSpacesRequested 
} from './venues.actions';


@Injectable()
export class VenueSpacesEffects {


    fetchVenueSpaces$ = createEffect(() => {
        return this.actions$
        .pipe(
            ofType<VenueSpacesRequested>(
            VenuesActionTypes.VenueSpacesRequested
            ),
            withLatestFrom(this.store.pipe(select(venueSpacesLoadedInState))),
            filter(([action, venueSpacesLoaded]) => !venueSpacesLoaded),
            mergeMap(action => this.venuesService.fetchAllVenueSpacesForTeacher()
            .pipe(
                map(venueSpaces => new VenueSpacesLoaded({ venueSpaces: venueSpaces })),
                catchError(err => {
                this.store.dispatch(
                    new VenueSpacesRequestCancelled({ err })
                );
                return of();
                })
            )
            )
        )
    });


    constructor(
        private actions$: Actions,
        private venuesService: VenuesServiceService,
        private store: Store<VenuesSpacesState>
    ) {}
}