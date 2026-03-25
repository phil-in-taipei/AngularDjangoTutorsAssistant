import { Component, OnInit } from '@angular/core';
import { Store } from '@ngrx/store';


import { VenuesSpacesState } from '../venues/state/venues.reducers';
import { VenueSpacesRequested } from '../venues/state/venues.actions';

@Component({
  selector: 'app-scheduling',
  templateUrl: './scheduling.component.html',
  styleUrl: './scheduling.component.css'
})
export class SchedulingComponent {

  constructor(private store: Store<VenuesSpacesState>) { }

  ngOnInit(): void {
    this.store.dispatch(new VenueSpacesRequested());
  }

}
